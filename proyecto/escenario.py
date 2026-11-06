"""Carga y dibujo de los sprites, anclados sobre casillas reales del terreno."""
from pathlib import Path
import pygame
from mapa import TH, TW

IMAGENES = {}
# Aspecto de cada tipo de enemigo (las reglas estan en enemigo.TIPOS): color de la
# barra y la etiqueta, escala del sprite, ancho de la barra de vida, ritmo de la
# animacion en reposo y sprites (el blindado cambia de sprite al romperse la armadura).
ASPECTO_ENEMIGO = {
    'comun':     {'color': (136, 183, 105), 'escala': 1.0,  'barra': 44, 'ritmo': 350.0, 'sprite': 'comun'},
    'corredor':  {'color': (237, 175, 68),  'escala': 1.0,  'barra': 44, 'ritmo': 240.0, 'sprite': 'corredor'},
    'blindado':  {'color': (100, 179, 215), 'escala': 1.0,  'barra': 44, 'ritmo': 350.0, 'sprite': 'blindado',
                  'sprite_roto': 'blindado_roto'},
    'escupidor': {'color': (191, 113, 215), 'escala': 1.0,  'barra': 44, 'ritmo': 350.0, 'sprite': 'escupidor'},
    'jefe':      {'color': (218, 78, 77),   'escala': 1.22, 'barra': 64, 'ritmo': 350.0, 'sprite': 'jefe'},
}
# Objetos "pequenos": se recortan a su parte solida (sin la sombra pegada al PNG)
# y se anclan por el CENTRO de su base. Valor: ancho maximo de la base en pixeles.
OBJETOS_ANCLADOS = {'suministros': None, 'refugio': TW}
# Autos isometricos (herramientas/generar_autos.py): el centro de su base esta en
# ORIGEN_AUTO dentro del PNG. Variantes 0-2 = colores; 3-5 = copia espejada.
ORIGEN_AUTO = (64, 90)
MEDIO_LARGO, MEDIO_ANCHO = 0.91, 0.45

def _sin_sombra_y_recortada(imagen, ancho_objetivo=None):
    """Quita los pixeles semitransparentes (la sombra dibujada en el PNG), recorta
    la imagen a lo que queda y, si se pide, la escala para que la base entre
    en una baldosa."""
    limpia = imagen.copy()
    for yy in range(limpia.get_height()):
        for xx in range(limpia.get_width()):
            r, g, b, a = limpia.get_at((xx, yy))
            if a < 255:
                limpia.set_at((xx, yy), (r, g, b, 0))
    limpia = limpia.subsurface(limpia.get_bounding_rect()).copy()
    if ancho_objetivo and limpia.get_width() > ancho_objetivo:
        factor = ancho_objetivo / limpia.get_width()
        limpia = pygame.transform.smoothscale(
            limpia, (ancho_objetivo, round(limpia.get_height() * factor)))
    return limpia

def cargar():
    ruta = Path(__file__).resolve().parent / 'recursos'
    nombres = [*(f'edificio_{n}' for n in range(5)), *(f'auto_{n}' for n in range(3)), 'escombros', 'suministros', 'refugio',
               'contenedor', *(f'cartel_{n}' for n in range(3)),
               *(f'mueble_{nombre}' for nombre in ('estante','mostrador','horno','mesa','armario','columna')),
               *(f'personaje_{nombre}' for nombre in ['jugador', *(a['sprite'] for a in ASPECTO_ENEMIGO.values()),
                                                    *(a['sprite_roto'] for a in ASPECTO_ENEMIGO.values() if 'sprite_roto' in a)])]
    for nombre in nombres:
        imagen = pygame.image.load(str(ruta / f'{nombre}.png')).convert_alpha()
        if nombre in OBJETOS_ANCLADOS:
            imagen = _sin_sombra_y_recortada(imagen, OBJETOS_ANCLADOS[nombre])
        IMAGENES[nombre] = imagen
    # El auto espejado mira en el otro eje de la rejilla (sigue una calle vertical).
    for n in range(3):
        IMAGENES[f'auto_{n + 3}'] = pygame.transform.flip(IMAGENES[f'auto_{n}'], True, False)

def sombra_contacto(lienzo, centro_base, ancho_base):
    """Sombra elipse pegada a la base del objeto, en el plano del suelo."""
    ancho, alto = round(ancho_base * 1.05), round(ancho_base * 0.5)
    capa = pygame.Surface((ancho, alto), pygame.SRCALPHA)
    pygame.draw.ellipse(capa, (8, 14, 14, 110), capa.get_rect())
    lienzo.blit(capa, capa.get_rect(center=centro_base))

