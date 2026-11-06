"""Acciones del jugador y de los enemigos: conectan las reglas del juego con el
sonido y los efectos visuales (particulas y numeros de dano)."""
from functools import partial

import pygame

import efectos
import sonido
from combate import atacar as _atacar
from enemigo import turno_enemigos as _turno_enemigos
from jugador import mover as _mover, usar_botiquin as _usar_botiquin
from pantalla import vertice_superior

# Las reglas piden efectos como funciones simples (celda, color...): se les fija
# aqui como convertir una casilla en pixeles.
particulas = partial(efectos.particulas, vertice=vertice_superior)
numero_flotante = partial(efectos.numero_flotante, vertice=vertice_superior)


def mover(g, destino):
    antes = g['jugador']
    _mover(g, destino, sonido.reproducir, particulas)
    if g['jugador'] != antes:
        g['caminar_hasta'] = pygame.time.get_ticks() + 330


def usar_botiquin(g):
    _usar_botiquin(g, sonido.reproducir, numero_flotante)


def turno_enemigos(g):
    antes = {id(z): z['pos'] for z in g['enemigos']}
    _turno_enemigos(g, sonido.reproducir, particulas, numero_flotante)
    for z in g['enemigos']:
        if antes.get(id(z)) != z['pos']:
            z['caminar_hasta'] = pygame.time.get_ticks() + 320


def atacar(g, destino):
    _atacar(g, destino, sonido.reproducir, particulas, numero_flotante)
