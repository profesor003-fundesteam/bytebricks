# Funciones de estadística para el dashboard

Para Mauro: estas funciones están en `src/estadistica.py` y devuelven tablas o diccionarios, nunca gráficos. Los cargadores están en `src/datos.py`. Cada resultado trae una frase lista para mostrar (campo `interpretacion`) y los números salen de pandas y scipy, así que la IA solo los explica.

## Cargadores (`src/datos.py`)

| Función | Devuelve |
|---|---|
| `cargar_accidentes_mes()` | anio, mes, provincia, valor, medida (`accidentes`, `heridos` o `muertos`) |
| `cargar_accidentes_clase()` | anio, provincia, clase (Colision, Atropello, Vuelco, Otras), accidentes |
| `cargar_lluvia()` | anio, mes, provincia, lluvia_mm (10 provincias, sin comarcas) |

## Funciones

**`indice_estacional(mes, medida="accidentes", excluir_anios=(2020,))`** devuelve mes, promedio e indice. Un índice de 1,10 significa que ese mes tiene 10 % más accidentes que un mes típico de su año. Se calcula dentro de cada año para que el crecimiento anual no distorsione. Para una gráfica de barras por mes.

**`efecto_anio_atipico(mes, anio=2020, medida="accidentes")`** devuelve mes, indice_con, indice_sin y diferencia. Con la base actual la diferencia máxima es 0,068 (enero pasa de 0,959 con 2020 a 0,891 sin 2020), así que 2020 sí distorsiona y por eso las demás funciones lo dejan fuera por defecto. Hay que decirlo en pantalla.

**`proporcion_clase_por_provincia(clase, incluir_comarcas=False)`** devuelve el porcentaje de cada clase en cada provincia; cada fila suma 100. Para barras apiladas.

**`chi_cuadrado_clase_provincia(clase, incluir_comarcas=False)`** devuelve un diccionario con chi2, p_valor, grados_libertad, n, v_cramer, frecuencia_esperada_minima, residuos (tabla), mayor_diferencia e interpretacion. Con tantos accidentes el p-valor siempre sale mínimo, así que lo que importa es `v_cramer`: 0,095, una relación débil.

**`correlacion_lluvia_accidentes(mes, lluvia, excluir_anios=(2020,))`** devuelve provincia, correlacion y meses. **`resumen_correlacion_lluvia(tabla)`** devuelve correlacion_media, provincias_positivas, provincias_negativas, provincia_mayor e interpretacion.

## Qué dicen los datos (2016-2025, sin 2020 donde se indica)

- Los meses con más accidentes son diciembre (índice 1,128) y octubre (1,078); los de menos son febrero (0,883) y enero (0,891).
- En todas las provincias predominan las colisiones, pero la mezcla cambia: Darién tiene 13,6 % de vuelcos y Bocas del Toro 12,2 %, contra 0,9 % en Panamá, que casi no tiene vuelcos y sí 95,9 % de colisiones. La diferencia es real pero débil en conjunto (V de Cramér = 0,095).
- La lluvia no muestra una relación clara con los accidentes: la correlación media entre provincias es 0,08 y el signo cambia. La mayor es Panamá (0,33).

## Advertencias que deben salir en pantalla

- La lluvia es una estimación de NASA POWER, no de estaciones. Sirve para la forma de la temporada seca y lluviosa, no para milímetros exactos (ver sección 4 de `docs/fuentes_datos.md`). Cualquier resultado con lluvia es exploratorio.
- Las comarcas se dejan fuera de la prueba de chi-cuadrado por defecto porque sus cifras son muy pequeñas.
- Las clases son cuatro porque la colisión con objeto fijo va dentro de Colision para comparar los 10 años (sección 5 de `docs/fuentes_datos.md`). Los Santos 2020 no tiene datos de clase.
- Una correlación o una diferencia entre provincias no prueba una causa.
