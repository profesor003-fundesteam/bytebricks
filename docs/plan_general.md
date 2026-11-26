# Plan general del Proyecto 1 (ByteBricks)

Accidentes de tránsito en Panamá, 2016-2025. Samsung Innovation Campus, Certificación en Python e Inteligencia Artificial.

Fecha de presentación: sábado 5 de diciembre de 2026. Actualizado el miércoles 25 de noviembre, quedan 10 días. El profe ya aprobó lo que tenemos hecho.

Este es el plan general. Cada rol tiene además su propio plan en `docs/roles/`, que amplía este documento. Lo marcado como "por confirmar" hay que verificarlo con el profe antes de afirmarlo.

## 1. Qué estamos construyendo

Un dashboard interactivo en Streamlit (`app.py`) que analiza los accidentes de tránsito de Panamá con pandas. En vez de comparar solo conteos por provincia, calcula tasas por cada 100 000 habitantes. Como comparación, con advertencia, prueba también la tasa por cada 1 000 vehículos. Cruza los accidentes con población, parque vehicular y calendario, y con lluvia solo si se consigue una fuente válida. Una API de IA explica los resultados en español. Pandas calcula todos los números y la IA solo los redacta.

Dato verificado contra el Cuadro 1 del INEC: 53 132 accidentes en 2025, 8,7 % más que en 2024. La suma de las provincias coincide con el total del INEC en los 10 años.

Prueba hecha el 23 de noviembre con datos de 2024: la tasa por 100 000 habitantes cambia el ranking (Herrera pasa del puesto 7 por conteo al 3 por tasa), mientras que la tasa por vehículo sale distorsionada por cómo se registran las placas (detalle en la sección 6).

## 2. Equipo y roles

Cada integrante tiene varios roles para que la carga quede equilibrada. Los roles ya están acordados entre los cuatro. El plan de cada uno está en `docs/roles/`.

Marian Barba
- Líder de proyecto e integradora: coordina, revisa los aportes de todos, mantiene el repositorio ordenado y lleva el calendario.
- Analista estadística: estacionalidad, chi-cuadrado y, si hay datos de lluvia, correlación (preguntas 7, 8 y 9).
- Datos mensuales: pasa a CSV las tablas del INEC por mes y por tipo de accidente, que vienen en PDF.
- Calidad: lleva la suite de pruebas completa, revisa que el dashboard corra desde cero y que los cambios de los demás no rompan nada. Cada quien prueba su propio módulo y Marian responde por el conjunto.
- Documentación y entregables: README, formulario de Samsung, PPT, valores UNESCO y guion del pitch.

José Brown
- Analista de datos: consigue y documenta las fuentes (población, vehículos, lluvia, feriados), limpia y une las tablas.
- Analista de tasas: tasas por habitante y por vehículo (preguntas 5, 6 y 10).

Mauro González
- Desarrollador del dashboard: pestañas nuevas en `app.py` para tasas, estadística e IA.
- Diseñador visual: gráficos y tema con la paleta Samsung.

Artemio Rodríguez
- Ingeniero de IA: informe por provincia y consulta en lenguaje natural con la API de IA.
- Pruebas de su módulo: tests de las funciones de IA, incluida la regla de que la IA no calcula cifras.
- Video y ensayo: video de un minuto y ensayo del pitch.

Todos programan, todos publican con su propia cuenta y todos presentan: la rúbrica de gestión premia la carga repartida de forma equitativa y que se note en el repositorio.

## 3. Qué hay que entregar

Según el formulario oficial de Samsung, cada integrante debe cargar todos los elementos en la plataforma.

1. PPT con el formato oficial del SIC y su línea gráfica. Debe mostrar planteamiento, objetivos, herramientas utilizadas y una breve explicación del resultado donde se vea la funcionalidad. Cuidar la ortografía.
2. Formulario de desarrollo completo: tabla de integrantes y roles, nombre de la prueba, descripción del problema con datos que lo respalden, y las seis preguntas (valor que genera, consideraciones para la comunidad, impacto, supuestos, preguntas pendientes y métrica principal).
3. Video de un minuto en formato horizontal, se puede grabar desde Zoom, explicando la propuesta.
4. Repositorio de GitHub con un README (planteamiento, objetivos, herramientas y resultado), los códigos, las bases de datos y las herramientas, de forma organizada. Hay que cargar el enlace en la plataforma.
5. Pitch de ventas ante el docente y tutor: una presentación breve y persuasiva que muestre el problema, los beneficios clave y lo que nos diferencia.

