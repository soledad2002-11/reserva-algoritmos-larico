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
- **Costo:** O(n · C), con n paquetes y capacidad C, porque la tabla tiene n x C celdas y cada una la calculo en un solo paso. En mi código además guardo una tabla de decisiones de n x C bytes, para saber qué paquetes se eligieron.
- Para comparar, con n = 1.000 y C = 10.000 la tabla hace 10 millones de pasos, mientras que probar todo haría 2^1000, un número imposible.

## d) Estructura para EstaEnElViaje
Usaría un **conjunto hash (set)** con los códigos de los paquetes elegidos. Armarlo cuesta O(k), una sola vez, y después cada consulta cuesta **O(1) en promedio**, porque calcula directo dónde está el código. En cambio, la lista de la ingenua recorre hasta k códigos en cada consulta, O(k).

Con números, como ejemplo (no lo medí): si hay k = 500 paquetes elegidos y 10.000 consultas, la lista hace hasta 10.000 x 500 = 5 millones de comparaciones, y el set hace 10.000 (más 500 para armarlo).
