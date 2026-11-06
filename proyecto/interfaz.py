"""Componentes de interfaz: botones de las pantallas y indicadores del panel inferior."""
import pygame

ANCHO_BOTON, ALTO_BOTON, SEPARACION = 340, 58, 20
BOTONES_Y = 420     # altura del primer boton en las pantallas de menu

# Botones del panel inferior durante la partida (coordenadas del lienzo de 1280x850).
BOTONES_PANEL = {'pistola': pygame.Rect(18, 773, 154, 48), 'bate': pygame.Rect(181, 773, 154, 48),
                 'botiquin': pygame.Rect(344, 773, 166, 48), 'turno': pygame.Rect(519, 773, 206, 48)}

# Botones de cada pantalla: (texto, accion). El primero es el principal (ENTER).
PANTALLAS = {
    'menu': [('COMENZAR JUEGO', 'comenzar'), ('SALIR', 'salir')],
    'nivel_completo': [('SIGUIENTE NIVEL', 'siguiente'), ('MENU PRINCIPAL', 'menu')],
    'victoria': [('JUGAR DE NUEVO', 'nueva'), ('MENU PRINCIPAL', 'menu')],
    'derrota': [('REINTENTAR NIVEL', 'reintentar'), ('MENU PRINCIPAL', 'menu')],
}


class Boton:
    def __init__(self, rect, texto, accion):
        self.rect = pygame.Rect(rect)
        self.texto = texto
        self.accion = accion

    def dibujar(self, superficie, fuente, sobre=False, principal=False):
        if principal:
            fondo = (150, 113, 56) if sobre else (121, 91, 46)
        else:
            fondo = (66, 84, 90) if sobre else (46, 60, 65)
        borde = (214, 220, 196) if sobre else (110, 130, 126)
        pygame.draw.rect(superficie, fondo, self.rect, border_radius=9)
        pygame.draw.rect(superficie, borde, self.rect, 3 if sobre else 2, border_radius=9)
        img = fuente.render(self.texto, True, (240, 240, 228))
        superficie.blit(img, img.get_rect(center=self.rect.center))


def botones_de(modo, ancho_pantalla, y_inicial):
    """Botones centrados de la pantalla 'modo' (lista vacia si no tiene)."""
    botones = []
    for i, (texto, accion) in enumerate(PANTALLAS.get(modo, [])):
        rect = (ancho_pantalla // 2 - ANCHO_BOTON // 2,
                y_inicial + i * (ALTO_BOTON + SEPARACION), ANCHO_BOTON, ALTO_BOTON)
        botones.append(Boton(rect, texto, accion))
    return botones


def boton_en(botones, pos):
    """Accion del boton que esta bajo 'pos' (o None)."""
    return next((b.accion for b in botones if b.rect.collidepoint(pos)), None)


def texto_centrado(superficie, fuente, msg, centro_x, y, color=(235, 238, 227)):
    img = fuente.render(str(msg), True, color)
    superficie.blit(img, img.get_rect(midtop=(centro_x, y)))


def barra_vida(superficie, rect, vida, vida_max):
    """Barra de vida: verde, ambar o roja segun el porcentaje restante."""
    rect = pygame.Rect(rect)
    fraccion = max(0, min(1, vida / vida_max))
    color = (84, 190, 118) if fraccion > .5 else (222, 176, 74) if fraccion > .25 else (206, 74, 68)
    pygame.draw.rect(superficie, (38, 42, 39), rect, border_radius=4)
    if fraccion > 0:
        relleno = pygame.Rect(rect.x, rect.y, max(4, round(rect.w * fraccion)), rect.h)
        pygame.draw.rect(superficie, color, relleno, border_radius=4)
    pygame.draw.rect(superficie, (120, 138, 130), rect, 1, border_radius=4)


def indicadores_turno(superficie, fuente, g, vida_max, pa_max, y):
    """Fila del panel con la barra de vida, los PA restantes y de quien es el turno."""
    superficie.blit(fuente.render('VIDA', True, (200, 208, 196)), (22, y))
    barra_vida(superficie, (70, y + 1, 190, 16), g['vida'], vida_max)
    superficie.blit(fuente.render('PA', True, (200, 208, 196)), (284, y))
    for i in range(pa_max):
        casilla = pygame.Rect(312 + i * 24, y + 1, 18, 16)
        if i < g['pa']:
            pygame.draw.rect(superficie, (226, 170, 66), casilla, border_radius=3)
        pygame.draw.rect(superficie, (160, 130, 70), casilla, 2, border_radius=3)
    insignia = pygame.Rect(430, y - 3, 270, 24)
    pygame.draw.rect(superficie, (34, 74, 58), insignia, border_radius=6)
    pygame.draw.rect(superficie, (84, 190, 118), insignia, 2, border_radius=6)
    img = fuente.render(f'TURNO {g["turno"]}: JUEGA P1', True, (206, 240, 214))
    superficie.blit(img, img.get_rect(center=insignia.center))
