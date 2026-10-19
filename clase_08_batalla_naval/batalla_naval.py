import random
import sys
import pygame

pygame.init()

TAM = 34
ANCHO, ALTO = 780, 490
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Batalla Naval contra la IA")
reloj = pygame.time.Clock()
fuente = pygame.font.SysFont("arial", 19)
fuente_grande = pygame.font.SysFont("arial", 36, bold=True)

# Posición superior izquierda de cada tablero.
OX_ENEMIGO, OX_JUGADOR, OY = 25, 415, 75
AGUA, BARCO, FALLO, TOCADO = ".", "B", "X", "T"


def crear_tablero():
    return [[AGUA for _ in range(10)] for _ in range(10)]


def colocar_barcos(tablero, tamanos=(5, 4, 3, 3, 2)):
    for tam in tamanos:
        while True:
            horizontal = random.choice([True, False])
            fila = random.randint(0, 9 if horizontal else 10 - tam)
            col = random.randint(0, 10 - tam if horizontal else 9)
            celdas = [(fila + (0 if horizontal else i),
                       col + (i if horizontal else 0)) for i in range(tam)]
            if all(tablero[f][c] == AGUA for f, c in celdas):
                for f, c in celdas:
                    tablero[f][c] = BARCO
                break


def reiniciar():
    global jugador, enemigo, disparos_jugador, disparos_enemigo
    global turno_jugador, cantidad_disparos, resultado, mensaje
    jugador = crear_tablero()
    enemigo = crear_tablero()
    colocar_barcos(jugador)
    colocar_barcos(enemigo)
    disparos_jugador = crear_tablero()  # Disparos de la IA sobre nosotros.
    disparos_enemigo = crear_tablero()  # Nuestros disparos sobre la IA.
    turno_jugador = True
    cantidad_disparos = 0
    resultado = None
    mensaje = "Tu turno: hacé clic en el tablero enemigo (izquierda)."


def barcos_restantes(tablero):
    return sum(fila.count(BARCO) for fila in tablero)


def disparar(tablero, marcas, fila, col):
    if marcas[fila][col] != AGUA:
        return None
    acierto = tablero[fila][col] == BARCO
    marcas[fila][col] = TOCADO if acierto else FALLO
    if acierto:
        tablero[fila][col] = TOCADO
    return acierto


def turno_ia():
    global turno_jugador, resultado, mensaje
    libres = [(f, c) for f in range(10) for c in range(10)
              if disparos_jugador[f][c] == AGUA]
    if not libres:
        return
    fila, col = random.choice(libres)
    acierto = disparar(jugador, disparos_jugador, fila, col)
    if barcos_restantes(jugador) == 0:
        resultado = "¡Perdiste!"
        mensaje = "La IA hundió todos tus barcos."
    elif acierto:
        mensaje = "La IA acertó y vuelve a disparar."
        turno_jugador = False
    else:
        mensaje = "La IA falló. ¡Tu turno!"
        turno_jugador = True


def dibujar_tablero(marcas, barcos, ox, titulo, mostrar_barcos):
    pantalla.blit(fuente.render(titulo, True, (255, 255, 255)), (ox, 40))
    for fila in range(10):
        for col in range(10):
            estado = marcas[fila][col]
            color = (35, 85, 150)
            if mostrar_barcos and barcos[fila][col] == BARCO:
                color = (115, 150, 160)
            if estado == FALLO:
                color = (70, 75, 90)
            elif estado == TOCADO:
                color = (220, 65, 65)
            pygame.draw.rect(pantalla, color,
                             (ox + col * TAM, OY + fila * TAM, TAM - 2, TAM - 2))
            if estado == FALLO:
                pygame.draw.circle(pantalla, (220, 230, 255),
                                   (ox + col * TAM + 16, OY + fila * TAM + 16), 3)


reiniciar()
ejecutando = True
proximo_turno_ia = 0

while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_r:
            reiniciar()
        elif (evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1
              and turno_jugador and resultado is None):
            mx, my = evento.pos
            col = (mx - OX_ENEMIGO) // TAM
            fila = (my - OY) // TAM
            if (OX_ENEMIGO <= mx < OX_ENEMIGO + 10 * TAM
                    and OY <= my < OY + 10 * TAM
                    and disparos_enemigo[fila][col] == AGUA):
                acierto = disparar(enemigo, disparos_enemigo, fila, col)
                cantidad_disparos += 1
                if barcos_restantes(enemigo) == 0:
                    resultado = "¡Ganaste!"
                    mensaje = f"Hundiste todos los barcos en {cantidad_disparos} disparos."
                elif acierto:
                    mensaje = "¡Tocado! Podés disparar otra vez."
                else:
                    mensaje = "Agua. Turno de la IA..."
                    turno_jugador = False
                    proximo_turno_ia = pygame.time.get_ticks() + 550

    if resultado is None and not turno_jugador and pygame.time.get_ticks() >= proximo_turno_ia:
        turno_ia()
        proximo_turno_ia = pygame.time.get_ticks() + 550

    pantalla.fill((18, 22, 40))
    dibujar_tablero(disparos_enemigo, enemigo, OX_ENEMIGO, "Enemigo (clic para disparar)", False)
    dibujar_tablero(disparos_jugador, jugador, OX_JUGADOR, "Tu tablero", True)
    pantalla.blit(fuente.render(f"Tus disparos: {cantidad_disparos}", True, (255, 255, 255)), (25, 425))
    pantalla.blit(fuente.render(mensaje, True, (255, 220, 140)), (25, 450))
    if resultado:
        texto = fuente_grande.render(resultado, True, (120, 255, 150) if resultado == "¡Ganaste!" else (255, 120, 120))
        pantalla.blit(texto, (410, 425))
    else:
        pantalla.blit(fuente.render("R: reiniciar", True, (200, 210, 230)), (635, 425))
    pygame.display.flip()
    reloj.tick(30)

pygame.quit()
sys.exit()
