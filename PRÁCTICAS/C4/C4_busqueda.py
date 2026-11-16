# =====================================================================
# C4: Búsqueda lineal vs búsqueda binaria (con protocolo de medición)
#
# Aquí comparo dos formas de buscar un dato en un arreglo ordenado de
# 1.000.000 de enteros, usando 1.000 claves que sí existen.
# Protocolo: 1 corrida de calentamiento (la descarto), luego 3 corridas
# medidas, y saco el promedio.
# También mido qué tanto cuesta ordenar con burbuja e inserción, usando
# el tamaño de MI proceso (el cuaderno del hostal), para decidir si
# conviene ordenar primero.
# =====================================================================

import random   # para generar y elegir números al azar
import time     # para medir cuánto tarda cada cosa


# ---------------------------------------------------------------------
# Búsqueda lineal: reviso el arreglo de principio a fin, elemento por
# elemento, hasta encontrar la clave. Es como revisar el cuaderno del
# hostal hoja por hoja. En el peor caso reviso los N elementos.
# ---------------------------------------------------------------------
def busqueda_lineal(lista, objetivo):
    for i, x in enumerate(lista):   # i es la posición, x es el valor
        if x == objetivo:           # si coincide, lo encontré
            return i                # devuelvo la posición
    return -1                       # si llego al final, no estaba


# ---------------------------------------------------------------------
# Búsqueda binaria: solo funciona si el arreglo YA está ordenado.
# Miro el elemento del medio: si la clave es menor, descarto la mitad
# derecha; si es mayor, descarto la izquierda. Repito con la mitad que
# me queda. Cada paso elimina la mitad de los datos.
# ---------------------------------------------------------------------
def busqueda_binaria(lista, objetivo):
    lo = 0                          # límite izquierdo de donde busco
    hi = len(lista) - 1             # límite derecho de donde busco
    while lo <= hi:                 # mientras me quede zona por revisar
        mid = (lo + hi) // 2        # posición del medio
        if lista[mid] == objetivo:
            return mid              # lo encontré
        elif lista[mid] < objetivo:
            lo = mid + 1            # la clave está a la derecha
        else:
            hi = mid - 1            # la clave está a la izquierda
    return -1


# ---------------------------------------------------------------------
# Burbuja: comparo cada par de vecinos y los intercambio si están al
# revés. Repito hasta que ya no haya cambios. Es sencillo pero lento
# porque hace muchísimas comparaciones.
# ---------------------------------------------------------------------
def ordenamiento_burbuja(lista):
    a = list(lista)                         # trabajo con una copia
    n = len(a)
    for i in range(n - 1):
        hubo_cambio = False
        for j in range(n - 1 - i):          # el final ya queda ordenado
            if a[j] > a[j + 1]:             # si están al revés...
                a[j], a[j + 1] = a[j + 1], a[j]   # ...los intercambio
                hubo_cambio = True
        if not hubo_cambio:                 # si no cambié nada, ya está ordenado
            break
    return a


# ---------------------------------------------------------------------
# Inserción: voy tomando cada elemento y lo meto en su lugar dentro de
# la parte que ya tengo ordenada, como ordenar cartas en la mano. Es muy
# buena cuando los datos ya vienen casi ordenados o cuando agrego pocos.
# ---------------------------------------------------------------------
def ordenamiento_insercion(lista):
    a = list(lista)
    for i in range(1, len(a)):
        actual = a[i]                       # el elemento que voy a ubicar
        j = i - 1
        while j >= 0 and a[j] > actual:     # corro a la derecha los mayores
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = actual                   # lo dejo en su lugar
    return a


# ---------------------------------------------------------------------
# medir: ejecuta una función y devuelve cuántos segundos tardó.
# ---------------------------------------------------------------------
def medir(func, *args):
    inicio = time.perf_counter()    # hora antes de empezar
    func(*args)
    return time.perf_counter() - inicio


# ---------------------------------------------------------------------
# promedio_protocolo: aplica el protocolo del profesor.
# 1) Una corrida de calentamiento que no cuento.
# 2) Tres corridas que sí cuento.
# 3) Devuelvo el promedio de las tres.
# ---------------------------------------------------------------------
def promedio_protocolo(func, *args, repeticiones=3):
    medir(func, *args)                                      # calentamiento
    tiempos = [medir(func, *args) for _ in range(repeticiones)]
    return sum(tiempos) / repeticiones


# ---------------------------------------------------------------------
# buscar_todas: hace una búsqueda por cada clave de la lista de claves.
# ---------------------------------------------------------------------
def buscar_todas(busqueda, lista, claves):
    for c in claves:
        busqueda(lista, c)


# ---------------------------------------------------------------------
# Programa principal
# ---------------------------------------------------------------------
if __name__ == "__main__":
    N = 1_000_000   # tamaño del arreglo ordenado (lo pide la práctica)
    K = 1000        # cantidad de claves que busco (todas existen)
    M = 2000        # tamaño de MI proceso: aprox. registros del cuaderno
                    # del hostal en un año (cámbialo si tu estimación es otra)

    random.seed(42)   # fijo la semilla para que se pueda repetir

    # Arreglo ordenado de N enteros distintos
    arreglo = sorted(random.sample(range(10 * N), N))
    # Elijo K claves que sí existen en el arreglo
    claves = random.sample(arreglo, K)

    print("Midiendo búsquedas, esto tarda unos minutos...")
    t_lineal = promedio_protocolo(buscar_todas, busqueda_lineal, arreglo, claves)
    t_binaria = promedio_protocolo(buscar_todas, busqueda_binaria, arreglo, claves)

    # Ahora mido el costo de ordenar con el tamaño de mi proceso
    datos = random.sample(range(10 * M), M)   # M datos desordenados
    t_burbuja = promedio_protocolo(ordenamiento_burbuja, datos)
    t_insercion = promedio_protocolo(ordenamiento_insercion, datos)

    # Muestro todo en formato de tabla para pegarlo en resultados.md
    print()
    print(f"| Algoritmo | Tiempo promedio de {K} búsquedas (N = {N}) |")
    print("|---|---|")
    print(f"| Búsqueda lineal | {t_lineal:.4f} s |")
    print(f"| Búsqueda binaria | {t_binaria:.6f} s |")
    print(f"| Cociente lineal/binaria | {t_lineal / t_binaria:.0f} veces |")
    print()
    print(f"| Ordenamiento (M = {M} datos, mi proceso) | Tiempo promedio |")
    print("|---|---|")
    print(f"| Burbuja | {t_burbuja:.4f} s |")
    print(f"| Inserción | {t_insercion:.4f} s |")
