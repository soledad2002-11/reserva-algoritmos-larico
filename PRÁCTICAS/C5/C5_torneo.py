# =====================================================================
# C5: Torneo de ordenamientos
#
# Comparo cuatro competidores con cantidades crecientes de datos
# (10.000, 20.000, 40.000 y 80.000):
#   1) Inserción  -> el cuadrático, O(n²)
#   2) MergeSort  -> O(n log n), hecho por mí
#   3) QuickSort  -> O(n log n) en promedio, hecho por mí
#   4) sorted()   -> el sort propio de Python, como cuarto competidor
# Protocolo: 1 corrida de calentamiento (la descarto), luego 3 corridas
# medidas y saco el promedio.
# Antes de medir, verifico que cada algoritmo deje el arreglo ordenado.
# =====================================================================

import random   # para generar los datos desordenados
import time     # para medir el tiempo


# ---------------------------------------------------------------------
# Inserción (cuadrático): tomo cada elemento y lo meto en su lugar
# dentro de la parte que ya está ordenada, como ordenar cartas.
# ---------------------------------------------------------------------
def insercion(lista):
    a = list(lista)                         # trabajo con una copia
    for i in range(1, len(a)):
        actual = a[i]                       # elemento que voy a ubicar
        j = i - 1
        while j >= 0 and a[j] > actual:     # corro a la derecha los mayores
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = actual                   # lo dejo en su lugar
    return a


# ---------------------------------------------------------------------
# MergeSort: divido la lista en dos mitades, ordeno cada mitad (con el
# mismo método) y luego las mezclo en orden.
# ---------------------------------------------------------------------
def mergesort(lista):
    if len(lista) <= 1:                     # 0 o 1 elemento: ya está ordenada
        return list(lista)
    medio = len(lista) // 2
    izq = mergesort(lista[:medio])          # ordeno la mitad izquierda
    der = mergesort(lista[medio:])          # ordeno la mitad derecha
    resultado = []                          # aquí mezclo las dos mitades
    i = j = 0
    while i < len(izq) and j < len(der):
        if izq[i] <= der[j]:                # saco el menor de los dos frentes
            resultado.append(izq[i])
            i += 1
        else:
            resultado.append(der[j])
            j += 1
    resultado.extend(izq[i:])               # agrego lo que sobró
    resultado.extend(der[j:])
    return resultado


# ---------------------------------------------------------------------
# QuickSort: elijo un pivote al azar y separo los datos en menores,
# iguales y mayores que el pivote. Luego ordeno los menores y los
# mayores con el mismo método.
# ---------------------------------------------------------------------
def quicksort(lista):
    if len(lista) <= 1:
        return list(lista)
    pivote = random.choice(lista)           # pivote al azar
    menores = [x for x in lista if x < pivote]
    iguales = [x for x in lista if x == pivote]
    mayores = [x for x in lista if x > pivote]
    return quicksort(menores) + iguales + quicksort(mayores)


# ---------------------------------------------------------------------
# sort_python: el sort que ya trae Python (sorted), cuarto competidor.
# ---------------------------------------------------------------------
def sort_python(lista):
    return sorted(lista)


# ---------------------------------------------------------------------
# esta_ordenado: verifica que cada elemento sea menor o igual al
# siguiente. Lo uso antes de medir para asegurarme de que cada
# algoritmo realmente ordena.
# ---------------------------------------------------------------------
def esta_ordenado(lista):
    for i in range(len(lista) - 1):
        if lista[i] > lista[i + 1]:
            return False
    return True


# ---------------------------------------------------------------------
# medir: ejecuta un algoritmo y devuelve cuántos segundos tardó.
# promedio_protocolo: 1 calentamiento descartado + las corridas medidas,
# y devuelve el promedio.
# ---------------------------------------------------------------------
def medir(func, datos):
    inicio = time.perf_counter()
    func(datos)
    return time.perf_counter() - inicio


def promedio_protocolo(func, datos, repeticiones=3, calentar=True):
    if calentar:
        medir(func, datos)                  # calentamiento (se descarta)
    tiempos = [medir(func, datos) for _ in range(repeticiones)]
    return sum(tiempos) / repeticiones


# ---------------------------------------------------------------------
# Programa principal
# ---------------------------------------------------------------------
if __name__ == "__main__":
    random.seed(42)                         # para que se pueda repetir
    cantidades = [10000, 20000, 40000, 80000]

    # Inserción a partir de este tamaño tarda demasiado: con 80.000 datos
    # son más de mil millones de pasos. Ahí hago solo 1 corrida medida
    # (sin calentamiento) y lo marco con * en la tabla.
    LIMITE_PROTOCOLO_COMPLETO = 40000

    # 1) Verifico que todos dejen el arreglo ordenado antes de medir
    prueba = random.sample(range(100000), 2000)
    for nombre, f in [("Inserción", insercion), ("MergeSort", mergesort),
                      ("QuickSort", quicksort), ("sorted de Python", sort_python)]:
        assert esta_ordenado(f(prueba)), f"{nombre} no ordenó bien"
    print("Verificación OK: los 4 algoritmos dejan el arreglo ordenado.")
    print("Midiendo, esto puede tardar bastante...")
    print()

    # 2) Mido cada cantidad y muestro la tabla
    print("| Cantidad de datos | Inserción (s) | MergeSort (s) | QuickSort (s) | sorted de Python (s) |")
    print("|---|---|---|---|---|")
    for n in cantidades:
        datos = random.sample(range(10 * n), n)   # n datos desordenados
        if n <= LIMITE_PROTOCOLO_COMPLETO:
            t_ins = promedio_protocolo(insercion, datos)
            marca = ""
        else:
            t_ins = promedio_protocolo(insercion, datos, repeticiones=1, calentar=False)
            marca = "*"
        t_mer = promedio_protocolo(mergesort, datos)
        t_qui = promedio_protocolo(quicksort, datos)
        t_sor = promedio_protocolo(sort_python, datos)
        print(f"| {n} | {t_ins:.4f}{marca} | {t_mer:.4f} | {t_qui:.4f} | {t_sor:.4f} |", flush=True)

    print()
    print("* Inserción con 80000 datos: 1 sola corrida medida, sin calentamiento (tarda demasiado).")
