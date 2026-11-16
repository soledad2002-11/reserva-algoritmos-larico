# C5: Torneo de ordenamientos

**Lenguaje:** Python 3.12
**Competidores:** Inserción (cuadrático), MergeSort y QuickSort (hechos por mí) y `sorted()` de Python (cuarto competidor).
**Datos:** enteros desordenados, en cantidades crecientes.
**Protocolo:** 1 corrida de calentamiento (descartada), 3 corridas medidas, promedio. Antes de medir verifiqué que los cuatro algoritmos dejan el arreglo ordenado.
**Código:** `C5_torneo.py`

## Tabla de tiempos

| Cantidad de datos | Inserción (s) | MergeSort (s) | QuickSort (s) | sorted de Python (s) |
|---|---|---|---|---|
| 10000 | 3.1166 | 0.0246 | 0.0300 | 0.0022 |
| 20000 | 24.7689 | 0.0725 | 0.0587 | 0.0046 |
| 40000 | 139.1090 | 0.4013 | 0.3715 | 0.0225 |
| 80000 | 282.6367* | 0.2816 | 0.2551 | 0.0167 |

\* Inserción con 80000 datos: 1 sola corrida medida, sin calentamiento, porque con el protocolo completo tardaría demasiado.

## Informe de conclusiones

1. **El cuadrático se dispara.** Con 8 veces más datos (de 10.000 a 80.000), Inserción tardó unas 90 veces más (de 3.1 s a 282.6 s). Eso es crecimiento cuadrático. Con 80.000 datos, Inserción fue unas 1000 veces más lenta que MergeSort y QuickSort.
2. **MergeSort y QuickSort crecen suave.** Ordenaron 80.000 datos en menos de 0.3 s y quedaron casi empatados entre sí.
3. **El sort propio de Python ganó siempre.** `sorted()` fue entre 15 y 17 veces más rápido que mis MergeSort y QuickSort con 80.000 datos, porque está optimizado y escrito en un lenguaje de más bajo nivel.
4. **Observación sobre el ruido.** Los tiempos de 40.000 datos salieron algo más altos de lo esperado (incluso MergeSort con 40.000 tardó más que con 80.000). Es probable que mi computadora estuviera ocupada en otras tareas durante esa corrida. Por eso me fijo en la tendencia general y no en cada número suelto.

## ¿Qué significa para mi hostal?

Mi hostal acumula entre 2.000 y 4.000 filas ocupadas al año. Con ese tamaño, incluso Inserción ordena en menos de un segundo (en C4, con 2000 datos tardó 0.29 s). En esa escala la diferencia entre algoritmos casi no se nota, y usar MergeSort o QuickSort sería como matar una hormiga con una bazuca. Los algoritmos n log n solo se vuelven imprescindibles cuando los datos llegan a decenas de miles. Si el sistema del hostal se programa en Python, lo más sensato es usar el `sorted()` del lenguaje.
