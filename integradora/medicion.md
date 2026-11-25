MARIA SOLEDAD INTA LARICO

# I3 Medir: furgoneta de reparto (Variante A)

## Cómo medí
- Usé Python 3.12. El código está en `planificador.py` y `medicion.py`.
- Usé la carga del enunciado: n paquetes al azar (con semilla fija) y una capacidad igual a un tercio del peso total.
- Medí con cuatro tamaños: n = 14, 16, 18 y 20 (cada +2 paquetes la ingenua se multiplica por ~4). Con n = 20 la ingenua tardó 2,17 s, que está dentro del rango pedido (entre 0,5 y 20 segundos).
- Apliqué el protocolo: 1 corrida de calentamiento (que descarto), 3 corridas medidas y el promedio.
- Verifiqué que las dos soluciones dan la misma ganancia en los cuatro tamaños.

## Tabla

| n (paquetes) | Ingenua (ms) | Veces mas | Mejorada (ms) | Veces mas | Misma ganancia |
|---|---|---|---|---|---|
| 14 | 23.13 | - | 0.164 | - | sí (420) |
| 16 | 111.66 | x4.83 | 0.382 | x2.32 | sí (431) |
| 18 | 470.35 | x4.21 | 0.253 | x0.66 | sí (648) |
| 20 | 2170.10 | x4.61 | 0.273 | x1.08 | sí (663) |

## Conclusión
1. **La ingenua se comporta como O(n · 2^n).** Al sumar 2 paquetes esperaba un poco más de x4, porque además de 2^2 = 4 también crece el factor n (me daba x4,57, x4,50 y x4,44), y me salió x4,83, x4,21 y x4,61. En total, de n = 14 a n = 20 el tiempo se multiplicó por 93,8, y con O(n · 2^n) esperaba 2^6 x (20/14) = 91,4. Es casi igual.
2. **La mejorada se comporta como O(n · C), pero con estos tamaños el ruido manda.** Como la capacidad es un tercio del peso total, C crece con n y el costo crece como n², así que esperaba cerca de x1,31, x1,27 y x1,23. Me salió x2,32, x0,66 y x1,08. Un x0,66 (el tiempo bajó al crecer n) no puede ser crecimiento real: es ruido. La mejorada tarda décimas de milisegundo y a esa escala el ruido de mi computadora pesa más que el algoritmo. En total creció x1,66 de n = 14 a n = 20 (esperaba cerca de x2,04). Lo que sí se ve claro es que no crece de forma exponencial.
Para confirmar su forma con menos ruido, la medí también con n = 100 a 800 (ver la sección siguiente).
3. **Las dos dieron la misma respuesta:** la misma ganancia en los cuatro tamaños (columna "Misma ganancia").
4. **El peor tiempo medido** fue 2.170,10 ms (2,17 s), con la ingenua y n = 20. Con n = 20 la mejorada tardó 0,273 ms, unas 7.950 veces menos.

## Mi solución a escala grande
Con 1.000 paquetes y capacidad 10.000, mi solución tardó **1.138,4 ms** (con el protocolo: 1 calentamiento + 3 corridas, promedio). Son 10 millones de celdas de la tabla (1.000 x 10.000). La ingenua haría 2^1000 combinaciones (más de 10^300), algo imposible.

## Mi solución con tamaños más grandes (para ver su forma con menos ruido)
Con n = 14 a 20 mi solución tarda décimas de milisegundo y el ruido de mi computadora manda. Por eso la medí también con n = 100, 200, 400 y 800 (archivo `medicion_escala.py`), con el mismo protocolo (1 calentamiento + 3 corridas, promedio). La capacidad es un tercio del peso total, así que C crece con n y el costo O(n · C) crece como n²: al duplicar n espero cerca de x4.

| n (paquetes) | Mejorada (ms) | Veces mas |
|---|---|---|
| 100 | 15.72 | - |
| 200 | 51.45 | x3.27 |
| 400 | 277.52 | x5.39 |
| 800 | 836.44 | x3.01 |

Salió x3.27, x5.39 y x3.01, cerca de x4, así que mi solución se comporta como O(n · C), como declaré. En los pasos de 200 a 400 (x5.39) y de 400 a 800 (x3.01) hubo variaciones respecto a x4, lo cual atribuyo al ruido.

## ¿Qué pasaría si la capacidad fuera 1.000.000.000 de kg?
Mi solución cuesta O(n · C), así que depende del **valor** de C. Con n = 1.000 y C = 10^9 serían 10^12 celdas, 100.000 veces más que con C = 10.000.
- **Tiempo:** con C = 10.000 tardó 1.138,4 ms, así que con C = 10^9 tardaría unos 1.138,4 ms x 100.000 = 113.840 segundos, es decir, unas 31,6 horas (más o menos 1,3 días). Es una estimación por escala, no la medí.
- **Memoria (el problema más serio):** mi tabla de decisiones ocupa n x C bytes = 1.000 x 10^9 = 10^12 bytes, o sea 1 terabyte, y el arreglo `mejor` tendría 10^9 entradas (unos 8 GB en Python). No cabría en la memoria y se caería antes de terminar.
- **Por qué pasa:** mi algoritmo es pseudopolinomial, o sea que su costo crece con el valor de C y no con la cantidad de dígitos para escribirlo. Escribir 10^9 usa "solo" 10 dígitos, pero la tabla tendría mil millones de columnas.
- **Qué haría:**
  1. Armar la tabla por **ganancia** en vez de por capacidad: dp[g] sería el menor peso con el que consigo la ganancia g. Como cada ganancia es a lo sumo 99, con 1.000 paquetes la ganancia total es a lo sumo 99.000, así que serían unos 1.000 x 99.000 = 99 millones de celdas, sin importar cuánto valga C.
  2. Si hubiera pocos paquetes (unos 40 o menos), dividirlos en dos mitades y combinar los resultados, con costo O(2^(n/2)).
  3. Aceptar una solución aproximada.
  El problema de la mochila es NP-difícil y no se conoce un algoritmo polinomial en el tamaño de la entrada.

