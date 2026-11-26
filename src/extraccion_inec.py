"""Extraccion de las tablas del INEC por mes y por clase de accidente (PDF a CSV).

Uso: python -m src.extraccion_inec
Descarga los PDF a data/raw/inec_pdf/, los convierte con pdftotext, valida los
numeros contra la base de accidentes y escribe los CSV en data/external/.
"""

import re
import subprocess
import unicodedata
import urllib.parse
import urllib.request
from pathlib import Path

import pandas as pd

from src.datos import RAIZ, cargar_accidentes

URL_BASE = "https://www.inec.gob.pa/archivos/"
RUTA_PDF = RAIZ / "data" / "raw" / "inec_pdf"
RUTA_EXTERNAL = RAIZ / "data" / "external"

# Cuadro 13 o 15: accidentes, heridos y muertos por provincia y mes.
ARCHIVOS_MES = {
    2016: "P8271451-13.pdf",
    2017: "P885113.pdf",
    2018: "P077474012020011414421413.pdf",
    2019: "P057951862021012713255613.pdf",
    2020: "P070554752021072810284213.pdf",
    2021: "P05334242022092913580213.pdf",
    2022: "P070903792023103113004613.pdf",
    2023: "P057951862025010311243813.pdf",
    2024: "P05334242025092314173315.pdf",
    2025: "P057951862026081013463715.xlsx.pdf",
}

# Cuadro 3: accidentes por clase, segun provincia, comarca, distrito y via.
ARCHIVOS_CLASE = {
    2016: "P8271451-03.pdf",
    2017: "P885103.pdf",
    2018: "P070554752020011414002703.pdf",
    2019: "P070554752021012713095003.pdf",
    2020: "P05334242021072809491503.pdf",
    2021: "P057951862022092913384303.pdf",
    2022: "P070554752023103112435603.pdf",
    2023: "P070554752025010310474203.pdf",
    2024: "P070554752025092313221903.pdf",
    2025: "P05334242026081013121203.xlsx.pdf",
}

MESES = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio",
    "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre",
]
PROVINCIAS = [
    "Bocas del Toro", "Cocle", "Colon", "Chiriqui", "Darien", "Herrera",
    "Los Santos", "Panama", "Panama Oeste", "Veraguas",
]
# Nombre en el PDF (sin tildes) y nombre normalizado de cada comarca.
COMARCAS = [
    ("Comarca Kuna Yala", "Guna Yala"),
    ("Comarca Embera", "Embera"),
    ("Comarca Ngabe Bugle", "Ngabe Bugle"),
]
# Orden de las columnas de clase segun cuantas trae la tabla de cada anio.
# Hasta 2018 la colision con objeto fijo va dentro de Colision.
CLASES_PUBLICADAS = {
    4: ["Colision", "Atropello", "Vuelco", "Otras"],
    5: ["Colision", "Colision con objeto fijo", "Vuelco", "Atropello", "Otras"],
    10: ["Colision", "Colision con objeto fijo", "Vuelco", "Atropello"] + ["Otras"] * 6,
}

# Datos que el INEC no publica en estas tablas. Quedan fuera del CSV y se documentan.
VACIOS_CONOCIDOS = {
    (2020, "Los Santos"): "El Cuadro 3 de 2020 omite la fila de Los Santos (PDF y Excel).",
}

# La fila de Veraguas de 2017 (1 593) no incluye los distritos Sona y Mariato, que el INEC
# puso en la pagina siguiente. Con ellos suma 1 732, igual que el Cuadro 1, y las cuatro
# clases cuadran con la fila TOTAL. Se suman a lo publicado en la fila de la provincia.
CORRECCIONES_CONOCIDAS = {
    (2017, "Veraguas"): {"Colision": 107, "Atropello": 5, "Vuelco": 24, "Otras": 3},
}

_NUMERO = re.compile(r"^(\d{1,3}(,\d{3})+|\d+|-)$")


