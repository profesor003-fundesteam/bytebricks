# Registro de fuentes de datos

Una entrada por dataset, con su estado. Verificación hecha entre el 23 y el 26 de noviembre de 2026: los archivos del INEC se descargaron y se leyeron. Estados: confirmado, parcial o no confirmado. La fecha de descarga definitiva y la licencia se completan cuando el archivo entre a `data/raw/` o `data/external/`.

## 1. Accidentes por provincia y año, 2016-2025 (confirmado, ya en el proyecto)

- Archivo: `data/raw/accidentes_provincia_anio.csv` (formato largo: anio, provincia, accidentes).
- Fuente: INEC / Contraloría General, con datos del Departamento de Operaciones del Tránsito de la Policía Nacional. Cuadro 1.
- Enlace: https://www.inec.gob.pa/archivos/P070554752026081013111101.xlsx.pdf
- Transcripción: manual desde el PDF. Un guion (-) del INEC se registró como 0.
- Verificación: la suma de provincias coincide con el total nacional del INEC en los 10 años (`data/raw/totales_inec_por_anio.csv`).
- Licencia: completar.

## 2. Población por provincia y comarca (confirmado, falta la serie 2016-2025)

- Censo 2023 y censos anteriores, 13 provincias y comarcas: Cuadro 1, población 1911 a 2023.
  https://www.inec.gob.pa/archivos/P0705547520231213140421Cuadro%2001.pdf
- Proyección al 1 de julio de 2023:
  https://www.inec.gob.pa/archivos/P0705547520250115100004Estimaci%C3%B3n%20Proyecci%C3%B3n%202023.pdf
- Proyección al 1 de julio de 2024, 13 unidades con comarcas. Suma 4 548 681, igual al total que publica el INEC:
  https://www.inec.gob.pa/archivos/P0705547520260319114406a-Estimaci%C3%B3n%20proyecci%C3%B3n%20Rep%C3%BAblica%202024.pdf
- Estado: solo se vieron las proyecciones de 2023 y 2024. Falta confirmar 2016 a 2022 y 2025.
- Problema: las series no coinciden entre sí. Bocas del Toro tiene 159 228 en el censo 2023, 194 971 en la proyección de 2023 y 186 740 en la de 2024. Chiriquí tiene 470 864 en la proyección de 2023 y 528 998 en la de 2024. Hay que elegir una sola serie y decir cuál se usa.
- Cuidado: la población de Panamá en 2010 incluye lo que hoy es Panamá Oeste, así que no es comparable.

## 3. Automóviles en circulación por provincia (parcial, con sesgo conocido)

- Fuente: INEC, publicación Transporte, "Automóviles en circulación por provincia". Hay publicación anual desde 2014; la de 2024 es preliminar.
- Cuadro 2, 2024 (total y por cada 1 000 habitantes):
  https://www.inec.gob.pa/archivos/P053342420251209131053Cuadro%202.pdf
- Cuadro 4, 2024, por provincia y tipo:
  https://www.inec.gob.pa/archivos/P0705547520251209131233Cuadro%204.pdf
- Informe completo 2024:
  https://www.inec.gob.pa/archivos/P0705547520251209113540Informe%20completo%20Transporte%20A%C3%B1o%202024.pdf
- Publicaciones de años anteriores (páginas del INEC): 2014 (ID 732), 2015 (ID 797), 2016 (ID 851), 2017 (ID 908) y 2018 (ID 986), en
  https://www.inec.gob.pa/publicaciones/Default3.aspx?ID_PUBLICACION=ID&ID_CATEGORIA=4&ID_SUBCATEGORIA=22
  Serie 2017-21 en Excel dentro de Panamá en Cifras (ID 1196, categoría 17, subcategoría 45).
- Cómo se mide: registros de venta de placas y pagos del impuesto de circulación en las tesorerías municipales. Excluye placas oficiales. No incluye las comarcas.
- Sesgo: en 2024 Panamá Oeste aparece con 43 379 vehículos (64,9 por 1 000 habitantes) contra 712 556 de Panamá (411,5), y Darién con 91. Probablemente muchos vehículos se registran en otra provincia (hipótesis, no comprobada). Por eso la tasa por vehículo sale distorsionada: Darién 2 044 accidentes por 1 000 vehículos, Panamá Oeste 183 y Panamá 39.
- Decisión: la tasa por habitante es la principal; la tasa por vehículo se muestra solo como comparación con esta advertencia, o se descarta.

## 4. Lluvia (confirmado, con límites)

