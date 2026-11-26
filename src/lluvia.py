"""Lluvia mensual por provincia (NASA POWER, variable PRECTOTCORR).

Uso: python -m src.lluvia
Cada provincia se resume con el promedio de unos puntos representativos
(cabeceras de distrito). La fuente trae milimetros por dia; aqui se convierte
a milimetros por mes. Los datos crudos quedan en data/raw/lluvia_nasa_power/.
"""

import calendar
import json
import urllib.request
from pathlib import Path

import pandas as pd

from src.datos import RAIZ

URL = (
    "https://power.larc.nasa.gov/api/temporal/monthly/point?parameters=PRECTOTCORR"
    "&community=AG&longitude={lon}&latitude={lat}&start={inicio}&end={fin}&format=JSON"
)
RUTA_CRUDOS = RAIZ / "data" / "raw" / "lluvia_nasa_power"
RUTA_SALIDA = RAIZ / "data" / "external" / "lluvia_mes_provincia.csv"
ANIOS = (2016, 2025)

# Puntos aproximados (latitud, longitud). Se omiten las comarcas por su tamano.
PUNTOS = {
    "Bocas del Toro": [(9.34, -82.25), (9.43, -82.52), (8.95, -82.15)],
    "Cocle": [(8.52, -80.36), (8.24, -80.55), (8.62, -80.59)],
    "Colon": [(9.36, -79.90), (9.55, -79.65), (8.90, -80.45)],
    "Chiriqui": [(8.43, -82.43), (8.78, -82.44), (8.28, -82.87)],
    "Darien": [(8.40, -78.15), (8.15, -77.69), (8.50, -77.97)],
    "Herrera": [(7.96, -80.43), (7.94, -80.78)],
    "Los Santos": [(7.77, -80.27), (7.41, -80.44)],
    "Panama": [(8.98, -79.52), (9.17, -79.10), (8.70, -78.62)],
    "Panama Oeste": [(8.88, -79.78), (8.95, -79.66), (8.75, -79.87)],
    "Veraguas": [(8.10, -80.98), (8.00, -81.32), (8.51, -81.07)],
}


def descargar_punto(lat: float, lon: float, carpeta: Path = RUTA_CRUDOS) -> dict:
    """Devuelve {'AAAAMM': mm por dia} de un punto, usando el cache si existe."""
    carpeta.mkdir(parents=True, exist_ok=True)
    archivo = carpeta / f"{lat}_{lon}_{ANIOS[0]}_{ANIOS[1]}.json"
    if not archivo.exists():
        url = URL.format(lat=lat, lon=lon, inicio=ANIOS[0], fin=ANIOS[1])
        with urllib.request.urlopen(url, timeout=60) as respuesta:
            archivo.write_bytes(respuesta.read())
    datos = json.loads(archivo.read_text())
    return datos["properties"]["parameter"]["PRECTOTCORR"]


def lluvia_mensual_punto(serie: dict) -> pd.DataFrame:
    """Pasa mm por dia a mm por mes. Ignora la clave anual (mes 13) y los -999."""
    filas = []
    for clave, mm_dia in serie.items():
        anio, mes = int(clave[:4]), int(clave[4:])
        if mes == 13 or mm_dia == -999:
            continue
        filas.append((anio, mes, mm_dia * calendar.monthrange(anio, mes)[1]))
    return pd.DataFrame(filas, columns=["anio", "mes", "lluvia_mm"])


def construir_tabla() -> pd.DataFrame:
    """Promedia los puntos de cada provincia y devuelve anio, mes, provincia, lluvia_mm."""
    partes = []
    for provincia, puntos in PUNTOS.items():
        series = [lluvia_mensual_punto(descargar_punto(lat, lon)) for lat, lon in puntos]
        promedio = pd.concat(series).groupby(["anio", "mes"], as_index=False)["lluvia_mm"].mean()
        promedio.insert(2, "provincia", provincia)
        partes.append(promedio)
    tabla = pd.concat(partes, ignore_index=True)
    tabla["lluvia_mm"] = tabla["lluvia_mm"].round(1)
    return tabla


if __name__ == "__main__":
    resultado = construir_tabla()
    RUTA_SALIDA.parent.mkdir(parents=True, exist_ok=True)
    resultado.to_csv(RUTA_SALIDA, index=False)
    print(f"{len(resultado)} filas escritas en {RUTA_SALIDA}")
