"""Carga y validacion de los datos de accidentes de transito (INEC)."""

from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
RUTA_RAW = RAIZ / "data" / "raw"

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