Además, el proyecto debe tener un nombre representativo, no puede repetirse en la sección y hay que informar el nombre al docente.

## 4. Rúbrica (100 puntos) y cómo la cubrimos

- Idea, 10 puntos: creatividad y novedad, diferenciación de lo ya existente, impacto en el interés público y demanda en el mundo real. Lo cubrimos con las tasas (no solo conteos), la inclusión de las comarcas y el uso por parte de INEC, Policía Nacional y Tránsito.
- Aplicación, 30 puntos: mantenimiento y desarrollo sostenible, herramientas adecuadas, métodos vistos en clase y herramientas basadas en investigación propia. Lo cubrimos con el código separado en `src/`, las pruebas automáticas, pandas y matplotlib vistos en clase, y Streamlit y la API de IA como investigación propia.
- Resultados, 30 puntos: rendimiento, practicidad, visualización de resultados y flujo de datos, y madurez de la propuesta. Lo cubrimos con un dashboard que corre en vivo, filtros, el flujo documentado (datos, pandas, dashboard, IA) y la verificación de datos contra el INEC.
- Gestión de proyectos, 10 puntos: carga repartida, comunicación, adaptación a imprevistos e hitos a tiempo. Lo cubrimos con roles claros, commits propios de cada integrante en el repositorio, y el calendario de la sección 7.
- Presentación y reporte, 20 puntos: informe claro, diapositivas bien preparadas, presentación fluida y respuesta a preguntas. Lo cubrimos con el guion, el ensayo con cronómetro y la ronda de preguntas del profe.

Streamlit y la API de IA fueron pedidos por el profe, y la rúbrica además premia las herramientas basadas en investigación propia.

## 5. Módulos de trabajo

- Módulo 0, coordinación y Git (Marian): orden del repositorio, revisión de los aportes, calendario.
- Módulo 1, datos (José): fuentes, descarga, registro en `docs/fuentes_datos.md`, limpieza y unión por provincia y año.
- Módulo 1b, datos mensuales (Marian): pasar a CSV las tablas del INEC por mes y por tipo de accidente.
- Módulo 2, tasas (José): tasa por habitante (la principal) y por vehículo (comparación con advertencia).
- Módulo 2b, estadística (Marian): estacionalidad, chi-cuadrado y, si hay datos de lluvia, correlación.
- Módulo 3, dashboard y visualización (Mauro): pestañas nuevas en `app.py`, gráficos y tema visual con la paleta Samsung.
- Módulo 4, IA (Artemio): informe por provincia y consulta en lenguaje natural. Regla: la IA elige entre funciones nuestras ya probadas y explica; no escribe código libre ni calcula.
- Módulo 5, calidad (Marian): suite de pruebas completa y revisión final. Artemio prueba el módulo de IA y cada quien prueba el suyo.
- Módulo 6, documentación y presentación (Marian): README, formulario, PPT, guion del pitch. Cada integrante prepara 3 diapositivas y Artemio graba el video.

Dependencias: el módulo 2 necesita los datos del módulo 1, el 2b necesita el 1b, y el 3 necesita las funciones de los módulos 2 y 2b. Para no bloquearse, Mauro avanza con los datos actuales mientras José y Marian consiguen los nuevos, y Artemio prueba la IA con la base que ya existe.

## 6. Datos que necesitamos

Cada dato nuevo se registra en `docs/fuentes_datos.md` con fuente, enlaces, estado y límites. El profe pidió datos reales de internet, no inventados. Verificación hecha el 23 de noviembre de 2026, descargando y leyendo los archivos del INEC.

- Accidentes por provincia y año: listo (INEC, Cuadro 1), verificado contra los totales.
- Población por provincia y comarca: confirmada. El censo 2023 y las proyecciones del INEC al 1 de julio cubren las 13 unidades. Falta confirmar las proyecciones de 2016 a 2022 y 2025, y elegir una sola serie, porque el censo y las proyecciones no coinciden (Bocas del Toro: 159 228 en el censo, 194 971 y 186 740 en las proyecciones de 2023 y 2024).
- Parque vehicular por provincia: existe cada año desde 2014, pero viene de registros de placas y distorsiona. En 2024 Panamá Oeste tiene 43 379 vehículos contra 712 556 de Panamá, y Darién solo 91, así que la tasa por vehículo no es confiable. No incluye comarcas.
- Lluvia mensual: no confirmada. El INEC la publicó por estación solo hasta 2014 y hoy los datos los tiene el IMHPA, que entrega datos crudos por solicitud formal y vende los certificados. Es opcional.
- Accidentes por mes, clase y víctimas: existen en PDF del INEC. La tabla por mes y clase separa distritos, no provincias. Por provincia hay víctimas por mes (2023 y 2025) y clase (2022). Falta confirmar qué años tiene cada tabla.
- Feriados y fechas especiales: lista propia, por calcular cada año.

