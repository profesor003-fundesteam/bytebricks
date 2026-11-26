"""Estadistica del proyecto: estacionalidad, tipo de accidente por provincia y lluvia.

Todas las funciones devuelven tablas o diccionarios, nunca graficos. Cada docstring
trae una frase en palabras simples que explica el resultado.
"""

import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency

ANIOS_ATIPICOS = (2020,)
COMARCAS = ("Guna Yala", "Embera", "Ngabe Bugle")


def _coma(valor: float, decimales: int) -> str:
    """Formatea con coma decimal, como se escribe en espanol."""
    return f"{valor:.{decimales}f}".replace(".", ",")


def _total_nacional_por_mes(mes: pd.DataFrame, medida: str, excluir_anios: tuple) -> pd.DataFrame:
    """Tabla con un anio por fila y los 12 meses en columnas (total nacional)."""
    datos = mes[(mes["medida"] == medida) & (~mes["anio"].isin(excluir_anios))]
    return datos.groupby(["anio", "mes"])["valor"].sum().unstack("mes")


def indice_estacional(
    mes: pd.DataFrame, medida: str = "accidentes", excluir_anios: tuple = ANIOS_ATIPICOS
) -> pd.DataFrame:
    """Devuelve mes, promedio e indice de cada mes del anio (total nacional).

    En palabras simples: un indice de 1,10 significa que ese mes tiene 10 % mas
    accidentes que un mes tipico de su mismo anio. El indice se calcula dentro de
    cada anio y luego se promedia, para que el crecimiento de los accidentes con
    los anios no distorsione los meses. Por defecto se deja fuera 2020, un anio
    atipico; pasa excluir_anios=() para incluirlo.
    """
    por_anio = _total_nacional_por_mes(mes, medida, excluir_anios)
    relativo = por_anio.div(por_anio.mean(axis=1), axis=0)
    tabla = pd.DataFrame({"promedio": por_anio.mean().round(0).astype(int), "indice": relativo.mean().round(3)})
    return tabla.rename_axis("mes").reset_index()


def efecto_anio_atipico(mes: pd.DataFrame, anio: int = 2020, medida: str = "accidentes") -> pd.DataFrame:
    """Devuelve mes, indice_con, indice_sin y diferencia al incluir o no un anio.

    En palabras simples: muestra cuanto cambia el indice de cada mes por culpa de
    2020, un anio atipico por la pandemia. Si la diferencia maxima es grande, hay
    que decir que 2020 distorsiona la estacionalidad.
    """
    con = indice_estacional(mes, medida, excluir_anios=())
    sin = indice_estacional(mes, medida, excluir_anios=(anio,))
    tabla = pd.DataFrame({"mes": con["mes"], "indice_con": con["indice"], "indice_sin": sin["indice"]})
    tabla["diferencia"] = (tabla["indice_con"] - tabla["indice_sin"]).round(3)
    return tabla


def _tabla_clase_provincia(clase: pd.DataFrame, incluir_comarcas: bool) -> pd.DataFrame:
    datos = clase if incluir_comarcas else clase[~clase["provincia"].isin(COMARCAS)]
    return datos.pivot_table(index="provincia", columns="clase", values="accidentes", aggfunc="sum", fill_value=0)


def proporcion_clase_por_provincia(clase: pd.DataFrame, incluir_comarcas: bool = False) -> pd.DataFrame:
    """Devuelve el porcentaje de cada clase de accidente en cada provincia (2016-2025).

    En palabras simples: de cada 100 accidentes de una provincia, cuantos fueron
    colisiones, atropellos, vuelcos u otros. Cada fila suma 100. Las comarcas se
    dejan fuera por defecto porque sus cifras son muy pequenas.
    """
    tabla = _tabla_clase_provincia(clase, incluir_comarcas)
    return (tabla.div(tabla.sum(axis=1), axis=0) * 100).round(1)