def sombra_auto(lienzo, centro_base, espejado):
    """Sombra rectangular sobre el suelo, alargada en el eje en que mira el auto."""
    lx, ly = (MEDIO_ANCHO, MEDIO_LARGO) if espejado else (MEDIO_LARGO, MEDIO_ANCHO)
    cx, cy = centro_base
    puntos = [(cx + (x - y) * TW / 2, cy + (x + y) * TH / 2)
              for x, y in ((-lx, -ly), (lx, -ly), (lx, ly), (-lx, ly))]
    xs, ys = [p[0] for p in puntos], [p[1] for p in puntos]
    capa = pygame.Surface((round(max(xs) - min(xs)) + 2, round(max(ys) - min(ys)) + 2), pygame.SRCALPHA)
    pygame.draw.polygon(capa, (8, 14, 14, 105),
                        [(px - min(xs) + 1, py - min(ys) + 1) for px, py in puntos])
    lienzo.blit(capa, (round(min(xs)) - 1, round(min(ys)) - 1))

def rectangulo(centro, celda, tipo, variante=0):
    """Posiciona cada objeto mediante un punto de apoyo dentro del sprite.

    El centro de la baldosa esta en (x, y + TH/2): esa es la altura de suelo.
    Para suministros y refugio usamos la coordenada local donde sus bases
    TOCAN ese suelo. Evita desplazar toda la imagen hasta el vertice frontal
    del rombo, que hacia que la base y la sombra quedaran separadas.
    """
    if not IMAGENES:
        cargar()
    x, y = centro(celda)
    if tipo == 'edificio':
        imagen = IMAGENES[f'edificio_{variante % 5}']
        pie = (x, y + 2 * TH)
        return imagen, imagen.get_rect(midbottom=pie)
    if tipo == 'auto':
        imagen = IMAGENES[f'auto_{variante % 6}']
        ox = ORIGEN_AUTO[0] if variante % 6 < 3 else imagen.get_width() - 1 - ORIGEN_AUTO[0]
        # Centro de la base del auto sobre el centro de la baldosa.
        return imagen, imagen.get_rect(topleft=(x - ox, y + TH // 2 - ORIGEN_AUTO[1]))
    if tipo in OBJETOS_ANCLADOS:
        imagen = IMAGENES[tipo]
        # El centro de la BASE del objeto coincide con el centro de la baldosa
        # (x, y + TH/2). La base es un rombo de ancho = ancho de la imagen, asi
        # que su vertice inferior queda ancho/4 por debajo de ese centro.
        base_x, base_y = x, y + TH // 2
        rect = imagen.get_rect(midbottom=(base_x, base_y + imagen.get_width() // 4))
        return imagen, rect
    imagen = IMAGENES[tipo]
    pie = (x, y + TH - 5)
    return imagen, imagen.get_rect(midbottom=pie)

def cimientos(lienzo, centro, celda):
    """Base de hormigon con el mismo rombo que las 4 casillas ocupadas."""
    x, y = centro(celda)
    puntos = [(x, y + 3), (x + TW - 5, y + TH),
              (x, y + TH * 2 - 4), (x - TW + 5, y + TH)]
    pygame.draw.polygon(lienzo, (91, 88, 77), puntos)
    pygame.draw.polygon(lienzo, (130, 125, 108), puntos, 2)
    pygame.draw.line(lienzo, (55, 53, 48), (x - 25, y + 54), (x + 24, y + 54), 2)

def dibujar(lienzo, centro, celda, tipo, variante=0, jugador_rect=None):
    imagen, destino = rectangulo(centro, celda, tipo, variante)
    if tipo in OBJETOS_ANCLADOS or tipo == 'contenedor' or tipo.startswith('mueble_'):
        x, y = centro(celda)
        sombra_contacto(lienzo, (x, y + TH // 2), min(70, imagen.get_width()))
    elif tipo == 'auto':
        x, y = centro(celda)
        sombra_auto(lienzo, (x, y + TH // 2), variante % 6 >= 3)
    # Si una construccion tapa al jugador, se vuelve transparente hasta salir de detras.
    if tipo == 'edificio' and jugador_rect is not None and destino.colliderect(jugador_rect):
        imagen = imagen.copy()
        imagen.set_alpha(95)
    lienzo.blit(imagen, destino)
