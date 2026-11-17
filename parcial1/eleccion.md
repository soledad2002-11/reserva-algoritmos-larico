MARIA SOLEDAD INTA LARICO 

# P1.3 Elegir

**Datos del hospital:** n = 300.000 números de historia clínica, 5.000 consultas al día, memoria limitada (no se puede duplicar el listado). Cuento operaciones en el peor caso. Uso log2(300.000) ≈ 18,2.

## Costo total de cada opción

| Opción | Cuenta | Total aproximado |
|---|---|---|
| 1. Recorrer el listado en cada consulta | 5.000 x 300.000 | **1,5 x 10^9** (1.500 millones) |
| 2. Ordenar una vez con n log n + búsqueda binaria | 300.000 x 18,2 (ordenar) + 5.000 x 18,2 (consultas) = 5,46 x 10^6 + 9,1 x 10^4 | **5,55 x 10^6** (unos 5,5 millones) |
| 3. Ordenar una vez con cuadrático + búsqueda binaria | n²/2 = 4,5 x 10^10 (ordenar) + 9,1 x 10^4 (consultas) | **4,5 x 10^10** (45.000 millones) |

La opción 2 cuesta unas 270 veces menos que la opción 1 y unas 8.100 veces menos que la opción 3.

## Apoyo con lo que medí en P1.2
En P1.2, la solución por pares con n = 8.000 hizo unos 32 millones de comparaciones (8.000 x 7.999 / 2) y tardó 1,8057 s, es decir, unos 17,7 millones de comparaciones por segundo en mi computadora (estimación gruesa: supongo que todas las operaciones cuestan parecido). Con esa velocidad, los totales de la tabla se traducen así:
- Opción 1: 1,5 x 10^9 / 17,7 x 10^6 = unos 85 s al día.
- Opción 2: 5,55 x 10^6 / 17,7 x 10^6 = unos 0,3 s al día.
- Opción 3: 4,5 x 10^10 / 17,7 x 10^6 = unos 2.540 s (cerca de 42 minutos) solo para ordenar.

Además, mi medición confirmó que lo cuadrático se multiplica por 4 al duplicar n. Con n = 300.000 (37,5 veces más que 8.000) el costo se multiplicaría por 37,5² = unas 1.406 veces, por eso la opción 3 no sirve con 300.000 datos. La opción 1 cabría en tiempo de máquina, pero la opción 2 cuesta unas 270 veces menos y deja cada consulta casi instantánea (unas 18 comparaciones).

## Mi elección
**Elijo la opción 2**: ordenar el listado cada mañana con un algoritmo n log n y buscar con búsqueda binaria. Como la memoria es limitada y no puedo duplicar el listado, no uso MergeSort (necesita memoria extra del tamaño de la lista) sino HeapSort, que ordena en el mismo lugar con O(1) de memoria extra y garantiza n log n en el peor caso. La búsqueda binaria tampoco necesita memoria extra.

## ¿A partir de cuántas consultas cambiaría de opinión?
Recorrer el listado cuesta q x n, y la opción 2 cuesta n log n + q log n. Igualando: q = n log n / (n - log n) = 5,46 x 10^6 / 299.982 ≈ 18,2. Si hubiera **menos de unas 19 consultas** al día, recorrer el listado costaría menos que ordenarlo, y elegiría la opción 1. Con 5.000 consultas, ordenar conviene por mucho. La opción 3 nunca la elegiría: para que le ganara a la opción 1 haría falta más de n/2 = 150.000 consultas, y aun así la opción 2 siempre es más barata.
