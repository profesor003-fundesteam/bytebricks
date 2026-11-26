"""Carga y validacion de los datos de accidentes de transito (INEC)."""

from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
RUTA_RAW = RAIZ / "data" / "raw"
RUTA_EXTERNAL = RAIZ / "data" / "external"

COLUMNAS_ACCIDENTES = {"anio", "provincia", "accidentes"}


def cargar_accidentes(ruta: Path = RUTA_RAW / "accidentes_provincia_anio.csv") -> pd.DataFrame:
    """Devuelve accidentes por provincia y anio en formato largo."""
    df = pd.read_csv(ruta)
    faltantes = COLUMNAS_ACCIDENTES - set(df.columns)
    if faltantes:
        raise ValueError(f"Faltan columnas en {ruta.name}: {sorted(faltantes)}")
    df = df.astype({"anio": int, "accidentes": int})
    if df.isnull().any().any():
        raise ValueError("El archivo de accidentes tiene valores nulos")
    if df.duplicated(["anio", "provincia"]).any():
        raise ValueError("Hay filas duplicadas por anio y provincia")
    return df


def cargar_totales_inec(ruta: Path = RUTA_RAW / "totales_inec_por_anio.csv") -> pd.DataFrame:
    """Devuelve el total nacional por anio tal como lo publica el INEC."""
    return pd.read_csv(ruta)


def verificar_totales(accidentes: pd.DataFrame, totales: pd.DataFrame) -> pd.DataFrame:
    """Compara la suma de provincias contra el total publicado por el INEC."""
    suma = accidentes.groupby("anio", as_index=False)["accidentes"].sum()
    out = totales.merge(suma, on="anio", how="outer")
    out["coincide"] = out["total_nacional"] == out["accidentes"]
    return out


def _leer_externo(ruta: Path, columnas: set) -> pd.DataFrame:
    df = pd.read_csv(ruta)
    faltantes = columnas - set(df.columns)
    if faltantes:
        raise ValueError(f"Faltan columnas en {ruta.name}: {sorted(faltantes)}")
    if df.isnull().any().any():
        raise ValueError(f"{ruta.name} tiene valores nulos")
    return df


def cargar_accidentes_mes(ruta: Path = RUTA_EXTERNAL / "accidentes_mes_provincia.csv") -> pd.DataFrame:
    """Devuelve anio, mes, provincia, valor y medida (accidentes, heridos o muertos)."""
    return _leer_externo(ruta, {"anio", "mes", "provincia", "valor", "medida"})


def cargar_accidentes_clase(ruta: Path = RUTA_EXTERNAL / "accidentes_clase_provincia.csv") -> pd.DataFrame:
    """Devuelve anio, provincia, clase y accidentes (cuatro clases comparables)."""
    return _leer_externo(ruta, {"anio", "provincia", "clase", "accidentes"})


def cargar_lluvia(ruta: Path = RUTA_EXTERNAL / "lluvia_mes_provincia.csv") -> pd.DataFrame:
    """Devuelve anio, mes, provincia y lluvia_mm (10 provincias, sin comarcas)."""
    return _leer_externo(ruta, {"anio", "mes", "provincia", "lluvia_mm"})
