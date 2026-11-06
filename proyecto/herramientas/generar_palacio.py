"""Genera recursos/edificio_4.png: el Palacio Legislativo.

Se dibuja con cajas isometricas (misma proyeccion 2:1 del juego) para que apoye
exactamente sobre las 4 casillas (2x2) del edificio: cuerpo de piedra con dos
pisos de ventanas y cornisa, portico central con seis columnas y frontón,
y la cupula sobre un tambor con columnas, linterna y bandera de Uruguay.
Uso:  python herramientas/generar_palacio.py
"""
import math

from comun import RECURSOS, TW2, TH2, sombrear     # tambien inicia Pygame sin ventana
import pygame

ANCHO, ALTO = 234, 250
OX, OY = 117, ALTO - 1 - 4 * TH2        # vertice superior de la base 2x2
INK = (30, 34, 36)
PIEDRA = (222, 212, 186)
GRANITO = (150, 140, 128)
VENTANA = (52, 66, 76)
CUPULA = (150, 170, 156)


def P(x, y, z=0):
    return (round(OX + (x - y) * TW2), round(OY + (x + y) * TH2 - z))


def poli(s, pts3d, color, borde=INK, ancho=1):
    pts = [P(*p) for p in pts3d]
    pygame.draw.polygon(s, color, pts)
    if borde:
        pygame.draw.polygon(s, borde, pts, ancho)


# Caras en coordenadas locales (u, z): 'L' = plano y=Y (mira abajo-izquierda),
# 'R' = plano x=2 (mira abajo-derecha); u crece hacia la derecha de la pantalla.
def pt(cara, u, z, plano):
    return P(u, plano, z) if cara == 'L' else P(2, 2 - u, z)


def rect(s, cara, u0, u1, z0, z1, color, plano, borde=None):
    pts = [pt(cara, u0, z0, plano), pt(cara, u1, z0, plano), pt(cara, u1, z1, plano), pt(cara, u0, z1, plano)]
    pygame.draw.polygon(s, color, pts)
    if borde:
        pygame.draw.polygon(s, borde, pts, 1)


def ventanas(s, cara, plano, longitud, z0, z1, n, ancho=0.17, saltar=()):
    paso = longitud / n
    for i in range(n):
        if i in saltar:
            continue
        u = paso * i + (paso - ancho) / 2
        rect(s, cara, u - .02, u + ancho + .02, z0 - 1, z1 + 2, sombrear(PIEDRA, 1.12), plano, None)   # marco
        rect(s, cara, u, u + ancho, z0, z1, VENTANA, plano, INK)
        rect(s, cara, u + ancho / 2 - .008, u + ancho / 2 + .008, z0, z1, sombrear(VENTANA, 1.5), plano)


def cuerpo(s, H, y1):
    # caras visibles de la caja principal: frente (y=y1), costado (x=2) y techo
    poli(s, [(0, y1, 0), (2, y1, 0), (2, y1, H), (0, y1, H)], PIEDRA)
    poli(s, [(2, 0, 0), (2, y1, 0), (2, y1, H), (2, 0, H)], sombrear(PIEDRA, .74))
    poli(s, [(0, 0, H), (2, 0, H), (2, y1, H), (0, y1, H)], (178, 172, 156))
    # zocalo de granito
    rect(s, 'L', 0, 2, 0, 8, GRANITO, y1, INK)
    rect(s, 'R', 0, y1, 0, 8, sombrear(GRANITO, .76), 0)
    # cornisa
    rect(s, 'L', 0, 2, H - 5, H, sombrear(PIEDRA, 1.1), y1, INK)
    rect(s, 'R', 0, y1, H - 5, H, sombrear(PIEDRA, .86), 0)
    # pilastras en los extremos
    for u0 in (0.0, 1.92):
        rect(s, 'L', u0, u0 + .08, 8, H - 5, sombrear(PIEDRA, 1.08), y1)


