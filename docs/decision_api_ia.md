# Decisión sobre la API de IA

Investigado el 25 de noviembre de 2026. Los límites y precios de las APIs gratuitas cambian seguido y las cifras de abajo salen de blogs y de la comunidad, no de pruebas propias. Antes de decidir, Artemio debe confirmar los límites reales en la consola de cada servicio.

## Decisión por ahora

Usamos la API de Gemini de Google (Google AI Studio), que fue la que sugirió el profe. Él aclaró que podemos usar cualquier API, siempre que sea gratuita. Dejamos Gemini documentada como la opción principal y evaluamos si alguna otra se adapta mejor. Hasta ahora no encontramos una claramente mejor para este proyecto.

## Qué necesita el proyecto de la API

- Redactar en español sencillo un informe por provincia a partir de números que ya calculó pandas.
- Opcional (se recorta primero): elegir una función de una lista cerrada para responder una pregunta del usuario, lo que se llama llamada a funciones o tool calling.
- Muy poco volumen: unas decenas de peticiones en el desarrollo y pocas en la demostración. Los límites gratuitos alcanzan.
- Solo se envían datos agregados y públicos, nunca información personal.

## Opciones gratuitas

Google Gemini (AI Studio)
- Sin tarjeta. Los modelos Flash y Flash-Lite y los modelos abiertos Gemma tienen acceso gratuito; los modelos Pro son de pago.
- Límites aproximados según blogs de octubre de 2026: unas 10 peticiones por minuto y entre 1 000 y 1 500 por día. Los límites son por proyecto y la cifra real aparece en AI Studio.
- En el nivel gratuito Google puede usar los datos para mejorar sus productos y recomienda no enviar información sensible. Para nosotros no es problema porque enviamos datos públicos y agregados.
- Soporta llamada a funciones.
- A favor: la sugirió el profe y es la más generosa de las gratuitas.

Groq
- Sin tarjeta, compatible con el formato de OpenAI y con llamada a funciones, modelos abiertos como Llama.
- El nivel gratuito tiene límites por minuto y por día, con un tope de tokens por minuto (12 000 en el modelo grande, según una fuente). Confirmar en la consola.
- A favor: muy rápido, buen respaldo si Gemini falla. En contra: menos calidad esperada en español que un modelo grande.

OpenRouter
- Modelos con sufijo gratuito, pero con unos 20 peticiones por minuto y 50 por día sin crédito. Los modelos gratuitos cambian seguido y algunas rutas gratuitas pueden registrar los mensajes.
- Se descarta como principal por el límite diario bajo y la inestabilidad de modelos.

Mistral (nivel Experiment)
- Gratuito, con límites bajos por minuto (2 peticiones por minuto según una fuente de junio de 2026). Puede servir como tercera opción.

## Recomendación

Gemini como principal y Groq como respaldo, detrás de una capa que permita cambiar de proveedor sin tocar el resto del código. Reglas de diseño para `src/ia.py`:

1. El proveedor, el modelo y la clave vienen de variables de entorno (`IA_PROVEEDOR`, `IA_MODELO`, `IA_API_KEY`), no del código. Los nombres de modelos gratuitos cambian, así que no se escriben fijos en el código: se toman de AI Studio el día que se use.
2. Siempre existe `informe_plantilla`, un informe sin IA, para que la demostración nunca se caiga.
3. Los informes por provincia se generan y verifican con anticipación y se guardan en `data/processed/informes_provincia.json`. Así la demostración no depende de los límites ni de la conexión, y el chat con IA queda como extra.
4. `verificar_cifras` rechaza cualquier texto que traiga un número que no esté en el resumen calculado por pandas.

## Pendiente de Artemio

- Crear la clave gratuita en Google AI Studio y confirmar en la consola los límites reales de su proyecto.
- Probar un informe corto con Gemini y medir si el español sale claro y sencillo.
- Probar el mismo informe con Groq como respaldo.
- Anotar aquí el modelo elegido, el costo (cero), los límites confirmados y qué se hace si falla.

## Fuentes consultadas

- Límites de Gemini: https://ai.google.dev/gemini-api/docs/rate-limits
- Límites de Groq: https://console.groq.com/docs/rate-limits
- Límites de OpenRouter: https://openrouter.ai/docs/api-reference/limits
