[Tu nombre completo]

# H2 Medición: buscar a un huésped por su nombre

## El problema
En mi caso, la operación que más hago es buscar a un huésped por su nombre para saber en qué habitaciones y fechas estuvo (unas 7.300 veces al año, ver inventario.md). Resuelvo el mismo problema con dos versiones, que están en `h2_medicion.py`.

## Mi estructura ingenua y por qué la pensé
Mi primera idea fue pasar el cuaderno tal cual a una **lista** de registros y, para buscar a un huésped, recorrerla entera de arriba abajo comparando nombres. Lo pensé así porque es lo más parecido a lo que hago hoy en el cuaderno y es lo más fácil de programar: a simple vista funciona y da la respuesta correcta. Pero al analizar mi caso vi que buscar es lo que más hago, y en la lista cada búsqueda cuesta O(n): con 3.650 registros miro hasta 3.650 filas, y como un huésped puede tener varias estadías, no puedo parar en la primera.

## La estructura que elegí
Una **tabla hash** con el nombre del huésped como clave (en Python, un `dict`). Buscar cuesta O(1) en promedio: la función hash calcula la casilla del nombre y voy directo. Armar la tabla cuesta O(n) una sola vez. (El árbol balanceado de estructura.md sirve para el siguiente, el rango y el orden, que son otras operaciones; no lo medí aquí y lo justifiqué con las cuentas de estructura.md.)

## Cómo medí
- Lenguaje: Python 3.12.
- Las dos versiones usan los mismos datos: registros (nombre, habitación, día del año) con el formato de mi hoja diaria, generados con una semilla fija.
- Cuatro tamaños que se duplican: n = 3.650 (mis filas de hoy), 7.300 (mi peor año), 14.600 y 29.200.
- Cada corrida hace 1.000 búsquedas de nombres que NO están (el peor caso: la lista revisa todo).
- Antes de medir verifiqué que las dos versiones dan la misma respuesta.
- Protocolo de clase: 1 corrida de calentamiento (descartada), 3 corridas medidas y promedio.

## Tabla (tiempo de 1.000 búsquedas)

| n | Ingenua (ms) | Veces mas | Elegida (ms) | Veces mas |
|---|---|---|---|---|
| 3650 | 146.16 | - | 0.0812 | - |
| 7300 | 403.09 | x2.76 | 0.0847 | x1.04 |
| 14600 | 520.58 | x1.29 | 0.0867 | x1.02 |
| 29200 | 1123.17 | x2.16 | 0.0882 | x1.02 |

Costo de armar la tabla hash (se paga una sola vez):

| n | Armar la tabla (ms) |
|---|---|
| 3650 | 0.81 |
| 7300 | 2.04 |
| 14600 | 5.46 |
| 29200 | 13.07 |

## Conclusión
1. **La ingenua se parece a O(n).** Al duplicar n, su tiempo se multiplicó por 2,76, 1,29 y 2,16 (esperaba cerca de 2). En total, con 8 veces más datos (de 3.650 a 29.200) el tiempo se multiplicó por 7,7 (146,16 ms a 1.123,17 ms), cerca del x8 de O(n). Si fuera O(n²) habría salido cerca de x4 por cada duplicación.
2. **La elegida se parece a O(1).** Casi no creció: 0,0812 ms con 3.650 registros y 0,0882 ms con 29.200 (x1,04, x1,02 y x1,02, un 9 % más con 8 veces más datos).
3. **Hay ruido.** Los pasos de la ingenua se desvían del x2 esperado: x2,76 arriba y x1,29 abajo. Supongo que mi computadora estaba haciendo otras cosas, pero no lo verifiqué. Por eso me fijo en la tendencia total (x7,7) y no en cada fila. Armar la tabla también creció algo más que x2 por paso (x2,5, x2,7 y x2,4).
4. **Qué significa para mi hostal.** Con n = 29.200, la ingenua tardó 1.123 ms y la elegida 0,088 ms, unas 12.700 veces menos. Armar la tabla cuesta 13,07 ms una sola vez y se paga con unas 12 búsquedas (con 3.650 registros, con unas 6), y yo hago unas 20 al día (estimación). Con mis 3.650 filas una búsqueda en lista tarda unos 0,15 ms, así que la mejora grande de mi hostal viene de pasar del cuaderno al programa. La tabla hash asegura que siga rápido si el registro crece.
