"""Cambios entre exterior e interior, conservando los recursos de cada escena."""
import mapa
import interiores


def interactuar(g, reproducir=None):
    """E consume 1 PA, solamente cuando se esta parado sobre una puerta.
    No se avanza el turno enemigo al cambiar de escena.
    """
    if g['pa'] < 1:
        g['mensaje'] = 'Necesitas 1 PA para usar la puerta.'
        return False
    if g['escena'] == 'calle':
        puerta = mapa.PUERTAS.get(g['jugador'])
        if puerta is None:
            g['mensaje'] = 'Parate en la casilla turquesa PUERTA y pulsa E.'
            return False
        edificio, tipo = puerta
        g['afuera'] = {'jugador': g['jugador'], 'enemigos': g['enemigos'],
                       'botiquines_suelo': g['botiquines_suelo'], 'municion': g['municion']}
        g['edificio_actual'] = edificio
        sala = g['salas'][edificio]
        datos = mapa.cargar_interior(g['nivel'], edificio)
        g['escena'] = 'interior'
        g['jugador'] = interiores.ENTRADA
        g['enemigos'], g['botiquines_suelo'], g['municion'] = sala['enemigos'], sala['botiquines_suelo'], sala['municion']
        g['pa'] -= 1
        g['mensaje'] = f'Entraste a {datos["nombre"]}. E desde la salida para volver (-1 PA).'
    else:
        if g['jugador'] != interiores.ENTRADA:
            g['mensaje'] = 'Regresa a la casilla SALIDA y pulsa E.'
            return False
        afuera = g['afuera']
        if afuera is None:
            raise RuntimeError('No hay escenario exterior para restaurar')
        g['salas'][g['edificio_actual']].update({
            'enemigos': g['enemigos'], 'botiquines_suelo': g['botiquines_suelo'], 'municion': g['municion']})
        mapa.cargar_nivel(g['nivel'])
        g['escena'] = 'calle'
        g['jugador'], g['enemigos'] = afuera['jugador'], afuera['enemigos']
        g['botiquines_suelo'], g['municion'] = afuera['botiquines_suelo'], afuera['municion']
        g['afuera'] = None
        g['edificio_actual'] = None
        g['pa'] -= 1
        g['mensaje'] = 'Volviste a la calle. Los recursos recogidos no reaparecen.'
    if reproducir:
        reproducir('puerta')
    return True


def enemigos_pendientes(g):
    """Solo cuentan enemigos de la escena exterior y el JEFE obligatorio.

    Los zombis de interiores opcionales son desafios con recompensas, no
    bloquean la salida del nivel si el jugador no explora ese edificio.
    """
    calle = g['enemigos'] if g['escena'] == 'calle' else g['afuera']['enemigos']
    total = len(calle)
    if g['nivel'] == 2:
        for sala in g['salas'].values():
            total += sum(z['tipo'] == 'jefe' for z in sala['enemigos'])
    return total
