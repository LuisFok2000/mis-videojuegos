import sys
import pygame

pygame.init()
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
reloj = pygame.time.Clock()
fuente = pygame.font.Font(None, 58)

pala = pygame.Rect(ANCHO // 2 - 60, ALTO - 40, 120, 15)
pelota = pygame.Rect(ANCHO // 2 - 8, ALTO // 2, 16, 16)
vel_x, vel_y = 5, -5

ladrillos = []
for fila in range(4):
    for col in range(10):
        ladrillos.append(pygame.Rect(col * 80 + 5, fila * 30 + 40, 70, 20))

vidas = 3
puntaje = 0
destruidos = 0
resultado = None

ejecutando = True
while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

    if resultado is None:
        # La paleta sigue al mouse sin salir de la pantalla.
        pala.x = pygame.mouse.get_pos()[0] - pala.width // 2
        pala.x = max(0, min(ANCHO - pala.width, pala.x))

        pelota.x += vel_x
        pelota.y += vel_y

        if pelota.left <= 0:
            pelota.left = 0
            vel_x = abs(vel_x)
        elif pelota.right >= ANCHO:
            pelota.right = ANCHO
            vel_x = -abs(vel_x)
        if pelota.top <= 0:
            pelota.top = 0
            vel_y = abs(vel_y)

        if pelota.colliderect(pala) and vel_y > 0:
            pelota.bottom = pala.top
            vel_y = -abs(vel_y)

        # Recorremos una copia para poder eliminar ladrillos.
        for ladrillo in ladrillos[:]:
            if pelota.colliderect(ladrillo):
                ladrillos.remove(ladrillo)
                puntaje += 10
                destruidos += 1
                vel_y *= -1
                # Cada cinco ladrillos la pelota acelera.
                if destruidos % 5 == 0:
                    vel_x += 1 if vel_x > 0 else -1
                    vel_y += 1 if vel_y > 0 else -1
                break

        if not ladrillos:
            resultado = '¡Ganaste!'
        elif pelota.top >= ALTO:
            vidas -= 1
            if vidas == 0:
                resultado = 'Perdiste'
            else:
                pelota.center = (ANCHO // 2, ALTO // 2)
                vel_x = 5 if vel_x > 0 else -5
                vel_y = -5

    pantalla.fill((15, 15, 30))
    pygame.draw.rect(pantalla, (90, 180, 255), pala)
    pygame.draw.ellipse(pantalla, (255, 255, 255), pelota)
    for ladrillo in ladrillos:
        pygame.draw.rect(pantalla, (255, 120, 120), ladrillo)

    pygame.display.set_caption(f'Arkanoid - Vidas: {vidas} - Puntaje: {puntaje} - Ladrillos: {len(ladrillos)}')
    if resultado is not None:
        mensaje = fuente.render(resultado, True, (255, 255, 255))
        pantalla.blit(mensaje, mensaje.get_rect(center=(ANCHO // 2, ALTO // 2)))
    pygame.display.flip()
    reloj.tick(60)

pygame.quit()
sys.exit()
