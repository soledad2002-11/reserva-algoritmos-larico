# MARIA SOLEDAD INTA LARICO
# =====================================================================
# Evaluación integradora - Variante A: medición
#
# Mido PlanificadorIngenuo contra PlanificadorMejorado con la CARGA del
# enunciado: n paquetes al azar (semilla fija) y una capacidad de un
# tercio del peso total. Cuatro tamaños n, n+2, n+4 y n+6 (cada +2
# paquetes la ingenua se multiplica por ~4). Protocolo: 1 corrida de
# calentamiento (la descarto), 3 corridas medidas y promedio.
# Este archivo va en la misma carpeta que planificador.py.
# =====================================================================

import random
import time
from planificador import PlanificadorIngenuo, PlanificadorMejorado


# ---------------------------------------------------------------------
# ejecutar_carga: genera n paquetes al azar, calcula la capacidad (un
# tercio del peso total) y le pide al planificador la ganancia máxima.
# ---------------------------------------------------------------------
def ejecutar_carga(plan, n):
    azar = random.Random(n)                       # semilla fija: mismos datos siempre
    paquetes = [("C" + str(i), azar.randint(5, 59), azar.randint(10, 99)) for i in range(n)]
    capacidad = sum(p[1] for p in paquetes) // 3
    ganancia, _ = plan.elegir(paquetes, capacidad)
    return ganancia


# ---------------------------------------------------------------------
# medir_una_vez: milisegundos de una corrida (con un planificador nuevo).
# promedio_protocolo: 1 calentamiento (se descarta) + 3 corridas, promedio.
# ---------------------------------------------------------------------
def medir_una_vez(fabrica, n):
    plan = fabrica()
    inicio = time.perf_counter()
    ejecutar_carga(plan, n)
    return (time.perf_counter() - inicio) * 1000


def promedio_protocolo(fabrica, n, repeticiones=3):
    medir_una_vez(fabrica, n)
    tiempos = [medir_una_vez(fabrica, n) for _ in range(repeticiones)]
    return sum(tiempos) / repeticiones


def medir_escala_grande(fabrica, n, capacidad, repeticiones=3):
    azar = random.Random(1)
    paquetes = [("C" + str(i), azar.randint(5, 59), azar.randint(10, 99)) for i in range(n)]

    def una_vez():
        inicio = time.perf_counter()
        fabrica().elegir(paquetes, capacidad)
        return (time.perf_counter() - inicio) * 1000

    una_vez()                                      # calentamiento
    return sum(una_vez() for _ in range(repeticiones)) / repeticiones


if __name__ == "__main__":
    # Elijo N_BASE para que la ingenua, con el mayor tamaño (N_BASE + 6),
    # tarde entre 0,5 y 20 segundos en MI computadora. Si tarda menos o
    # más, cambio N_BASE y repito.
    N_BASE = 14
    tamanos = [N_BASE, N_BASE + 2, N_BASE + 4, N_BASE + 6]

    print("| n (paquetes) | Ingenua (ms) | Veces mas | Mejorada (ms) | Veces mas | Misma ganancia |")
    print("|---|---|---|---|---|---|")
    ant_ing = ant_mej = None
    for n in tamanos:
        g_ing = ejecutar_carga(PlanificadorIngenuo(), n)
        g_mej = ejecutar_carga(PlanificadorMejorado(), n)
        t_ing = promedio_protocolo(PlanificadorIngenuo, n)
        t_mej = promedio_protocolo(PlanificadorMejorado, n)
        x_ing = f"x{t_ing / ant_ing:.2f}" if ant_ing else "-"
        x_mej = f"x{t_mej / ant_mej:.2f}" if ant_mej else "-"
        print(f"| {n} | {t_ing:.2f} | {x_ing} | {t_mej:.3f} | {x_mej} | {'sí' if g_ing == g_mej else 'NO'} ({g_ing}) |", flush=True)
        ant_ing, ant_mej = t_ing, t_mej

    print()
    t = medir_escala_grande(PlanificadorMejorado, 1000, 10000)
    print(f"Mejorada con 1.000 paquetes y capacidad 10.000: {t:.1f} ms (protocolo: 1 calentamiento + 3 corridas, promedio)")
