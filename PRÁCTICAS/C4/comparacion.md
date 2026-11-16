# C4: Comparación medida de búsqueda lineal vs búsqueda binaria

**Lenguaje:** Python 3.12
**Datos:** un arreglo ordenado de 1.000.000 de enteros y 1.000 claves que sí existen en el arreglo (como pide la práctica). Las dos búsquedas se midieron sobre el mismo arreglo.
**Protocolo:** 1 corrida de calentamiento (descartada), 3 corridas medidas y promedio.
**Código:** `C4_busqueda.py`

## Tabla 1: búsqueda lineal vs binaria

| Algoritmo | Costo (peor caso) | Tiempo promedio de 1.000 búsquedas | Tiempo por búsqueda |
|---|---|---|---|
| Búsqueda lineal | O(n) | 159,3170 s | 0,159 s |
| Búsqueda binaria | O(log n) | 0,014370 s | 0,0000144 s |
| **Cociente lineal / binaria** | | **11.087 veces** | |

**Cómo leer la tabla:** la lineal revisa hasta n elementos y la binaria descarta la mitad en cada paso, unos 20 pasos con n = 1.000.000. Por eso el cociente es tan grande. Lo medido coincide con lo que predice el O. Hay algo de ruido de mi computadora, pero con una diferencia de más de 10.000 veces no cambia la conclusión.

## Tabla 2: costo de ordenar (tamaño de mi proceso: 2.000 registros)

| Algoritmo | Costo (peor caso) | Tiempo promedio |
|---|---|---|
| Burbuja | O(n²) | 0,6848 s |
| Inserción | O(n²) | 0,2884 s |

Inserción fue unas 2,4 veces más rápida que Burbuja (0,6848 / 0,2884). Medí con 2.000 datos, que es del mismo orden que mis unas 3.650 filas estimadas al año (ver C6).

## ¿En mi proceso conviene ordenar primero?

Sí conviene ordenar primero: ordenar mis unos 2.000 registros una sola vez con Inserción cuesta 0,29 s, y eso se recupera después de unas 900 búsquedas (estimación), porque cada búsqueda binaria es miles de veces más barata que una lineal y la lista ordenada se mantiene metiendo cada huésped nuevo en su lugar.
Elijo Inserción y no Burbuja porque fue 2,4 veces más rápida (0,29 s contra 0,68 s) y porque con tan pocos datos MergeSort o QuickSort serían una bazuca para una hormiga (para el peor caso de 7.300 filas lo comparo en C6).

## Cómo calculé las 900 búsquedas (estimación)

- Tiempo por búsqueda lineal con 1.000.000 de datos: 159,3 s / 1.000 = 0,159 s. Con 2.000 datos, escalando por tamaño: 0,159 x (2.000 / 1.000.000) = 0,00032 s.
- Tiempo por búsqueda binaria con 2.000 datos: unos 0,000008 s (escalado por log n, estimación).
- Ahorro por búsqueda: 0,00032 - 0,000008 = unos 0,00031 s.
- Punto de equilibrio: 0,2884 s / 0,00031 s = **unas 930 búsquedas**, que redondeo a unas 900.

**Limitación honesta:** este cálculo es una estimación por escala, no una medición directa con 2.000 datos. En mi hostal se busca pocas veces, así que la ventaja en tiempo de computadora se acumula despacio. Pero hoy cada búsqueda a mano en el cuaderno toma entre 10 y 30 minutos (estimación), y una lista ordenada la baja a segundos. Eso es lo que justifica ordenar.
