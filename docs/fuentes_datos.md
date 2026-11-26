# Registro de fuentes de datos

Una entrada por dataset, con su estado. Verificación hecha el 23 de noviembre de 2026: los archivos del INEC se descargaron y se leyeron. Estados: confirmado, parcial o no confirmado. La fecha de descarga definitiva y la licencia se completan cuando el archivo entre a `data/raw/` o `data/external/`.

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

## 4. Lluvia (no confirmado)

- INEC publicó la lluvia mensual por estación y provincia, pero lo encontrado llega hasta 2014:
  https://www.inec.gob.pa/archivos/P7391121-02.pdf (mensual 2014) y https://www.inec.gob.pa/archivos/P7391121-01.pdf (anual 2005-14).
- La entidad actual es el Instituto de Meteorología e Hidrología de Panamá (IMHPA), no ETESA. Sus boletines climáticos mensuales son públicos pero en PDF y descriptivos, por ejemplo:
  https://www.imhpa.gob.pa/uploads/documentos/boletn_de_pronstico_climtico_octubre_2025.pdf
- Los datos crudos de estaciones se piden por solicitud formal al IMHPA (contacto público: info@imhpa.gob.pa) y los datos certificados se venden. Probablemente no llegan a tiempo para el 5 de diciembre.
- Alternativa por probar: una fuente satelital o de reanálisis de lluvia mensual gratuita. No se ha verificado cuál ni si se puede promediar por provincia.
- Decisión: la lluvia es opcional y es lo primero que se recorta.

## 5. Accidentes por mes, clase y víctimas (parcial, todo en PDF)

- Por mes y clase existe para varios años, pero separa los distritos de Panamá, San Miguelito y Arraiján del resto del país, no por provincia. Ejemplos: 2019 (https://www.inec.gob.pa/archivos/P05334242021012713061702.pdf), 2024 (https://www.inec.gob.pa/archivos/P070554752025092313213002.pdf) y 2025 (https://www.inec.gob.pa/archivos/P070554752026081013114102.xlsx.pdf).
- Víctimas por provincia y mes: 2023 (https://www.inec.gob.pa/archivos/P057951862025010311243813.pdf) y 2025 (https://www.inec.gob.pa/archivos/P057951862026081013463715.xlsx.pdf).
- Clase de accidente y víctimas por provincia y comarca: 2022, Cuadro 16 (https://www.inec.gob.pa/archivos/P070554752023110110155716.pdf).
- Compendio 2024 con serie 2015-24 por provincia: https://www.inec.gob.pa/archivos/P0705547520250923131031COMPENDIO%20BOLETIN%20DE%20ACCIDENTES%20DE%20TRANSITO%20A%C3%91O%202024.pdf
- Comentarios anuales: 2025 (https://www.inec.gob.pa/archivos/P053342420260810130702COMENTARIO.pdf) y 2022 (https://www.inec.gob.pa/archivos/P053342420231031123622COMENTARIO.pdf).
- Estado: falta confirmar qué años tiene cada tabla antes de prometer series largas. Para pasar los PDF a CSV funciona `pdftotext -layout`, que ya se probó con los archivos del INEC.

## 6. Feriados y fechas especiales (no buscado)

- Lista propia, manual. Carnaval y Semana Santa cambian de fecha cada año, hay que calcularlas. Verificar contra una fuente oficial.

## Prueba de tasas con 2024

Con la proyección de población 2024 y los accidentes de 2024, la tasa por 100 000 habitantes cambia el ranking: Panamá 1 703, Panamá Oeste 1 093, Herrera 864 (séptima por conteo, tercera por tasa), Chiriquí 851, Colón 831. Las comarcas quedan con las tasas más bajas: Ngäbe Buglé 34, Guna Yala 21 y Emberá 0. Puede ser menos tráfico o menos registro, no se sabe y no hay que concluir nada sin más datos.

Portal de datos abiertos: https://www.datosabiertos.gob.pa
