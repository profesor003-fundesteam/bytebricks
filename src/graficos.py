"""Figuras de matplotlib y seaborn para el dashboard."""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.figure import Figure


def linea_total(total: pd.Series) -> Figure:
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(total.index, total.values, marker="o")
    ax.set_title("Accidentes de transito en Panama por anio")
    ax.set_xlabel("Anio")
    ax.set_ylabel("Accidentes")
    ax.set_xticks(total.index)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    return fig


def barras_provincias(resumen: pd.DataFrame) -> Figure:
    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.bar(resumen.index, resumen["total"])
    ax.set_title("Accidentes acumulados por provincia")
    ax.set_ylabel("Accidentes")
    ax.tick_params(axis="x", rotation=60)
    fig.tight_layout()
    return fig


def mapa_calor(tabla: pd.DataFrame) -> Figure:
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(tabla.T, cmap="Reds", ax=ax, cbar_kws={"label": "Accidentes"})
    ax.set_title("Accidentes por provincia y anio")
    ax.set_xlabel("Anio")
    ax.set_ylabel("")
    fig.tight_layout()
    return fig


def barras_zonas(zonas: pd.DataFrame) -> Figure:
    fig, ax = plt.subplots(figsize=(9, 4))
    zonas.plot(kind="bar", stacked=True, ax=ax)
    ax.set_title("Accidentes por zona")
    ax.set_ylabel("Accidentes")
    ax.set_xlabel("Anio")
    fig.tight_layout()
    return fig
