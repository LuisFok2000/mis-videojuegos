"""Genera los sprites de autos isometricos (recursos/auto_0..2.png).

Cada auto es un conjunto de cajas proyectadas con la misma conversion 2:1 del
motor (iso_tools): sx = (x - y) * TW/2 ; sy = (x + y) * TH/2 - altura.
El auto mira hacia +x (abajo a la derecha). El juego usa tambien una copia
espejada (mira hacia +y) para que los autos sigan la direccion de la calle.
Uso:  python herramientas/generar_autos.py
"""
import random

from comun import RECURSOS, TW2, TH2, sombrear     # tambien inicia Pygame sin ventana
import pygame

K = 1.3                      # escala del auto respecto de la baldosa
ANCHO, ALTO = 129, 124       # lienzo; el centro de la base cae en ORIGEN
ORIGEN = (64, 90)

# (nombre, color base de la carroceria)
# (nombre, carroceria, cabina, tipo). 0: taxi de Montevideo (negro con techo amarillo),
# 1: omnibus urbano (blanco con franja azul), 2: auto blanco con franja verde.
COLORES = [('taxi', (38, 40, 44), (226, 182, 56), 'taxi'), ('omnibus', (226, 228, 214), None, 'bus'),
           ('blanco_verde', (222, 220, 200), (222, 220, 200), 'verde')]
CONTORNO = (22, 25, 27)
VIDRIO = (84, 118, 130)
GRIETA = (176, 204, 208)


def P(x, y, z):
    """Punto del mundo (en baldosas, y altura en px) -> pixel del lienzo."""
    return (round(ORIGEN[0] + (x - y) * TW2 * K), round(ORIGEN[1] + (x + y) * TH2 * K - z * K))


def cara(sup, pts3d, color, borde=CONTORNO):
    pts = [P(*p) for p in pts3d]
    pygame.draw.polygon(sup, color, pts)
    pygame.draw.polygon(sup, borde, pts, 1)
    return pts


def caja(sup, x0, x1, y0, y1, z0, z1, color):
    """Dibuja las tres caras visibles: techo, lado izquierdo (y=y1) y frente (x=x1)."""
    cara(sup, [(x0, y1, z0), (x1, y1, z0), (x1, y1, z1), (x0, y1, z1)], sombrear(color, 1.0))
    cara(sup, [(x1, y0, z0), (x1, y1, z0), (x1, y1, z1), (x1, y0, z1)], sombrear(color, 0.72))
    cara(sup, [(x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)], sombrear(color, 1.18))


def rueda(sup, x, y, z):
    cx, cy = P(x, y, z)
    pygame.draw.ellipse(sup, (18, 20, 21), (cx - 9, cy - 8, 18, 17))
    pygame.draw.ellipse(sup, (70, 74, 74), (cx - 9, cy - 8, 18, 17), 1)
    pygame.draw.circle(sup, (134, 138, 132), (cx, cy), 3)


