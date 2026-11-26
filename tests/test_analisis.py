import pytest

from src import analisis, datos


@pytest.fixture(scope="module")
def accidentes():
    return datos.cargar_accidentes()


def test_totales_coinciden_con_inec(accidentes):
    verificacion = datos.verificar_totales(accidentes, datos.cargar_totales_inec())
    assert verificacion["coincide"].all()


def test_diez_anios_y_trece_provincias(accidentes):
    assert accidentes["anio"].nunique() == 10
    assert accidentes["provincia"].nunique() == 13


def test_total_2025(accidentes):
    assert analisis.total_por_anio(accidentes)[2025] == 53132


def test_crecimiento_excluye_base_cero(accidentes):
    tabla = analisis.tabla_anio_provincia(accidentes)
    crecimiento = analisis.crecimiento_periodo(tabla, 2016, 2025)
    assert crecimiento.replace([float("inf"), float("-inf")], float("nan")).notna().all()
