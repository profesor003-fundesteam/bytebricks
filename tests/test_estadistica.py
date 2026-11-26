import numpy as np
import pandas as pd
import pytest
from scipy.stats import chi2_contingency

from src import datos, estadistica


@pytest.fixture(scope="module")
def mes():
    return datos.cargar_accidentes_mes()


@pytest.fixture(scope="module")
def clase():
    return datos.cargar_accidentes_clase()


@pytest.fixture(scope="module")
def lluvia():
    return datos.cargar_lluvia()


def _mes_sintetico() -> pd.DataFrame:
    """Dos anios con la misma forma estacional, el segundo con el doble de accidentes."""
    forma = np.arange(1, 13) * 10
    filas = []
    for anio, factor in ((2018, 1), (2019, 2)):
        for numero, valor in enumerate(forma, start=1):
            filas.append((anio, numero, "Panama", int(valor * factor), "accidentes"))
    return pd.DataFrame(filas, columns=["anio", "mes", "provincia", "valor", "medida"])


def test_cargadores_traen_las_columnas_esperadas(mes, clase, lluvia):
    assert {"anio", "mes", "provincia", "valor", "medida"} <= set(mes.columns)
    assert {"anio", "provincia", "clase", "accidentes"} <= set(clase.columns)
    assert {"anio", "mes", "provincia", "lluvia_mm"} <= set(lluvia.columns)


def test_indice_estacional_no_depende_del_crecimiento_anual():
    tabla = estadistica.indice_estacional(_mes_sintetico(), excluir_anios=())
    esperado = (np.arange(1, 13) / np.arange(1, 13).mean()).round(3)
    assert list(tabla["indice"]) == list(esperado)
    assert tabla["indice"].mean() == pytest.approx(1.0, abs=0.001)


def test_indice_estacional_excluye_los_anios_pedidos():
    mes = _mes_sintetico()
    mes.loc[mes["anio"] == 2019, "valor"] = 100
    sin = estadistica.indice_estacional(mes, excluir_anios=(2019,))
    assert sin["promedio"].iloc[0] == 10


def test_indice_estacional_real_diciembre_es_el_mes_mas_alto(mes):
    tabla = estadistica.indice_estacional(mes)
    assert len(tabla) == 12
    assert tabla.loc[tabla["indice"].idxmax(), "mes"] == 12
    assert tabla.loc[tabla["indice"].idxmin(), "mes"] in (1, 2)


def test_2020_distorsiona_la_estacionalidad(mes):
    efecto = estadistica.efecto_anio_atipico(mes, 2020)
    assert list(efecto.columns) == ["mes", "indice_con", "indice_sin", "diferencia"]
    assert efecto["diferencia"].abs().max() > 0.05


def test_proporcion_clase_suma_cien_y_deja_fuera_las_comarcas(clase):
    tabla = estadistica.proporcion_clase_por_provincia(clase)
    assert (tabla.sum(axis=1).round(0) == 100).all()
    assert len(tabla) == 10 and "Embera" not in tabla.index
    assert len(estadistica.proporcion_clase_por_provincia(clase, incluir_comarcas=True)) == 13


def test_chi_cuadrado_coincide_con_scipy(clase):
    resultado = estadistica.chi_cuadrado_clase_provincia(clase)
    tabla = clase[~clase["provincia"].isin(estadistica.COMARCAS)].pivot_table(
        index="provincia", columns="clase", values="accidentes", aggfunc="sum"
    )
    chi2, _, grados, _ = chi2_contingency(tabla)
    assert resultado["chi2"] == pytest.approx(chi2, abs=0.1)
    assert resultado["grados_libertad"] == grados == 27
    assert resultado["n"] == int(tabla.to_numpy().sum())


def test_chi_cuadrado_dice_que_la_relacion_es_debil(clase):
    resultado = estadistica.chi_cuadrado_clase_provincia(clase)
    assert 0 < resultado["v_cramer"] < 0.1
    assert resultado["frecuencia_esperada_minima"] >= 5
    assert "débil" in resultado["interpretacion"]
    assert resultado["mayor_diferencia"]["clase"] == "Vuelco"


def test_chi_cuadrado_sin_relacion_no_ve_diferencias():
    filas = [(2020, p, c, 100) for p in ("A", "B", "C") for c in ("Colision", "Vuelco")]
    resultado = estadistica.chi_cuadrado_clase_provincia(pd.DataFrame(filas, columns=["anio", "provincia", "clase", "accidentes"]))
    assert resultado["v_cramer"] == 0
    assert resultado["interpretacion"].startswith("No hay evidencia")


def test_chi_cuadrado_funciona_con_las_comarcas(clase):
    resultado = estadistica.chi_cuadrado_clase_provincia(clase, incluir_comarcas=True)
    assert resultado["grados_libertad"] == 36


def test_correlacion_lluvia_detecta_una_relacion_perfecta():
    meses = range(1, 13)
    lluvia = pd.DataFrame({"anio": 2021, "mes": list(meses), "provincia": "Panama", "lluvia_mm": [m * 10.0 for m in meses]})
    mes = pd.DataFrame({"anio": 2021, "mes": list(meses), "provincia": "Panama", "valor": [100 + m for m in meses], "medida": "accidentes"})
    tabla = estadistica.correlacion_lluvia_accidentes(mes, lluvia)
    assert tabla["correlacion"].iloc[0] == 1.0 and tabla["meses"].iloc[0] == 12


def test_correlacion_lluvia_real_es_debil(mes, lluvia):
    tabla = estadistica.correlacion_lluvia_accidentes(mes, lluvia)
    assert len(tabla) == 10
    assert (tabla["meses"] == 108).all()  # 9 anios de 12 meses, sin 2020
    resumen = estadistica.resumen_correlacion_lluvia(tabla)
    assert abs(resumen["correlacion_media"]) < 0.2
    assert resumen["provincias_positivas"] + resumen["provincias_negativas"] == 10
    assert resumen["interpretacion"].startswith("No se ve una relación clara")