def _sin_tildes(texto: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFKD", texto) if not unicodedata.combining(c))


def _limpiar(texto: str) -> str:
    """Quita tildes y puntos guia, y deja el texto en una sola linea."""
    texto = re.sub(r"[\u2026.]{2,}|\u2026", " ", _sin_tildes(texto))
    return re.sub(r"\s+", " ", texto).strip()


def _valor(token: str) -> int:
    """Convierte un numero del INEC. El guion significa cantidad nula o cero."""
    return 0 if token == "-" else int(token.replace(",", ""))


def descargar_pdf(nombre: str, carpeta: Path = RUTA_PDF) -> Path:
    """Descarga un PDF del INEC si todavia no esta en disco."""
    carpeta.mkdir(parents=True, exist_ok=True)
    destino = carpeta / nombre
    if not destino.exists():
        url = URL_BASE + urllib.parse.quote(nombre)
        peticion = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(peticion, timeout=60) as respuesta:
            destino.write_bytes(respuesta.read())
    return destino


def pdf_a_texto(ruta: Path) -> str:
    """Convierte un PDF a texto conservando las columnas (pdftotext -layout)."""
    salida = subprocess.run(
        ["pdftotext", "-layout", str(ruta), "-"], capture_output=True, text=True, check=True
    )
    return salida.stdout


def extraer_mes_provincia(texto: str, anio: int) -> pd.DataFrame:
    """Devuelve anio, mes (1 a 12), provincia, valor y medida (accidentes, heridos, muertos).

    Falla si una fila no suma su total o si los meses no suman la fila anual.
    Las comarcas que la tabla no trae como columna no aparecen en el resultado.
    """
    limpio = _limpiar(texto)
    inicio = re.search(r"Accidentes de transito (?=[\d-])", limpio)
    if inicio is None:
        raise ValueError(f"{anio}: no se encontro la fila de accidentes")
    encabezado = limpio[: inicio.start()]
    cuerpo = limpio[inicio.start():]
    corte = re.search(r"\s-\s+Cantidad nula|Fuente:", cuerpo)
    tokens = (cuerpo[: corte.start()] if corte else cuerpo).split()

    filas, actual, i = [], None, 0
    while i < len(tokens):
        token = tokens[i]
        if tokens[i:i + 3] == ["Accidentes", "de", "transito"]:
            actual = ["accidentes", 0, []]
            i += 3
        elif token in ("Heridos", "Muertos") or token in MESES:
            if token in MESES:
                actual = [actual[0], MESES.index(token) + 1, []]
            else:
                actual = [token.lower(), 0, []]
            i += 1
        else:
            if actual is not None and _NUMERO.match(token):
                if not actual[2]:
                    filas.append(actual)
                actual[2].append(_valor(token))
            i += 1

    columnas = list(PROVINCIAS)
    if "Kuna" in encabezado:
        columnas.append("Guna Yala")
    if "Embera" in encabezado:
        columnas.append("Embera")
    columnas.append("Ngabe Bugle")

    registros, anuales = [], {}
    for medida, mes, valores in filas:
        if len(valores) != len(columnas) + 1:
            raise ValueError(f"{anio} {medida} {mes}: {len(valores)} valores y se esperaban {len(columnas) + 1}")
        if sum(valores[1:]) != valores[0]:
            raise ValueError(f"{anio} {medida} {mes}: las provincias no suman el total")
        if mes == 0:
            anuales[medida] = valores[1:]
            continue
        for provincia, valor in zip(columnas, valores[1:]):
            registros.append((anio, mes, provincia, valor, medida))

    df = pd.DataFrame(registros, columns=["anio", "mes", "provincia", "valor", "medida"])
    for medida, valores in anuales.items():
        sumas = df[df["medida"] == medida].groupby("provincia", sort=False)["valor"].sum()
        if df[df["medida"] == medida]["mes"].nunique() != 12 or list(sumas) != valores:
            raise ValueError(f"{anio} {medida}: los 12 meses no suman la fila anual")
    return df


def extraer_clase_provincia(texto: str, anio: int) -> pd.DataFrame:
    """Devuelve anio, provincia, clase y accidentes con cuatro clases comparables.

    Las clases son Colision (incluye colision con objeto fijo), Atropello,
    Vuelco y Otras. Asi las cifras de los 10 anios se pueden comparar.
    """
    tokens = _limpiar(texto).split()
    if "TOTAL" not in tokens:
        raise ValueError(f"{anio}: no se encontro la fila TOTAL")
    pos = tokens.index("TOTAL") + 1
    cantidad = 0
    while pos + cantidad < len(tokens) and _NUMERO.match(tokens[pos + cantidad]):
        cantidad += 1
    n_clases = cantidad - 1
    if n_clases not in CLASES_PUBLICADAS:
        raise ValueError(f"{anio}: la tabla trae {n_clases} clases y no se conoce ese formato")

    def buscar(nombre: str, desde: int):
        palabras = nombre.split()
        for i in range(desde, len(tokens) - cantidad):
            siguiente = tokens[i + len(palabras): i + len(palabras) + cantidad]
            if tokens[i:i + len(palabras)] == palabras and all(_NUMERO.match(t) for t in siguiente):
                return i, [_valor(t) for t in siguiente]
        return None

    unidades = [(p, p) for p in PROVINCIAS] + COMARCAS
    agrupar = {"Colision": "Colision", "Colision con objeto fijo": "Colision",
               "Vuelco": "Vuelco", "Atropello": "Atropello", "Otras": "Otras"}
    registros, desde = [], pos + cantidad
    for nombre_pdf, nombre in unidades:
        hallado = buscar(nombre_pdf, desde)
        if hallado is None:
            if nombre in PROVINCIAS and (anio, nombre) not in VACIOS_CONOCIDOS:
                raise ValueError(f"{anio}: no se encontro la provincia {nombre}")
            continue
        desde, valores = hallado[0] + 1, hallado[1]
        if sum(valores[1:]) != valores[0]:
            raise ValueError(f"{anio} {nombre}: las clases no suman el total")
        conteo = dict.fromkeys(["Colision", "Atropello", "Vuelco", "Otras"], 0)
        for clase, valor in zip(CLASES_PUBLICADAS[n_clases], valores[1:]):
            conteo[agrupar[clase]] += valor
        for clase, extra in CORRECCIONES_CONOCIDAS.get((anio, nombre), {}).items():
            conteo[clase] += extra
        registros += [(anio, nombre, clase, valor) for clase, valor in conteo.items()]
    return pd.DataFrame(registros, columns=["anio", "provincia", "clase", "accidentes"])


def validar_contra_base(tabla: pd.DataFrame, columna: str, base: pd.DataFrame) -> pd.DataFrame:
    """Compara los totales anuales por provincia con la base verificada del INEC.

    Devuelve las filas que no coinciden (vacio si todo cuadra). Una provincia que
    la tabla no trae cuenta como cero, salvo los vacios conocidos de la fuente.
    """
    if "medida" in tabla.columns:
        tabla = tabla[tabla["medida"] == "accidentes"]
    suma = tabla.groupby(["anio", "provincia"], as_index=False)[columna].sum()
    suma = suma.rename(columns={columna: "en_tabla"})
    union = base.rename(columns={"accidentes": "en_base"}).merge(
        suma, on=["anio", "provincia"], how="outer"
    ).fillna(0)
    distintas = union[union["en_base"] != union["en_tabla"]]
    conocido = [(a, p) in VACIOS_CONOCIDOS for a, p in zip(distintas["anio"], distintas["provincia"])]
    return distintas[[not c for c in conocido]].reset_index(drop=True)


def generar_csv(carpeta_salida: Path = RUTA_EXTERNAL) -> dict:
    """Descarga, convierte, valida y escribe los dos CSV. Devuelve las diferencias halladas."""
    base = cargar_accidentes()
    meses, clases = [], []
    for anio, nombre in ARCHIVOS_MES.items():
        meses.append(extraer_mes_provincia(pdf_a_texto(descargar_pdf(nombre)), anio))
    for anio, nombre in ARCHIVOS_CLASE.items():
        clases.append(extraer_clase_provincia(pdf_a_texto(descargar_pdf(nombre)), anio))
    mes = pd.concat(meses, ignore_index=True)
    clase = pd.concat(clases, ignore_index=True)

    diferencias = {
        "mes": validar_contra_base(mes, "valor", base),
        "clase": validar_contra_base(clase, "accidentes", base),
    }
    carpeta_salida.mkdir(parents=True, exist_ok=True)
    mes.to_csv(carpeta_salida / "accidentes_mes_provincia.csv", index=False)
    clase.to_csv(carpeta_salida / "accidentes_clase_provincia.csv", index=False)
    return diferencias


if __name__ == "__main__":
    resultado = generar_csv()
    for nombre, tabla in resultado.items():
        print(f"Diferencias contra la base en {nombre}: {len(tabla)}")
        if len(tabla):
            print(tabla.to_string())
