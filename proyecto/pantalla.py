"""Ventana, lienzo fijo y utilidades de dibujo compartidas por todo el juego.

Se dibuja siempre sobre 'lienzo' (1280x850) y presentar() lo escala al monitor
sin recortar texto. Al importar este modulo se inicia Pygame.
"""
import math
import pygame
from engine.iso_tools import grid_to_iso, iso_to_grid

import mapa
from mapa import ANCHO, ALTO, TW, TH

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
lienzo = pygame.Surface((ANCHO, ALTO))
_pantalla_completa = True


def _abrir_ventana():
    if _pantalla_completa:
        return pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    return pygame.display.set_mode((ANCHO, ALTO), pygame.RESIZABLE)


ventana = _abrir_ventana()
pygame.display.set_caption('Dead Zone - Uruguay | Version completa')

fuente_normal = pygame.font.SysFont('consolas', 21, bold=True)
fuente_chica = pygame.font.SysFont('consolas', 16)
fuente_grande = pygame.font.SysFont('consolas', 52, bold=True)
fuente_media = pygame.font.SysFont('consolas', 26, bold=True)
fuente_etiqueta = pygame.font.SysFont('consolas', 11, bold=True)     # nombre sobre cada enemigo
fuente_puerta = pygame.font.SysFont('consolas', 12, bold=True)       # carteles ENTRAR / SALIDA
PANEL_Y = ALTO - 190                                              # y donde empieza el panel inferior


def alternar_pantalla_completa():
    global _pantalla_completa, ventana
    _pantalla_completa = not _pantalla_completa
    ventana = _abrir_ventana()


def area_visible():
    sw, sh = ventana.get_size()
    scale = min(sw / ANCHO, sh / ALTO)
    w, h = round(ANCHO * scale), round(ALTO * scale)
    return pygame.Rect((sw - w)//2, (sh - h)//2, w, h)


def raton_en_lienzo(pos):
    """Posicion del raton en coordenadas del lienzo (fuera de el: (-999, -999))."""
    rect = area_visible()
    if not rect.collidepoint(pos):
        return (-999, -999)
    return ((pos[0] - rect.x) * ANCHO / rect.w,
            (pos[1] - rect.y) * ALTO / rect.h)


def presentar():
    """Escala el lienzo al monitor y lo muestra."""
    rect = area_visible()
    ventana.fill((0, 0, 0))
    pygame.transform.smoothscale(lienzo, rect.size, ventana.subsurface(rect))
    pygame.display.flip()


def texto(msg, x, y, color=(235, 238, 227), fuente=fuente_normal):
    lienzo.blit(fuente.render(str(msg), True, color), (x, y))


def vertice_superior(celda):
    """OJO: pese al nombre, devuelve el vertice SUPERIOR del rombo de la casilla.
    El centro del suelo de la casilla esta TH // 2 mas abajo (y + TH // 2)."""
    sx, sy = grid_to_iso(*celda, TW, TH)
    return round(mapa.ORIGEN[0] + sx), round(mapa.ORIGEN[1] + sy)


def rombo(celda, color, border=None):
    x, y = vertice_superior(celda)
    points = [(x, y), (x + TW // 2, y + TH // 2), (x, y + TH), (x - TW // 2, y + TH // 2)]
    pygame.draw.polygon(lienzo, color, points)
    if border is not None: pygame.draw.polygon(lienzo, border, points, 1)

def casilla_bajo_raton(pos):
    # iso_to_grid devuelve coordenadas fraccionarias: la celda se obtiene por floor.
    gx, gy = iso_to_grid(pos[0] - mapa.ORIGEN[0], pos[1] - mapa.ORIGEN[1], TW, TH)
    celda = (math.floor(gx), math.floor(gy))
    return celda if 0 <= celda[0] < mapa.TAMANO and 0 <= celda[1] < mapa.TAMANO else None
