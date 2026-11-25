# H3 Estrategia: ¿voraz o programación dinámica?

## 1. Mi caso y la decisión que se repite
En el Hostal Kantu Flor (Copacabana), con 20 habitaciones, en temporada alta (por ejemplo, agosto, cuando se llena casi una semana y media) llegan más solicitudes de reserva de las que caben. Cada semana tengo que decidir cuáles aceptar. Esa decisión se repite, y el resultado que quiero optimizar es el dinero que entra: la mayor suma de pagos sin pasar la capacidad.

## 2. Cómo lo modelé (un problema análogo)
Lo modelo como una mochila: cada solicitud "pesa" las habitaciones-noche que ocupa (habitaciones x noches) y "vale" lo que paga. La capacidad de una semana es 20 habitaciones x 7 noches = 140 habitaciones-noche. Cada solicitud se acepta entera o no se acepta.

Es un problema análogo y no el caso exacto: el hostal real también depende de qué noches se ocupan, del tipo de habitación y de cuántas personas viajan. Por eso lo declaro como una simplificación.

## 3. ¿Admite una estrategia voraz?
Un voraz funciona cuando se cumplen dos propiedades: (1) la elección local lleva al óptimo (lo que elijo ahora nunca me arrepiento), y (2) lo que queda después de elegir es el mismo problema pero más chico.

Probé el voraz de aceptar primero la solicitud que paga más por habitación-noche, con este ejemplo (capacidad 10; los números los inventé para ilustrar):

| Solicitud | Habitaciones-noche | Paga (Bs) | Bs por hab-noche |
|---|---|---|---|
| A | 6 | 390 | 65 |
| B | 5 | 300 | 60 |
| C | 5 | 300 | 60 |

- **Voraz:** acepta A primero (65 es lo más alto), y como B y C pesan 5, ya no caben (6 + 5 = 11 > 10). Gana **390**.
- **Lo mejor posible:** aceptar B y C (5 + 5 = 10) gana **600**.

Aquí la propiedad (2) sí se cumple, porque después de aceptar A queda el mismo problema con capacidad 4. Lo que falla es la propiedad (1): la elección local de A no lleva al óptimo. Por eso **mi caso NO admite un voraz** para maximizar el dinero.

Además, con mi código probé 200 casos al azar con 12 solicitudes y capacidad 140, y el voraz no llegó al óptimo enAdemás, con mi código probé 200 casos al azar con 12 solicitudes y capacidad 140, y el voraz no llegó al óptimo en 5 de ellos (2,5 %). Falla pocas veces, pero un voraz tiene que acertar siempre, y basta un contraejemplo para descartarlo. de ellos. Falla pocas veces, pero un voraz tiene que acertar siempre, y basta un contraejemplo para descartarlo.

El voraz sí serviría si el objetivo fuera otro: aceptar la mayor cantidad de solicitudes, porque en ese caso aceptar primero las que ocupan menos habitaciones-noche es una elección local segura. Pero mi objetivo es el dinero.

## 4. ¿Admite programación dinámica?
Sí, porque se cumplen sus dos propiedades:

1. **Los subproblemas se repiten.** La pregunta "¿cuál es el mayor pago usando las primeras i solicitudes con capacidad c?" aparece una y otra vez al decidir las siguientes. Con fuerza bruta se vuelve a resolver en cada combinación; con una tabla la resuelvo una sola vez y la guardo.
2. **La solución se arma con soluciones de pedazos.** El mayor pago para (i, c) sale de dos opciones: no acepto la solicitud i (queda el mejor de las i-1 solicitudes con la misma capacidad) o la acepto (su pago más el mejor de las i-1 solicitudes con la capacidad que queda). Me quedo con la mayor:
   mejor(i, c) = máximo entre mejor(i-1, c) y mejor(i-1, c - peso_i) + pago_i, con mejor(0, c) = 0.

**Ejemplo con la tabla** (el mismo ejemplo A, B, C con capacidad 10):

| Solicitudes revisadas | c=0 | c=1 | c=2 | c=3 | c=4 | c=5 | c=6 | c=7 | c=8 | c=9 | c=10 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ninguna | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| hasta A | 0 | 0 | 0 | 0 | 0 | 0 | 390 | 390 | 390 | 390 | 390 |
| hasta B | 0 | 0 | 0 | 0 | 0 | 300 | 390 | 390 | 390 | 390 | 390 |
| hasta C | 0 | 0 | 0 | 0 | 0 | 300 | 390 | 390 | 390 | 390 | **600** |

La celda final se calcula así: máximo entre 390 (no acepto C) y 300 + 300 = 600 (acepto C y miro la celda de c=5 en la fila de B). El mayor pago es 600. Para saber cuáles acepté retrocedo: en c=10 la fila de C vale 600 y la de B vale 390, cambió, así que acepto C y me quedan 5; en c=5 la fila de B vale 300 y la de A vale 0, cambió, así que acepto B y me quedan 0. A no. Aceptadas: B y C.

## 5. Costos de cada estrategia
Con n = 30 solicitudes en una semana (estimación) y capacidad 140:

| Estrategia | Costo | Pasos aproximados | ¿Siempre correcta? |
|---|---|---|---|
| Fuerza bruta | O(2^n) subconjuntos (en mi código O(n · 2^n)) | 2^30 = 1.074 millones de subconjuntos | Sí |
| Voraz | O(n log n) | unos 150 | No (390 contra 600) |
| Programación dinámica | O(n · capacidad) | 30 x 140 = 4.200 celdas | Sí |

## 6. Límites
- El modelo ignora qué noches exactas se ocupan, el tipo de habitación y el número de personas.
- El costo de la tabla crece con la capacidad. Con 140 habitaciones-noche es chica, y si fuera enorme la tabla se volvería imposible de guardar.
- En mi hostal esta decisión solo importa en temporada alta, cuando hay más solicitudes que lugar.
- Los datos de la comparación (en comparacion.md) son simulados.

## 7. Conclusión
Mi caso **no admite una estrategia voraz** (contraejemplo: 390 contra 600) y **sí admite programación dinámica**, porque los subproblemas se repiten y la solución se arma con soluciones de pedazos. La comparación medida con fuerza bruta está en `comparacion.md`.
