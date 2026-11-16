# C5: Torneo de ordenamientos

**Lenguaje:** Python 3.12
**Competidores:** Inserción (cuadrático, O(n²)), MergeSort y QuickSort (hechos por mí, O(n log n)) y `sorted()` de Python (cuarto competidor).
**Datos:** enteros desordenados, en cantidades crecientes que se duplican (10.000, 20.000, 40.000 y 80.000).
**Protocolo:** 1 corrida de calentamiento (descartada), 3 corridas medidas y promedio. Antes de medir verifiqué que los cuatro algoritmos dejan el arreglo ordenado.
**Código:** `C5_torneo.py`

## Tabla de tiempos (segundos)

| Cantidad de datos | Inserción | MergeSort | QuickSort | sorted de Python |
|---|---|---|---|---|
| 10.000 | 3,1166 | 0,0246 | 0,0300 | 0,0022 |
| 20.000 | 24,7689 | 0,0725 | 0,0587 | 0,0046 |
| 40.000 | 139,1090 | 0,4013 | 0,3715 | 0,0225 |
| 80.000 | 282,6367* | 0,2816 | 0,2551 | 0,0167 |

\* Inserción con 80.000 datos: 1 sola corrida medida, sin calentamiento, porque con el protocolo completo tardaría demasiado.

## Cuántas veces crece el tiempo al duplicar los datos

| Paso | Inserción | MergeSort | QuickSort | sorted |
|---|---|---|---|---|
| 10.000 a 20.000 | x7,95 | x2,95 | x1,96 | x2,09 |
| 20.000 a 40.000 | x5,62 | x5,54 | x6,33 | x4,89 |
| 40.000 a 80.000 | x2,03* | x0,70 | x0,69 | x0,74 |
| **Total, 10.000 a 80.000 (8 veces más datos)** | **x90,7** | **x11,4** | **x8,5** | **x7,6** |

**Qué se espera según el O:** si los datos crecen 8 veces, un algoritmo O(n²) debería tardar unas 64 veces más (8 al cuadrado), y uno O(n log n) unas 9,8 veces más (8 x 16,3 / 13,3).

## Informe de conclusiones

1. **El cuadrático se dispara.** Inserción creció x90,7 con 8 veces más datos, cerca del orden cuadrático esperado (x64). MergeSort (x11,4), QuickSort (x8,5) y `sorted()` (x7,6) crecieron cerca de lo esperado para n log n (x9,8). Con 80.000 datos, Inserción tardó unas 1.000 veces más que MergeSort y QuickSort.
2. **MergeSort y QuickSort quedaron casi empatados.** Ordenaron 80.000 datos en menos de 0,3 s.
3. **El sort propio de Python ganó siempre.** Con 80.000 datos fue unas 15 a 17 veces más rápido que mi MergeSort y mi QuickSort, porque está muy optimizado y escrito en un lenguaje de más bajo nivel.
4. **Los tiempos tienen ruido y no lo oculto.** Con 40.000 datos, los cuatro algoritmos salieron más lentos de lo esperado a la vez (MergeSort con 40.000 tardó más que con 80.000). Como afectó a todos por igual, lo atribuyo a una causa externa común, probablemente mi computadora ocupada con otros procesos, y no a los algoritmos. No lo verifiqué. Además, Inserción con 80.000 se midió una sola vez. Por eso me baso en el crecimiento total (de 10.000 a 80.000) y no en cada paso suelto.
5. **Una advertencia sobre consistencia.** El tiempo de Inserción con 2.000 datos que medí en C4 (0,29 s) es mayor de lo que predice la tendencia de esta tabla (unos 0,12 s, escalando desde 3,12 s con 10.000 datos). Es otra señal de variación entre corridas de mi computadora.

## ¿Qué significa para mi hostal?

Mi hostal acumula unas 3.650 filas al año (estimación) y, como máximo teórico, 7.300. Escalando desde esta tabla (estimación, no medida), Inserción tardaría unos 0,4 s con 3.650 datos y unos 1,7 s con 7.300. Con ese tamaño la diferencia entre algoritmos casi no se nota hoy. Usar MergeSort o QuickSort sería como matar una hormiga con una bazuca si solo pensara en el presente.

## Mi elección y por qué

Elijo ordenar con el **sort del lenguaje** (`sorted()`, que usa un método n log n) y no con Inserción, por tres razones:
- Fue el más rápido en todos los tamaños.
- Pienso en el peor caso y en que el registro crece: Inserción pasó de 3 s a 282 s, mientras que los n log n siguieron por debajo de 0,3 s.
- Entre mis dos implementaciones, prefiero MergeSort a QuickSort porque garantiza n log n en el peor caso, y QuickSort, aunque con pivote al azar casi nunca falla, puede llegar a O(n²).

Inserción la conservo solo para agregar un huésped nuevo a una lista ya ordenada (ver C6).
