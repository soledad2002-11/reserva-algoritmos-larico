# C6: Mi elección de algoritmo de ordenamiento para el hostal

## 1. Mi proceso y sus datos

**Proceso:** buscar a un huésped por nombre en el registro del Hostal Kantu Flor (Copacabana). Hoy el registro es una hoja diaria de hospedaje escrita a mano, sin orden por nombre. Se usa, por ejemplo, cuando un huésped vuelve a reclamar un objeto olvidado y hay que saber en qué habitación y qué fechas estuvo.

**Cuántos datos:**
- El hostal tiene 20 habitaciones y una hoja por día (unas 365 al año).
- **Hoy:** unas 3.650 filas ocupadas acumuladas en el último año (estimación, con ocupación promedio de la mitad de las habitaciones: 20 x 0,5 x 365).
- **Peor mes:** 600 filas (las 20 habitaciones ocupadas todos los días, 20 x 30).
- **Peor año:** 7.300 filas (20 x 365, todo lleno todo el año).

*Nota: el peor mes (600 filas) y el peor año (7.300 filas) son el máximo teórico, con las 20 habitaciones ocupadas todos los días. En la realidad la ocupación varía (hay días vacíos y temporadas altas como agosto), así que el valor esperado es menor, pero uso el máximo para estar segura de que mi elección aguanta el peor escenario.*

## 2. La operación que más pesa

**La operación que más pesa es ordenar el registro por nombre.** Lo justifico comparando el costo de cada operación de mi proceso en el peor caso, con n = 7.300 filas:

| Operación | Cuándo ocurre | Costo en el peor caso |
|---|---|---|
| Buscar un huésped, búsqueda lineal (sin ordenar) | cada vez que alguien pregunta | 7.300 comparaciones, O(n) |
| Buscar un huésped, búsqueda binaria (ya ordenado) | cada vez que alguien pregunta | unas 13 comparaciones, O(log n) |
| Insertar un huésped nuevo en la lista ya ordenada | una vez por huésped nuevo | hasta 7.300 desplazamientos, O(n) |
| Ordenar todo el registro con Inserción | una vez | unas 26.645.000 comparaciones (n²/2), O(n²) |
| Ordenar todo el registro con MergeSort | una vez | unas 93.000 comparaciones (n log2 n), O(n log n) |

**Por qué pesa más ordenar:**
- Ordenar con un algoritmo cuadrático cuesta 26.645.000 / 7.300 = **3.650 veces más** que una búsqueda lineal. Es decir, una sola ordenación equivale a 3.650 búsquedas.
- Para que buscar pesara más que ordenar tendría que buscar más de 3.650 veces. En el hostal las búsquedas son ocasionales (estimación: unas pocas por semana, menos de 3.650 al año).
- Buscar es lo que más se nota hoy porque el cuaderno no tiene orden. Pero en una lista ordenada una búsqueda cuesta solo unas 13 comparaciones. El costo de buscar depende de si los datos están ordenados, y por eso lo que decide el costo total es cómo ordeno.
- Insertar un huésped nuevo cuesta como máximo 7.300 movimientos, unas 3.650 veces menos que ordenar todo con Inserción.
- Si ordeno con MergeSort, ordenar baja a unas 93.000 comparaciones, equivalentes a unas 13 búsquedas lineales. Ese es el ahorro que justifica mi elección.

## 3. Dos candidatos de ordenamiento

| | Candidato A: Inserción | Candidato B: MergeSort |
|---|---|---|
| Peor caso | O(n²) | O(n log n) |
| Mejor caso | O(n) (si ya está casi ordenado) | O(n log n) |
| Memoria extra | ninguna | O(n) |
| Comparaciones en el peor caso con 7.300 filas | unas 26 millones (n²/2) | unas 93.000 (n log2 n) |

## 4. Mi elección y por qué

**Elijo MergeSort (en la práctica, el sort del lenguaje) para ordenar el registro completo, e Inserción solo para agregar un huésped nuevo a una lista que ya está ordenada.**

**Por qué:**
- Pienso en el peor caso. Con 7.300 filas (máximo teórico, todo lleno todo el año), Inserción hace millones de comparaciones, mientras que MergeSort garantiza n log n sin importar cómo vengan los datos.
- **Evidencia, C5:** con 10.000 datos, Inserción tardó 3,12 s y MergeSort 0,0246 s. Con 80.000 datos, Inserción tardó 282,6 s (una sola corrida) y MergeSort 0,28 s. El sort de Python fue aún más rápido: 0,0022 s con 10.000 datos.
- **Evidencia, C4:** ordenar 2.000 datos con Inserción tardó 0,29 s, que es aceptable ahora, pero crece con el cuadrado de n. Con 7.300 filas estimo unos 3,8 s (estimación por escala, no medida).
- **Evidencia, C4:** la búsqueda binaria fue 11.087 veces más rápida que la lineal con 1.000.000 de datos (0,0144 s contra 159,3 s para 1.000 búsquedas). Eso justifica pagar el costo de ordenar.
- Inserción sí me sirve para el trabajo diario: meter un huésped nuevo en una lista ya ordenada hace pocos movimientos, y no hace falta algo más complejo.

**Una honestidad necesaria:** con mis tamaños actuales (unos miles de filas), cualquiera de los dos serviría. Elijo B por el peor caso y porque no se vuelve lento si el registro crece a varios años.

## 5. Cómo lo voy a medir

- **Tamaños:** 1.000, 2.000, 4.000, 7.300 (peor año) y 36.500 filas (5 años en el peor caso).
- **Datos:** nombres con el formato de mi muestra ("Huesped 00001"), desordenados.
- **Qué mido:** el tiempo de ordenar con Inserción, con MergeSort y con el sort del lenguaje; y después el tiempo de buscar 1.000 nombres con búsqueda binaria sobre la lista ordenada.
- **Protocolo:** 1 corrida de calentamiento (descartada), 3 corridas medidas y promedio, igual que en C4 y C5. Antes de medir, verifico que cada algoritmo deje la lista ordenada.
