"""Metricas del analisis base: totales, variaciones, concentracion y crecimiento."""

import pandas as pd

ZONAS_METROPOLITANAS = ("Panama", "Panama Oeste")


def total_por_anio(df: pd.DataFrame) -> pd.Series:
    return df.groupby("anio")["accidentes"].sum()


def variacion_anual(total: pd.Series) -> pd.Series:
    """Variacion porcentual respecto al anio anterior."""
    return (total.pct_change() * 100).round(1)


def tabla_anio_provincia(df: pd.DataFrame) -> pd.DataFrame:
    return df.pivot_table(index="anio", columns="provincia", values="accidentes", aggfunc="sum")


def resumen_provincias(df: pd.DataFrame) -> pd.DataFrame:
    """Total acumulado, promedio anual y porcentaje por provincia."""
    r = df.groupby("provincia")["accidentes"].agg(total="sum", promedio_anual="mean")
    r["porcentaje"] = (r["total"] / r["total"].sum() * 100).round(1)
    r["promedio_anual"] = r["promedio_anual"].round(0).astype(int)
    return r.sort_values("total", ascending=False)


def peso_zona_metropolitana(tabla: pd.DataFrame) -> pd.Series:
    """Porcentaje del total que concentran Panama y Panama Oeste, por anio."""
    presentes = [p for p in ZONAS_METROPOLITANAS if p in tabla.columns]
    return (tabla[presentes].sum(axis=1) / tabla.sum(axis=1) * 100).round(1)


def accidentes_por_zona(tabla: pd.DataFrame) -> pd.DataFrame:
    presentes = [p for p in ZONAS_METROPOLITANAS if p in tabla.columns]
    zonas = tabla[presentes].copy()
    zonas["Resto del pais"] = tabla.drop(columns=presentes).sum(axis=1)
    return zonas


def crecimiento_periodo(tabla: pd.DataFrame, anio_inicio: int, anio_fin: int) -> pd.Series:
    """Crecimiento porcentual por provincia. Excluye las que parten de 0."""
    base = tabla.loc[anio_inicio]
    base = base[base > 0]
    cambio = (tabla.loc[anio_fin, base.index] - base) / base * 100
    return cambio.round(1).sort_values(ascending=False)


def efecto_2020(total: pd.Series) -> dict:
    """Caida en 2020 frente a 2019, recuperacion hasta el ultimo anio y brecha con 2019."""
    ultimo = total.index.max()
    return {
        "caida_2020": round((total[2020] - total[2019]) / total[2019] * 100, 1),
        "recuperacion": round((total[ultimo] - total[2020]) / total[2020] * 100, 1),
        "ultimo_vs_2019": round((total[ultimo] - total[2019]) / total[2019] * 100, 1),
        "ultimo_anio": int(ultimo),
    }
