"""Torneo de ordenamiento: insercion vs MergeSort vs QuickSort vs sort nativo.

Uso:
    python torneo.py                  # tamanos por defecto: 10000 20000 40000 80000
    python torneo.py 1000 2000        # tamanos personalizados (para probar rapido)

Protocolo: 1 corrida de calentamiento (no cuenta) + 3 corridas medidas -> promedio.
Antes de medir, se verifica que cada algoritmo deje el arreglo ordenado.
"""
import random
import sys
import time

TAMANOS = [10_000, 20_000, 40_000, 80_000]
CORRIDAS = 3
SEMILLA = 42


def insercion(a):
    for i in range(1, len(a)):
        clave = a[i]
        j = i - 1
        while j >= 0 and a[j] > clave:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = clave
    return a


def merge_sort(a):
    if len(a) <= 1:
        return a
    medio = len(a) // 2
    izq = merge_sort(a[:medio])
    der = merge_sort(a[medio:])
    res = []
    i = j = 0
    while i < len(izq) and j < len(der):
        if izq[i] <= der[j]:
            res.append(izq[i])
            i += 1
        else:
            res.append(der[j])
            j += 1
    res.extend(izq[i:])
    res.extend(der[j:])
    return res


def quick_sort(a):
    def particionar(lo, hi):
        p = random.randint(lo, hi)
        a[p], a[hi] = a[hi], a[p]
        pivote = a[hi]
        i = lo
        for j in range(lo, hi):
            if a[j] < pivote:
                a[i], a[j] = a[j], a[i]
                i += 1
        a[i], a[hi] = a[hi], a[i]
        return i

    def ordenar(lo, hi):
        while lo < hi:
            p = particionar(lo, hi)
            # recursion en la parte menor para limitar la profundidad
            if p - lo < hi - p:
                ordenar(lo, p - 1)
                lo = p + 1
            else:
                ordenar(p + 1, hi)
                hi = p - 1

    ordenar(0, len(a) - 1)
    return a


def sort_nativo(a):
    a.sort()
    return a


ALGORITMOS = [
    ("Insercion", insercion),
    ("MergeSort", merge_sort),
    ("QuickSort", quick_sort),
    ("sort() de Python", sort_nativo),
]


def medir(funcion, datos):
    copia = datos[:]
    t0 = time.perf_counter()
    funcion(copia)
    return time.perf_counter() - t0


def main():
    tamanos = [int(x) for x in sys.argv[1:]] or TAMANOS
    random.seed(SEMILLA)

    # 1) Verificacion de correccion
    prueba = [random.randint(0, 1_000_000) for _ in range(1000)]
    esperado = sorted(prueba)
    for nombre, f in ALGORITMOS:
        assert f(prueba[:]) == esperado, f"{nombre} no ordena bien"
    print("Verificacion OK: todos dejan el arreglo ordenado.\n")

    # 2) Calentamiento (no cuenta)
    for _, f in ALGORITMOS:
        f(prueba[:])

    # 3) Torneo
    resultados = {nombre: [] for nombre, _ in ALGORITMOS}
    for n in tamanos:
        datos = [random.randint(0, 1_000_000) for _ in range(n)]
        for nombre, f in ALGORITMOS:
            tiempos = [medir(f, datos) for _ in range(CORRIDAS)]
            prom = sum(tiempos) / CORRIDAS
            resultados[nombre].append(prom)
            print(f"n={n:>7,}  {nombre:<18} {prom:9.4f} s")
        print()

    # 4) Tabla en Markdown
    cab = "| Algoritmo | " + " | ".join(f"{n:,}" for n in tamanos) + " |"
    sep = "|---|" + "---|" * len(tamanos)
    filas = [
        f"| {nombre} | " + " | ".join(f"{t:.4f} s" for t in tiempos) + " |"
        for nombre, tiempos in resultados.items()
    ]
    tabla = "\n".join([cab, sep] + filas)
    print(tabla)
    with open("tabla_tiempos.md", "w", encoding="utf-8") as fh:
        fh.write(tabla + "\n")
    print("\nTabla guardada en tabla_tiempos.md")


if __name__ == "__main__":
    main()