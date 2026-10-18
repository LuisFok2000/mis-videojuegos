import sys
import pygame

pygame.init()
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
reloj = pygame.time.Clock()
fuente = pygame.font.Font(None, 54)

GRAVEDAD = 0.5
VEL_MOV = 6
FUERZA_SALTO = -13

plataformas = [
    pygame.Rect(0, ALTO - 40, ANCHO, 40),
    pygame.Rect(200, 450, 180, 25),
    pygame.Rect(450, 360, 180, 25),
    pygame.Rect(600, 250, 180, 25),
]
bananas_iniciales = [(250, 420), (500, 330), (650, 220)]

# Enemigos que patrullan sobre las plataformas.
enemigos = [
    {'rect': pygame.Rect(270, 425, 25, 25), 'izq': 200, 'der': 380, 'vel': 2},
    {'rect': pygame.Rect(530, 335, 25, 25), 'izq': 450, 'der': 630, 'vel': -2},
]

mono = pygame.Rect(100, 300, 40, 40)
pos_y = float(mono.y)
vel_y = 0
vidas = 3
juntas = 0
bananas = [pygame.Rect(x, y, 20, 20) for x, y in bananas_iniciales]
inicio = pygame.time.get_ticks()
resultado = None
segundos_finales = 0
inmune_hasta = 0
en_piso = False

def reiniciar_posicion():
    global pos_y, vel_y
    mono.topleft = (100, 300)
    pos_y = float(mono.y)
    vel_y = 0

ejecutando = True
while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        elif evento.type == pygame.KEYDOWN and resultado is None:
            if evento.key == pygame.K_SPACE and en_piso:
                vel_y = FUERZA_SALTO

    if resultado is None:
        ahora = pygame.time.get_ticks()
        segundos = (ahora - inicio) // 1000
        teclas = pygame.key.get_pressed()
        vel_x = (int(teclas[pygame.K_RIGHT]) - int(teclas[pygame.K_LEFT])) * VEL_MOV
        mono.x += vel_x
        # Puede salirse por los costados y caer: se reinicia al caer al vacío.
        anterior_abajo = mono.bottom
        vel_y += GRAVEDAD
        pos_y += vel_y
        mono.y = round(pos_y)

        en_piso = False
        for p in plataformas:
            if mono.colliderect(p) and vel_y >= 0 and anterior_abajo <= p.top:
                mono.bottom = p.top
                pos_y = float(mono.y)
                vel_y = 0
                en_piso = True
                break

        for banana in bananas[:]:
            if mono.colliderect(banana):
                bananas.remove(banana)
                juntas += 1

        for enemigo in enemigos:
            caja = enemigo['rect']
            caja.x += enemigo['vel']
            if caja.left <= enemigo['izq'] or caja.right >= enemigo['der']:
                enemigo['vel'] *= -1
                caja.x = max(enemigo['izq'], min(enemigo['der'] - caja.width, caja.x))
            if mono.colliderect(caja) and ahora >= inmune_hasta:
                vidas -= 1
                if vidas <= 0:
                    resultado = 'Perdiste'
                    segundos_finales = segundos
                else:
                    reiniciar_posicion()
                    inmune_hasta = ahora + 1200
                break

        if mono.top > ALTO:
            # Al caer, vuelven a aparecer las bananas y se reinicia el contador.
            reiniciar_posicion()
            bananas = [pygame.Rect(x, y, 20, 20) for x, y in bananas_iniciales]
            juntas = 0
            inicio = pygame.time.get_ticks()

        if not bananas and resultado is None:
            resultado = '¡Ganaste!'
            segundos_finales = segundos
    else:
        segundos = segundos_finales

    pantalla.fill((150, 210, 255))
    for p in plataformas:
        pygame.draw.rect(pantalla, (90, 60, 30), p)
    pygame.draw.rect(pantalla, (160, 110, 50), mono)
    for b in bananas:
        pygame.draw.circle(pantalla, (255, 220, 60), b.center, 10)
    for enemigo in enemigos:
        pygame.draw.rect(pantalla, (210, 60, 60), enemigo['rect'])

    pygame.display.set_caption(f'El Mono - Bananas: {juntas}/3 - Vidas: {vidas} - Tiempo: {segundos}s')
    if resultado is not None:
        mensaje = fuente.render(f'{resultado} - {segundos_finales} segundos', True, (20, 20, 20))
        pantalla.blit(mensaje, mensaje.get_rect(center=(ANCHO // 2, 170)))
    pygame.display.flip()
    reloj.tick(60)

pygame.quit()
sys.exit()
