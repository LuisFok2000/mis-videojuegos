"""Entrada del usuario: teclado y raton. Cada evento se traduce en una accion de
juego (acciones.py) o en un cambio de pantalla; no dibuja nada."""
import pygame

import mapa
from mapa import ANCHO
from partida import nueva_partida, reintentar, avanzar, volver_al_menu
import transiciones
import interiores
import interfaz
import sonido
import pantalla
import acciones

DIRECCIONES = {pygame.K_w: (0, -1), pygame.K_UP: (0, -1), pygame.K_s: (0, 1), pygame.K_DOWN: (0, 1),
               pygame.K_a: (-1, 0), pygame.K_LEFT: (-1, 0), pygame.K_d: (1, 0), pygame.K_RIGHT: (1, 0)}


def ejecutar(accion, g):
    """Accion de un boton de pantalla. Devuelve (nueva partida, seguir_ejecutando)."""
    sonido.pitido()                         # retorno de sonido al interactuar
    if accion == 'salir':
        return g, False
    if accion == 'menu':
        sonido.cambiar_ambiente('calle')
        return volver_al_menu(), True
    sonido.cambiar_ambiente('calle')
    return avanzar(g), True                 # comenzar / siguiente / nueva / reintentar


def _usar_puerta(g):
    if transiciones.interactuar(g, sonido.reproducir):
        sonido.cambiar_ambiente(mapa.AMBIENTE)


def _tecla(event, g, running):
    key = event.key
    if key == pygame.K_F11:
        pantalla.alternar_pantalla_completa()
    elif key == pygame.K_m:
        sonido.silenciado = not sonido.silenciado
        sonido.actualizar_volumen()
    elif key == pygame.K_ESCAPE:
        if g['modo'] in ('nivel_completo', 'victoria', 'derrota'):
            g, running = ejecutar('menu', g)
        elif g['modo'] == 'juego':
            sonido.pitido()
            g['modo'] = 'menu'
    elif key == pygame.K_r:
        g = reintentar(g) if g['modo'] == 'juego' else nueva_partida()
        sonido.cambiar_ambiente('calle')
    elif g['modo'] != 'juego' and key in (pygame.K_RETURN, pygame.K_SPACE):
        g, running = ejecutar(interfaz.botones_de(g['modo'], ANCHO, interfaz.BOTONES_Y)[0].accion, g)
    elif g['modo'] == 'juego':
        if key == pygame.K_e:
            _usar_puerta(g)
        elif key in DIRECCIONES:
            dx, dy = DIRECCIONES[key]
            acciones.mover(g, (g['jugador'][0] + dx, g['jugador'][1] + dy))
        elif key == pygame.K_1:
            g['arma'] = 'pistola'
            sonido.pitido()
        elif key == pygame.K_2:
            g['arma'] = 'bate'
            sonido.pitido()
        elif key == pygame.K_h:
            acciones.usar_botiquin(g)
        elif key == pygame.K_SPACE:
            acciones.turno_enemigos(g)
    return g, running


def _clic(event, g, running, hover):
    pos = pantalla.raton_en_lienzo(event.pos)
    if g['modo'] != 'juego':
        accion = interfaz.boton_en(interfaz.botones_de(g['modo'], ANCHO, interfaz.BOTONES_Y), pos)
        if accion:
            g, running = ejecutar(accion, g)
        return g, running
    boton = next((k for k, rect in interfaz.BOTONES_PANEL.items() if rect.collidepoint(pos)), None)
    if boton:
        sonido.pitido()
        if boton in ('pistola', 'bate'):
            g['arma'] = boton
        elif boton == 'botiquin':
            acciones.usar_botiquin(g)
        elif boton == 'turno':
            acciones.turno_enemigos(g)
    elif hover is not None:
        if any(z['pos'] == hover for z in g['enemigos']):
            acciones.atacar(g, hover)
        elif hover == g['jugador'] and (hover in mapa.PUERTAS or
                                       (g['escena'] == 'interior' and hover == interiores.ENTRADA)):
            _usar_puerta(g)
        else:
            acciones.mover(g, hover)
    return g, running


def procesar_eventos(g, hover):
    """Atiende todos los eventos pendientes. Devuelve (partida, seguir_ejecutando)."""
    running = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            g, running = _tecla(event, g, running)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            g, running = _clic(event, g, running, hover)
    return g, running