def chi_cuadrado_clase_provincia(clase: pd.DataFrame, incluir_comarcas: bool = False) -> dict:
    """Prueba si el tipo de accidente depende de la provincia (chi-cuadrado).

    En palabras simples: dice si la mezcla de tipos de accidente cambia de una
    provincia a otra y que tan fuerte es ese cambio. Con tantos accidentes el
    p-valor casi siempre sale minimo, asi que lo que importa es v_cramer (cerca de
    0 es una relacion debil, cerca de 1 es fuerte). Devuelve chi2, p_valor,
    grados_libertad, n, v_cramer, frecuencia_esperada_minima, residuos (tabla de
    cuanto se aleja cada provincia y clase de lo esperado), mayor_diferencia e
    interpretacion (una frase lista para mostrar).
    """
    tabla = _tabla_clase_provincia(clase, incluir_comarcas)
    chi2, p_valor, grados, esperada = chi2_contingency(tabla)
    n = int(tabla.to_numpy().sum())
    v_cramer = float(np.sqrt(chi2 / (n * (min(tabla.shape) - 1))))
    residuos = ((tabla - esperada) / np.sqrt(esperada)).round(1)
    mayor = residuos.stack().abs().idxmax()
    fuerza = "débil" if v_cramer < 0.1 else "moderada" if v_cramer < 0.3 else "fuerte"
    p_texto = "menor que 0,001" if p_valor < 0.001 else f"igual a {_coma(p_valor, 3)}"
    if p_valor < 0.05:
        interpretacion = (
            f"El tipo de accidente sí cambia entre provincias (p {p_texto}), "
            f"pero la relación es {fuerza} (V de Cramér = {_coma(v_cramer, 3)})."
        )
    else:
        interpretacion = f"No hay evidencia de que el tipo de accidente cambie entre provincias (p {p_texto})."
    return {
        "chi2": round(float(chi2), 1),
        "p_valor": float(p_valor),
        "grados_libertad": int(grados),
        "n": n,
        "v_cramer": round(v_cramer, 3),
        "frecuencia_esperada_minima": round(float(esperada.min()), 1),
        "residuos": residuos,
        "mayor_diferencia": {
            "provincia": mayor[0],
            "clase": mayor[1],
            "residuo": float(residuos.loc[mayor]),
        },
        "interpretacion": interpretacion,
    }


def correlacion_lluvia_accidentes(
    mes: pd.DataFrame, lluvia: pd.DataFrame, excluir_anios: tuple = ANIOS_ATIPICOS
) -> pd.DataFrame:
    """Devuelve provincia, correlacion y meses entre la lluvia y los accidentes del mes.

    En palabras simples: dice si en los meses mas lluviosos de una provincia hay mas
    (positivo) o menos (negativo) accidentes de lo normal para ese anio. Cerca de 0
    significa que no hay relacion clara. Los accidentes se miden contra el promedio
    mensual de su provincia y anio, para quitar el efecto del crecimiento anual. La
    lluvia es una estimacion de NASA POWER con limites (ver docs/fuentes_datos.md),
    asi que el resultado es exploratorio. Por defecto se deja fuera 2020.
    """
    accidentes = mes[(mes["medida"] == "accidentes") & (~mes["anio"].isin(excluir_anios))].copy()
    accidentes["relativo"] = accidentes["valor"] / accidentes.groupby(["anio", "provincia"])["valor"].transform("mean")
    unidos = accidentes.merge(lluvia, on=["anio", "mes", "provincia"])
    filas = []
    for provincia, grupo in unidos.groupby("provincia"):
        correlacion = grupo["relativo"].corr(grupo["lluvia_mm"])
        if pd.notna(correlacion):
            filas.append((provincia, round(float(correlacion), 2), len(grupo)))
    return pd.DataFrame(filas, columns=["provincia", "correlacion", "meses"])


def resumen_correlacion_lluvia(tabla: pd.DataFrame) -> dict:
    """Resume la correlacion con la lluvia de todas las provincias en una frase.

    En palabras simples: promedia las correlaciones y dice si hay una relacion
    clara entre lluvia y accidentes. Devuelve correlacion_media, provincias_positivas,
    provincias_negativas, provincia_mayor y interpretacion.
    """
    media = float(tabla["correlacion"].mean())
    mayor = tabla.loc[tabla["correlacion"].abs().idxmax()]
    if abs(media) < 0.2:
        interpretacion = (
            f"No se ve una relación clara entre la lluvia y los accidentes "
            f"(correlación media {_coma(media, 2)}); el signo cambia entre provincias."
        )
    else:
        sentido = "más" if media > 0 else "menos"
        interpretacion = f"En promedio hay {sentido} accidentes en los meses lluviosos (correlación media {_coma(media, 2)})."
    return {
        "correlacion_media": round(media, 2),
        "provincias_positivas": int((tabla["correlacion"] > 0).sum()),
        "provincias_negativas": int((tabla["correlacion"] < 0).sum()),
        "provincia_mayor": {"provincia": mayor["provincia"], "correlacion": float(mayor["correlacion"])},
        "interpretacion": interpretacion,
    }
