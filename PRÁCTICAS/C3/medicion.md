# C3: Medición empírica de crecimiento

## Qué hice
Comparé dos procesos escritos en Python: uno con un ciclo que da n vueltas (lineal) y otro con dos ciclos, uno dentro del otro (cuadrático). Los medí con tres tamaños: n, 4n y 16n (n = 250, 1.000 y 4.000). Apliqué el protocolo: una corrida de calentamiento que no conté, 5 corridas medidas y el promedio. El código está en `C3_medicion.py`.

## Tabla de mediciones

| n | Proceso lineal (ms) | Veces mas | Proceso cuadrático (ms) | Veces mas |
|---:|---:|---:|---:|---:|
| 250 | 0.0132 | - | 3.4062 | - |
| 1000 | 0.0771 | x5.85 | 41.8588 | x12.29 |
| 4000 | 0.1722 | x2.23 | 872.4163 | x20.84 |

## Qué muestra la tabla
1. **Proceso lineal.** Al multiplicar el tamaño por 4, esperaba que el tiempo se multiplicara por cerca de 4, porque hace n pasos (O(n)). Me salió x5,85 y x2,23. En total, con 16 veces más datos (de 250 a 4.000), el tiempo se multiplicó por 13,0, cerca del x16 que predice O(n).
2. **Proceso cuadrático.** Al multiplicar el tamaño por 4, esperaba cerca de x16, porque hace n x n pasos (4 x 4 = 16). Me salió x12,29 y x20,84, uno por debajo y otro por encima. En total, con 16 veces más datos, el tiempo se multiplicó por 256,1, y O(n²) predice 16 x 16 = 256.
3. **Ruido.** Los pasos individuales se desvían de lo esperado (x5,85 y x2,23 en el lineal, x12,29 y x20,84 en el cuadrático), pero las desviaciones se compensan y el total sale casi exacto. No verifiqué la causa; supongo que mi computadora estaba haciendo otras cosas. El proceso lineal tarda décimas de milisegundo y a esa escala el ruido pesa más que el algoritmo, por eso miro la tendencia total y no cada número suelto.
4. **Comparación.** Con n = 4.000, el proceso cuadrático tardó 872,42 ms y el lineal 0,17 ms, unas 5.066 veces más. Los tiempos son de mi computadora y cambian en otra; lo que importa es la forma del crecimiento.

## Cómo se relaciona con el código
- `proceso_lineal` tiene un ciclo que da n vueltas, así que hace n pasos: O(n).
- `proceso_cuadratico` tiene un ciclo dentro de otro, y cada uno da n vueltas, así que hace n x n pasos: O(n²).
- La O grande describe cómo crece el costo al aumentar n, y las constantes (por ejemplo, el costo de cada suma) se descartan porque no cambian la forma del crecimiento.
