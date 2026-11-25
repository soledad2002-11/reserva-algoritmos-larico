MARIA SOLEDAD INTA LARICO

# I1 Analizar y elegir: furgoneta de reparto (Variante A)

## a) Costo de PlanificadorIngenuo.Elegir
Es **O(n · 2^n)**. Lo saqué mirando los dos ciclos del código.

El ciclo de afuera prueba todas las combinaciones de paquetes. Cada paquete puede ir o no ir, así que con n paquetes son 2 x 2 x ... x 2 = 2^n combinaciones. Para cada combinación, el ciclo de adentro revisa los n paquetes para sumar el peso y la ganancia. Entonces son 2^n combinaciones por n pasos cada una, o sea n · 2^n.

Por ejemplo, con 18 paquetes: 18 x 262.144 = unos 4,7 millones de pasos. Si agrego 2 paquetes, las combinaciones se multiplican por 4 (2 x 2), y por eso el enunciado dice que cada +2 paquetes la ingenua se multiplica por 4.

Además, `EstaEnElViaje` de la ingenua busca en una lista recorriéndola, así que cuesta O(k), con k = los paquetes elegidos.

## b) La recurrencia T(n) = 2T(n-1) + 1
El teorema maestro de bolsillo **no se puede usar** aquí. Ese teorema sirve para recurrencias de la forma T(n) = a·T(n/b) + n^d, donde el problema se **divide** entre un número b mayor que 1 (por ejemplo, entre 2). En esta recurrencia el problema no se divide: cada llamada solo le quita un paquete (n-1). Como no hay ningún b, no puedo comparar a con b^d.

Lo resolví expandiendo la recurrencia:
T(n) = 2T(n-1) + 1 = 4T(n-2) + 3 = 8T(n-3) + 7 = ... = 2^k · T(n-k) + (2^k - 1).
Con T(1) = 1 y k = n-1, queda T(n) = 2^(n-1) + 2^(n-1) - 1 = 2^n - 1, o sea **O(2^n)**.

Lo entiendo así: por cada paquete hago dos llamadas (lo llevo o no lo llevo), y eso se duplica en cada nivel, hasta llegar a 2^n llamadas.

Una aclaración para no confundirme: la versión con máscara de bits del código cuesta n · 2^n porque vuelve a sumar los n paquetes en cada combinación, y la versión recursiva, que va arrastrando la suma mientras decide, cuesta 2^n. Las dos son exponenciales.

## c) ¿Sirve un voraz? Contraejemplo con números
Usé el primer caso de las pruebas: P1 (10 kg, ganancia 60), P2 (20 kg, ganancia 100) y P3 (30 kg, ganancia 120), con capacidad 50 kg.

| Paquete | Kg | Ganancia | Ganancia por kg |
|---|---|---|---|
| P1 | 10 | 60 | 6 |
| P2 | 20 | 100 | 5 |
| P3 | 30 | 120 | 4 |

- **Voraz (el que más ganancia da por kg):** lleva P1 (10 kg), después P2 (llevo 30 kg en total), y P3 ya no cabe porque 30 + 30 = 60 y la capacidad es 50. Ganancia: 60 + 100 = **160**.
- **Lo mejor posible:** P2 + P3 pesan 20 + 30 = 50 kg y dan 100 + 120 = **220**.

Como 160 es menos que 220, **el voraz no sirve**: elegir lo que parece mejor al inicio (P1) me deja peor al final.

**La estrategia que elijo es programación dinámica**, con una tabla.
- **Qué se repite:** la pregunta "¿cuál es la mejor ganancia usando los primeros i paquetes con capacidad c?". En la solución de probar todo, esa misma pregunta se resuelve muchas veces. En la tabla la resuelvo una sola vez y guardo el resultado.
- **Por qué funciona:** la mejor respuesta para i paquetes y capacidad c sale de dos opciones. Si no llevo el paquete i, es la mejor de los i-1 paquetes con la misma capacidad. Si lo llevo, es su ganancia más la mejor de los i-1 paquetes con la capacidad que queda (c menos su peso). Me quedo con la mayor de las dos.
- **En fórmula:** mejor(i, c) = máximo entre mejor(i-1, c) y mejor(i-1, c - peso_i) + ganancia_i, y mejor(0, c) = 0. Si el paquete i pesa más que c, solo vale la primera opción.
- **Costo:** O(n · C), con n paquetes y capacidad C, porque la tabla tiene n x C celdas y cada una la calculo en un solo paso. En mi código además guardo una tabla de decisiones de n x C bytes, para saber qué paquetes se eligieron.
- Para comparar, con n = 1.000 y C = 10.000 la tabla hace 10 millones de pasos, mientras que probar todo haría 2^1000, un número imposible.