def auto(color, semilla, cab=None, tipo='taxi'):
    cab = cab or color
    azar = random.Random(semilla)
    s = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
    LX, LY = 0.66, 0.31                     # medio largo y medio ancho
    caja(s, -LX, LX, -LY, LY, 5, 15, color)             # chasis y capot
    for x in (-0.40, 0.38):                              # ruedas del lado visible
        rueda(s, x, LY, 4)
    # Paragolpes y faros en el frente (cara x = +LX).
    cara(s, [(LX, -LY, 5), (LX, LY, 5), (LX, LY, 8), (LX, -LY, 8)], (46, 48, 50))
    for y in (-0.20, 0.18):
        cara(s, [(LX, y - .07, 10), (LX, y + .07, 10), (LX, y + .07, 13), (LX, y - .07, 13)], (236, 214, 120))
    # Cabina: lados verticales y parabrisas inclinado.
    bx0, bx1, tx0, tx1, cy = -0.34, 0.20, -0.28, 0.06, 0.27
    lado = [(bx0, cy, 15), (bx1, cy, 15), (tx1, cy, 28), (tx0, cy, 28)]
    cara(s, lado, sombrear(cab, 0.85))
    ventana = [(bx0 + .06, cy, 17), (bx1 - .05, cy, 17), (tx1 - .01, cy, 26), (tx0 + .03, cy, 26)]
    pygame.draw.polygon(s, VIDRIO, [P(*p) for p in ventana])
    pygame.draw.line(s, sombrear(cab, 0.7), P(-0.06, cy, 17), P(-0.06, cy, 26), 3)   # pilar central
    parabrisas = [(bx1, -cy, 15), (bx1, cy, 15), (tx1, cy, 28), (tx1, -cy, 28)]
    cara(s, parabrisas, sombrear(cab, 0.6))
    interior = [(bx1 - .02, -cy + .05, 17), (bx1 - .02, cy - .05, 17), (tx1 - .01, cy - .05, 26), (tx1 - .01, -cy + .05, 26)]
    pygame.draw.polygon(s, sombrear(VIDRIO, 0.9), [P(*p) for p in interior])
    cara(s, [(tx0, -cy, 28), (tx1, -cy, 28), (tx1, cy, 28), (tx0, cy, 28)], sombrear(cab, 1.12))
    if tipo == 'taxi':                                      # luminaria TAXI sobre el techo
        caja(s, -0.16, -0.02, -0.08, 0.08, 28, 33, (240, 230, 170))
    if tipo == 'verde':                                     # franja verde lateral
        pygame.draw.line(s, (52, 150, 96), P(-0.60, LY, 10), P(0.60, LY, 10), 4)
    # Desgaste: grietas en el parabrisas, oxido, rayones y manijas.
    pygame.draw.line(s, GRIETA, P(0.15, -0.10, 18), P(0.09, 0.05, 25), 1)
    pygame.draw.line(s, GRIETA, P(0.11, 0.02, 21), P(0.14, 0.17, 24), 1)
    pygame.draw.line(s, GRIETA, P(-0.05, cy, 18), P(0.02, cy, 24), 1)
    for _ in range(9):                                     # manchas de oxido en el costado
        px, pz = azar.uniform(-0.55, 0.55), azar.uniform(6, 13)
        x, y = P(px, LY, pz)
        pygame.draw.rect(s, (122, 70, 42), (x, y, azar.choice((2, 3, 4)), 2))
    pygame.draw.line(s, sombrear(color, 0.5), P(-0.08, LY, 6), P(-0.08, LY, 14), 1)   # junta de puerta
    pygame.draw.line(s, sombrear(color, 0.5), P(0.30, LY, 6), P(0.30, LY, 14), 1)
    pygame.draw.line(s, (214, 214, 200), P(-0.18, LY, 12), P(-0.10, LY, 12), 1)       # manija
    pygame.draw.line(s, sombrear(color, 1.3), P(0.10, 0.31, 14), P(0.55, 0.31, 14), 1)  # borde del capot
    return s


def omnibus(color, semilla):
    """Omnibus urbano: caja larga y alta, ventanas corridas, franja azul y parabrisas grande."""
    azar = random.Random(semilla)
    s = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
    LX, LY, ZT = 0.80, 0.33, 40
    caja(s, -LX, LX, -LY, LY, 6, ZT, color)
    for x in (-0.50, 0.46):
        rueda(s, x, LY, 5)
    # franja azul y ventanas del costado visible (plano y = LY)
    cara(s, [(-LX, LY, 9), (LX, LY, 9), (LX, LY, 15), (-LX, LY, 15)], (52, 104, 170), borde=(52, 104, 170))
    n = 5
    ancho = 2 * LX / n
    for i in range(n):
        x0 = -LX + i * ancho + 0.05
        cara(s, [(x0, LY, 20), (x0 + ancho - 0.10, LY, 20), (x0 + ancho - 0.10, LY, 34), (x0, LY, 34)], VIDRIO)
    pygame.draw.line(s, (60, 66, 70), P(-LX, LY, 17), P(LX, LY, 17), 1)
    # frente (plano x = LX): parabrisas, cartel de destino, faros y paragolpes
    cara(s, [(LX, -LY + .05, 18), (LX, LY - .05, 18), (LX, LY - .05, 35), (LX, -LY + .05, 35)], (70, 100, 112))
    cara(s, [(LX, -LY + .08, 36), (LX, LY - .08, 36), (LX, LY - .08, 39), (LX, -LY + .08, 39)], (244, 170, 52))
    for y in (-0.22, 0.20):
        cara(s, [(LX, y - .06, 9), (LX, y + .06, 9), (LX, y + .06, 13), (LX, y - .06, 13)], (236, 214, 120))
    cara(s, [(LX, -LY, 6), (LX, LY, 6), (LX, LY, 8), (LX, -LY, 8)], (46, 48, 50))
    for _ in range(7):                                        # desgaste
        px, pz = azar.uniform(-0.7, 0.7), azar.uniform(7, 12)
        x, y = P(px, LY, pz)
        pygame.draw.rect(s, (122, 90, 60), (x, y, azar.choice((2, 3, 4)), 2))
    return s


def main():
    destino = RECURSOS
    for i, (nombre, color, cab, tipo) in enumerate(COLORES):
        img = omnibus(color, 100 + i) if tipo == 'bus' else auto(color, 100 + i, cab, tipo)
        pygame.image.save(img, str(destino / f'auto_{i}.png'))
        print('auto', i, nombre)


if __name__ == '__main__':
    main()
