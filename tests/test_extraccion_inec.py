import pandas as pd
import pytest

from src import datos, extraccion_inec as ext

NOMBRES_PROVINCIAS = {
    "Bocas del Toro", "Cocle", "Colon", "Chiriqui", "Darien", "Herrera", "Los Santos",
    "Panama", "Panama Oeste", "Veraguas", "Guna Yala", "Embera", "Ngabe Bugle",
}
NOMBRES_PDF = [
    "Bocas del Toro", "Coclé", "Colón", "Chiriquí", "Darién", "Herrera", "Los Santos",
    "Panamá", "Panamá Oeste", "Veraguas",
]


def _fmt(valor: int) -> str:
    return f"{valor:,}"


def _texto_mes() -> str:
    """Tabla mensual de prueba con 10 provincias y la comarca Ngabe Bugle (11 columnas)."""
    meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio",
             "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    lineas = [
        "Cuadro 13. ACCIDENTES DE TRÁNSITO, HERIDOS Y MUERTOS EN LA REPÚBLICA: AÑO 2016",
        "Accidentes de tránsito, heridos y muertos",
        "Mes  Total  Bocas del Toro  Coclé  Colón  Chiriquí  Comarca Ngäbe Buglé",
    ]
    for etiqueta in ("Accidentes de tránsito", "Heridos", "Muertos"):
        por_mes = [[m + j for j in range(11)] for m in range(1, 13)]
        anual = [sum(f[j] for f in por_mes) for j in range(11)]
        lineas.append(f"{etiqueta}  {_fmt(sum(anual))}  " + "  ".join(_fmt(v) for v in anual))
        for nombre, fila in zip(meses, por_mes):
            lineas.append(f"    {nombre}  {_fmt(sum(fila))}  " + "  ".join(_fmt(v) for v in fila))
    lineas += ["- Cantidad nula o cero.", "Fuente: Departamento de Operaciones del Tránsito."]
    return "\n".join(lineas)


def _texto_clase() -> str:
    """Tabla por clase de prueba con 5 clases: total, colision, objeto fijo, vuelco, atropello, otras."""
    lineas = [
        "Cuadro 3. ACCIDENTES DE TRÁNSITO EN LA REPÚBLICA, POR CLASE: AÑO 2022",
        "TOTAL  103  70  20  5  6  2",
        "Calles y avenidas del distrito de Colón  7  5  1  1  0  0",
    ]
    for nombre in NOMBRES_PDF:
        lineas.append(f"{nombre}  10  5  2  1  1  1")
        lineas.append("    Otras carreteras vecinales  10  5  2  1  1  1")
        lineas.append(f"  {nombre}  4  2  1  1  -  -")
    lineas.append("Comarca Ngäbe Buglé  3  1  1  -  1  -")
    return "\n".join(lineas)


def test_mes_provincia_devuelve_meses_y_medidas():
    df = ext.extraer_mes_provincia(_texto_mes(), 2016)
    assert set(df["medida"]) == {"accidentes", "heridos", "muertos"}
    assert df["mes"].nunique() == 12
    assert df["provincia"].nunique() == 11
    assert not df.duplicated(["anio", "mes", "provincia", "medida"]).any()


def test_mes_provincia_rechaza_un_total_que_no_suma():
    texto = _texto_mes().replace("Enero  ", "Enero  9", 1)
    with pytest.raises(ValueError):
        ext.extraer_mes_provincia(texto, 2016)


def test_clase_provincia_agrupa_en_cuatro_clases_y_conserva_el_total():
    df = ext.extraer_clase_provincia(_texto_clase(), 2022)
    assert set(df["clase"]) == {"Colision", "Atropello", "Vuelco", "Otras"}
    bocas = df[df["provincia"] == "Bocas del Toro"].set_index("clase")["accidentes"]
    assert bocas["Colision"] == 7 and bocas["Vuelco"] == 1 and bocas.sum() == 10
    esperadas = (NOMBRES_PROVINCIAS - {"Guna Yala", "Embera"})
    assert set(df["provincia"]) == esperadas


def test_clase_provincia_ignora_el_distrito_con_nombre_de_provincia():
    df = ext.extraer_clase_provincia(_texto_clase(), 2022)
    colon = df[df["provincia"] == "Colon"]["accidentes"].sum()
    assert colon == 10


@pytest.fixture(scope="module")
def mes():
    return pd.read_csv(ext.RUTA_EXTERNAL / "accidentes_mes_provincia.csv")


@pytest.fixture(scope="module")
def clase():
    return pd.read_csv(ext.RUTA_EXTERNAL / "accidentes_clase_provincia.csv")


def test_csv_mes_cuadra_con_la_base(mes):
    assert ext.validar_contra_base(mes, "valor", datos.cargar_accidentes()).empty


def test_csv_clase_cuadra_con_la_base(clase):
    assert ext.validar_contra_base(clase, "accidentes", datos.cargar_accidentes()).empty


def test_csv_mes_cubre_diez_anios_y_doce_meses(mes):
    assert sorted(mes["anio"].unique()) == list(range(2016, 2026))
    assert (mes.groupby("anio")["mes"].nunique() == 12).all()
    assert not mes.duplicated(["anio", "mes", "provincia", "medida"]).any()


def test_csv_usan_los_nombres_de_provincia_de_la_base(mes, clase):
    assert set(mes["provincia"]) <= NOMBRES_PROVINCIAS
    assert set(clase["provincia"]) <= NOMBRES_PROVINCIAS


def test_csv_mes_totales_nacionales_por_anio(mes):
    totales = datos.cargar_totales_inec().set_index("anio")["total_nacional"]
    accidentes = mes[mes["medida"] == "accidentes"].groupby("anio")["valor"].sum()
    assert (accidentes == totales).all()


def test_csv_mes_victimas_2023_y_2025(mes):
    victimas = mes.groupby(["anio", "medida"])["valor"].sum()
    assert victimas[(2023, "heridos")] == 14246 and victimas[(2023, "muertos")] == 362
    assert victimas[(2025, "heridos")] == 17405 and victimas[(2025, "muertos")] == 360


def test_csv_clase_corrige_veraguas_2017(clase):
    veraguas = clase[(clase["anio"] == 2017) & (clase["provincia"] == "Veraguas")]
    assert veraguas["accidentes"].sum() == 1732


def test_csv_clase_deja_vacio_los_santos_2020(clase):
    assert clase[(clase["anio"] == 2020) & (clase["provincia"] == "Los Santos")].empty


def test_csv_clase_cuatro_clases_por_provincia_y_anio(clase):
    assert set(clase["clase"]) == {"Colision", "Atropello", "Vuelco", "Otras"}
    assert (clase.groupby(["anio", "provincia"])["clase"].nunique() == 4).all()