**Ejemplo de cómo se llena la tabla** (segundo caso de las pruebas: P1 2 kg y ganancia 3, P2 3 kg y 4, P3 4 kg y 5, P4 5 kg y 6, capacidad 8):

| Paquetes revisados | c=0 | c=1 | c=2 | c=3 | c=4 | c=5 | c=6 | c=7 | c=8 |
|---|---|---|---|---|---|---|---|---|---|
| ninguno | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| hasta P1 | 0 | 0 | 3 | 3 | 3 | 3 | 3 | 3 | 3 |
| hasta P2 | 0 | 0 | 3 | 4 | 4 | 7 | 7 | 7 | 7 |
| hasta P3 | 0 | 0 | 3 | 4 | 5 | 7 | 8 | 9 | 9 |
| hasta P4 | 0 | 0 | 3 | 4 | 5 | 7 | 8 | 9 | **10** |

Cada celda usa solo celdas ya calculadas. Por ejemplo, la celda (hasta P2, c=5) es el máximo entre 3 (no llevo P2) y 3 + 4 = 7 (llevo P2 y miro la celda de c=2 en la fila de arriba), o sea 7. La ganancia máxima es 10.

**Cómo sé qué paquetes elegí:** retrocedo desde la última celda. P4: en c=8 vale 10 y en la fila de arriba vale 9, cambió, así que llevo P4 y me quedan 8-5 = 3 kg. P3: en c=3 vale 4 y arriba también 4, no cambió, no lo llevo. P2: en c=3 vale 4 y arriba 3, cambió, lo llevo y me quedan 0 kg. P1: no. Elegidos: P2 y P4, con ganancia 4 + 6 = 10, que es lo que esperan las pruebas.

## d) Estructura para EstaEnElViaje
Usaría un **conjunto hash (set)** con los códigos de los paquetes elegidos. Armarlo cuesta O(k), una sola vez, y después cada consulta cuesta **O(1) en promedio**, porque calcula directo dónde está el código. En cambio, la lista de la ingenua recorre hasta k códigos en cada consulta, O(k).

Con números, como ejemplo (no lo medí): si hay k = 500 paquetes elegidos y 10.000 consultas, la lista hace hasta 10.000 x 500 = 5 millones de comparaciones, y el set hace 10.000 (más 500 para armarlo).

Dos aclaraciones: el O(1) es en promedio, porque si muchos códigos cayeran en la misma casilla (colisiones) se acercaría a O(k), pero con códigos como C0, C1, C2... el set los reparte bien. Y lo que pago es memoria extra, O(k).

## e) Resumen de costos y cómo mi código cumple lo que declaré

| | Ingenua | Mejorada (la mía) |
|---|---|---|
| Elegir (tiempo) | O(n · 2^n) | O(n · C) |
| Elegir (memoria) | O(n) | O(n · C) bytes (tabla de decisiones) |
| EstaEnElViaje | O(k) | O(1) en promedio |

Por qué el costo real de mi código es el que declaré:
- Tiene **dos ciclos anidados**: el de afuera recorre los n paquetes y el de adentro recorre las capacidades desde C hacia abajo hasta el peso del paquete. Son como máximo n x C pasos, y cada uno hace una suma y una comparación (O(1)).
- **No hay fuerza bruta ni recursión sin memoria**: no pruebo subconjuntos ni llamo a ninguna función recursiva.
- **Reconstruir los paquetes elegidos** son n pasos retrocediendo por la tabla de decisiones, O(n), que no cambia el total.
- **Los bordes:** con capacidad 0 la tabla tiene una sola celda y nada se lleva; con lista vacía no se recorre nada; un paquete que pesa más que la capacidad se salta.
- **Un límite:** si hubiera dos soluciones igual de buenas, mi código devuelve una de ellas. Las pruebas tienen óptimo único, así que no afecta.
