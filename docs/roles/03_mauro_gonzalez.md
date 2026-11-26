# Plan de Mauro González

Roles: desarrollador del dashboard y diseñador visual.

Este plan amplía `docs/plan_general.md`. Presentación: sábado 5 de diciembre de 2026.

## Tu papel

Eres quien hace que todo se vea y funcione en la pantalla. El dashboard es el entregable principal, y lo que la rúbrica mira en Resultados (visualización, practicidad, rendimiento y madurez) depende de tu trabajo. Los demás te entregan funciones y tú las conviertes en pestañas claras.

## Contexto que necesitas

El proyecto es un dashboard interactivo en Streamlit sobre los accidentes de tránsito de Panamá entre 2016 y 2025, con datos oficiales del INEC. Compara provincias por tasas (accidentes en relación con la cantidad de gente) y una IA explica los resultados con palabras sencillas. Fecha de presentación: sábado 5 de diciembre de 2026. Todo el contexto completo está en `docs/plan_general.md`; léelo antes de empezar.

Lo que ya existe:
- `app.py`: dashboard base con filtros por año y provincia y cuatro pestañas.
- `src/datos.py`: `cargar_accidentes()`, `cargar_totales_inec()` y `verificar_totales()`.
- `src/analisis.py`: totales por año, variación anual, resumen por provincia, crecimiento por periodo, peso de Panamá y Panamá Oeste, y efecto de 2020.
- `src/graficos.py`: figuras de matplotlib y seaborn.
- `tests/`: pruebas de los datos y las métricas.
- `data/raw/accidentes_provincia_anio.csv`: formato largo (anio, provincia, accidentes), 13 provincias y comarcas por 10 años, verificado contra los totales del INEC.
- `docs/fuentes_datos.md`: dónde está cada dato, su estado y sus límites. Léelo antes de buscar datos nuevos.

Los nombres de provincias van sin tildes y siempre iguales: Bocas del Toro, Cocle, Colon, Chiriqui, Darien, Herrera, Los Santos, Panama, Panama Oeste, Veraguas, Guna Yala, Embera y Ngabe Bugle. Cualquier tabla nueva debe usar exactamente esos nombres para poder unirse con la base.

Reglas del proyecto:
- Pandas calcula todos los números. La IA solo los explica y nunca inventa cifras.
- Todo dato nuevo se registra en `docs/fuentes_datos.md` con su fuente, enlace, estado y límites. No se inventan datos: si un dato no existe, la celda queda vacía y se explica.
- Las cifras de las comarcas (Guna Yala, Emberá y Ngäbe Buglé) son muy pequeñas: no se sacan conclusiones sin más datos.
- La tasa por vehículo se muestra solo como comparación con advertencia, porque el registro de placas la distorsiona.
- Las funciones van en `src/` y devuelven datos; `app.py` solo arma la pantalla. Cada función nueva lleva su prueba en `tests/`.
- Código claro, sin emojis, con nombres en español y comentarios solo donde hagan falta.

## Tus tareas, en orden

### 1. Tema visual de Samsung (jueves 26)

Crea `.streamlit/config.toml` con los colores del PPT oficial del SIC (colores principal, de fondo, del texto y de las tarjetas). Como referencia, el azul de Samsung ronda el `#1428A0`; verifícalo contra el PPT oficial antes de usarlo. Aplica la misma paleta a los gráficos en `src/graficos.py` y pon la fuente en cada gráfico. Que el dashboard y la presentación se vean como un solo producto.

### 2. Estructura del dashboard (jueves 26)

Deja `app.py` delgado: filtros, métricas y la lista de pestañas. Crea `src/vistas.py` con una función por pestaña (`mostrar_tendencia`, `mostrar_provincias`, `mostrar_tasas`, `mostrar_estadistica`, `mostrar_ia` y `mostrar_acerca`). Así cada integrante entrega funciones y tú las conectas sin tocar su código. Mueve a esas funciones lo que ya existe, sin cambiar lo que se ve hoy.

### 3. Pestaña "Acerca de" (jueves 26 y viernes 27)

Debe explicar con palabras simples: qué es el proyecto, de dónde salen los datos (enlaces del INEC), qué es una tasa, las limitaciones (las comarcas tienen cifras pequeñas, los vehículos tienen un sesgo de registro) y cómo se conecta con la UNESCO (inclusión y supervisión humana). Incluye al equipo con sus roles.

### 4. Pestaña Tasas (lunes 30)

Cuando José suba `src/tasas.py`, arma la pestaña: barras de la tasa por 100 000 habitantes con selector de año, comparación del ranking por conteo contra el ranking por tasa, y la tasa por vehículo con su advertencia visible. Muestra un aviso en las comarcas. Ponte de acuerdo con José en los nombres y parámetros de las funciones antes de que termine, para no esperar.

### 5. Pestañas de estadística e IA (martes 1 de diciembre)

Con las funciones de Marian (`src/estadistica.py`) y de Artemio (`src/ia.py`), arma las pestañas. Cada resultado va acompañado de una frase en palabras simples. Si falta una función, la pestaña muestra un mensaje claro en vez de fallar.

### 6. Rendimiento y practicidad

Usa `st.cache_data` en la carga de datos, mantén la app rápida y revisa que nunca se caiga si falta un archivo o si la IA no responde. Que un compañero pueda correrla con solo `pip install -r requirements.txt` y `streamlit run app.py`.

### 7. Pruebas del dashboard

Crea `tests/test_app.py` con `streamlit.testing.v1.AppTest`: que la app cargue sin errores, que muestre las métricas correctas, que avise si no hay provincias seleccionadas y que cada pestaña se pueda abrir.

## Mientras esperas las funciones de los demás

Avanza con lo que ya existe: el tema, la estructura de `src/vistas.py` y la pestaña "Acerca de". Puedes probar las pestañas nuevas con datos de ejemplo, pero no los subas ni los muestres como reales.

## Primer paso hoy

Clonar el repositorio, correr `streamlit run app.py` para ver el estado actual y abrir el PPT oficial para sacar los colores.

## Cómo subir tu trabajo (Git)

Trabajamos directo en `main`, sin ramas ni pull requests, porque este repositorio es solo del Proyecto 1. Para no pisarnos, edita sobre todo tus propios archivos y actualiza siempre antes de subir.

Una sola vez:

    git config --global user.name "Tu Nombre"
    git config --global user.email "tu-correo@ejemplo.com"
    git clone https://github.com/profesor003-fundesteam/bytebricks.git
    cd bytebricks
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt

Cada vez que empiezas:

    git pull --rebase origin main

Mientras trabajas, commits pequeños con un mensaje en primera persona:

    git status
    git add <tus archivos>
    git commit -m "feat: agrego <lo que hiciste>"

Para subir:

    git pull --rebase origin main
    git push origin main

Prefijos: `feat`, `fix`, `data`, `docs`, `test` y `chore`. Si aparece un conflicto, no lo resuelvas a ciegas: avisa a Marian. Nunca uses `git push --force`. No subas claves, el entorno virtual, cédulas ni los documentos de Samsung. Sube tu trabajo seguido: la rúbrica mira que la carga esté repartida y que se note en el historial de cada quien.
