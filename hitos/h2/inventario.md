# Inventario de operaciones: registro de huéspedes del hostal

## 1. Qué datos guarda mi proceso

Guardo un registro por cada habitación ocupada en cada día, copiado de la "Hoja diaria de hospedaje" del Hostal Kantu Flor (Copacabana). Cada registro tiene: fecha, número de habitación, tipo de habitación, nombre del huésped, precio, cantidad de huéspedes, tiempo de estadía, garage, pago en efectivo, pago por QR y si ya canceló (pagó).

**Claves de búsqueda:**
- El **nombre del huésped**, para saber en qué habitación y qué fechas estuvo. Mi hoja no guarda el documento, por eso la clave es el nombre.
- El par **habitación + fecha**, para saber si una habitación está ocupada ese día.

**Cuántos datos:**
- **Hoy:** unas 3.650 filas acumuladas en el último año (estimación: un promedio de 10 habitaciones ocupadas por día, 10 x 365).
- **Peor mes:** 600 filas (máximo teórico: las 20 habitaciones ocupadas los 30 días, 20 x 30).(estimación).
- **Peor año:** 7.300 filas (20 habitaciones x 365 días, todo lleno todo el año).

## 2. Operaciones que hago y cuántas veces (estimaciones)

| Operación | Ejemplo en mi hostal | Veces por día | Veces por año (aprox.) |
|---|---|---|---|
| Buscar por clave | Buscar a un huésped por su nombre; ver si una habitación está ocupada en una fecha | 20 | 7.300 |
| Insertar | Registrar a un huésped en una habitación (una fila por habitación ocupada) | 10 | 3.650 |
| Borrar | Anular un registro mal escrito o una reserva cancelada | 2 por semana | unas 100 |
| El menor o el siguiente | Saber la próxima fecha de salida o el siguiente huésped que llega | 2 | unas 730 |
| Buscar por rango | Listar los huéspedes entre dos fechas (ocupación de una semana o de un mes) | 2 o 3 por mes | unas 30 |
| Recorrer en orden | Reporte mensual de todo el registro, ordenado por fecha (el cierre de caja diario solo mira las filas de ese día, unas 10, y no lo cuento) | 1 por mes | 12 |

## 3. Cuáles hago más veces

Las que más repito son **buscar por clave** (unas 7.300 veces al año) e **insertar** (unas 3.650). Juntas suman unas 10.950 de las unas 11.800 operaciones al año, es decir, cerca del **93 %**. Las demás las hago pocas veces: el menor o el siguiente es la más frecuente de ellas (unas 730), y el rango y el recorrido en orden son raras (30 y 12 al año).

## 4. ¿Necesito orden, rangos o solo buscar por clave?

**Mayormente busco por clave exacta** (el nombre del huésped o habitación + fecha). Pero **sí necesito orden en tres casos**, aunque pocos:
- **El siguiente o el menor** (unas 730 veces al año): la próxima salida o llegada.
- **Un rango de fechas** (unas 30 veces al año): la ocupación de una semana o un mes.
- **Recorrer todo en orden por fecha** (12 veces al año): el reporte mensual.

Son pocas comparadas con buscar e insertar, pero con estructuras que no guardan orden cada una cuesta O(n) o n log n. Por eso, en `estructura.md` las comparo con números antes de decidir.

## 5. Costo de cada operación según la estructura

Costos del mapa de estructuras de la clase 9. n = filas guardadas (unas 3.650 hoy). \* es costo promedio y \*\* es amortizado.

| Operación | Arreglo | Lista | Tabla hash | Árbol balanceado | Resuelve barato | Sufre |
|---|---|---|---|---|---|---|
| Buscar por clave | O(n) | O(n) | O(1)\* | O(log n) | Tabla hash | Arreglo y lista (mi cuaderno de hoy) |
| Insertar | O(1)\*\* | O(1) | O(1)\* | O(log n) | Arreglo, lista y hash | Ninguna sufre; el árbol es algo más caro |
| Borrar (lo deduje, no está en el mapa de clase) | O(n) | O(n) | O(1)\* | O(log n) | Tabla hash | Arreglo y lista: hay que encontrarlo primero |
| El menor o el siguiente | O(n) | O(n) | O(n) | O(log n) | Árbol balanceado | Arreglo, lista y hash |
| Un rango de valores | O(n) | O(n) | O(n) | O(log n + k) | Árbol balanceado | Arreglo, lista y hash |
| Recorrer en orden | n log n | n log n | n log n | O(n) | Árbol balanceado | Arreglo, lista y hash |

(k = cuántos valores devuelve el rango.)

**La peor estructura para mi caso** es la lista sin orden, que es mi cuaderno de hoy: buscar cuesta O(n) y buscar es lo que más hago.
