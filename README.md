# Análisis de Algoritmos: el caso del Hostal Kantu Flor
**MARIA SOLEDAD INTA LARICO**

## Mi caso y mi proceso real
El Hostal Kantu Flor (Copacabana) tiene 20 habitaciones y registra a sus huéspedes a mano en una hoja diaria de hospedaje. El proceso lento que elegí optimizar es **buscar a un huésped** (por ejemplo, cuando vuelve a reclamar un objeto olvidado): hoy se revisa hoja por hoja y se estima que tarda entre 10 y 30 minutos. A lo largo del curso fui probando, con mediciones en mi computadora, qué algoritmo y qué estructura lo resuelven mejor.

## Índice del expediente
| Parte | Qué contiene | Enlace |
|---|---|---|
| H1: mi proceso lento | Descripción del proceso y muestra de 20 filas (simulada, con el formato real de mi hoja) | [h1/](h1/) |
| Prácticas C3, C4, C5 y C6 | Medición empírica de crecimiento, búsqueda lineal contra binaria, torneo de ordenamientos y elección del algoritmo | [PRÁCTICAS/](PR%C3%81CTICAS/) | |
| Parcial 1 | Costos, recurrencias, cura de un código lento y elección con números | [parcial1/](parcial1/) |
| H2: la estructura de mi caso | Inventario de operaciones, estructura (tabla hash + árbol balanceado) y medición | [hitos/h2/](hitos/h2/) |
| Parcial 2 | Pedidos de una pastelería: heap + set contra lista simple | [parcial2/](parcial2/) |
| Evaluación integradora | Furgoneta de reparto (mochila): análisis, programación dinámica y medición | [integradora/](integradora/) |
| H3: la estrategia de mi caso | ¿Voraz o programación dinámica? Argumento y comparación medida con fuerza bruta | [h3/](h3/) |

## Resultados clave (medidos en mi computadora)
- Con 1.000.000 de datos, la búsqueda binaria fue 11.087 veces más rápida que la lineal (C4).
- Con 29.200 registros, la lista tardó 1.123 ms y la tabla hash 0,088 ms (H2).
- Con n = 19 solicitudes, la fuerza bruta tardó 1.169 ms y la programación dinámica 0,26 ms (H3).

## Cómo medí
Todas las mediciones usan el mismo protocolo: 1 corrida de calentamiento (descartada), 3 corridas medidas y promedio. Cada tabla dice cuántas veces más tarda cada fila respecto de la anterior, y la conclusión menciona el ruido de la medición. Los tiempos son de mi computadora y cambian en otra; lo que importa es la forma del crecimiento.

## Honestidad sobre los datos
- La muestra de `h1/` mantiene el formato real de mi hoja diaria, pero los nombres y las fechas están simulados para proteger la privacidad de los huéspedes.
- Las cantidades de operaciones por día y por año (por ejemplo, unas 3.650 filas al año) son estimaciones de cómo trabaja el hostal, no mediciones.
- Los datos de las mediciones de las prácticas, parciales e hitos son simulados.

## Estado: lo que falta
- **H3:** estrategia, comparación medida y este README, listos.
- **Evaluación integradora:** entregada en [integradora/](integradora/).
- **Falta para la defensa:** repasar y poder explicar cada archivo con mis palabras, y comprobar que todos los enlaces de este índice abran.

## Cómo ejecutar el código
Está escrito en Python 3.12. Por ejemplo: `python comparacion.py` dentro de `h3/`.
