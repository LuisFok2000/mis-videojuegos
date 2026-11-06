"""Dead Zone: Uruguay. Punto de entrada y bucle principal.

Cada fotograma: leer la entrada (entrada.py), dibujar (dibujo_mundo.py y
dibujo_panel.py) y mostrar el lienzo en el monitor (pantalla.py). Las reglas
estan en los demas modulos.
"""
import pygame

import dibujo_mundo
import dibujo_panel
import entrada
import niveles
import pantalla
import sonido
from partida import volver_al_menu


def main():
    niveles.validar_todos()
    sonido.iniciar_audio()
    reloj = pygame.time.Clock()
    g = volver_al_menu()
    ejecutando = True
    while ejecutando:
        raton = pantalla.raton_en_lienzo(pygame.mouse.get_pos())
        hover = pantalla.casilla_bajo_raton(raton) if g['modo'] == 'juego' else None
        g, ejecutando = entrada.procesar_eventos(g, hover)
        if g['modo'] == 'juego':
            dibujo_mundo.dibujar_mundo(g, hover)
            dibujo_panel.dibujar_panel(g)
        else:
            dibujo_panel.dibujar_pantalla(g, raton)
        pantalla.presentar()
        reloj.tick(60)
    pygame.quit()


if __name__ == '__main__':
    main()
