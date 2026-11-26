# ByteBricks: accidentes de tránsito en Panamá (2016-2025)

Proyecto 1 del Samsung Innovation Campus, Certificación en Python e Inteligencia Artificial.

## Equipo ByteBricks

- Marian Barba: líder, estadística, calidad y documentación
- José Brown: datos y tasas
- Mauro González: dashboard y diseño visual
- Artemio Rodríguez: inteligencia artificial, video y ensayo

## Qué vamos a hacer

Analizamos con Python y pandas los accidentes de tránsito de Panamá entre 2016 y 2025, con estadísticas oficiales del INEC. En lugar de comparar solo conteos por provincia, calculamos tasas por cada 100 000 habitantes y, como comparación con advertencia, por vehículo. Cruzamos los accidentes con población, parque vehicular y calendario, y con lluvia si se consigue una fuente válida, para ver qué factores se relacionan con el aumento.

Como valor agregado con IA, pandas calcula todas las cifras y un modelo de lenguaje solo las explica en español (informe por provincia y consulta en lenguaje natural). La IA no inventa números.

## Cómo lo vamos a hacer

El resultado final es un dashboard interactivo hecho con Streamlit (`app.py`), no un notebook.

1. Base de accidentes por provincia y año, verificada contra los totales del INEC (listo).
2. Dashboard base con filtros, tendencia nacional, provincias y verificación de datos (listo).
3. Datos extra con fuente y fecha documentadas: accidentes por mes y clase, y lluvia mensual (listo; población y vehículos en curso).
4. Estadística: estacionalidad, tipo de accidente, chi-cuadrado y correlación con lluvia (listo en `src/estadistica.py`).
5. Tasas por habitante y por vehículo (en curso).
6. Parte de IA integrada al dashboard (en curso).
7. Presentación.

## Estructura

- `app.py`: punto de entrada del dashboard (Streamlit).
- `src/`: lógica separada de la interfaz: `datos.py` (carga y validación), `analisis.py` (métricas) y `graficos.py` (figuras).
- `tests/`: pruebas de los datos y las métricas.
- `data/raw/`: datos originales; `data/external/`: datos extra; `data/processed/`: tablas limpias.
- `docs/`: plan del proyecto y registro de fuentes.
- `figures/`: gráficos exportados para la presentación.

## Fuente de datos

INEC / Contraloría General, con datos del Departamento de Operaciones del Tránsito de la Policía Nacional. Cuadro 1, accidentes por provincia y comarca, 2016-25:
https://www.inec.gob.pa/archivos/P070554752026081013111101.xlsx.pdf

La suma de las provincias coincide con el total nacional publicado por el INEC en los 10 años. El resto de las fuentes está en `docs/fuentes_datos.md`.
