import pandas as pd

from src import lluvia


def test_lluvia_mensual_punto_convierte_mm_dia_a_mm_mes():
    serie = {"202402": 1.0, "202413": 5.0, "202403": -999.0}
    df = lluvia.lluvia_mensual_punto(serie)
    assert len(df) == 1
    assert df.iloc[0]["lluvia_mm"] == 29.0  # febrero de 2024 tiene 29 dias


def test_csv_lluvia_cubre_diez_provincias_y_diez_anios():
    df = pd.read_csv(lluvia.RUTA_SALIDA)
    assert df["provincia"].nunique() == 10
    assert len(df) == 10 * 120
    assert not df.duplicated(["anio", "mes", "provincia"]).any()
    assert df["lluvia_mm"].notna().all() and (df["lluvia_mm"] >= 0).all()


def test_csv_lluvia_usa_los_nombres_de_la_base():
    df = pd.read_csv(lluvia.RUTA_SALIDA)
    base = pd.read_csv(lluvia.RAIZ / "data" / "raw" / "accidentes_provincia_anio.csv")
    assert set(df["provincia"]) <= set(base["provincia"])


def test_csv_lluvia_la_epoca_lluviosa_supera_a_la_seca():
    df = pd.read_csv(lluvia.RUTA_SALIDA)
    por_mes = df.groupby("mes")["lluvia_mm"].mean()
    assert por_mes.loc[5:11].mean() > 3 * por_mes.loc[1:3].mean()
