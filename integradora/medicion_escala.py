# MARIA SOLEDAD INTA LARICO
# =====================================================================
# Evaluación integradora - Variante A: mi solución en tamaños más grandes
#
# Con n = 14 a 20 la mejorada tarda décimas de milisegundo y el ruido
# domina. Aquí la mido con n = 100, 200, 400 y 800 paquetes (la capacidad
# es un tercio del peso total, así que crece con n) para ver mejor su
# forma. Protocolo: 1 calentamiento + 3 corridas, promedio.
# Va en la misma carpeta que planificador.py y medicion.py.
# =====================================================================

from planificador import PlanificadorMejorado
from medicion import ejecutar_carga, promedio_protocolo

if __name__ == "__main__":
    print("| n (paquetes) | Mejorada (ms) | Veces mas |")
    print("|---|---|---|")
    anterior = None
    for n in [100, 200, 400, 800]:
        t = promedio_protocolo(PlanificadorMejorado, n)
        x = f"x{t / anterior:.2f}" if anterior else "-"
        print(f"| {n} | {t:.2f} | {x} |", flush=True)
        anterior = t
