"""Panel inferior de la partida y pantallas de menu (menu principal, nivel
completado, victoria y derrota). Solo dibuja: no cambia las reglas del juego."""
import pygame

import mapa
from mapa import ANCHO, ALTO
import interfaz
import transiciones
from jugador import VIDA_MAXIMA, PA_POR_TURNO
from pantalla import (lienzo, texto, fuente_normal, fuente_chica, fuente_grande, fuente_media, PANEL_Y)


def dibujar_botones(g):
    labels = [('pistola','1  PISTOLA'), ('bate','2  BATE'), ('botiquin','H  BOTIQUIN'), ('turno','ESPACIO  TURNO')]
    for key, label in labels:
        rect = interfaz.BOTONES_PANEL[key]
        active = g['arma'] == key if key in ('pistola','bate') else False
        color = (64,106,100) if active else (46,60,65)
        if key == 'turno': color = (121,91,46)
        pygame.draw.rect(lienzo, color, rect, border_radius=7)
        pygame.draw.rect(lienzo, (147,159,144) if active else (88,106,105), rect, 2, border_radius=7)
        texto(label, rect.x+12, rect.y+13, fuente=fuente_chica)


def texto_mision(g):
    """Objetivo en dos lineas, actualizado segun el avance de la partida."""
    pendientes = transiciones.enemigos_pendientes(g)
    if g['suministros']:
        if pendientes:
            return ('Suministros recogidos. Elimina a los zombis',
                    'y vuelve al refugio.')
        return ('Suministros recogidos. Vuelve al refugio.', '')
    if g['nivel'] == 1:
        return ('Mision: busca suministros DENTRO de Farmashop,',
                'elimina zombis y regresa al refugio.')
    if g['nivel'] == 2:
        return ('Mision: entra al PALACIO, derrota al jefe,',
                'recoge suministros y vuelve al refugio.')
    if not pendientes:
        return ('Zona despejada. Recoge los suministros',
                'y vuelve al refugio.')
    return ('Mision: elimina a los zombis, recoge los',
            'suministros y vuelve al refugio.')


def dibujar_panel(g):
    """Panel inferior: vida, PA, mision, botones y mensaje."""
    pygame.draw.rect(lienzo, (22, 31, 33), (0, PANEL_Y, ANCHO, ALTO-PANEL_Y))
    pygame.draw.line(lienzo, (91,120,112), (0,PANEL_Y),(ANCHO,PANEL_Y),3)
    texto(f'DEAD ZONE  /  NIVEL {g["nivel"]+1}: {mapa.NOMBRE}', 22, PANEL_Y+12, (220, 206, 148), fuente_media)
    texto(f'VIDA  {g["vida"]}/{VIDA_MAXIMA}     PA  {g["pa"]}/{PA_POR_TURNO}     BALAS  {g["balas"]}     BOTIQUINES  {g["botiquines"]}', 22, PANEL_Y+47)
    texto(f'Zombis: {transiciones.enemigos_pendientes(g)}  |  Turno: {g["turno"]}  |  Suministros: {"RECOGIDOS" if g["suministros"] else "PENDIENTES"}', 755, PANEL_Y+16, fuente=fuente_chica)
    linea_uno, linea_dos = texto_mision(g)
    texto(linea_uno, 755, PANEL_Y+44, fuente=fuente_chica)
    if linea_dos:
        texto(linea_dos, 755, PANEL_Y+66, fuente=fuente_chica)
    dibujar_botones(g)
    interfaz.indicadores_turno(lienzo, fuente_chica, g, VIDA_MAXIMA, PA_POR_TURNO, PANEL_Y + 78)
    texto(g['mensaje'][:107], 22, ALTO-20, (230,211,133), fuente_chica)
    texto('E: puertas | F11: pantalla | M: sonido | ESC: menu', 754, ALTO-45, fuente=fuente_chica)


def dibujar_pantalla(g, raton):
    """Menu principal y pantallas de nivel completado, victoria y derrota."""
    lienzo.fill((16, 23, 25))
    cx = ANCHO // 2
    title = {'menu': 'DEAD ZONE', 'nivel_completo': 'NIVEL COMPLETADO',
             'victoria': 'VICTORIA!', 'derrota': 'GAME OVER'}[g['modo']]
    interfaz.texto_centrado(lienzo, fuente_grande, title, cx, 190, (210, 204, 145))
    lineas = {'menu': ['ULTIMO SUPERVIVIENTE', 'Sobrevivi al apocalipsis zombi'],
              'nivel_completo': ['Suministros a salvo y zona despejada.',
                                 'Pasas al nivel siguiente: +4 PV y +6 balas.'],
              'victoria': ['Obtuviste los suministros y escapaste.',
                      f'Completaste los {len(mapa.NIVELES)} niveles.'],
              'derrota': ['Los zombis te alcanzaron.', '']}[g['modo']]
    for k, linea in enumerate(lineas):
        interfaz.texto_centrado(lienzo, fuente_normal, linea, cx, 285 + k * 42)
    botones = interfaz.botones_de(g['modo'], ANCHO, interfaz.BOTONES_Y)
    for k, boton in enumerate(botones):
        boton.dibujar(lienzo, fuente_media, boton.rect.collidepoint(raton), principal=(k == 0))
    ayuda = 'ENTER: comenzar   |   M: audio' if g['modo'] == 'menu' else \
            'ENTER: boton principal   |   ESC: menu principal   |   M: audio'
    interfaz.texto_centrado(lienzo, fuente_chica, ayuda, cx, ALTO - 70, (160, 172, 160))
