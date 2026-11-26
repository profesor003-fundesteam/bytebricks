# Plan de Artemio Rodríguez

Roles: ingeniero de IA, pruebas de IA, y video y ensayo.

Este plan amplía `docs/plan_general.md`. Presentación: sábado 5 de diciembre de 2026.

## Tu papel

Eres quien hace que la IA explique los resultados sin inventar nada. Esa es la parte distinta del proyecto, y el profe pidió una API de IA. Tu regla de oro: pandas calcula los números y la IA solo los redacta. También grabas el video de un minuto y diriges el ensayo del pitch.

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

### 1. Elegir la API de IA (jueves 26)

Compara dos o tres opciones: costo, capa gratuita o crédito para estudiantes, límites, facilidad con Python y calidad en español. Revisa los precios y límites hoy, porque cambian. Anota la decisión en `docs/decision_api_ia.md` (cuál elegiste, cuánto cuesta, quién lo paga y qué haces si falla). Habla con el grupo antes de gastar dinero.

### 2. Claves y seguridad (jueves 26)

La clave va en un archivo `.env`, que no se sube nunca (ya está en `.gitignore`). Crea un `.env.example` sin la clave para que los demás sepan qué variable poner. Antes de tu primer commit, revisa con `git status` que `.env` no aparezca. Solo se envían a la API datos agregados, nunca información personal.

### 3. Informe por provincia (jueves 26 al sábado 28)

Crea `src/ia.py` con estas funciones:
- `resumen_provincia`: calcula con pandas, usando `src/analisis.py`, los números de una provincia (total, variación, crecimiento, peso en el país) y los devuelve en un diccionario.
- `generar_informe`: manda ese resumen a la API y devuelve un texto breve en español simple. El mensaje a la IA debe decir que use solo esos números, que no agregue otros ni invente causas, y que escriba para alguien que no sabe estadística.
- `verificar_cifras`: revisa que cada número que aparece en el texto de la IA esté en el resumen. Si hay uno que no está, rechaza el texto.
- `informe_plantilla`: arma el mismo informe con una plantilla, sin IA. Se usa si no hay clave, no hay internet o la verificación falla, para que la demostración nunca se caiga.

Terminado cuando: el informe sale para cualquier provincia, un número inventado se rechaza, y sin clave igual se muestra el informe con plantilla.

### 4. Chat con los datos (domingo 29 al martes 1 de diciembre)

Es lo primero que se recorta si hay atraso, así que hazlo después del informe. La IA no escribe ni ejecuta código. En su lugar, defines una lista cerrada de funciones permitidas de `src/` (por ejemplo crecimiento por periodo, resumen por provincia y las tasas de José) con sus parámetros validados. La IA elige una función y sus parámetros, el programa la ejecuta con pandas, y la IA explica el resultado. Si la IA pide algo fuera de la lista, se rechaza.

### 5. Pruebas (todos los días)

Crea `tests/test_ia.py` con la API simulada, sin llamadas reales, para no gastar. Prueba que `verificar_cifras` rechace un número inventado, que una función fuera de la lista sea rechazada, que la plantilla funcione y que sin clave no haya error. Corre `pytest` antes de cada push.

### 6. Entrega a Mauro

Pásale los nombres y parámetros de las funciones de `src/ia.py` para que arme la pestaña. Primera versión del informe: viernes 27. Chat: martes 1 de diciembre.

### 7. Video (jueves 3)

Un minuto, en formato horizontal, grabado desde Zoom. Estructura: el problema, qué hicimos, una demostración corta del dashboard y el valor para quien decide. Prepara el texto con Marian y ensáyalo antes de grabar.

### 8. Ensayo del pitch (jueves 3 y viernes 4)

Dirige dos ensayos con cronómetro. Agrega una ronda de preguntas difíciles, de las que puede hacer el profe: por qué tasas y no conteos, por qué la IA no inventa números, qué limitaciones tienen los datos.

## Primer paso hoy

Clonar el repositorio y empezar el punto 1: comparar las APIs y avisar al grupo cuál propones.

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
