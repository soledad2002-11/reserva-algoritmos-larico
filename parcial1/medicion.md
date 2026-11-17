MARIA SOLEDAD INTA LARICO 

# P1.2 Curar y medir

## Mi cura
Mi cura recorre la lista una sola vez y guarda en un conjunto (set) los carnets que ya vio: si encuentra uno que ya estaba, hay un repetido. Su costo es O(n) en promedio (con memoria extra O(n)), y no modifica la lista que recibe. Pasa los 5 casos de prueba.

## Cómo medí
- Lenguaje: Python 3.12. Código en `medicion.py`.
- Peor caso para las dos: lista sin repetidos (hay que mirarla toda).
- Cuatro tamaños que se duplican: 1.000, 2.000, 4.000 y 8.000. Con 8.000 la solución lenta tarda unos 1,8 s, dentro del rango pedido (0,5 a 20 s).
- Protocolo: 1 corrida de calentamiento (descartada), 3 corridas medidas y promedio.
- Ejecuté el programa completo tres veces. La tabla es de la tercera ejecución, y las otras dos las uso para hablar del ruido.

## Tabla

| n | Por pares (s) | x respecto a la fila anterior | Mi cura (ms) | x respecto a la fila anterior |
|---|---|---|---|---|
| 1000 | 0.0252 | - | 0.0572 | - |
| 2000 | 0.1134 | x4.51 | 0.2214 | x3.87 |
| 4000 | 0.5011 | x4.42 | 0.3236 | x1.46 |
| 8000 | 1.8057 | x3.60 | 0.8626 | x2.67 |

## Conclusión
1. **Por pares se comporta como O(n²).** Al duplicar n, el tiempo se multiplicó por 4,51, 4,42 y 3,60. Esperaba x4, porque si T(n) = c·n² entonces T(2n) = 4·T(n). El último salió algo menor y lo atribuyo al ruido, aunque no lo verifiqué.
2. **Mi cura se comporta como O(n), pero con mucho ruido.** Esperaba cerca de x2 al duplicar n y salió x3,87, x1,46 y x2,67. Mis tiempos son de fracciones de milisegundo (entre 0,06 y 0,86 ms), y a esa escala cualquier cosa de mi computadora pesa más que el algoritmo. Midiendo el crecimiento total de 1.000 a 8.000 (se espera x8), salió x15,1 en esta ejecución, y en mis otras dos ejecuciones salió x7,2 y x10,2.
3. **Hay ruido en la cura y casi nada en la lenta.** Con n = 8.000, la lenta dio 1,7972 s, 1,8773 s y 1,8057 s en mis tres ejecuciones (menos de 5 % de diferencia). La cura, con el mismo paso de 2.000 a 4.000, dio x1,86, x1,22 y x1,46.
4. **El peor tiempo medido fue 1,8057 s, con la solución por pares y n = 8.000** (en la ejecución más lenta de las tres fue 1,8773 s). Con el mismo n, mi cura tardó 0,8626 ms, o sea unas 2.100 veces menos.
