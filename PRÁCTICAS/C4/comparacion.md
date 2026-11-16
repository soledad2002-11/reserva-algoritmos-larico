# C4: Comparación medida de búsqueda lineal vs búsqueda binaria

**Lenguaje:** Python 3.12
**Datos:** arreglo ordenado de 1.000.000 de enteros y 1.000 claves que sí existen.
**Protocolo:** 1 corrida de calentamiento (descartada), 3 corridas medidas, promedio.
**Código:** `C4_busqueda.py`

## Tabla 1: búsqueda

| Algoritmo | Tiempo promedio de 1000 búsquedas (N = 1.000.000) |
|---|---|
| Búsqueda lineal | 159.3170 s |
| Búsqueda binaria | 0.014370 s |
| Cociente lineal/binaria | 11087 veces |

## Tabla 2: costo de ordenar (tamaño de mi proceso: 2000 registros)

| Algoritmo | Tiempo promedio |
|---|---|
| Burbuja | 0.6848 s |
| Inserción | 0.2884 s |

## ¿En mi proceso conviene ordenar primero?

En mi proceso sí conviene ordenar primero: ordenar mis unos 2000 registros una sola vez cuesta apenas 0.29 s, y con 1.000.000 de datos la búsqueda binaria fue 11.087 veces más rápida que la lineal, así que el costo se recupera rápido y la ventaja crece cuando el cuaderno crece.
Elijo inserción y no burbuja porque fue más del doble de rápida (0.29 s contra 0.68 s) y además me sirve para meter cada huésped nuevo en su lugar sin reordenar todo; MergeSort o QuickSort serían como matar una hormiga con una bazuca para solo 2000 datos.

*Nota: estimo que ordenar se paga después de unas 900 búsquedas (calculado escalando el tiempo lineal medido a 2000 datos). Es una estimación, no una medición directa.*
