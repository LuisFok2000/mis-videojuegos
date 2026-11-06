"""Minimapas interiores 6x6. Datos puros, independientes del motor grafico.

Se crean por edificio y se conservan al salir: los recursos no reaparecen.
Cada edificio tiene una puerta exterior y otra interior en (2, 5).
"""

from collections import deque

TAMANO = 6
ENTRADA = (2, 5)
NOMBRES = {0: 'FARMASHOP', 1: 'ALMACEN', 2: 'PANADERIA', 3: 'CASA', 4: 'PALACIO LEGISLATIVO'}
# Muebles solidos con variantes visuales; ninguno puede ocupar la puerta.
MUEBLES = {
    0: {(1, 2): 'estante', (4, 2): 'estante', (1, 3): 'estante', (4, 3): 'estante'},
    1: {(1, 1): 'mostrador', (4, 1): 'estante', (1, 3): 'estante'},
    2: {(1, 2): 'mostrador', (4, 2): 'estante', (2, 1): 'horno'},
    3: {(1, 3): 'mesa', (4, 3): 'armario', (4, 1): 'armario'},
    4: {(1, 1): 'columna', (0, 3): 'columna', (5, 3): 'columna', (4, 3): 'columna'},
}


def crear(tipo, nivel):
    """Contenido determinista; la farmacia del nivel 2 y el Palacio del 3
    guardan suministros obligatorios. El Palacio tiene el jefe final.
    """
    contenido = {
        0: {'botiquines': {(3, 4)}, 'municion': {(2, 1)}, 'enemigos': [((3, 2), 'comun')]},
        1: {'botiquines': {(4, 4)}, 'municion': {(2, 2)}, 'enemigos': []},
        2: {'botiquines': {(4, 4)}, 'municion': {(3, 1)}, 'enemigos': [((3, 3), 'corredor')]},
        3: {'botiquines': {(3, 3)}, 'municion': {(2, 2)}, 'enemigos': []},
        4: {'botiquines': {(4, 4)}, 'municion': {(2, 3)}, 'enemigos': [((3, 1), 'jefe')]},
    }[tipo]
    # Ajustes por nivel para que el primer nivel no exija explorar interiores.
    spawns = contenido['enemigos'] if nivel > 0 else []
    suministros = (4, 1) if (nivel, tipo) in ((1, 0), (2, 4)) else None
    return {'tipo': tipo, 'nombre': NOMBRES[tipo], 'entrada': ENTRADA,
            'muebles': dict(MUEBLES[tipo]), 'muros': set(MUEBLES[tipo]),
            'botiquines': set(contenido['botiquines']), 'municion': set(contenido['municion']),
            'enemigos': list(spawns), 'suministros': suministros,
            'ambiente': 'palacio' if tipo == 4 else 'interior'}


def validar(contenido):
    """Valida acceso a botiquines, balas, zombis, suministros y salida."""
    muros = contenido['muros']
    posibles = set(contenido['botiquines']) | set(contenido['municion'])
    posibles |= {p for p, _ in contenido['enemigos']}
    if contenido['suministros'] is not None:
        posibles.add(contenido['suministros'])
    assert not (posibles & muros), 'Objeto interior dentro de mueble'
    assert all(0 <= x < TAMANO and 0 <= y < TAMANO for x, y in muros | posibles | {ENTRADA})
    cola, vistos = deque([ENTRADA]), {ENTRADA}
    while cola:
        x, y = cola.popleft()
        for p in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
            if all(0 <= v < TAMANO for v in p) and p not in muros and p not in vistos:
                vistos.add(p)
                cola.append(p)
    assert posibles <= vistos, 'Objetos del interior inaccesibles'
    posiciones = [pos for pos, _ in contenido['enemigos']]
    assert len(set(posiciones)) == len(posiciones), 'Dos enemigos en la misma casilla'
