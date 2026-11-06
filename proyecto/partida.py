"""Estado de una partida y flujo entre niveles (nueva, reintentar, siguiente)."""
import mapa
import jugador
import enemigo
import efectos
import interiores

def nueva_partida(nivel=0, previo=None):
    """Crea el estado de un nivel. 'previo' arrastra vida, balas y botiquines
    del nivel anterior; sin el, se empieza con los atributos iniciales."""
    mapa.cargar_nivel(nivel)
    atributos = previo or jugador.atributos_iniciales()
    g = jugador.crear(atributos)
    g.update(efectos.estado_visual())
    salas = {}
    for pos, tipo in mapa.EDIFICIOS:
        datos = interiores.crear(tipo, nivel)
        salas[pos] = {'enemigos': enemigo.crear_enemigos(datos['enemigos']),
                      'botiquines_suelo': set(datos['botiquines']), 'municion': set(datos['municion'])}
    g.update({'enemigos': enemigo.crear_enemigos(mapa.ENEMIGOS), 'botiquines_suelo': set(mapa.BOTIQUINES),
              'municion': set(), 'escena': 'calle', 'salas': salas, 'afuera': None, 'edificio_actual': None,
              'mensaje': mapa.MENSAJE, 'turno': 1, 'modo': 'juego',
              'nivel': nivel, 'entrada': dict(atributos)})
    return g

def volver_al_menu():
    """Partida nueva detenida en la pantalla del menu principal."""
    efectos.limpiar()
    g = nueva_partida()
    g['modo'] = 'menu'
    return g

def reintentar(g):
    """Vuelve a empezar el nivel actual con lo que traia el jugador al entrar."""
    return nueva_partida(g['nivel'], g['entrada'])

def siguiente_nivel(g):
    """Pasa al nivel siguiente conservando vida, balas y botiquines (con bonus)."""
    return nueva_partida(g['nivel'] + 1, jugador.atributos_para_siguiente_nivel(g))

def avanzar(g):
    """ENTER o clic en una pantalla que no es de juego."""
    efectos.limpiar()
    if g['modo'] == 'nivel_completo':
        return siguiente_nivel(g)
    if g['modo'] == 'derrota':
        return reintentar(g)
    return nueva_partida()
