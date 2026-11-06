"""Particulas de impactos y numeros de dano."""
import math
import random

PARTICULAS = []
NUMEROS = []


def estado_visual():
    """Temporizadores de animacion que guarda la partida (disparo, golpe, herida, impacto)."""
    return {'destello': None, 'golpe': 0, 'fogonazo': 0, 'herido': 0}


def limpiar():
    PARTICULAS.clear()
    NUMEROS.clear()


def particulas(celda, color, cantidad=12, *, vertice):
    """Chispas en una casilla. 'vertice' convierte la casilla en pixeles (pantalla.vertice_superior)."""
    x, y = vertice(celda)
    for _ in range(cantidad):
        angulo = random.random() * math.tau
        velocidad = random.uniform(1.2, 4.0)
        PARTICULAS.append([float(x), float(y - 22), math.cos(angulo) * velocidad,
                           math.sin(angulo) * velocidad - 1, random.randint(14, 28), color])


def numero_flotante(celda, rotulo, color, *, vertice):
    x, y = vertice(celda)
    NUMEROS.append([float(x), float(y - 60), rotulo, color, 45])


def dibujar_efectos(lienzo, texto, fuente):
    import pygame        # aqui y no arriba: las pruebas de reglas no necesitan Pygame
    for p in PARTICULAS[:]:
        p[0] += p[2]; p[1] += p[3]; p[3] += .11; p[4] -= 1
        pygame.draw.circle(lienzo, p[5], (int(p[0]), int(p[1])), max(1, p[4] // 9))
        if p[4] <= 0:
            PARTICULAS.remove(p)
    for n in NUMEROS[:]:
        n[1] -= .55; n[4] -= 1
        texto(n[2], int(n[0] - 14), int(n[1]), n[3], fuente)
        if n[4] <= 0:
            NUMEROS.remove(n)
