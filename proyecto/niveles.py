"""Datos de los niveles de calle y su validacion. Sin dependencias graficas.

Los sprites de edificios, autos y carteles se generan con herramientas/generar_*.py.
"""
from collections import deque

import interiores

TAMANO_CALLE = 12

# Cada edificio tiene una puerta transitable fuera de su huella 2x2.
NIVELES = [
    {
        'nombre': 'BARRIO INFECTADO',
        'mensaje': 'Barrio: derrota a los zombis, recoge suministros y busca refugio. E: entrar.',
        'inicio': (0, 5), 'suministros': (3, 8), 'refugio': (11, 11),
        'edificios': [((2, 1), 0), ((8, 1), 2), ((1, 10), 3)],
        'puertas': [((2, 1), (3, 3)), ((8, 1), (9, 3)), ((1, 10), (3, 11))],
        'autos': [((4, 4), 3), ((7, 7), 1), ((9, 6), 2)],
        'escombros': [(3, 6), (5, 8), (8, 8)],
        'enemigos': [((8, 5), 'comun'), ((6, 9), 'corredor'), ((10, 3), 'comun')],
        'botiquines': {(2, 6), (8, 9)},
        'calles': ((4, 6), (4, 6)), 'linea': (5, 5),
        'pasto': ((75, 92, 76), (70, 87, 71)),
        # Decoracion puramente visual: no bloquea caminos ni puertas.
        'decoracion': [((0, 1), 'cartel_1'), ((11, 2), 'cartel_0'), ((0, 3), 'contenedor'), ((8, 11), 'contenedor')],
    },
    {
        'nombre': 'AVENIDA BLOQUEADA',
        'mensaje': 'Los suministros estan DENTRO de Farmashop. Busca la puerta y pulsa E.',
        'inicio': (0, 6), 'suministros': None, 'refugio': (11, 6),
        'edificios': [((1, 1), 1), ((5, 2), 0), ((10, 1), 3), ((1, 10), 2)],
        'puertas': [((1, 1), (2, 3)), ((5, 2), (5, 4)), ((10, 1), (9, 2)), ((1, 10), (3, 11))],
        'autos': [((4, 5), 1), ((6, 6), 0), ((9, 8), 5)],
        'escombros': [(2, 5), (8, 3), (9, 4), (8, 10), (6, 8)],
        'enemigos': [((8, 2), 'escupidor'), ((6, 4), 'comun'), ((10, 6), 'blindado'),
                   ((9, 9), 'corredor'), ((4, 7), 'comun')],
        'botiquines': {(2, 7), (7, 4)},
        'calles': ((5, 6), (8, 9)), 'linea': (5, 8),
        'pasto': ((92, 86, 66), (86, 80, 62)),
        # Decoracion puramente visual: no bloquea caminos ni puertas.
        'decoracion': [((0, 0), 'cartel_2'), ((11, 10), 'cartel_0'), ((0, 5), 'contenedor'), ((9, 11), 'contenedor')],
    },
    {
        'nombre': 'PALACIO LEGISLATIVO',
        'mensaje': 'Mision final: suministros en el Palacio. Derrota al JEFE y vuelve al refugio.',
        'inicio': (0, 6), 'suministros': None, 'refugio': (11, 11),
        'edificios': [((4, 1), 4), ((1, 1), 1), ((9, 1), 0), ((1, 9), 2)],
        'puertas': [((4, 1), (5, 3)), ((1, 1), (2, 3)), ((9, 1), (10, 3)), ((1, 9), (3, 10))],
        'autos': [((4, 5), 1), ((7, 7), 3), ((9, 5), 2)],
        'escombros': [(3, 6), (6, 6), (8, 4), (8, 9)],
        'enemigos': [((7, 3), 'escupidor'), ((6, 9), 'corredor'), ((10, 8), 'blindado')],
        'botiquines': {(2, 7), (8, 10)},
        'calles': ((5, 7), (5, 7)), 'linea': (6, 6),
        'pasto': ((82, 94, 79), (70, 84, 70)),
        # Decoracion puramente visual: no bloquea caminos ni puertas.
        'decoracion': [((0, 0), 'cartel_2'), ((11, 0), 'cartel_1'), ((0, 4), 'contenedor'), ((7, 11), 'contenedor')],
    },
]


def casillas_edificios(edificios):
    """Casillas que ocupa cada edificio (huella de 2x2)."""
    return {(col + dc, fila + df) for (col, fila), _ in edificios
            for dc in (0, 1) for df in (0, 1)}


def _alcanzable(inicio, destino, muros, tamano=TAMANO_CALLE):
    vistos, cola = {inicio}, deque([inicio])
    while cola:
        x, y = cola.popleft()
        if (x, y) == destino:
            return True
        for p in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= p[0] < tamano and 0 <= p[1] < tamano and p not in muros and p not in vistos:
                vistos.add(p)
                cola.append(p)
    return False


def validar(nivel):
    """Comprueba que el nivel es jugable: nada solapado y todo alcanzable."""
    edif = casillas_edificios(nivel['edificios'])
    muros = edif | {p for p, _ in nivel['autos']} | set(nivel['escombros'])
    enemigos = {pos for pos, _ in nivel['enemigos']}
    libres = enemigos | set(nivel['botiquines']) | {nivel['inicio'], nivel['refugio']}
    if nivel['suministros'] is not None:
        libres.add(nivel['suministros'])
    puertas = dict(nivel['puertas'])
    assert len(puertas) == len(nivel['edificios'])
    assert set(puertas) == {pos for pos, _ in nivel['edificios']}
    assert len(set(puertas.values())) == len(puertas)
    assert not (set(puertas.values()) & libres), f"Puerta ocupada en {nivel['nombre']}"
    libres |= set(puertas.values())
    assert all(0 <= c < TAMANO_CALLE and 0 <= f < TAMANO_CALLE for c, f in muros | libres), nivel['nombre']
    assert not muros & libres, f"Objeto sobre obstaculo: {nivel['nombre']}"
    assert len(edif) == 4 * len(nivel['edificios']), f"Edificios superpuestos: {nivel['nombre']}"
    assert len(muros) == len(edif) + len(nivel['autos']) + len(nivel['escombros'])
    assert len(enemigos) == len(nivel['enemigos'])
    decoracion = {celda for celda, _ in nivel['decoracion']}
    assert not decoracion & (muros | libres), f"Decoracion sobre un objeto: {nivel['nombre']}"
    for pos, puerta in nivel['puertas']:
        px, py = pos
        assert puerta in {(px, py + 2), (px + 1, py + 2), (px + 2, py), (px + 2, py + 1),
                          (px - 1, py), (px - 1, py + 1), (px, py - 1), (px + 1, py - 1)}, f"Puerta separada: {pos}"
    for destino in libres:
        assert _alcanzable(nivel['inicio'], destino, muros), f"Inalcanzable {destino}: {nivel['nombre']}"
    if nivel['suministros'] is not None:
        assert _alcanzable(nivel['suministros'], nivel['refugio'], muros)


def validar_todos():
    """Valida los niveles de calle y todos los interiores posibles. Se llama al
    iniciar el juego y desde las pruebas (ya no se ejecuta al importar)."""
    for indice, nivel in enumerate(NIVELES):
        validar(nivel)
        for _, tipo in nivel['edificios']:
            interiores.validar(interiores.crear(tipo, indice))
    for tipo in interiores.NOMBRES:
        for indice in range(len(NIVELES)):
            interiores.validar(interiores.crear(tipo, indice))
