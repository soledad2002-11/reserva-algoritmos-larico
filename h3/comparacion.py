# =====================================================================
# H3 - Comparación medida: ¿qué solicitudes de reserva acepto en una semana?
#
# Mi caso (Hostal Kantu Flor): en temporada alta llegan más solicitudes de
# las que caben. Lo modelo como una MOCHILA (problema análogo):
#   - capacidad = habitaciones-noche de la semana (20 habitaciones x 7 noches = 140)
#   - cada solicitud "pesa" habitaciones x noches y "vale" lo que paga (Bs)
#   - quiero la mayor suma de pagos sin pasarme de la capacidad
# Resuelvo el MISMO problema por fuerza bruta (2^n) y por programación
# dinámica (tabla n x capacidad), y mido las dos.
# =====================================================================

import random
import time

CAPACIDAD = 20 * 7     # habitaciones-noche de una semana


# ---------------------------------------------------------------------
# Genero n solicitudes (id, peso, pago). Peso = habitaciones x noches
# (de 1 a 3 habitaciones, de 2 a 7 noches). Pago = peso x precio por
# habitación-noche (de 55 a 80 Bs). Semilla fija: siempre los mismos datos.
# ---------------------------------------------------------------------
def generar_solicitudes(n, semilla=7):
    azar = random.Random(semilla + n)
    solicitudes = []
    for i in range(n):
        peso = azar.randint(1, 3) * azar.randint(2, 7)
        pago = peso * azar.randint(55, 80)
        solicitudes.append(("S" + str(i), peso, pago))
    return solicitudes


# ---------------------------------------------------------------------
# FUERZA BRUTA: pruebo TODOS los subconjuntos (2^n). Cada subconjunto es
# una máscara de bits; para cada uno sumo peso y pago de las n solicitudes.
# Costo: O(n * 2^n).
# ---------------------------------------------------------------------
def fuerza_bruta(solicitudes, capacidad):
    n = len(solicitudes)
    mejor = 0
    mejor_mascara = 0
    for mascara in range(1 << n):
        peso = 0
        pago = 0
        for i in range(n):
            if mascara & (1 << i):
                peso += solicitudes[i][1]
                pago += solicitudes[i][2]
        if peso <= capacidad and pago > mejor:
            mejor = pago
            mejor_mascara = mascara
    elegidas = [solicitudes[i][0] for i in range(n) if mejor_mascara & (1 << i)]
    return mejor, elegidas


# ---------------------------------------------------------------------
# PROGRAMACIÓN DINÁMICA: mejor[c] = mayor pago posible con capacidad c
# usando las solicitudes ya revisadas. Para cada solicitud (peso w, pago p),
# de mayor a menor capacidad: mejor[c] = max(mejor[c], mejor[c - w] + p).
# La tabla "tomar" anota dónde convino aceptarla, para reconstruir cuáles
# se eligieron. Costo: O(n * capacidad).
# ---------------------------------------------------------------------
def dinamica(solicitudes, capacidad):
    n = len(solicitudes)
    mejor = [0] * (capacidad + 1)
    tomar = []
    for i in range(n):
        _, w, p = solicitudes[i]
        decision = bytearray(capacidad + 1)
        for c in range(capacidad, w - 1, -1):
            if mejor[c - w] + p > mejor[c]:
                mejor[c] = mejor[c - w] + p
                decision[c] = 1
        tomar.append(decision)
    elegidas = []
    c = capacidad
    for i in range(n - 1, -1, -1):
        if tomar[i][c]:
            elegidas.append(solicitudes[i][0])
            c -= solicitudes[i][1]
    return mejor[capacidad], elegidas


# ---------------------------------------------------------------------
# VORAZ (solo para mostrar que se equivoca): acepto primero la solicitud
# que paga más por habitación-noche, mientras quepa.
# ---------------------------------------------------------------------
def voraz(solicitudes, capacidad):
    orden = sorted(solicitudes, key=lambda s: s[2] / s[1], reverse=True)
    usado = 0
    total = 0
    for _, w, p in orden:
        if usado + w <= capacidad:
            usado += w
            total += p
    return total


