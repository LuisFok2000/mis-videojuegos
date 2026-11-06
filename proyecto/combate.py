"""Reglas de ataque, alcance y bloqueo de linea de vision."""
import mapa
import transiciones

COSTO_ATAQUE_PA = 2


def distancia(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# Cada arma: alcance en casillas, dano, si es a distancia (necesita municion y
# linea de tiro libre), y la animacion que dispara en el estado de la partida.
ARMAS = {
    'pistola': {'alcance': 4, 'danio': 4, 'a_distancia': True, 'efecto': 'fogonazo'},
    'bate':    {'alcance': 1, 'danio': 3, 'a_distancia': False, 'efecto': 'golpe'},
}

def alcance(arma):
    return ARMAS[arma]['alcance']

def tiro_valido(arma, origen, destino):
    """El bate golpea siempre; la pistola necesita que ningun obstaculo bloquee el tiro."""
    return not ARMAS[arma]['a_distancia'] or linea_libre(origen, destino)

def linea_libre(start, end):
    """Supercover: recorre la linea entre centros de casillas; una caja bloquea."""
    x0, y0 = start[0] + .5, start[1] + .5
    x1, y1 = end[0] + .5, end[1] + .5
    steps = max(1, int(max(abs(x1-x0), abs(y1-y0))*24))
    for i in range(1, steps):
        t = i / steps
        x, y = x0+(x1-x0)*t, y0+(y1-y0)*t
        if (int(x), int(y)) in mapa.MUROS:
            return False
        # Una bala que cruza justo la esquina de dos cajas tampoco pasa.
        if abs(x-round(x)) < .018 and abs(y-round(y)) < .018:
            a, b = int(x), int(y)
            if (a-1,b) in mapa.MUROS and (a,b-1) in mapa.MUROS:
                return False
    return True

def atacar(g, destino, reproducir, particulas, numero_flotante):
    if g['pa'] < COSTO_ATAQUE_PA:
        g['mensaje'] = f'Atacar cuesta {COSTO_ATAQUE_PA} PA.'
        return
    z = next((z for z in g['enemigos'] if z['pos'] == destino), None)
    if z is None:
        g['mensaje'] = 'Selecciona un zombi haciendo clic sobre el.'
        return
    arma = ARMAS[g['arma']]
    if distancia(g['jugador'], destino) > arma['alcance']:
        g['mensaje'] = 'Enemigo fuera de alcance.'
        return
    if arma['a_distancia'] and not linea_libre(g['jugador'], destino):
        g['mensaje'] = 'Disparo bloqueado por obstaculos: cambia de posicion.'
        return
    if arma['a_distancia'] and g['balas'] <= 0:
        g['mensaje'] = 'Sin municion. Cambia al bate con tecla 2.'
        return
    g['pa'] -= COSTO_ATAQUE_PA
    if arma['a_distancia']:
        g['balas'] -= 1
    tipo = z.get('tipo', 'comun')
    if z['armadura']:
        if g['arma'] == 'pistola':
            reproducir('pistola')
            g['fogonazo'] = 10
            particulas(destino, (112, 181, 213), 10)
            numero_flotante(destino, 'BLOQUEADO', (149, 224, 252))
            g['mensaje'] = 'La armadura detiene las balas. Rompela con el BATE!'
            return
        z['armadura'] = False
        reproducir('bate')
        g['golpe'] = 10
        particulas(destino, (112, 181, 213), 20)
        numero_flotante(destino, 'ARMADURA ROTA', (150, 231, 250))
        g['destello'] = (destino, 12)
        g['mensaje'] = 'Armadura destruida! Ahora la pistola puede herirlo.'
        return
    damage = arma['danio']
    z['vida'] -= damage
    reproducir(g['arma'])
    g[arma['efecto']] = 10
    particulas(destino, (175,43,48), 17)
    numero_flotante(destino, f'-{damage}', (255,188,146))
    g['destello'] = (destino, 12)
    if z['vida'] <= 0:
        g['enemigos'].remove(z)
        g['mensaje'] = f'Eliminaste un {tipo}!'
        if not g['enemigos']:
            if g.get('escena') == 'interior':
                g['mensaje'] = 'Interior despejado! Revisa los recursos y vuelve a la salida.'
            elif transiciones.enemigos_pendientes(g):
                g['mensaje'] = 'Exterior despejado. Todavia falta derrotar al jefe del Palacio.'
            else:
                g['mensaje'] = ('Zona despejada. Vuelve al refugio.' if g['suministros']
                                else 'Zona despejada. Recoge los suministros y vuelve al refugio.')
    else:
        g['mensaje'] = f'Impacto! {tipo.capitalize()} con {z["vida"]} PV.'
