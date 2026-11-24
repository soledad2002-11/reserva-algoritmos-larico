# MARIA SOLEDAD INTA LARICO
# =====================================================================
# Evaluación integradora - Variante A: Furgoneta de reparto
#
# Caso: elegir qué paquetes llevar (cada uno con peso en kg y ganancia en
# Bs) para ganar lo máximo sin pasarme de la capacidad de la furgoneta.
# Cada paquete se lleva entero o no se lleva (es una mochila 0/1).
#
# Aquí porto el código de C# a Python:
#   - PlanificadorIngenuo: prueba todos los subconjuntos (2^n).
#   - PlanificadorMejorado: MI solución, con programación dinámica y un set.
# =====================================================================


# Un paquete es una tupla (codigo, kg, ganancia).


# ---------------------------------------------------------------------
# SOLUCIÓN INGENUA: prueba TODOS los subconjuntos (2^n).
# Cada subconjunto es un número "máscara": si el bit i está encendido, el
# paquete i va en el subconjunto. Para cada máscara sumo peso y ganancia
# recorriendo los n paquetes. Costo: O(n * 2^n).
# ---------------------------------------------------------------------
class PlanificadorIngenuo:
    def __init__(self):
        self._elegidos = []

    def elegir(self, paquetes, capacidad_kg):
        n = len(paquetes)
        mejor = 0
        mejor_mascara = 0
        for mascara in range(1 << n):
            kg = 0
            ganancia = 0
            for i in range(n):
                if mascara & (1 << i):
                    kg += paquetes[i][1]
                    ganancia += paquetes[i][2]
            if kg <= capacidad_kg and ganancia > mejor:
                mejor = ganancia
                mejor_mascara = mascara
        self._elegidos = [paquetes[i][0] for i in range(n) if mejor_mascara & (1 << i)]
        return mejor, list(self._elegidos)

    def esta_en_el_viaje(self, codigo):
        return codigo in self._elegidos          # recorre la lista: O(k)


# ---------------------------------------------------------------------
# MI SOLUCIÓN: programación dinámica (tabla) + un set para las consultas.
#
# Idea: mejor[c] = la mayor ganancia posible con capacidad c usando los
# paquetes que ya revisé. Reviso los paquetes uno por uno. Para cada
# paquete (peso w, ganancia g) y cada capacidad c (de mayor a menor):
#     mejor[c] = max( mejor[c],  mejor[c - w] + g )
#                    no lo llevo   lo llevo
# Esos subproblemas "mejor ganancia con capacidad c" se repiten muchísimo
# en la fuerza bruta; aquí cada uno se calcula UNA sola vez.
#
# Para saber QUÉ paquetes se eligieron, anoto en una tabla "tomar" si en
# cada paquete y capacidad convenía llevarlo, y al final retrocedo por esa
# tabla desde la capacidad total.
#
# Costos que declaro (n = paquetes, C = capacidad):
#   Elegir            O(n * C) en tiempo y memoria (tabla de decisiones)
#   EstaEnElViaje     O(1) en promedio (un set con los códigos elegidos)
# ---------------------------------------------------------------------
class PlanificadorMejorado:
    def __init__(self):
        self._elegidos = set()        # códigos que van en la furgoneta

    def elegir(self, paquetes, capacidad_kg):
        n = len(paquetes)
        c_max = max(capacidad_kg, 0)
        mejor = [0] * (c_max + 1)                    # mejor[c]: ganancia máxima con capacidad c
        tomar = []                                   # tomar[i][c] = 1 si el paquete i se lleva con capacidad c

        for i in range(n):
            _, w, g = paquetes[i]
            decision = bytearray(c_max + 1)          # todo en 0 (no lo llevo)
            if w <= c_max:                           # si el paquete no cabe, no cambia nada
                for c in range(c_max, w - 1, -1):    # de mayor a menor, para no usar el mismo paquete dos veces
                    con_el_paquete = mejor[c - w] + g
                    if con_el_paquete > mejor[c]:
                        mejor[c] = con_el_paquete
                        decision[c] = 1
            tomar.append(decision)

        # Reconstruyo qué paquetes se eligieron, retrocediendo por la tabla
        elegidos = []
        c = c_max
        for i in range(n - 1, -1, -1):
            if tomar[i][c]:
                elegidos.append(paquetes[i][0])
                c -= paquetes[i][1]

        self._elegidos = set(elegidos)               # para consultar en O(1)
        return mejor[c_max], elegidos

    def esta_en_el_viaje(self, codigo):
        return codigo in self._elegidos              # O(1) en promedio


# ---------------------------------------------------------------------
# Los casos de prueba (todos con óptimo único): (qué, paquetes, capacidad,
# ganancia esperada, códigos esperados).
# ---------------------------------------------------------------------
CASOS = [
    ("el voraz se equivoca", [("P1", 10, 60), ("P2", 20, 100), ("P3", 30, 120)], 50, 220, ["P2", "P3"]),
    ("cuatro paquetes", [("P1", 2, 3), ("P2", 3, 4), ("P3", 4, 5), ("P4", 5, 6)], 8, 10, ["P2", "P4"]),
    ("capacidad cero", [("P1", 5, 10), ("P2", 7, 12)], 0, 0, []),
    ("sin paquetes", [], 30, 0, []),
    ("nada cabe", [("P1", 40, 90), ("P2", 50, 100)], 30, 0, []),
    ("entran todos", [("P1", 5, 10), ("P2", 7, 12), ("P3", 3, 4)], 100, 26, ["P1", "P2", "P3"]),
]


def probar(titulo, fabrica):
    bien = 0
    total = 0
    for que, paquetes, capacidad, esperada, codigos in CASOS:
        plan = fabrica()
        ganancia, elegidos = plan.elegir(paquetes, capacidad)
        total += 1
        if ganancia == esperada and sorted(elegidos) == sorted(codigos):
            bien += 1
        else:
            print(f"   MAL en «{que}»: esperado {esperada} con {codigos}, obtuvo {ganancia} con {elegidos}")
    # Después de elegir, ¿qué paquetes van en el viaje? (primer caso)
    plan = fabrica()
    plan.elegir(CASOS[0][1], CASOS[0][2])
    total += 2
    if plan.esta_en_el_viaje("P2"):
        bien += 1
    else:
        print("   MAL en «esta_en_el_viaje(P2)»: esperado True")
    if not plan.esta_en_el_viaje("P1"):
        bien += 1
    else:
        print("   MAL en «esta_en_el_viaje(P1)»: esperado False")
    print(f"{titulo}: {bien} de {total} pruebas correctas")


if __name__ == "__main__":
    probar("PlanificadorIngenuo ", PlanificadorIngenuo)
    probar("PlanificadorMejorado", PlanificadorMejorado)
