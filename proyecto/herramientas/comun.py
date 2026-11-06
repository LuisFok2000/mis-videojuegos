"""Piezas compartidas por los generadores de sprites que usan Pygame
(generar_autos.py y generar_palacio.py).

Importar este modulo inicia Pygame sin ventana y deja la raiz del proyecto en
sys.path, para leer el tamano de baldosa directamente de mapa.py: asi los
sprites generados siempre encajan con la rejilla del juego.
"""
import os
import sys
from pathlib import Path

os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')
import pygame

RAIZ = Path(__file__).resolve().parent.parent
RECURSOS = RAIZ / 'recursos'
sys.path.insert(0, str(RAIZ))
from mapa import TW, TH

pygame.init()
TW2, TH2 = TW // 2, TH // 2      # media baldosa isometrica (38 x 19)


def sombrear(color, k):
    """Oscurece (k < 1) o aclara (k > 1) un color RGB."""
    return tuple(max(0, min(255, int(v * k))) for v in color)
