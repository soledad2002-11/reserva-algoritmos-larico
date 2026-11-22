# MARIA SOLEDAD INTA LARICO
# =====================================================================
# Parcial 2 - Variante B: medición de ReceptorIngenuo contra ReceptorMejorado
#
# Uso la CARGA del enunciado: llegan n pedidos y después se preparan los n.
# Tres tamaños que se duplican (n, 2n, 4n) y el protocolo de clase:
# 1 corrida de calentamiento (la descarto), 3 corridas medidas y promedio.
# Este archivo va en la misma carpeta que solucion.py, de donde importo
# las dos clases.
# =====================================================================

import time
from solucion import ReceptorIngenuo, ReceptorMejorado


# ---------------------------------------------------------------------
# ejecutar_carga: n pedidos llegan y luego se preparan los n.
# Los plazos se repiten (15, 30, 45, 60, 75 y 90 minutos), así que hay
# muchos empates y el desempate se usa de verdad.
# Devuelve un "control" (suma de los largos de los nombres) para
# comprobar que las dos soluciones sacan los mismos pedidos.
# ---------------------------------------------------------------------
def ejecutar_carga(receptor, n):
    for i in range(n):
        receptor.registrar("Q" + str(i), ((i * 6007) % 6 + 1) * 15)
    control = 0
    for _ in range(n):
        control += len(receptor.preparar_siguiente())
    return control


# ---------------------------------------------------------------------
# Cada corrida usa un receptor NUEVO (vacío), para que una corrida no
# afecte a la siguiente. Devuelve milisegundos.
# ---------------------------------------------------------------------
def medir_una_vez(clase, n):
    receptor = clase()
    inicio = time.perf_counter()
    ejecutar_carga(receptor, n)
    return (time.perf_counter() - inicio) * 1000


# Protocolo: 1 calentamiento (se descarta) + 3 corridas medidas + promedio.
def promedio_protocolo(clase, n, repeticiones=3):
    medir_una_vez(clase, n)
    tiempos = [medir_una_vez(clase, n) for _ in range(repeticiones)]
    return sum(tiempos) / repeticiones


if __name__ == "__main__":
    # Elijo N_BASE para que la ingenua, con el mayor tamaño (4 x N_BASE),
    # tarde entre 0,5 y 20 segundos en MI computadora. Si tarda menos o
    # más, cambio N_BASE y repito.
    N_BASE = 1000
    tamanos = [N_BASE, N_BASE * 2, N_BASE * 4]

    # Verifico que las dos dan el mismo resultado en la carga
    assert ejecutar_carga(ReceptorIngenuo(), 500) == ejecutar_carga(ReceptorMejorado(), 500)
    print("Verificación OK: las dos soluciones preparan los mismos pedidos.")
    print()

    print("| n | Ingenua (ms) | Veces mas | Mejorada (ms) | Veces mas |")
    print("|---|---|---|---|---|")
    ant_ing = ant_mej = None
    for n in tamanos:
        t_ing = promedio_protocolo(ReceptorIngenuo, n)
        t_mej = promedio_protocolo(ReceptorMejorado, n)
        x_ing = f"x{t_ing / ant_ing:.2f}" if ant_ing else "-"
        x_mej = f"x{t_mej / ant_mej:.2f}" if ant_mej else "-"
        print(f"| {n} | {t_ing:.2f} | {x_ing} | {t_mej:.2f} | {x_mej} |", flush=True)
        ant_ing, ant_mej = t_ing, t_mej
