# MARIA SOLEDAD INTA LARICO 
# =====================================================================
# Parcial 2 - Variante B: Pedidos de una pastelería
#
# Caso: los pedidos llegan con un plazo en minutos. Se prepara primero el
# de menor plazo; si dos tienen el mismo plazo, primero el que llegó antes.
#
# Aquí porto el código de C# a Python y escribo mi solución mejorada.
#   - ReceptorIngenuo: lista simple (correcta pero lenta), la del enunciado.
#   - ReceptorMejorado: MI solución, con un heap y un set.
# =====================================================================

import heapq   # módulo de Python que implementa el heap (cola de prioridad)


# ---------------------------------------------------------------------
# SOLUCIÓN INGENUA (lista simple): correcta pero lenta.
# Guarda los pedidos en una lista como tuplas (nombre, plazo, llegada).
#   - preparar_siguiente: recorre TODA la lista para hallar el menor, O(n),
#     y luego lo borra de la lista (correr los demás), otro O(n).
#   - esta_pendiente: recorre toda la lista, O(n).
# ---------------------------------------------------------------------
class ReceptorIngenuo:
    def __init__(self):
        self._lista = []        # tuplas (nombre, plazo, llegada)
        self._llegadas = 0      # cuenta cuántos pedidos han llegado

    def registrar(self, pedido, plazo_minutos):
        self._lista.append((pedido, plazo_minutos, self._llegadas))
        self._llegadas += 1

    def preparar_siguiente(self):
        if not self._lista:
            return None
        mejor = 0
        for i in range(1, len(self._lista)):
            p = self._lista[i]
            m = self._lista[mejor]
            # p[1] es el plazo y p[2] la llegada
            if p[1] < m[1] or (p[1] == m[1] and p[2] < m[2]):
                mejor = i
        nombre = self._lista[mejor][0]
        del self._lista[mejor]
        return nombre

    def esta_pendiente(self, pedido):
        for p in self._lista:
            if p[0] == pedido:
                return True
        return False

    @property
    def pendientes(self):
        return len(self._lista)


# ---------------------------------------------------------------------
# MI SOLUCIÓN: heap + set.
#   - El HEAP guarda tuplas (plazo, llegada, nombre). El heap siempre deja
#     el MENOR arriba, y Python compara las tuplas campo por campo: primero
#     el plazo y, si empatan, la llegada. Así el DESEMPATE sale solo: con
#     el mismo plazo sale primero el que llegó antes (llegada menor).
#     El nombre nunca se compara porque la llegada es única.
#   - El SET guarda los nombres de los pedidos que siguen pendientes, para
#     responder "¿sigue pendiente?" sin recorrer nada.
#
# Costos que declaro (n = pedidos pendientes):
#   registrar            O(log n)   heappush + agregar al set O(1)
#   preparar_siguiente   O(log n)   heappop + quitar del set O(1)
#   esta_pendiente       O(1)       buscar en el set (promedio)
#   pendientes           O(1)       el tamaño del set
# ---------------------------------------------------------------------
class ReceptorMejorado:
    def __init__(self):
        self._heap = []             # (plazo, llegada, nombre)
        self._pendientes = set()    # nombres que siguen pendientes
        self._llegadas = 0          # número de llegada para el desempate

    def registrar(self, pedido, plazo_minutos):
        heapq.heappush(self._heap, (plazo_minutos, self._llegadas, pedido))  # O(log n)
        self._pendientes.add(pedido)                                         # O(1)
        self._llegadas += 1

    def preparar_siguiente(self):
        if not self._heap:
            return None
        plazo, llegada, nombre = heapq.heappop(self._heap)   # saca el menor: O(log n)
        self._pendientes.discard(nombre)                     # O(1)
        return nombre

    def esta_pendiente(self, pedido):
        return pedido in self._pendientes                    # O(1) en promedio

    @property
    def pendientes(self):
        return len(self._pendientes)                         # O(1)


# ---------------------------------------------------------------------
# El guion de pruebas: cada paso es (operación, argumento, plazo, esperado).
# Es el mismo del enunciado. Incluye el desempate: Torta y Pan tienen
# plazo 120 y debe salir primero Torta (llegó antes); Galletas y Alfajor
# tienen plazo 30.
# ---------------------------------------------------------------------
GUION = [
    ("registrar", "Torta", 120, ""), ("registrar", "Galletas", 30, ""),
    ("registrar", "Pan", 120, ""), ("registrar", "Brazo", 60, ""),
    ("pendientes", "", 0, "4"),
    ("esta", "Galletas", 0, "True"), ("esta", "Flan", 0, "False"),
    ("preparar", "", 0, "Galletas"), ("esta", "Galletas", 0, "False"),
    ("preparar", "", 0, "Brazo"),
    ("registrar", "Alfajor", 30, ""),
    ("preparar", "", 0, "Alfajor"), ("preparar", "", 0, "Torta"),
    ("preparar", "", 0, "Pan"),
    ("preparar", "", 0, "(ninguno)"), ("pendientes", "", 0, "0"),
]


def ejecutar(receptor, op, arg, plazo):
    if op == "registrar":
        receptor.registrar(arg, plazo)
        return ""
    if op == "preparar":
        resultado = receptor.preparar_siguiente()
        return "(ninguno)" if resultado is None else resultado
    if op == "esta":
        return str(receptor.esta_pendiente(arg))
    return str(receptor.pendientes)


def probar(titulo, receptor):
    bien = 0
    total = 0
    for op, arg, plazo, esperado in GUION:
        obtenido = ejecutar(receptor, op, arg, plazo)
        if op == "registrar":
            continue
        total += 1
        if obtenido == esperado:
            bien += 1
        else:
            print(f"   MAL en «{op} {arg}»: esperado {esperado}, obtuvo {obtenido}")
    print(f"{titulo}: {bien} de {total} pasos correctos")


if __name__ == "__main__":
    probar("ReceptorIngenuo ", ReceptorIngenuo())
    probar("ReceptorMejorado", ReceptorMejorado())
