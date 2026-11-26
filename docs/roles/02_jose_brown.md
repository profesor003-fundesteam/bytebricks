# Plan de José Brown

Roles: analista de datos y analista de tasas.

Este plan amplía `docs/plan_general.md`. Presentación: sábado 5 de diciembre de 2026.

## Tu papel

Eres quien consigue y prepara los datos que hacen especial al proyecto: población y vehículos. Con ellos calculas las tasas, que es lo que cambia el ranking de provincias y le da sentido al análisis. Tu trabajo es la base de lo que Mauro muestra en el dashboard.

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

### 1. Población 2016-2025 (jueves 26)

Ya confirmamos que el INEC publica el censo 2023 y proyecciones de población al 1 de julio por provincia y comarca. Solo vimos las de 2023 y 2024. Los enlaces están en la sección 2 de `docs/fuentes_datos.md`.
1. Busca en el INEC las proyecciones de 2016 a 2022 y 2025.
2. Elige una sola serie y documenta cuál. Ojo: el censo y las proyecciones no coinciden entre sí (Bocas del Toro tiene 159 228 en el censo 2023, 194 971 en la proyección de 2023 y 186 740 en la de 2024). No mezcles series sin decirlo.
3. Guarda `data/external/poblacion_provincia_anio.csv` con las columnas anio, provincia, poblacion y origen: 13 unidades por 10 años son 130 filas. Si te falta un año y decides interpolar, marca esa fila con origen "interpolado" y los demás con "dato".
4. Verifica que la suma de las 13 unidades de cada año iguale el total nacional del mismo archivo.

Terminado cuando: el CSV existe, suma bien en cada año y la serie elegida está justificada en `docs/fuentes_datos.md`.

### 2. Vehículos por provincia (jueves 26 y viernes 27)

El INEC publica los automóviles en circulación por provincia cada año desde 2014. Los enlaces están en la sección 3 de `docs/fuentes_datos.md`.
1. Descarga las tablas de 2016 a 2024 (la de 2025 puede no existir todavía: si no está, no la inventes).
2. Guarda `data/external/vehiculos_provincia_anio.csv` con las columnas anio, provincia y vehiculos. Son 10 provincias; las comarcas no aparecen en la fuente, déjalas fuera y no las rellenes.
3. Anota el sesgo en `docs/fuentes_datos.md`: Panamá Oeste y Darién salen con muy pocos vehículos porque el registro de placas se hace en otros lugares.

Terminado cuando: el CSV tiene los años que existen y el sesgo está documentado.

### 3. Limpieza y unión (viernes 27)

En `src/datos.py` agrega `cargar_poblacion()`, `cargar_vehiculos()` y una función que una todo con la base de accidentes por anio y provincia. Valida que no haya duplicados, que los nombres de provincias coincidan exactamente con la base, y que los nulos sean solo los esperados (las comarcas en vehículos). Agrega pruebas en `tests/test_datos.py`.

### 4. Tasas (sábado 28 al lunes 30)

Crea `src/tasas.py` con funciones que devuelvan tablas:
- `tasa_por_100mil_habitantes`: accidentes divididos entre población, por 100 000.
- `tasa_por_mil_vehiculos`: igual con vehículos, ignorando las comarcas. Pon la advertencia del sesgo en el docstring.
- Una función que compare el ranking por conteo contra el ranking por tasa en un año.
- Una función que calcule qué provincias empeoraron más desde 2019 según su tasa (pregunta 10 del plan).

Como referencia, la prueba que hice con la proyección de 2024 dio, por 100 000 habitantes: Panamá 1 703, Panamá Oeste 1 093, Herrera 864 y Chiriquí 851, y Herrera pasa del puesto 7 por conteo al 3 por tasa. Tu serie puede dar números distintos: documenta la diferencia en vez de forzarla. Cada función lleva su prueba en `tests/test_tasas.py`.

Terminado cuando: las funciones corren con datos reales, tienen pruebas y Mauro las conectó al dashboard.

### 5. Entrega a Mauro (lunes 30)

Avísale por el grupo cuando `src/tasas.py` esté subido, con los nombres de las funciones y qué devuelve cada una. Antes, ponte de acuerdo con él en esas firmas para que no tenga que adivinar.

### 6. Fuentes

Mantén `docs/fuentes_datos.md` al día: cada archivo nuevo lleva fuente, enlace, fecha de descarga y límites.

## Primer paso hoy

Clonar el repositorio, abrir el INEC y buscar las proyecciones de población de 2016 a 2022 y 2025.

## Cómo subir tu trabajo (Git)

Nadie sube directo a `main`. Cada cambio va en una rama propia y entra por un pull request (PR). El PR corre el CI, una revisión automática que ejecuta `pytest` y confirma que todo funciona junto con lo de los demás. Solo se une cuando el CI sale en verde.

Una sola vez:

    git config --global user.name "Tu Nombre"
    git config --global user.email "tu-correo@ejemplo.com"
    git clone https://github.com/profesor003-fundesteam/bytebricks.git
    cd bytebricks
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt

Cada vez que empiezas una tarea, parte de un `main` actualizado y crea tu rama (prefijo y tema, por ejemplo `data/poblacion` o `feat/tasas`):

    git switch main
    git pull --rebase origin main
    git switch -c feat/tu-tarea

Mientras trabajas, commits pequeños con un mensaje en primera persona:

    git status
    git add <tus archivos>
    git commit -m "feat: agrego <lo que hiciste>"

Para subir, actualiza tu rama con `main`, prueba en local y sube la rama:

    git fetch origin
    git rebase origin/main
    pytest
    git push -u origin feat/tu-tarea

Abre el PR con `gh pr create --fill` o con el botón "Compare & pull request" de GitHub. Espera el CI en verde. Si falla, mira el error en la pestaña Checks, arréglalo en la misma rama y vuelve a subir: el PR se actualiza solo. Cuando el CI esté en verde y Marian lo haya revisado, se une con "Squash and merge" (queda un solo commit por PR, a nombre de quien lo escribió). Después borra la rama y vuelve a `main`:

    git switch main
    git pull --rebase origin main

Prefijos: `feat`, `fix`, `data`, `docs`, `test` y `chore`. Si aparece un conflicto al hacer `rebase`, no lo resuelvas a ciegas: avisa a Marian. Nunca uses `git push --force` sobre `main`. No subas claves, el entorno virtual, cédulas ni los documentos de Samsung (el CI lo revisa). Sube tu trabajo seguido: la rúbrica mira que la carga esté repartida y que se note en el historial de cada quien.
