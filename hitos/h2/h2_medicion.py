# =====================================================================
# H2 - Medición: buscar a un huésped por su nombre en el registro del hostal
#
# El MISMO problema resuelto con dos versiones:
#   - INGENUA: una lista de registros, como mi cuaderno. Para buscar,
#     la recorro entera.
#   - ELEGIDA: una tabla hash (en Python, un diccionario o dict) con el
#     nombre del huésped como clave.
#
# El problema: "¿en qué habitaciones y en qué días estuvo este huésped?"
#
# Cómo mido: 4 tamaños que se duplican (n, 2n, 4n, 8n) y el protocolo de
# clase: 1 corrida de calentamiento (la descarto), 3 corridas medidas y
# saco el promedio.
# =====================================================================

import random   # para generar datos al azar (pero siempre los mismos)
import time     # para medir cuánto tarda cada cosa


# ---------------------------------------------------------------------
# generar_registros: crea n registros del hostal.
# Cada registro es una tupla (nombre, habitacion, dia), como una fila de
# mi hoja diaria de hospedaje.
# - Uso una semilla fija (42) para que los datos sean siempre los mismos
#   y mis resultados se puedan repetir.
# - Hay menos nombres distintos que registros (el 60 %), porque hay
#   huéspedes que vuelven y aparecen en varias estadías.
# ---------------------------------------------------------------------
def generar_registros(n, semilla=42):
    azar = random.Random(semilla)
    cantidad_nombres = max(1, int(n * 0.6))
    registros = []
    for _ in range(n):
        nombre = f"Huesped {azar.randrange(cantidad_nombres):05d}"
        habitacion = azar.randint(50, 69)      # mis 20 habitaciones (50 a 69)
        dia = azar.randint(1, 365)             # día del año
        registros.append((nombre, habitacion, dia))
    return registros


# ---------------------------------------------------------------------
# VERSIÓN INGENUA: buscar en la lista.
# Reviso TODOS los registros uno por uno y me quedo con los que tienen el
# nombre que busco. No puedo parar en el primero que encuentre, porque un
# huésped puede tener varias estadías.
# Costo: O(n) por cada búsqueda (miro los n registros).
# ---------------------------------------------------------------------
def buscar_en_lista(registros, nombre):
    encontrados = []
    for r in registros:                        # r = (nombre, habitacion, dia)
        if r[0] == nombre:                     # r[0] es el nombre
            encontrados.append((r[1], r[2]))   # guardo (habitacion, dia)
    return encontrados


# ---------------------------------------------------------------------
# VERSIÓN ELEGIDA: tabla hash (dict).
# armar_tabla: recorro los registros UNA sola vez y agrupo las estadías
# por nombre: nombre -> lista de (habitacion, dia). Cuesta O(n), pero se
# paga una sola vez.
# ---------------------------------------------------------------------
def armar_tabla(registros):
    tabla = {}
    for nombre, habitacion, dia in registros:
        # setdefault crea la lista vacía si el nombre es nuevo
        tabla.setdefault(nombre, []).append((habitacion, dia))
    return tabla


# buscar_en_tabla: la función hash calcula la casilla del nombre y voy
# directo, sin recorrer los demás. Si el nombre no está, devuelve [].
# Costo: O(1) en promedio.
def buscar_en_tabla(tabla, nombre):
    return tabla.get(nombre, [])


# ---------------------------------------------------------------------
# Para medir hago varias búsquedas seguidas. Una "corrida" mide el tiempo
# total de todas las búsquedas de la lista "nombres".
# ---------------------------------------------------------------------
def buscar_todas_lista(registros, nombres):
    for nombre in nombres:
        buscar_en_lista(registros, nombre)


def buscar_todas_tabla(tabla, nombres):
    for nombre in nombres:
        buscar_en_tabla(tabla, nombre)


# ---------------------------------------------------------------------
# medir_una_vez: ejecuta una función y devuelve cuántos milisegundos tardó.
# promedio_protocolo: aplica el protocolo de clase.
#   1) Una corrida de calentamiento que NO cuento (la primera vez suele
#      ser más lenta y ensuciaría la medición).
#   2) Tres corridas que sí cuento.
#   3) Devuelvo el promedio de esas tres.
# ---------------------------------------------------------------------
def medir_una_vez(func, *args):
    inicio = time.perf_counter()               # hora antes de empezar
    func(*args)
    return (time.perf_counter() - inicio) * 1000   # segundos -> milisegundos


def promedio_protocolo(func, *args, repeticiones=3):
    medir_una_vez(func, *args)                 # calentamiento (se descarta)
    tiempos = [medir_una_vez(func, *args) for _ in range(repeticiones)]
    return sum(tiempos) / repeticiones         # promedio de las 3


# ---------------------------------------------------------------------
# Programa principal
# ---------------------------------------------------------------------
if __name__ == "__main__":
    # Cuatro tamaños que se duplican (n, 2n, 4n y 8n). Parto de mis 3.650
    # filas de hoy (ver inventario.md); 7.300 es mi peor año.
    N_BASE = 3650
    K = 1000          # cantidad de búsquedas en cada corrida
    tamanos = [N_BASE, N_BASE * 2, N_BASE * 4, N_BASE * 8]

    # 1) Verifico que las dos versiones dan LA MISMA respuesta. Si no
    #    dieran lo mismo, no estarían resolviendo el mismo problema y la
    #    comparación no valdría. (Incluyo un nombre que no existe.)
    prueba = generar_registros(N_BASE)
    tabla_prueba = armar_tabla(prueba)
    for nombre in ["Huesped 00000", "Huesped 00007", "Huesped 00100", "Huesped 02000", "Nadie 1"]:
        assert buscar_en_lista(prueba, nombre) == buscar_en_tabla(tabla_prueba, nombre), nombre
    print("Verificación OK: la lista y la tabla hash dan las mismas respuestas.")
    print()

    # 2) Mido. Busco nombres que NO están en el registro: es el peor caso,
    #    porque la lista tiene que revisar todo y aun así no encuentra nada.
    ausentes = [f"Visitante {i:05d}" for i in range(K)]

    print(f"Tiempo de {K} búsquedas (ms), protocolo: 1 calentamiento + 3 corridas, promedio")
    print("| n | Ingenua (ms) | Veces mas | Elegida (ms) | Veces mas |")
    print("|---|---|---|---|---|")
    ant_lista = ant_tabla = None     # tiempos de la fila anterior
    armados = []                     # aquí guardo cuánto cuesta armar la tabla
    for n in tamanos:
        registros = generar_registros(n)
        tabla = armar_tabla(registros)
        t_lista = promedio_protocolo(buscar_todas_lista, registros, ausentes)
        t_tabla = promedio_protocolo(buscar_todas_tabla, tabla, ausentes)
        armados.append((n, promedio_protocolo(armar_tabla, registros)))
        # "Veces mas" = tiempo de esta fila / tiempo de la fila anterior
        x_lista = f"x{t_lista / ant_lista:.2f}" if ant_lista else "-"
        x_tabla = f"x{t_tabla / ant_tabla:.2f}" if ant_tabla else "-"
        print(f"| {n} | {t_lista:.2f} | {x_lista} | {t_tabla:.4f} | {x_tabla} |", flush=True)
        ant_lista, ant_tabla = t_lista, t_tabla

    # 3) Costo de armar la tabla hash (se paga una sola vez)
    print()
    print("Costo de armar la tabla hash (una sola vez)")
    print("| n | Armar la tabla (ms) |")
    print("|---|---|")
    for n, t in armados:
        print(f"| {n} | {t:.2f} |")
