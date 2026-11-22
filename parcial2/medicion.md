MARIA SOLEDAD INTA LARICO

# P2.3 Medir: pedidos de una pastelería (Variante B)

## Qué comparé
`ReceptorIngenuo` (lista simple) contra `ReceptorMejorado` (heap + set), con la carga del enunciado: llegan n pedidos y después se preparan los n. Los costos que declaré en eleccion.md son:
- Ingenua: preparar recorre todos los pendientes, O(n) cada vez, así que la carga completa cuesta O(n²).
- Mejorada: registrar y preparar cuestan O(log n) cada uno, así que la carga completa cuesta O(n log n).

## Cómo medí
- Lenguaje: Python 3.12. Código en `P2_medicion.py` (usa las clases de `solucion.py`).
- Tres tamaños que se duplican: n = 1.000, 2.000 y 4.000 pedidos. Con 4.000, la ingenua tardó 1,46 s, dentro del rango pedido (entre 0,5 y 20 segundos).
- Cada corrida usa un receptor nuevo (vacío). Los plazos se repiten (15 a 90 minutos), así que hay muchos empates.
- Antes de medir verifiqué que las dos soluciones preparan los mismos pedidos.
- Protocolo de clase: 1 corrida de calentamiento (descartada), 3 corridas medidas y promedio.

## Tabla

| n | Ingenua (ms) | Veces mas | Mejorada (ms) | Veces mas |
|---|---|---|---|---|
| 1000 | 129.10 | - | 2.25 | - |
| 2000 | 550.96 | x4.27 | 5.05 | x2.25 |
| 4000 | 1458.81 | x2.65 | 7.23 | x1.43 |

## Conclusión
## Conclusión
1. **La ingenua se parece a O(n²).** Al duplicar n esperaba cerca de x4 y salió x4,27 y x2,65. En total, con 4 veces más pedidos (de 1.000 a 4.000) el tiempo se multiplicó por 11,3: O(n²) predice x16 y O(n) predice x4, así que se parece más a O(n²), aunque quedó por debajo de x16.
2. **La mejorada creció mucho menos, pero con estos tamaños no puedo distinguir n log n de n.** Al duplicar n salió x2,25 y x1,43, y en total x3,2 (O(n log n) predice cerca de x4,8 y O(n) predice x4). Quedó por debajo de las dos predicciones; lo atribuyo a que sus tiempos son de pocos milisegundos y a costos fijos y ruido de mi computadora, pero no lo verifiqué. Lo que sí se ve es que no crece de forma cuadrática.
3. **Hay ruido y por eso miro la tendencia.** Los pasos x2,65 (ingenua) y x1,43 (mejorada) salieron por debajo de lo esperado. La diferencia entre ingenua y mejorada fue de unas 57 veces con 1.000 pedidos, 109 con 2.000 y 202 con 4.000: crece al duplicar n, como se espera de n² contra n log n, y con los 120.000 pedidos de una jornada sería mucho mayor.
