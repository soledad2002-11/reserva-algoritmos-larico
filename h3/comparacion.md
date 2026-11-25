# H3 Comparación medida: ¿qué solicitudes acepto en una semana?

## El problema
El mismo problema de mi estrategia.md: elegir qué solicitudes de reserva aceptar en una semana para ganar lo máximo sin pasar la capacidad de 140 habitaciones-noche (20 habitaciones x 7 noches). Es un problema análogo a mi caso (una mochila). Lo resolví con fuerza bruta (O(n · 2^n)) y con programación dinámica (O(n · capacidad)). Código en `comparacion.py`.

## Cómo medí
- Python 3.12. Datos simulados: solicitudes de 1 a 3 habitaciones por 2 a 7 noches, pagando entre 55 y 80 Bs por habitación-noche, con semilla fija.
- Cuatro tamaños: n = 16, 17, 18 y 19. No puedo duplicar n literalmente porque 2^n explotaría (de n = 20 a n = 40 pasaría de 1 millón a un billón de subconjuntos); por eso subo n de 1 en 1, y cada +1 solicitud duplica el trabajo de la fuerza bruta.
- Antes de medir verifiqué que las dos estrategias dan el mismo pago y que las solicitudes elegidas caben en la capacidad.
- Protocolo: 1 corrida de calentamiento (descartada), 3 corridas medidas y promedio.

## Tabla

| n (solicitudes) | Fuerza bruta (ms) | Veces mas | Dinámica (ms) | Veces mas | Mismo resultado |
|---|---|---|---|---|---|
| 16 | 116.87 | - | 0.307 | - | sí (9343 Bs) |
| 17 | 267.20 | x2.29 | 0.273 | x0.89 | sí (8975 Bs) |
| 18 | 540.10 | x2.02 | 0.315 | x1.16 | sí (9548 Bs) |
| 19 | 1168.96 | x2.16 | 0.262 | x0.83 | sí (9878 Bs) |

## Conclusión
1. **La fuerza bruta se comporta como O(n · 2^n).** Cada +1 solicitud esperaba cerca de x2,1 (2 x 17/16 = 2,13, 2 x 18/17 = 2,12 y 2 x 19/18 = 2,11) y salió x2,29, x2,02 y x2,16. En total, de n = 16 a n = 19 (8 veces más combinaciones) el tiempo se multiplicó por 10,0, y la teoría predice 8 x 19/16 = 9,5.
2. **La dinámica se parece a O(n · capacidad), pero el ruido domina.** La capacidad es fija (140), así que al subir n esperaba solo un 6 % más por fila (x1,06), y salió x0,89, x1,16 y x0,83. En total quedó en x0,85 cuando esperaba x1,19. Sus tiempos son de décimas de milisegundo (0,26 a 0,31 ms), y a esa escala el ruido de mi computadora pesa más que el algoritmo, así que con estos tamaños no puedo distinguir su crecimiento. Lo que sí se ve es que no crece de forma exponencial, mientras la fuerza bruta se multiplicó por 10.
3. **Las dos dieron el mismo resultado** en los cuatro tamaños (columna "Mismo resultado"), con solicitudes que caben en la capacidad.
4. **La diferencia crece al subir n.** Con n = 16 la fuerza bruta tardó 381 veces más que la dinámica (116,87 / 0,307), y con n = 19 tardó 4.462 veces más (1.168,96 / 0,262). Con las unas 30 solicitudes que estimo para una semana, la fuerza bruta haría 2^30 = 1.074 millones de subconjuntos, y por escala tardaría unos 3.780 segundos (63 minutos) para una sola semana (estimación, no medida), contra 30 x 140 = 4.200 celdas de la dinámica.
