[Tu nombre completo]

# Inventario de operaciones: registro de huéspedes del hostal

## 1. Qué datos guarda mi proceso

Guarda un registro por cada habitación ocupada cada día: fecha, habitación, huésped, precio, cantidad de personas, noches y pago. El hostal tiene 20 habitaciones.

- **Hoy:** unas 3.650 filas acumuladas en el último año (estimación: promedio de 10 habitaciones ocupadas por día).
- **Peor mes:** 600 filas (máximo teórico: 20 habitaciones ocupadas los 30 días). 

## 2. Operaciones, cuántas veces y qué estructura las resuelve barato

| Operación | Ejemplo en el hostal | Cuántas veces (estimación) | Estructura que la resuelve barato | Cuál sufre |
|---|---|---|---|---|
| Buscar por clave | Verificar si una habitación está libre en una fecha (clave: habitación + fecha), o buscar a un huésped por documento | **Muchas:** de 10 a 30 veces al día | Tabla hash, O(1) en promedio | Lista sin orden (cuaderno): O(n) |
| Insertar | Registrar un check-in | **Muchas:** de 5 a 20 por día | Tabla hash, O(1); árbol balanceado, O(log n) | Arreglo ordenado: O(n) por los desplazamientos |
| Borrar | Anular una reserva | Pocas: unas pocas por semana | Tabla hash, O(1); árbol balanceado, O(log n) | Arreglo: O(n) |
| Recorrer en orden | Cierre de caja del día y reporte mensual, ordenados por fecha | Pocas: 1 vez al día y 1 vez al mes | Árbol balanceado: recorrido en orden, O(n) | Tabla hash: hay que ordenar después, O(n log n) |
| El menor o el mayor | La próxima salida o la última llegada | Pocas: 1 vez al día | Árbol balanceado, O(log n); cola de prioridad (heap), O(1) para verlo | Tabla hash: hay que revisar todo, O(n) |
| Buscar por rango | Huéspedes entre dos fechas (ocupación de una semana o del mes) | Pocas: 1 vez al mes | Árbol balanceado, O(log n + k) | Tabla hash: O(n) |

## 3. Qué elijo y por qué

Las operaciones que más hago (buscar por clave e insertar) piden una **tabla hash**, porque las dos cuestan O(1) en promedio. Para las que hago pocas veces pero necesitan orden (recorrer, el menor o el mayor, rango) me sirve un **árbol balanceado** ordenado por fecha, que las resuelve sin tener que ordenar cada vez.

**Una honestidad necesaria:** con 600 a 3.650 filas y tan pocas operaciones al día, incluso una lista ordenada bastaría. Elijo estas estructuras pensando en el peor caso y en que el registro crezca.