Decisiones:
- La tasa por habitante es la principal. La tasa por vehículo se muestra solo como comparación con advertencia, o se descarta.
- Plan B de lluvia: probar una fuente satelital gratuita antes del viernes 27 de noviembre. Si no sirve, la lluvia se descarta y la estadística usa meses, tipo de accidente y calendario.
- Plan B de población: si solo se consiguen algunos años de proyección, se usa una sola serie documentada y se explica la limitación.

## 7. Calendario hasta el 5 de diciembre

Con el profe nos vemos lunes, miércoles y sábado. El sábado 28 es clase normal, sin proyecto. La semana del 30 de noviembre sí vemos proyecto el lunes y el miércoles. El profe no nos asigna tareas: solo le mostramos por dónde vamos.

- Miércoles 25: se publica todo lo que hay en el repositorio y cada quien lo clona y configura Git.
- Jueves 26 y viernes 27: José confirma la serie de población 2016-2025 y descarga las tablas de vehículos por año. Marian pasa a CSV las tablas mensuales y prueba una fuente satelital de lluvia (si no sirve el viernes 27, la lluvia se descarta). Mauro prepara el tema visual y la pestaña "Acerca de". Artemio compara APIs de IA y arma el informe por provincia con la base actual.
- Sábado 28: clase normal; cada quien avanza por su cuenta.
- Domingo 29: revisión de avance del grupo por llamada o chat. Se decide qué se recorta si hay atraso.
- Lunes 30: sesión de proyecto. José entrega las funciones de tasas y Mauro las integra al dashboard.
- Martes 1 de diciembre: se integran estadística e IA en el dashboard.
- Miércoles 2: sesión de proyecto. Congelamos funcionalidades; desde aquí solo se corrigen errores y se mejora la documentación.
- Jueves 3: PPT, video y formulario terminados. Primer ensayo del pitch.
- Viernes 4: segundo ensayo y cada integrante carga todo en la plataforma.
- Sábado 5 de diciembre: presentación.

Si algo se atrasa, se recorta alcance antes que fecha. Orden de recorte: primero la lluvia, luego el chat con IA, la estadística avanzada y la tasa por vehículo. Las tasas por habitante, la verificación y el informe por provincia son el mínimo.

## 8. Flujo de trabajo con Git

El repositorio es del profe (`https://github.com/profesor003-fundesteam/bytebricks`) y es el repositorio oficial del Proyecto 1. Cada proyecto tendrá su propio repositorio, así que no hace falta trabajar por ramas ni abrir pull requests: todos trabajamos directo en `main`. Por eso hay tres hábitos que evitan pisarnos.

1. Cada quien edita sobre todo sus propios archivos (los de su plan en `docs/roles/`).
2. Siempre se actualiza antes de subir.
3. Los commits son pequeños y frecuentes, con un mensaje claro.

Configuración, una sola vez por persona (con tu propio nombre y correo, para que tus commits cuenten como tuyos):

    git config --global user.name "Tu Nombre"
    git config --global user.email "tu-correo@ejemplo.com"
    git clone https://github.com/profesor003-fundesteam/bytebricks.git
    cd bytebricks

Cada vez que empiezas a trabajar:

    git pull --rebase origin main

Mientras trabajas, commits pequeños y con un mensaje en primera persona:

    git status
    git add src/tasas.py tests/test_tasas.py
    git commit -m "feat: agrego la tasa por 100 mil habitantes"

Al terminar un avance, subes:

    git pull --rebase origin main
    git push origin main

Prefijos de los mensajes: `feat` (algo nuevo), `fix` (un arreglo), `data` (datos), `docs` (documentación), `test` (pruebas) y `chore` (orden y configuración).

Si al hacer `git pull --rebase` aparece un conflicto, no lo resuelvas a ciegas: corre `git status`, abre el archivo marcado, deja la versión correcta, y luego `git add` de ese archivo y `git rebase --continue`. Si no estás seguro, avisa a Marian antes de seguir.

