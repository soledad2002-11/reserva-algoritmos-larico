MARIA SOLEDAD INTA LARICO 

# P2.1 Elegir: pedidos de una pastelería (Variante B)

## 1. El caso
Los pedidos llegan con un plazo en minutos y se preparan del menor plazo al mayor; si dos tienen el mismo plazo, primero el que llegó antes. Una jornada normal tiene 120.000 registros, 120.000 preparaciones y 40.000 consultas de "¿sigue pendiente?".

## 2. Estructuras que elijo
Combino dos estructuras:
- Una **cola de prioridad (heap)** con tuplas (plazo, llegada, nombre), para sacar siempre el pedido más urgente.
- Un **conjunto hash (set)** con los nombres de los pedidos pendientes, para saber si uno sigue pendiente y para contar.

Las dos se actualizan juntas: al registrar un pedido entra a las dos, y al prepararlo sale de las dos. Los nombres son únicos, así que no hay duplicados.

## 3. Tabla de operaciones

| Operación | Veces por jornada | Estructura | Costo O |
|---|---|---|---|
| Registrar | 120.000 | Heap + set | O(log n) (el heap) + O(1) (el set) = O(log n) |
| PrepararSiguiente | 120.000 | Heap + set | O(log n) (sacar el menor del heap) + O(1) (quitarlo del set) = O(log n) |
| EstaPendiente | 40.000 | Set | O(1) en promedio |
| Pendientes | no la indica el enunciado | Set (su tamaño) | O(1) |

## 4. Por qué no sirve la lista simple (con números)
Uso n = 120.000 y log2(n) ≈ 16,9. Cuento pasos o comparaciones, no segundos, y supongo el peor caso con la lista llena (estimación).

| | Lista simple | Mi solución (heap + set) |
|---|---|---|
| Registrar (120.000) | 120.000 x 1 = 120.000 | 120.000 x (16,9 + 1) = 2,14 millones |
| Preparar (120.000) | la lista se vacía mientras preparo: n²/2 = 7.200 millones (recorre todo para buscar el menor) | 120.000 x (16,9 + 1) = 2,14 millones |
| EstaPendiente (40.000) | 40.000 x 120.000 = 4.800 millones (recorre todo) | 40.000 x 1 = 40.000 |
| **Total de la jornada** | **unos 12.000 millones** | **unos 4,3 millones** |

La lista simple cuesta unas 2.800 veces más. Sus dos operaciones caras, preparar y consultar, recorren toda la lista cada vez (O(n)). Con mi solución preparar cuesta O(log n) y consultar O(1).

## 5. Por qué esta combinación y no otra
- **Solo un heap:** preparar sería barato, pero EstaPendiente costaría O(n), que son 40.000 x 120.000 = 4.800 millones de pasos, y se perdería la ventaja.
- **Solo un set o diccionario:** consultar sería O(1), pero sacar el menor costaría O(n) (hay que revisar todo): unos 7.200 millones en total.
- **Un árbol balanceado ordenado por (plazo, llegada)** también serviría, con O(log n) para registrar y preparar. Prefiero el heap porque es lo más simple para "sacar el más urgente", y el árbol sabe hacer cosas que aquí no pido (rangos). Además, en Python no hay un árbol balanceado en la librería estándar.
- **El costo que pago:** más memoria (los nombres están en las dos estructuras) y hay que mantener las dos sincronizadas.

## 6. El desempate
El heap guarda tuplas (plazo, llegada, nombre). Python compara primero el plazo y, si empatan, el número de llegada, que sube de uno en uno. Así, con el mismo plazo sale primero el que llegó antes. El nombre nunca se compara, porque el número de llegada es único.

## 7. Condiciones en las que cambiaría de opinión
- **Si se agregara "cancelar un pedido"** (sacar uno cualquiera): en el heap eso cuesta O(n), porque hay que encontrarlo. Pasaría a un árbol balanceado ordenado por (plazo, llegada), donde borrar cuesta O(log n).
- **Si pidieran "los pedidos con plazo entre 30 y 60 minutos"** (un rango): también un árbol balanceado, con O(log n + k), porque el heap no sabe de rangos.
- **Si hubiera muy pocos pendientes** (unas decenas): con 20 pedidos la lista recorre 20 pasos y el heap unos 4, una diferencia irrelevante. Elegiría la lista simple y no mantendría dos estructuras.