# Verifico que un conjunto de solicitudes cabe y que su pago es el declarado
def es_valida(solicitudes, elegidas, capacidad, pago_declarado):
    por_id = {s[0]: s for s in solicitudes}
    peso = sum(por_id[e][1] for e in elegidas)
    pago = sum(por_id[e][2] for e in elegidas)
    return peso <= capacidad and pago == pago_declarado


def medir_una_vez(func, *args):
    inicio = time.perf_counter()
    func(*args)
    return (time.perf_counter() - inicio) * 1000


def promedio_protocolo(func, *args, repeticiones=3):
    medir_una_vez(func, *args)                        # calentamiento (se descarta)
    tiempos = [medir_una_vez(func, *args) for _ in range(repeticiones)]
    return sum(tiempos) / repeticiones


if __name__ == "__main__":
    # --- 1) El contraejemplo de mi estrategia.md: capacidad 10 ---
    ejemplo = [("A", 6, 390), ("B", 5, 300), ("C", 5, 300)]
    print("Ejemplo (capacidad 10): A 6 hab-noche paga 390; B 5 paga 300; C 5 paga 300")
    print(f"  Voraz: {voraz(ejemplo, 10)} | Dinámica: {dinamica(ejemplo, 10)} | Fuerza bruta: {fuerza_bruta(ejemplo, 10)}")
    print()

    # --- 2) ¿Qué tan seguido se equivoca el voraz? (200 casos al azar, n = 12) ---
    falla = 0
    for k in range(200):
        s = generar_solicitudes(12, semilla=1000 + k)
        if voraz(s, CAPACIDAD) < dinamica(s, CAPACIDAD)[0]:
            falla += 1
    print(f"En 200 casos al azar con 12 solicitudes y capacidad {CAPACIDAD}, el voraz no llegó al óptimo en {falla}.")
    print()

    # --- 3) Comparación medida: cuatro tamaños (n, n+1, n+2, n+3) ---
    # Con fuerza bruta no puedo duplicar n (2^n explotaría), así que subo
    # n de 1 en 1: cada +1 solicitud duplica el trabajo de la fuerza bruta.
    N_BASE = 16
    tamanos = [N_BASE, N_BASE + 1, N_BASE + 2, N_BASE + 3]
    print(f"Capacidad fija: {CAPACIDAD} habitaciones-noche. Protocolo: 1 calentamiento + 3 corridas, promedio.")
    print("| n (solicitudes) | Fuerza bruta (ms) | Veces mas | Dinámica (ms) | Veces mas | Mismo resultado |")
    print("|---|---|---|---|---|---|")
    ant_fb = ant_dp = None
    for n in tamanos:
        s = generar_solicitudes(n)
        g_fb, e_fb = fuerza_bruta(s, CAPACIDAD)
        g_dp, e_dp = dinamica(s, CAPACIDAD)
        ok = (g_fb == g_dp) and es_valida(s, e_fb, CAPACIDAD, g_fb) and es_valida(s, e_dp, CAPACIDAD, g_dp)
        t_fb = promedio_protocolo(fuerza_bruta, s, CAPACIDAD)
        t_dp = promedio_protocolo(dinamica, s, CAPACIDAD)
        x_fb = f"x{t_fb / ant_fb:.2f}" if ant_fb else "-"
        x_dp = f"x{t_dp / ant_dp:.2f}" if ant_dp else "-"
        print(f"| {n} | {t_fb:.2f} | {x_fb} | {t_dp:.3f} | {x_dp} | {'sí' if ok else 'NO'} ({g_fb} Bs) |", flush=True)
        ant_fb, ant_dp = t_fb, t_dp
