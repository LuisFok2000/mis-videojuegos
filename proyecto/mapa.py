"""Escena activa del juego (calle o interior) y dimensiones de la pantalla.

Las colisiones y dimensiones activas se publican como variables de modulo, de
modo que combate, jugador, enemigo y la vista usen la misma escena actual.
Los datos de los niveles estan en niveles.py y los de las habitaciones en interiores.py.
"""
import interiores
import niveles
from niveles import NIVELES, casillas_edificios

ANCHO, ALTO = 1280, 850
TW, TH = 76, 38              # ancho y alto de una baldosa isometrica
TAMANO = niveles.TAMANO_CALLE  # lado de la escena activa (12 en la calle, 6 en interiores)
ORIGEN = (ANCHO // 2, 74)


def _activar(**c):
    """Deja una escena (calle o interior) como activa: copia sus datos a las
    variables del modulo que leen los demas modulos (mapa.MUROS, mapa.ENEMIGOS...)."""
    global NOMBRE, MENSAJE, INICIO, SUMINISTROS, REFUGIO, EDIFICIOS, AUTOS
    global ESCOMBROS, ENEMIGOS, BOTIQUINES, CASILLAS_EDIFICIOS, MUROS, CALLES, LINEA, PASTO, DECORACION
    global TAMANO, ORIGEN, PUERTAS, EN_INTERIOR, MUEBLES, TIPO_INTERIOR, AMBIENTE
    NOMBRE, MENSAJE = c['nombre'], c['mensaje']
    INICIO, SUMINISTROS, REFUGIO = c['inicio'], c['suministros'], c['refugio']
    EDIFICIOS, AUTOS, ESCOMBROS = c['edificios'], c['autos'], c['escombros']
    ENEMIGOS, BOTIQUINES, PUERTAS = c['enemigos'], c['botiquines'], c['puertas']
    CALLES, LINEA, PASTO = c['calles'], c['linea'], c['pasto']
    CASILLAS_EDIFICIOS = casillas_edificios(EDIFICIOS)
    DECORACION = c['decoracion']
    MUROS, MUEBLES = c['muros'], c['muebles']
    TAMANO, ORIGEN = c['tamano'], c['origen']
    EN_INTERIOR, TIPO_INTERIOR, AMBIENTE = c['en_interior'], c['tipo_interior'], c['ambiente']


def cargar_nivel(indice):
    """Deja el nivel 'indice' (la calle) como escena activa."""
    n = NIVELES[indice]
    puertas = {puerta: (pos, tipo) for pos, tipo in n['edificios']
               for edif, puerta in n['puertas'] if edif == pos}
    _activar(nombre=n['nombre'], mensaje=n['mensaje'], inicio=n['inicio'],
             suministros=n['suministros'], refugio=n['refugio'], edificios=n['edificios'],
             autos=n['autos'], escombros=n['escombros'], enemigos=n['enemigos'],
             botiquines=n['botiquines'], puertas=puertas, calles=n['calles'],
             linea=n['linea'], pasto=n['pasto'], decoracion=n['decoracion'],
             muros=casillas_edificios(n['edificios']) | {p for p, _ in n['autos']} | set(n['escombros']),
             muebles={}, tamano=niveles.TAMANO_CALLE, origen=(ANCHO // 2, 74),
             en_interior=False, tipo_interior=None, ambiente='calle')


def cargar_interior(indice, edificio):
    """Deja el interior de 'edificio' (en el nivel 'indice') como escena activa."""
    tipos = dict(NIVELES[indice]['edificios'])
    c = interiores.crear(tipos[edificio], indice)
    _activar(nombre=c['nombre'],
             mensaje='E: salir (1 PA) al regresar a la puerta. Busca objetos en estantes.',
             inicio=c['entrada'], suministros=c['suministros'], refugio=None, edificios=[],
             autos=[], escombros=[], enemigos=c['enemigos'], botiquines=c['botiquines'], puertas={},
             calles=((-1, -1), (-1, -1)), linea=(-1, -1), pasto=((90, 80, 66), (90, 80, 66)), decoracion=[],
             muros=c['muros'], muebles=c['muebles'], tamano=interiores.TAMANO, origen=(ANCHO // 2, 166),
             en_interior=True, tipo_interior=c['tipo'], ambiente=c['ambiente'])
    return c


cargar_nivel(0)
