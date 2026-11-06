"""El superviviente: atributos, movimiento, curacion y progreso entre niveles."""
import mapa
import transiciones

VIDA_MAXIMA = 12                 # vida maxima
PA_POR_TURNO = 4            # puntos de accion que se recuperan cada turno
BALAS_INICIALES = 12
BOTIQUINES_INICIALES = 1
CURACION_BOTIQUIN = 5       # PV que recupera un botiquin
BONUS_PV_NIVEL = 4          # PV extra al pasar de nivel (sin pasar de VIDA_MAXIMA)
BONUS_BALAS_NIVEL = 6       # balas extra al pasar de nivel

def vecinos(celda):
    x, y = celda
    for nxt in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
        if 0 <= nxt[0] < mapa.TAMANO and 0 <= nxt[1] < mapa.TAMANO and nxt not in mapa.MUROS:
            yield nxt


def atributos_iniciales():
    """Lo que el jugador trae al empezar una partida nueva."""
    return {'vida': VIDA_MAXIMA, 'balas': BALAS_INICIALES, 'botiquines': BOTIQUINES_INICIALES}

def atributos_para_siguiente_nivel(g):
    """Lo que se conserva (y se bonifica) al completar un nivel."""
    return {'vida': min(VIDA_MAXIMA, g['vida'] + BONUS_PV_NIVEL),
            'balas': g['balas'] + BONUS_BALAS_NIVEL, 'botiquines': g['botiquines']}

def crear(atributos):
    """Campos del estado de la partida que pertenecen al jugador."""
    return {'jugador': mapa.INICIO, 'vida': atributos['vida'], 'pa': PA_POR_TURNO,
            'balas': atributos['balas'], 'botiquines': atributos['botiquines'],
            'suministros': False, 'arma': 'pistola'}

def iniciar_turno(g):
    """Nuevo turno del jugador: recupera los PA y avanza el contador."""
    g['pa'] = PA_POR_TURNO
    g['turno'] += 1

def recibir_danio(g, cantidad):
    g['vida'] -= cantidad
    g['herido'] = 15

def mover(g, destino, reproducir, particulas):
    if g['pa'] < 1:
        g['mensaje'] = 'Sin PA: pulsa ESPACIO para terminar turno.'
        return
    occupied = {z['pos'] for z in g['enemigos']}
    if destino not in vecinos(g['jugador']) or destino in occupied:
        g['mensaje'] = 'Solo podes moverte a una casilla vecina libre.'
        return
    g['jugador'] = destino
    reproducir('paso')
    g['pa'] -= 1
    if mapa.SUMINISTROS is not None and destino == mapa.SUMINISTROS and not g['suministros']:
        g['suministros'] = True
        reproducir('recoger')
        particulas(destino,(241,201,88),16)
        g['mensaje'] = ('Suministros recogidos. Elimina a los zombis y vuelve al refugio.'
                        if transiciones.enemigos_pendientes(g) else 'Suministros recogidos. Vuelve al refugio.')
    if mapa.REFUGIO is not None and destino == mapa.REFUGIO:
        if g['suministros'] and transiciones.enemigos_pendientes(g) == 0:
            # Si quedan niveles, se pasa al siguiente; si no, victoria final.
            g['modo'] = 'nivel_completo' if g['nivel'] + 1 < len(mapa.NIVELES) else 'victoria'
            g['mensaje'] = 'Llegaste al refugio con los suministros.'
        elif not g['suministros']:
            g['mensaje'] = 'Primero debes recoger los suministros.'
        else:
            g['mensaje'] = 'Aun hay zombis de la mision (o el jefe) por eliminar.'
    if destino in g.get('municion', set()):
        g['municion'].remove(destino)
        g['balas'] += 5
        reproducir('recoger')
        particulas(destino, (243, 202, 92), 12)
        g['mensaje'] = 'Encontraste municion: +5 balas.'
    if destino in g['botiquines_suelo']:
        g['botiquines_suelo'].remove(destino)
        g['botiquines'] += 1
        reproducir('recoger')
        particulas(destino,(224,237,222),12)
        g['mensaje'] = 'Recogiste un botiquin (+1).'
    elif destino not in (mapa.SUMINISTROS, mapa.REFUGIO):
        g['mensaje'] = 'Te moviste (-1 PA).'

def usar_botiquin(g, reproducir, numero_flotante):
    if g['botiquines'] < 1 or g['pa'] < 1 or g['vida'] == VIDA_MAXIMA:
        g['mensaje'] = 'Necesitas botiquin, 1 PA y vida por recuperar.'
        return
    g['botiquines'] -= 1
    g['pa'] -= 1
    g['vida'] = min(VIDA_MAXIMA, g['vida'] + CURACION_BOTIQUIN)
    reproducir('recoger')
    numero_flotante(g['jugador'], f'+{CURACION_BOTIQUIN}', (122,242,144))
    g['mensaje'] = f'Usaste un botiquin: +{CURACION_BOTIQUIN} PV (maximo {VIDA_MAXIMA}).'