- Archivo: `data/external/lluvia_mes_provincia.csv` (anio, mes, provincia, lluvia_mm). 10 provincias por 120 meses, 2016 a 2025. No incluye comarcas por su tamaño.
- Fuente: NASA POWER, API mensual, variable PRECTOTCORR (precipitación corregida, reanálisis MERRA-2). Entrega milímetros por día y aquí se multiplican por los días del mes. https://power.larc.nasa.gov/
- Método: promedio simple de 2 o 3 puntos por provincia (cabeceras de distrito, coordenadas aproximadas en `src/lluvia.py`). Se reproduce con `python -m src.lluvia`; los datos crudos quedan en `data/raw/lluvia_nasa_power/`.
- Verificación, hecha el 26 de noviembre de 2026: se comparó con 8 estaciones del INEC de 2014 (Cuadro 121-02, https://www.inec.gob.pa/archivos/P7391121-02.pdf) usando coordenadas aproximadas. La correlación mensual con la estación va de 0,56 a 0,95 (mediana 0,73; Santiago 0,95, David 0,83, Cerro Punta 0,56). Los totales anuales no cuadran: NASA queda por debajo en Bocas del Toro (2 462 mm contra 3 532), Changuinola, David y Santiago, y por encima en Tocumen y Cerro Punta.
- Conclusión: sirve para la forma de la temporada seca y lluviosa (promedio nacional: enero 49 mm, abril 173, mayo 305, octubre 350, diciembre 132), no para milímetros exactos. Cualquier correlación con accidentes es exploratoria y debe decirlo.
- Descartado: ERA5 (Open-Meteo) se probó como control y correlacionó peor en 6 de las 8 estaciones (0,43 a 0,82), así que no se usa.
- Límites: la celda de NASA mide unos 50 km, así que Herrera y Los Santos comparten celdas y los puntos de una provincia pueden caer en la misma celda. No es lluvia de estación. Los puntos son aproximados.
- Alternativa que no se usó: datos de estaciones del IMHPA (antes ETESA), que se piden por solicitud formal (contacto público: info@imhpa.gob.pa) y no llegan a tiempo para el 5 de diciembre.

## 5. Accidentes por mes, clase y víctimas (confirmado, 2016-2025)

- Archivos: `data/external/accidentes_mes_provincia.csv` (anio, mes, provincia, valor, medida) y `data/external/accidentes_clase_provincia.csv` (anio, provincia, clase, accidentes). Se regeneran con `python -m src.extraccion_inec`, que necesita `pdftotext` (paquete `poppler-utils`).
- Fuente: INEC, publicación anual "Accidentes de Tránsito", con datos del Departamento de Operaciones del Tránsito de la Policía Nacional. Lista de años: https://www.inec.gob.pa/publicaciones/Default2.aspx?ID_CATEGORIA=5&ID_SUBCATEGORIA=40. Los nombres de los 20 PDF usados están en `src/extraccion_inec.py`.
- Mes por provincia: Cuadro 13 (2016 a 2023) y Cuadro 15 (2024 y 2025). Existe para los 10 años. `medida` toma tres valores: accidentes, heridos y muertos. El guion del INEC se registró como 0.
- Clase por provincia: Cuadro 3 (accidentes por clase, provincia, comarca, distrito y vía). Existe para los 10 años. Solo se toman las filas de provincia y comarca.
- Verificación, hecha el 26 de noviembre de 2026: los accidentes por provincia y año de los dos CSV coinciden con `data/raw/accidentes_provincia_anio.csv` en los 10 años (0 diferencias). En cada fila las provincias suman el total, y los 12 meses suman la fila anual de cada medida. Los heridos y muertos de 2023 (14 246 y 362) y de 2025 (17 405 y 360) coinciden con el INEC. Todo está en `tests/test_extraccion_inec.py`.
- Clases: para comparar los 10 años se usan cuatro, Colision, Atropello, Vuelco y Otras. Hasta 2018 el INEC no separaba la colisión con objeto fijo; desde 2019 sí, pero aquí va dentro de Colision para que las series sean comparables. Otras reúne caída de persona o cosa del vehículo, colisión y vuelco, colisión y atropello, y atropello con fuga, colisión o vuelco. Desde 2024 el INEC publica diez clases y se agrupan igual.
- Comarcas: las tablas mensuales solo traen la columna de Guna Yala desde 2019 y la de Emberá solo en 2020. Donde no hay columna no hay filas, y el total anual de la base para esa comarca es 0, así que no falta nada.
- Vacío de la fuente: el Cuadro 3 de 2020 no trae Los Santos ni en el PDF ni en el Excel. Esa provincia y año no están en `accidentes_clase_provincia.csv`; el total de 528 accidentes sí está en la base y en la tabla mensual. No se derivó restando.
- Corrección de la fuente: en el Cuadro 3 de 2017 la fila de Veraguas dice 1 593, pero omite a Soná y Mariato (139 accidentes), que quedaron en la página siguiente. Con ellos suma 1 732, igual que los Cuadros 1 y 13, y las cuatro clases cuadran con la fila TOTAL (56 847). Se sumaron esos dos distritos (ver `CORRECCIONES_CONOCIDAS` en el código).
- Aclaración sobre el Cuadro 16 de 2022 que figuraba aquí: cuenta víctimas (13 917 = heridos más muertos), no accidentes, y no se usa. Los accidentes por clase salen del Cuadro 3.
- No se extrajo el Cuadro 2 (mes y clase por distrito) porque separa Panamá, San Miguelito y Arraiján del resto del país, no por provincia.
- Cifra de 2025: se usa la final (53 132). El avance preliminar de febrero de 2026 decía 52 812.
- Comentarios anuales: 2025 (https://www.inec.gob.pa/archivos/P053342420260810130702COMENTARIO.pdf) y 2022 (https://www.inec.gob.pa/archivos/P053342420231031123622COMENTARIO.pdf).

## 6. Feriados y fechas especiales (no buscado)

- Lista propia, manual. Carnaval y Semana Santa cambian de fecha cada año, hay que calcularlas. Verificar contra una fuente oficial.

## Prueba de tasas con 2024

Con la proyección de población 2024 y los accidentes de 2024, la tasa por 100 000 habitantes cambia el ranking: Panamá 1 703, Panamá Oeste 1 093, Herrera 864 (séptima por conteo, tercera por tasa), Chiriquí 851, Colón 831. Las comarcas quedan con las tasas más bajas: Ngäbe Buglé 34, Guna Yala 21 y Emberá 0. Puede ser menos tráfico o menos registro, no se sabe y no hay que concluir nada sin más datos.

Portal de datos abiertos: https://www.datosabiertos.gob.pa
