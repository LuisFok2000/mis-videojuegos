"""Tipos de zombis, atributos y acciones de la IA por turnos."""
import random
from collections import deque
from jugador import recibir_danio, iniciar_turno, vecinos
from combate import distancia, linea_libre

# Reglas de cada tipo (el aspecto visual esta en escenario.ASPECTO_ENEMIGO).
# armadura: True si empieza con armadura (las balas no le hacen dano hasta romperla con el bate).
TIPOS = {
    'comun': {'nombre': 'Comun', 'vida': 6, 'pasos': 2, 'rango': 1, 'danio': 2, 'armadura': False},
    'corredor': {'nombre': 'Corredor', 'vida': 4, 'pasos': 3, 'rango': 1, 'danio': 2, 'armadura': False},
    'blindado': {'nombre': 'Blindado', 'vida': 9, 'pasos': 1, 'rango': 1, 'danio': 3, 'armadura': True},
    'escupidor': {'nombre': 'Escupidor', 'vida': 5, 'pasos': 1, 'rango': 3, 'danio': 2, 'armadura': False},
    'jefe': {'nombre': 'Jefe', 'vida': 15, 'pasos': 3, 'rango': 1, 'danio': 5, 'armadura': False},
}


def paso_hacia(start, goal, occupied):
    """BFS: primer paso de un camino corto evitando paredes y otros zombis."""
    queue = deque([start])
    previous = {start: None}
    while queue:
        celda = queue.popleft()
        if celda == goal:
            break
        for nxt in vecinos(celda):
            if nxt not in previous and (nxt not in occupied or nxt == goal):
                previous[nxt] = celda
                queue.append(nxt)
    if goal not in previous:
        return None
    celda = goal
    while previous[celda] is not None and previous[celda] != start:
        celda = previous[celda]
    return celda if celda != goal or distancia(start, goal) == 1 else goal


def crear_enemigos(spawns):
    """spawns: lista de ((x, y), tipo)."""
    zombies = []
    for pos, tipo in spawns:
        if tipo not in TIPOS:
            raise ValueError(f'Tipo de zombi desconocido: {tipo}')
        config = TIPOS[tipo]
        zombies.append({'pos': tuple(pos), 'tipo': tipo, 'vida': config['vida'],
                        'vida_max': config['vida'], 'armadura': config['armadura']})
    return zombies


def puede_atacar(z, objetivo):
    """La escupida requiere alcance y trayectoria libre de obstaculos."""
    tipo = TIPOS[z['tipo']]
    separacion = distancia(z['pos'], objetivo)
    if z['tipo'] == 'escupidor':
        return 1 <= separacion <= tipo['rango'] and linea_libre(z['pos'], objetivo)
    return separacion == 1


def turno_enemigos(g, reproducir, particulas, numero_flotante):
    """Cada enemigo se mueve segun su tipo y puede atacar UNA vez por turno."""
    golpes = 0
    mensajes = []
    for z in list(g['enemigos']):
        config = TIPOS[z['tipo']]
        for paso_n in range(config['pasos'] + 1):
            if puede_atacar(z, g['jugador']):
                recibir_danio(g, config['danio'])
                color = (175, 84, 217) if z['tipo'] == 'escupidor' else (182, 43, 45)
                particulas(g['jugador'], color, 16)
                numero_flotante(g['jugador'], f'-{config["danio"]}', (255, 102, 96))
                reproducir('escupitajo' if z['tipo'] == 'escupidor' else 'herida')
                golpes += 1
                if z['tipo'] == 'escupidor':
                    mensajes.append('Escupidor: ataque a distancia!')
                break
            if paso_n == config['pasos']:
                break
            bloqueados = {other['pos'] for other in g['enemigos'] if other is not z}
            paso = paso_hacia(z['pos'], g['jugador'], bloqueados)
            if paso is None or paso == g['jugador'] or paso in bloqueados:
                break
            z['pos'] = paso
            if random.random() < .12:
                reproducir('zombi')
        if g['vida'] <= 0:
            g['modo'] = 'derrota'
            break
    if g['modo'] == 'juego':
        iniciar_turno(g)
        if mensajes:
            g['mensaje'] = ' '.join(mensajes) + ' Tu turno.'
        elif golpes:
            g['mensaje'] = f'Los zombis atacaron {golpes} vez/veces. Tu turno.'
        else:
            g['mensaje'] = 'Los zombis avanzaron. Tu turno.'
