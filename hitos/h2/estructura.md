# Estructura elegida para mi caso: registro de huéspedes del hostal

## 1. Qué elijo

Elijo **dos estructuras que se reparten el trabajo**:
- Una **tabla hash**, con el nombre del huésped como clave, para buscar por clave.
- Un **árbol balanceado ordenado por fecha**, para el menor o el siguiente, el rango y recorrer en orden.

Cada registro nuevo se guarda en las dos. Elijo según las operaciones que más hago (ver inventario.md): buscar por clave e insertar son cerca del 93 % de mis operaciones.

## 2. Costo O de cada operación con mi elección

n = filas guardadas (unas 3.650 hoy, hasta 7.300 en el peor año).

| Operación | Veces por año | Estructura | Costo O | Por qué |
|---|---|---|---|---|
| Buscar por clave (huésped) | 7.300 | Tabla hash | O(1) en promedio | La función hash calcula la casilla del nombre y voy directo, sin recorrer los demás registros. |
| Insertar | 3.650 | Tabla hash + árbol | O(1) + O(log n) = O(log n) | Guardo en la casilla (O(1)) y cuelgo el nodo en el árbol bajando por una rama (altura cercana a log n). |
| Borrar | unas 100 | Tabla hash + árbol | O(log n) | Quito de la casilla (O(1)) y del árbol (O(log n)). |
| El menor o el siguiente | 730 | Árbol balanceado | O(log n) | El árbol guarda las fechas ordenadas, así que llego bajando por una rama. En la tabla hash costaría O(n) porque no guarda orden. |
| Buscar por rango de fechas | 30 | Árbol balanceado | O(log n + k) | Salto al primer valor del rango (log n) y recorro solo los k resultados. En la tabla hash costaría O(n). |
| Recorrer en orden por fecha | 12 | Árbol balanceado | O(n) | El recorrido inorden del árbol entrega los datos ya ordenados. En la tabla hash tendría que ordenar primero: n log n. |

## 3. Por qué dos estructuras y no una: las cuentas

Calculé cuántos pasos cuesta todo mi año con cada estructura, multiplicando el costo de cada operación por cuántas veces la hago (inventario.md). Uso n = 3.650, log2(n) ≈ 11,8 y k = 70 para el rango (estimación: una semana de registros, 10 por día). Son pasos o comparaciones, no segundos.

| Estructura | Cuenta | Total al año |
|---|---|---|
| Lista sin orden (mi cuaderno de hoy) | 7.300 x 3.650 + 3.650 x 1 + 100 x 3.650 + 730 x 3.650 + 30 x 3.650 + 12 x (3.650 x 11,8) | **30,3 millones** |
| Tabla hash sola | 7.300 x 1 + 3.650 x 1 + 100 x 1 + 730 x 3.650 + 30 x 3.650 + 12 x (3.650 x 11,8) | **3,3 millones** |
| Árbol balanceado solo | 7.300 x 11,8 + 3.650 x 11,8 + 100 x 11,8 + 730 x 11,8 + 30 x (11,8 + 70) + 12 x 3.650 | **185.000** |
| Tabla hash + árbol balanceado | 7.300 x 1 + 3.650 x (1 + 11,8) + 100 x (1 + 11,8) + 730 x 11,8 + 30 x (11,8 + 70) + 12 x 3.650 | **110.000** |

**Lo que dicen las cuentas:**
- Mi cuaderno de hoy (lista sin orden) es la peor: cuesta unas 275 veces más que hash + árbol, sobre todo por las 7.300 búsquedas de O(n).
- La tabla hash sola parece perfecta para buscar e insertar, pero sale unas 30 veces más cara que hash + árbol. El motivo es que "el siguiente" lo hago 730 veces al año y en la hash cuesta O(n) cada vez: 730 x 3.650 = 2,66 millones de pasos, más que todo lo demás junto.
- Hash + árbol es la más barata. El árbol solo cuesta unas 1,7 veces más (185.000 contra 110.000) y es más simple, porque guarda los datos una sola vez. Elijo hash + árbol porque buscar es lo que más hago (7.300 veces al año), y ahí la hash cuesta 1 paso y el árbol casi 12.

## 4. Límites de mi elección

- Todos estos números son **estimaciones** de cómo trabaja mi hostal (ver inventario.md). Cuento pasos, no segundos.
- La tabla hash solo encuentra coincidencias exactas. Si buscara por un nombre parcial o aproximado, no me serviría.
- El O(1) de la tabla hash depende del factor de carga α (datos / casilleros). Si los casilleros no crecen, cada búsqueda cuesta cerca de α, o sea O(n). La cura es el rehash: cuando α pasa de 0,75 se duplican los casilleros y se reubican las claves.
- El árbol tiene que estar **balanceado**: si los datos llegan ya ordenados (por ejemplo por fecha) y el árbol no se reacomoda, se degenera en una lista y cuesta O(n). Los árboles balanceados (AVL, rojinegros) se reacomodan solos, y mi lenguaje los trae o hay librerías.
- Mantener dos estructuras cuesta más memoria y hay que actualizar las dos al insertar y borrar. Lo acepto porque mis datos son pocos.
- Con 3.650 filas, incluso una lista sin orden tardaría milisegundos en una computadora. Elijo estas estructuras pensando en el peor caso y en que el registro crezca, y lo compruebo con una medición.