def portico(s, y1, H):
    y2 = 2.0
    zc = 44                                     # altura de la cornisa del portico
    # costado derecho del portico (plano x=1.5) y escalinata
    poli(s, [(1.5, y1, 0), (1.5, y2, 0), (1.5, y2, zc), (1.5, y1, zc)], sombrear(PIEDRA, .72))
    for k in range(3):                          # escalones al frente
        poli(s, [(.42 - k*.03, y2 + 0.0, k*2), (1.58 + k*.03, y2, k*2), (1.58 + k*.03, y2, k*2 + 2), (.42 - k*.03, y2, k*2 + 2)],
             sombrear(GRANITO, 1.12 - k * .06))
    # puerta central
    rect(s, 'L', .86, 1.14, 6, 25, (44, 52, 56), y2, INK)
    pygame.draw.polygon(s, (44, 52, 56), [pt('L', .86, 25, y2), pt('L', 1.0, 31, y2), pt('L', 1.14, 25, y2)])
    # columnas
    cols = [0.55 + i * 0.18 for i in range(6)]
    for u in cols:
        rect(s, 'L', u - .035, u + .035, 6, zc - 4, sombrear(PIEDRA, 1.18), y2, sombrear(INK, 1.4))
        rect(s, 'L', u - .055, u + .055, 6, 8, sombrear(PIEDRA, .9), y2)
        rect(s, 'L', u - .055, u + .055, zc - 6, zc - 4, sombrear(PIEDRA, 1.25), y2)
        rect(s, 'L', u + .012, u + .035, 8, zc - 6, sombrear(PIEDRA, .82), y2)         # sombra de la columna
    # arquitrabe, friso y frontón
    rect(s, 'L', .42, 1.58, zc - 4, zc + 2, sombrear(PIEDRA, 1.14), y2, INK)
    rect(s, 'L', .42, 1.58, zc + 2, zc + 7, sombrear(PIEDRA, .98), y2, INK)
    tri = [pt('L', .40, zc + 7, y2), pt('L', 1.60, zc + 7, y2), pt('L', 1.0, zc + 21, y2)]
    pygame.draw.polygon(s, sombrear(PIEDRA, 1.1), tri)
    pygame.draw.polygon(s, INK, tri, 1)
    pygame.draw.polygon(s, sombrear(PIEDRA, .92), [pt('L', .52, zc + 9, y2), pt('L', 1.48, zc + 9, y2), pt('L', 1.0, zc + 18, y2)])
    # costado del frontón (lado derecho): cubierta inclinada
    pygame.draw.polygon(s, sombrear(PIEDRA, .66), [pt('L', 1.6, zc + 7, y2), pt('L', 1.0, zc + 21, y2),
                                               P(1.0, y1, zc + 21), P(1.6, y1, zc + 7)])
    pygame.draw.polygon(s, INK, [pt('L', 1.6, zc + 7, y2), pt('L', 1.0, zc + 21, y2),
                                 P(1.0, y1, zc + 21), P(1.6, y1, zc + 7)], 1)


def elipse(s, cx, cy, rx, ry, color, borde=None):
    r = pygame.Rect(0, 0, round(rx * 2), round(ry * 2))
    r.center = (round(cx), round(cy))
    pygame.draw.ellipse(s, color, r)
    if borde:
        pygame.draw.ellipse(s, borde, r, 1)


