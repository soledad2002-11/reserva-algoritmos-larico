# Inventario de operaciones: registro de huéspedes del hostal

## 1. Qué datos guarda mi proceso

Guardo un registro por cada habitación ocupada en cada día, copiado de la "Hoja diaria de hospedaje" del Hostal Kantu Flor (Copacabana). Cada registro tiene: fecha, número de habitación, tipo de habitación, nombre del huésped, precio, cantidad de huéspedes, tiempo de estadía, garage, pago en efectivo, pago por QR y si ya canceló (pagó).

**Claves de búsqueda:**
- El **nombre del huésped**, para saber en qué habitación y qué fechas estuvo. Mi hoja no guarda el documento, por eso la clave es el nombre.
- El par **habitación + fecha**, para saber si una habitación está ocupada ese día.

**Cuántos datos:**
- **Hoy:** unas 3.650 filas acumuladas en el último año (estimación: un promedio de 10 habitaciones ocupadas por día, 10 x 365).
- **Peor mes:** 600 filas (máximo teórico: las 20 habitaciones ocupadas los 30 días, 20 x 30). 
- **Peor año:** 7.300 filas (20 habitaciones x 365 días, todo lleno todo el año).

## 2. Operaciones que hago, cuántas veces y qué estructura las resuelve barato

| Operación | Ejemplo en mi hostal | Veces por día (estimación) | Veces por año (aprox.) | Estructura que la resuelve barato | Estructura que sufre |
|---|---|---|---|---|---|
| Buscar por clave | Buscar a un huésped por su nombre; ver si una habitación está ocupada en una fecha | 20 | 7.300 | Tabla hash, O(1) en promedio | Lista sin orden (mi cuaderno), O(n) |
| Insertar | Registrar a un huésped en una habitación (una fila por habitación ocupada) | 10 | 3.650 | Tabla hash, O(1) en promedio | Arreglo ordenado, O(n) por correr los demás datos |
| Borrar | Anular un registro mal escrito o una reserva cancelada | 2 por semana | unas 100 | Tabla hash, O(1) en promedio | Lista o arreglo, O(n) |
| El menor o el siguiente | Saber la próxima fecha de salida o el siguiente huésped que llega | 2 | unas 730 | Árbol balanceado, O(log n) | Tabla hash, O(n): no guarda orden |
| Buscar por rango | Listar los huéspedes entre dos fechas (ocupación de una semana o de un mes) | 2 o 3 por mes | unas 30 | Árbol balanceado, O(log n + k) | Tabla hash y lista, O(n) |
| Recorrer en orden | Cierre de caja del día y reporte mensual, ordenados por fecha | 1 al día + 1 al mes | unas 380 | Árbol balanceado, O(n) | Tabla hash y lista, O(n log n): hay que ordenar primero |

## 3. Cuáles hago más veces

Las que más repito son **buscar por clave** (unas 7.300 veces al año) e **insertar** (unas 3.650). Juntas suman unas 10.950 de las unas 12.190 operaciones al año, es decir, cerca del 90 %. Las demás (borrar, el menor o el siguiente, rango y recorrer en orden) las hago pocas veces, entre una vez al día y una vez al mes.

Esto importa para elegir la estructura: tiene que ser barata, sobre todo, para buscar e insertar, y las operaciones que necesitan orden se pueden resolver con otra estructura porque se hacen pocas veces.
