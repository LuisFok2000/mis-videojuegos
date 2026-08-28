import math
import sys
import pygame

pygame.init()

ANCHO, ALTO = 900, 600

pantalla = pygame.display.set_mode((ANCHO, ALTO))
reloj = pygame.time.Clock()

GRAVEDAD = 0.25
POTENCIA = 22

# Posición del cañón
origen = (90, ALTO - 30)

# Cada bala guarda:
# x, y, velocidad en x y velocidad en y
balas = []

# Creamos varios blancos
blancos = [
    {"x": x, "ancho": 60, "alto": 40}
    for x in range(350, 850, 90)
]

puntos = 0
angulo = 0
ganaste = False

# Fuentes para la pantalla de victoria
fuente_grande = pygame.font.Font(None, 80)
fuente_boton = pygame.font.Font(None, 40)

# Botón Aceptar
boton_aceptar = pygame.Rect(
    ANCHO // 2 - 100,
    ALTO // 2 + 60,
    200,
    60
)


def disparar(angulo):
    rad = math.radians(angulo)

    vx = POTENCIA * math.cos(rad)
    vy = -POTENCIA * math.sin(rad)

    balas.append({
        "x": origen[0],
        "y": origen[1],
        "vx": vx,
        "vy": vy
    })


ejecutando = True

while ejecutando:

    # 1) EVENTOS
    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            ejecutando = False

        # Si todavía no ganó, puede apuntar y disparar
        if not ganaste:

            if evento.type == pygame.MOUSEMOTION:

                mx, my = pygame.mouse.get_pos()

                angulo = math.degrees(
                    math.atan2(
                        origen[1] - my,
                        mx - origen[0]
                    )
                )

            elif evento.type == pygame.MOUSEBUTTONDOWN:
                disparar(angulo)

        # Si ganó, solamente controlamos el botón Aceptar
        else:

            if evento.type == pygame.MOUSEBUTTONDOWN:

                if boton_aceptar.collidepoint(evento.pos):
                    ejecutando = False

    # Solo calculamos la física mientras no haya ganado
    if not ganaste:

        # 2) FÍSICA DE CADA BALA
        for b in balas[:]:

            # La bala avanza según su velocidad
            b["x"] += b["vx"]
            b["y"] += b["vy"]

            # La gravedad hace que la bala vaya cayendo
            b["vy"] += GRAVEDAD

            # Rebote contra el piso
            if b["y"] > ALTO - 10:
                b["vy"] *= -0.7
                b["y"] = ALTO - 10

            # 3) COMPROBAR IMPACTO CONTRA LOS BLANCOS
            for blanco in blancos[:]:

                if (
                    blanco["x"] <= b["x"] <= blanco["x"] + blanco["ancho"]
                    and
                    ALTO - 90 <= b["y"] <= ALTO - 90 + blanco["alto"]
                ):
                    # Destruir el blanco
                    blancos.remove(blanco)

                    # Eliminar la bala que impactó
                    balas.remove(b)

                    # Sumar 10 puntos
                    puntos += 10

                    break

        # Comprobar si se destruyeron todos los blancos
        if len(blancos) == 0:
            ganaste = True

    # 4) DIBUJAR
    pantalla.fill((25, 25, 45))

    # Piso
    pygame.draw.rect(
        pantalla,
        (80, 220, 120),
        (0, ALTO - 10, ANCHO, 10)
    )

    # Dibujar blancos
    for blanco in blancos:
        pygame.draw.rect(
            pantalla,
            (220, 80, 80),
            (
                blanco["x"],
                ALTO - 90,
                blanco["ancho"],
                blanco["alto"]
            )
        )

    # Dibujar el cañón
    rad = math.radians(angulo)

    pygame.draw.line(
        pantalla,
        (240, 200, 60),
        origen,
        (
            origen[0] + 60 * math.cos(rad),
            origen[1] - 60 * math.sin(rad)
        ),
        6
    )

    # Dibujar las balas
    for b in balas:
        pygame.draw.circle(
            pantalla,
            (240, 240, 240),
            (int(b["x"]), int(b["y"])),
            8
        )

    # Pantalla de victoria
    if ganaste:

        # Texto GANASTE
        texto_ganaste = fuente_grande.render(
            "¡GANASTE!",
            True,
            (255, 255, 255)
        )

        rect_ganaste = texto_ganaste.get_rect(
            center=(ANCHO // 2, ALTO // 2 - 60)
        )

        pantalla.blit(texto_ganaste, rect_ganaste)

        # Mostrar puntaje
        texto_puntos = fuente_boton.render(
            f"Puntos: {puntos}",
            True,
            (255, 255, 255)
        )

        rect_puntos = texto_puntos.get_rect(
            center=(ANCHO // 2, ALTO // 2)
        )

        pantalla.blit(texto_puntos, rect_puntos)

        # Dibujar botón Aceptar
        pygame.draw.rect(
            pantalla,
            (80, 180, 100),
            boton_aceptar
        )

        texto_aceptar = fuente_boton.render(
            "Aceptar",
            True,
            (255, 255, 255)
        )

        rect_texto_aceptar = texto_aceptar.get_rect(
            center=boton_aceptar.center
        )

        pantalla.blit(
            texto_aceptar,
            rect_texto_aceptar
        )

    pygame.display.set_caption(
        f"Cañones - Puntos: {puntos}"
    )

    pygame.display.flip()

    reloj.tick(60)


pygame.quit()
sys.exit()