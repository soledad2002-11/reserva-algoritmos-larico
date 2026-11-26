# =====================================================================
# C3 - Medición empírica de crecimiento
#
# Comparo dos procesos:
#   - uno con UN ciclo que se repite n veces (lineal, O(n))
#   - uno con DOS ciclos, uno dentro del otro (cuadrático, O(n²))
# y mido cuánto tardan con tres tamaños: n, 4n y 16n.
#
# Protocolo: primero una corrida de calentamiento que NO cuento (la
# primera vez suele ser más lenta); después repito cada medición varias
# veces y saco el promedio.
# =====================================================================

import time

REPETICIONES = 5     # cuántas corridas mido y promedio (después del calentamiento)


# ---------------------------------------------------------------------
# Proceso lineal: UN ciclo que da n vueltas y en cada una hace una
# suma. Hace n pasos, por eso es O(n).
# ---------------------------------------------------------------------
def proceso_lineal(n):
    total = 0
    for i in range(n):
        total += i
    return total


# ---------------------------------------------------------------------
# Proceso cuadrático: DOS ciclos, uno dentro del otro. El de afuera da
# n vueltas y, en cada una, el de adentro da otras n vueltas: n x n
# pasos, por eso es O(n²).
# ---------------------------------------------------------------------
def proceso_cuadratico(n):
    cuenta = 0
    for i in range(n):
        for j in range(n):
            cuenta += 1
    return cuenta


# ---------------------------------------------------------------------
# medir_una_vez: cuántos milisegundos tarda una ejecución.
# promedio_protocolo: 1 corrida de calentamiento (se descarta) y luego
# REPETICIONES corridas medidas; devuelvo el promedio.
# ---------------------------------------------------------------------
def medir_una_vez(proceso, n):
    inicio = time.perf_counter()
    proceso(n)
    return (time.perf_counter() - inicio) * 1000


def promedio_protocolo(proceso, n):
    medir_una_vez(proceso, n)                                   # calentamiento
    tiempos = [medir_una_vez(proceso, n) for _ in range(REPETICIONES)]
    return sum(tiempos) / REPETICIONES


if __name__ == "__main__":
    # Tres tamaños: n, 4n y 16n. Elijo n para que el proceso cuadrático
    # con el tamaño más grande tarde unos segundos en MI computadora.
    n = 250
    tamanos = [n, 4 * n, 16 * n]

    print(f"Protocolo: 1 calentamiento + {REPETICIONES} corridas medidas, promedio")
    print("| n | Proceso lineal (ms) | Veces mas | Proceso cuadrático (ms) | Veces mas |")
    print("|---:|---:|---:|---:|---:|")
    ant_l = ant_c = None
    for tam in tamanos:
        t_l = promedio_protocolo(proceso_lineal, tam)
        t_c = promedio_protocolo(proceso_cuadratico, tam)
        x_l = f"x{t_l / ant_l:.2f}" if ant_l else "-"
        x_c = f"x{t_c / ant_c:.2f}" if ant_c else "-"
        print(f"| {tam} | {t_l:.4f} | {x_l} | {t_c:.4f} | {x_c} |", flush=True)
        ant_l, ant_c = t_l, t_c