def cupula(s, H):
    cx, cy0 = P(1.0, 0.9, H)
    r = .46
    rx, ry = r * math.sqrt(2) * TW2, r * math.sqrt(2) * TH2
    ZD = 22                                      # alto del tambor
    # base cuadrada baja que sostiene el tambor
    # tambor: cilindro de piedra con columnas
    pygame.draw.rect(s, sombrear(PIEDRA, .9), (cx - rx, cy0 - ZD, rx * 2, ZD))
    elipse(s, cx, cy0, rx, ry, sombrear(PIEDRA, .9))
    pygame.draw.rect(s, sombrear(PIEDRA, .9), (cx - rx, cy0 - ZD, rx * 2, ZD))
    pygame.draw.line(s, INK, (cx - rx, cy0 - ZD), (cx - rx, cy0), 1)
    pygame.draw.line(s, INK, (cx + rx - 1, cy0 - ZD), (cx + rx - 1, cy0), 1)
    pygame.draw.arc(s, INK, pygame.Rect(round(cx - rx), round(cy0 - ry), round(rx * 2), round(ry * 2)), math.pi, math.tau, 1)
    for k in range(-4, 5):                        # columnas y ventanitas del tambor
        ang = k * math.pi / 9
        x = cx + rx * math.sin(ang)
        yb = cy0 + ry * math.cos(ang)
        pygame.draw.line(s, sombrear(PIEDRA, 1.22), (x, yb - ZD + 3), (x, yb - 2), 2)
        if k % 2:
            pygame.draw.rect(s, VENTANA, (round(x) - 2, round(yb) - ZD + 8, 4, 8))
    cy1 = cy0 - ZD
    elipse(s, cx, cy1, rx + 2, ry + 1.2, sombrear(PIEDRA, 1.18), INK)             # cornisa del tambor
    # cupula: media elipsoide con gajos
    alto = 30
    pts = [(cx + rx * math.cos(a), cy1 - alto * math.sin(a)) for a in [i * math.pi / 24 for i in range(25)]]
    pts += [(cx - rx * math.cos(a), cy1 + ry * math.sin(a)) for a in [i * math.pi / 24 for i in range(25)]][::-1][:0]
    base = [(cx - rx + 2 * rx * i / 24, cy1 + ry * math.sin(math.acos((i / 12) - 1 if 0 <= i <= 24 else 0))) for i in range(25)]
    pygame.draw.polygon(s, CUPULA, pts + base[::-1][1:-1])
    pygame.draw.polygon(s, sombrear(CUPULA, .7), [(cx + 2, cy1 - alto * .96)] + [(cx + rx * math.cos(a), cy1 - alto * math.sin(a))
                                                                          for a in [i * math.pi / 24 for i in range(0, 13)]] + [(cx + rx, cy1)] + [(cx, cy1 + ry)])
    for a in range(0, 180, 30):                   # gajos
        b = math.radians(a)
        bx, by = cx + rx * math.cos(b), cy1 + ry * math.sin(b)
        linea = []
        for i in range(0, 11):
            h = i / 10
            rho = math.sqrt(max(0, 1 - h * h))
            linea.append((cx + (bx - cx) * rho, cy1 + (by - cy1) * rho - alto * h))
        if len(linea) > 1:
            pygame.draw.lines(s, sombrear(CUPULA, .62), False, linea, 1)
    pygame.draw.arc(s, sombrear(CUPULA, 1.25), pygame.Rect(round(cx - rx + 5), round(cy1 - alto + 4), round(rx * 1.2), round(alto * 1.4)), 1.3, 2.4, 2)
    pygame.draw.polygon(s, INK, pts, 1)
    # linterna, aguja y bandera
    cyl = cy1 - alto + 1
    pygame.draw.rect(s, sombrear(PIEDRA, 1.1), (cx - 4, cyl - 9, 8, 10))
    pygame.draw.rect(s, INK, (cx - 4, cyl - 9, 8, 10), 1)
    pygame.draw.polygon(s, sombrear(CUPULA, 1.1), [(cx - 5, cyl - 9), (cx + 5, cyl - 9), (cx, cyl - 17)])
    pygame.draw.line(s, (60, 60, 60), (cx, cyl - 17), (cx, cyl - 34), 1)
    for k in range(9):                            # bandera de Uruguay (franjas blancas y azules)
        pygame.draw.rect(s, (250, 250, 250) if k % 2 == 0 else (60, 110, 190), (cx + 1, cyl - 34 + k, 16, 1))
    pygame.draw.rect(s, (250, 250, 250), (cx + 1, cyl - 34, 6, 5))
    pygame.draw.circle(s, (240, 190, 40), (cx + 4, cyl - 32), 2)


def palacio():
    s = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
    H, y1 = 50, 1.8
    cuerpo(s, H, y1)
    ventanas(s, 'L', y1, 2, 14, 24, 8, saltar=(3, 4))
    ventanas(s, 'L', y1, 2, 30, 41, 8, saltar=(3, 4))
    ventanas(s, 'R', 0, y1, 14, 24, 5, ancho=.14)
    ventanas(s, 'R', 0, y1, 30, 41, 5, ancho=.14)
    portico(s, y1, H)
    cupula(s, H)
    return s


def main():
    destino = RECURSOS / 'edificio_4.png'
    pygame.image.save(palacio(), str(destino))
    print('Palacio Legislativo ->', destino)


if __name__ == '__main__':
    main()
