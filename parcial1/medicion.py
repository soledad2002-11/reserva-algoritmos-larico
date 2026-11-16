# MARIA SOLEDAD INTA LARICO 
# Parcial 1 - Variante A (Registro de carnets) - Código de medición en Python
#
# Aquí porto el código de C# a Python. La función lenta es la misma lógica
# del enunciado (no la cambio). Después escribo mi cura y mido las dos.

import random
import time


# ---------------------------------------------------------------------
# Solución ACTUAL (lenta): comparo cada carnet con todos los que le siguen.
# Hace n(n-1)/2 comparaciones en el peor caso, o sea O(n²).
# ---------------------------------------------------------------------
def hay_repetidos_por_pares(carnets):
    for i in range(len(carnets)):
        for j in range(i + 1, len(carnets)):
            if carnets[i] == carnets[j]:
                return True
    return False


# ---------------------------------------------------------------------
# MI CURA: uso un conjunto (set). Recorro la lista una sola vez: si el
# carnet ya está en "vistos", encontré un repetido; si no, lo guardo.
# Buscar en un set cuesta O(1) en promedio, así que todo cuesta O(n).
# No modifico la lista original (solo la leo).
# ---------------------------------------------------------------------
def hay_repetidos_curado(carnets):
    vistos = set()
    for c in carnets:
        if c in vistos:
            return True
        vistos.add(c)
    return False


# ---------------------------------------------------------------------
# El peor caso para las dos: una lista sin repetidos (hay que mirarla toda).
# Genero los números 0..n-1 y los mezclo con una semilla fija.
# ---------------------------------------------------------------------
def generar_sin_repetidos(n, semilla=42):
    datos = list(range(n))
    random.Random(semilla).shuffle(datos)
    return datos


# ---------------------------------------------------------------------
# Los cinco casos que mi cura debe pasar (el resultado esperado va al final).
# ---------------------------------------------------------------------
CASOS = [
    ([7, 3, 9, 3, 5], True,  "repetido en el medio"),
    ([7, 3, 9, 4, 5], False, "sin repetidos"),
    ([],              False, "lista vacía"),
    ([8],             False, "un solo elemento"),
    ([4, 1, 2, 6, 4], True,  "repetido en los extremos"),
]


def probar_casos():
    todos_ok = True
    for datos, esperado, que in CASOS:
        lenta = hay_repetidos_por_pares(datos)
        curada = hay_repetidos_curado(datos)
        ok = (lenta == esperado) and (curada == esperado)
        todos_ok = todos_ok and ok
        print(f"{que:<26} esperado {str(esperado):<5} | por pares {str(lenta):<5} | mi cura {str(curada):<5} | {'OK' if ok else 'FALLA'}")
    return todos_ok


# ---------------------------------------------------------------------
# Protocolo de medición: 1 corrida de calentamiento (se descarta),
# 3 corridas medidas y se promedian. Devuelve segundos.
# ---------------------------------------------------------------------
def medir_una_vez(func, datos):
    inicio = time.perf_counter()
    func(datos)
    return time.perf_counter() - inicio


def promedio_protocolo(func, datos, repeticiones=3):
    medir_una_vez(func, datos)                       # calentamiento
    tiempos = [medir_una_vez(func, datos) for _ in range(repeticiones)]
    return sum(tiempos) / repeticiones


# ---------------------------------------------------------------------
# Programa principal
# ---------------------------------------------------------------------
if __name__ == "__main__":
    print("== Los 5 casos de prueba ==")
    if not probar_casos():
        print("Hay casos que fallan: corrige antes de medir.")
        raise SystemExit

    # Cuatro tamaños que se duplican. Elijo N_BASE para que la solución
    # lenta con el mayor tamaño (8 x N_BASE) tarde entre 0,5 y 20 segundos
    # en MI computadora. Si tarda menos o más, cambio N_BASE y repito.
    N_BASE = 1000
    tamanos = [N_BASE, N_BASE * 2, N_BASE * 4, N_BASE * 8]

    print()
    print("== Medición en el peor caso (lista sin repetidos) ==")
    print("| n | Por pares (s) | x respecto a la fila anterior | Mi cura (ms) | x respecto a la fila anterior |")
    print("|---|---|---|---|---|")
    ant_lenta = ant_cura = None
    for n in tamanos:
        datos = generar_sin_repetidos(n)
        t_lenta = promedio_protocolo(hay_repetidos_por_pares, datos)
        t_cura = promedio_protocolo(hay_repetidos_curado, datos)
        x_lenta = f"x{t_lenta / ant_lenta:.2f}" if ant_lenta else "-"
        x_cura = f"x{t_cura / ant_cura:.2f}" if ant_cura else "-"
        print(f"| {n} | {t_lenta:.4f} | {x_lenta} | {t_cura * 1000:.4f} | {x_cura} |", flush=True)
        ant_lenta, ant_cura = t_lenta, t_cura
