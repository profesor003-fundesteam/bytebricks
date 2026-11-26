# Plan de Marian Barba

Roles: líder de proyecto e integradora, analista estadística, calidad, y documentación y entregables.

Este plan amplía `docs/plan_general.md`. Presentación: sábado 5 de diciembre de 2026.

## Tu papel

Eres quien mantiene al equipo avanzando y quien responde por que lo entregado sea correcto y se vea bien. Además haces la estadística del proyecto (qué meses y tipos de accidente pesan más) y escribes lo que se entrega: README, formulario, PPT y guion del pitch.

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

### 1. Datos mensuales y por tipo de accidente (jueves 26 y viernes 27)

El INEC publica estas tablas en PDF. Los enlaces y años que vimos están en la sección 5 de `docs/fuentes_datos.md`.
1. Confirma qué años existen para cada tabla: víctimas por provincia y mes, clase de accidente por provincia, y mes y clase (esta última separa distritos, no provincias).
2. Convierte cada PDF con `pdftotext -layout archivo.pdf -` y limpia el resultado con pandas.
3. Guarda los resultados en `data/external/accidentes_mes_provincia.csv` (anio, mes, provincia, valor) y `data/external/accidentes_clase_provincia.csv` (anio, provincia, clase, accidentes).
4. Comprueba que los totales coincidan con los del PDF y anótalo en `docs/fuentes_datos.md`.

Terminado cuando: los CSV existen, los totales cuadran y la fuente de cada uno está registrada. No prometas años que no pudiste confirmar.

### 2. Lluvia (viernes 27)

Prueba una fuente satelital o de reanálisis gratuita con lluvia mensual que se pueda promediar por provincia. Si el viernes 27 no tienes una serie clara y verificable, la lluvia se descarta: anótalo en `docs/fuentes_datos.md` y sigue con meses, tipo de accidente y calendario. Es lo primero que se recorta.

### 3. Estadística (viernes 27 al martes 1 de diciembre)

Crea `src/estadistica.py` con funciones que devuelvan tablas o valores, no gráficos:
- Estacionalidad: promedio de accidentes por mes y un índice (promedio del mes dividido entre el promedio general), para ver qué épocas del año son peores. Revisa si 2020 distorsiona y dilo.
- Relación entre tipo de accidente y provincia con chi-cuadrado (`scipy.stats.chi2_contingency`; agrega `scipy` a `requirements.txt`). Si prefieres algo más simple, compara proporciones con `groupby` y `pivot_table`.
- Si hay lluvia, correlación con `.corr()`.

Cada resultado debe poder explicarse con una frase en palabras simples; escríbela en el docstring. Pásale a Mauro los nombres y parámetros de las funciones antes del lunes 30 para que arme la pestaña. Cada función lleva su prueba en `tests/test_estadistica.py`.

Terminado cuando: las funciones corren con datos reales, tienen pruebas y Mauro las pudo conectar.

### 4. Calidad (todos los días, revisión final el miércoles 2)

- `pytest` debe pasar siempre. Corre `git pull --rebase origin main` y luego `pytest` cada día.
- Revisa los commits de los demás con `git log --oneline` y confirma que cada uno suba su parte.
- Antes del jueves 3, prueba todo desde cero: entorno virtual nuevo, `pip install -r requirements.txt`, `streamlit run app.py`.
- Lista final: ortografía, sin cédulas ni claves en el repositorio, `requirements.txt` completo, todas las fuentes registradas.

### 5. Documentación y entregables (hasta el viernes 4)

- README: planteamiento, objetivos, herramientas y resultado. Mantenlo al día cada vez que cambie algo importante.
- Formulario de desarrollo de Samsung: responde con tus palabras la tabla de integrantes y roles, el nombre del proyecto, la descripción con datos que respalden el problema, y las seis preguntas. Guárdalo en `docs/formulario_desarrollo.md`. Los datos que respaldan el problema están en la base verificada del INEC.
- PPT con el formato oficial del SIC y su línea gráfica. Cada integrante prepara 3 diapositivas y tú las ensamblas. Debe mostrar planteamiento, objetivos, herramientas y resultado con la funcionalidad.
- Guion del pitch de ventas: problema, solución, beneficios y lo que nos diferencia. El repaso de 40 segundos ya está hecho.
- Valores UNESCO: la inclusión es el valor principal, con transparencia y supervisión humana. Está en la sección 9 del plan general.

### 6. Liderazgo

- Domingo 29: revisión de avance con los cuatro. Decide qué se recorta si hay atraso, en este orden: lluvia, chat con IA, estadística avanzada, tasa por vehículo.
- Miércoles 2: congelamos funcionalidades.
- Viernes 4: cada integrante carga todos los elementos en la plataforma. Confirma que los cuatro lo hicieron.

## Primer paso hoy

Publicar todo lo que hay en el repositorio, avisar al grupo para que lo clone, y empezar el punto 1: abrir las tablas mensuales del INEC y listar qué años existen.

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