Reglas:
- Nunca usar `git push --force`.
- No subir claves de la API de IA ni el entorno virtual. Las claves van en un archivo `.env` que no se sube (ya está en `.gitignore`).
- No subir documentos con derechos de Samsung (la plantilla del formulario y su PDF): se trabajan en local.
- No subir datos personales (por ejemplo, cédulas) al repositorio, que es público.
- Subir tu trabajo seguido: la rúbrica de gestión mira que la carga esté repartida y que se note en el historial de cada quien.
- Si quieres probar algo arriesgado, puedes usar una rama temporal y fusionarla cuando funcione, pero no es obligatorio.
- Si GitHub rechaza el push por permisos, avisa a Marian para revisarlo con el profe.

## 9. Valores UNESCO

El profe pidió relacionar el proyecto con al menos un valor de la UNESCO. Usamos la Recomendación sobre la Ética de la Inteligencia Artificial (2021), por confirmar con el profe.

- Valor principal, diversidad e inclusión: la base incluye las comarcas (Ngäbe Buglé, Guna Yala y Emberá) y las tasas por habitante evitan que el conteo bruto oculte a las provincias más pequeñas (Herrera pasa del puesto 7 al 3). Las comarcas tienen cifras muy pequeñas y las tasas más bajas, que pueden deberse a menos tráfico o a menos registro; no se concluye nada sin más datos y así se dice en el dashboard.
- Derechos humanos y no causar daño: el análisis ayuda a priorizar dónde actuar para proteger vidas.
- Transparencia y explicabilidad: cada dato tiene fuente y fecha, y la IA solo explica números que pandas ya calculó.
- Supervisión humana: la IA redacta y las personas interpretan.
- Privacidad: solo datos agregados y públicos.

## 10. Pendientes

Ya resuelto: el profe aprobó lo que tenemos hecho, pidió Streamlit y la API de IA, y confirmó que cada proyecto tiene su propio repositorio y se trabaja sin ramas.

Por avisar o confirmar con el profe (él no tiene que aprobar el plan, solo saber por dónde vamos):
- Que el marco de la UNESCO sea la Recomendación sobre la Ética de la IA.
- Hora y formato exactos de la presentación del sábado 5 de diciembre.
- Si el dashboard se presenta corriendo en vivo o publicado.

Decisiones del equipo:
- API de IA: por ahora Gemini de Google, que sugirió el profe, aunque podemos usar cualquier API gratuita. Artemio confirma los límites reales y prueba Groq como respaldo. Detalle en `docs/decision_api_ia.md`.
- Si un dato no está publicado, usar una estimación citando la fuente o aplicar el plan B de la sección 6.
- Qué serie de población usar (censo o una proyección) y cómo explicar las diferencias entre ellas.
- Si la tasa por vehículo se muestra con advertencia o se descarta.
- Si se consigue una fuente de lluvia válida o la lluvia sale del alcance.

## 11. Riesgos

- La lluvia puede no tener una fuente válida por provincia y mes: es opcional y se recorta primero (sección 6).
- El parque vehicular distorsiona la tasa por vehículo por cómo se registran las placas, y no cubre las comarcas: la tasa por habitante es la principal.
- La serie de población puede ser inconsistente entre censo y proyecciones, o faltar algún año: se elige una sola serie y se documenta.
- Los nombres de provincias pueden no coincidir entre tablas: se normalizan antes de unir. En la base van sin tildes a propósito.
- Los PDF del INEC hay que pasarlos a CSV y puede haber errores de lectura: se verifican contra los totales publicados.
- La IA puede inventar cifras: regla de oro, pandas calcula y la IA explica.
- Alguien puede no entregar su parte: revisión del avance a mitad de camino, el 29 de noviembre.
- La API de IA gratuita puede tener límites o fallar: los informes por provincia se generan con anticipación y se guardan, existe un informe con plantilla sin IA, y el proveedor se puede cambiar sin tocar el resto del código.

## 12. Estructura del repositorio

Los archivos van en la raíz del repositorio, sin carpeta extra, porque este repositorio es solo del Proyecto 1.

- `app.py`: dashboard de Streamlit, el entregable principal.
- `src/`: `datos.py`, `analisis.py`, `graficos.py` y, más adelante, `tasas.py`, `estadistica.py` e `ia.py`.
- `tests/`: pruebas automáticas.
- `data/raw/`, `data/external/` y `data/processed/`: datos originales, extra y limpios.
- `docs/`: este plan, el registro de fuentes y `roles/` con el plan de cada integrante.
- `figures/`: gráficos exportados para la presentación.
