"""Dashboard de accidentes de transito en Panama (ByteBricks).

Ejecutar con: streamlit run app.py
"""

import streamlit as st

from src import analisis, datos, graficos

st.set_page_config(page_title="ByteBricks | Accidentes en Panama", layout="wide")


@st.cache_data
def cargar() -> tuple:
    return datos.cargar_accidentes(), datos.cargar_totales_inec()


accidentes, totales_inec = cargar()

st.title("Accidentes de transito en Panama, 2016-2025")
st.caption(
    "Equipo ByteBricks. Samsung Innovation Campus, Certificacion en Python e Inteligencia Artificial. "
    "Fuente: INEC, con datos del Departamento de Operaciones del Transito de la Policia Nacional."
)

anios = sorted(accidentes["anio"].unique())
provincias = sorted(accidentes["provincia"].unique())

with st.sidebar:
    st.header("Filtros")
    rango = st.slider("Rango de anios", anios[0], anios[-1], (anios[0], anios[-1]))
    seleccion = st.multiselect("Provincias y comarcas", provincias, default=provincias)

if not seleccion:
    st.warning("Selecciona al menos una provincia o comarca.")
    st.stop()

filtrado = accidentes[
    accidentes["anio"].between(*rango) & accidentes["provincia"].isin(seleccion)
]
total = analisis.total_por_anio(filtrado)
tabla = analisis.tabla_anio_provincia(filtrado)
resumen = analisis.resumen_provincias(filtrado)

col1, col2, col3 = st.columns(3)
col1.metric(f"Accidentes en {rango[1]}", f"{total[rango[1]]:,}")
if rango[0] != rango[1]:
    variacion = analisis.variacion_anual(total).iloc[-1]
    col2.metric("Variacion frente al anio anterior", f"{variacion:.1f} %")
col3.metric("Provincia con mas accidentes", resumen.index[0])

tab_total, tab_prov, tab_zona, tab_datos = st.tabs(
    ["Tendencia nacional", "Provincias", "Panama y Panama Oeste", "Verificacion de datos"]
)

with tab_total:
    st.pyplot(graficos.linea_total(total))
    if {2019, 2020}.issubset(total.index):
        e = analisis.efecto_2020(total)
        st.write(
            f"En 2020 los accidentes cayeron {abs(e['caida_2020'])} % frente a 2019. "
            f"Hasta {e['ultimo_anio']} se recuperaron {e['recuperacion']} % y el total quedo "
            f"{e['ultimo_vs_2019']} % respecto a 2019."
        )
    st.dataframe(
        {"Total": total, "Variacion anual (%)": analisis.variacion_anual(total)},
        width="stretch",
    )

with tab_prov:
    st.pyplot(graficos.barras_provincias(resumen))
    st.pyplot(graficos.mapa_calor(tabla))
    st.dataframe(resumen, width="stretch")
    if rango[0] != rango[1]:
        st.subheader(f"Crecimiento {rango[0]} a {rango[1]} (%)")
        st.caption("Se excluyen las provincias que parten de 0 accidentes.")
        st.dataframe(analisis.crecimiento_periodo(tabla, *rango), width="stretch")

with tab_zona:
    peso = analisis.peso_zona_metropolitana(tabla)
    st.pyplot(graficos.barras_zonas(analisis.accidentes_por_zona(tabla)))
    st.write("Porcentaje del total que concentran Panama y Panama Oeste, por anio:")
    st.dataframe(peso.rename("Peso (%)"), width="stretch")

with tab_datos:
    st.write("La suma de las provincias debe coincidir con el total publicado por el INEC.")
    verificacion = datos.verificar_totales(accidentes, totales_inec)
    st.dataframe(verificacion, width="stretch")
    if verificacion["coincide"].all():
        st.success("Los totales coinciden en todos los anios.")
    else:
        st.error("Hay anios donde la suma no coincide con el INEC.")
