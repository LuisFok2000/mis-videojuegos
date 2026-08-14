import random
import sys
import pygame

pygame.init()

ANCHO, ALTO = 600, 600
CELDA = 30

COLUMNAS = ANCHO // CELDA
FILAS = ALTO // CELDA

pantalla = pygame.display.set_mode((ANCHO, ALTO))
reloj = pygame.time.Clock()

# El cuerpo de la serpiente.
# Cada elemento representa una posición (columna, fila).
# El primer elemento es la cabeza.
serpiente = [(5, 5)]

# (dx, dy): inicialmente se mueve hacia la derecha.
direccion = (1, 0)


def manzana_nueva():
    while True:
        m = (
            random.randint(0, COLUMNAS - 1),
            random.randint(0, FILAS - 1)
        )

        if m not in serpiente:
            return m


manzana = manzana_nueva()
puntos = 0
manzana_dorada = None

# Leer récord guardado
try:
    with open("record.txt") as f:
        record = int(f.read())
except FileNotFoundError:
    record = 0


def dibujar_celda(pos, color):
    pygame.draw.rect(
        pantalla,
        color,
        (
            pos[0] * CELDA,
            pos[1] * CELDA,
            CELDA - 2,
            CELDA - 2
        )
    )


ejecutando = True

while ejecutando:

    # 1) LEER TECLADO
    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            ejecutando = False

        elif evento.type == pygame.KEYDOWN:

            # No permitimos girar 180 grados.
            if evento.key == pygame.K_UP and direccion != (0, 1):
                direccion = (0, -1)

            elif evento.key == pygame.K_DOWN and direccion != (0, -1):
                direccion = (0, 1)

            elif evento.key == pygame.K_LEFT and direccion != (1, 0):
                direccion = (-1, 0)

            elif evento.key == pygame.K_RIGHT and direccion != (-1, 0):
                direccion = (1, 0)

    # 2) CREAR LA NUEVA POSICIÓN DE LA CABEZA
    cabeza = (
        serpiente[0][0] + direccion[0],
        serpiente[0][1] + direccion[1]
    )

    serpiente.insert(0, cabeza)

    # 3) COMPROBAR SI COMIÓ
    if cabeza == manzana:
        puntos += 1
        manzana = manzana_nueva()

        # 20% de probabilidad de que aparezca una manzana dorada
        if random.random() < 0.2:
            manzana_dorada = manzana_nueva()

    elif cabeza == manzana_dorada:
        puntos += 5
        manzana_dorada = None

    else:
        # Si no comió, eliminamos la cola.
        serpiente.pop()

    # 4) COMPROBAR COLISIONES
    if (
        cabeza[0] < 0
        or cabeza[0] >= COLUMNAS
        or cabeza[1] < 0
        or cabeza[1] >= FILAS
        or cabeza in serpiente[1:]
    ):
        ejecutando = False

    # Actualizar y guardar récord
    if puntos > record:
        record = puntos

        with open("record.txt", "w") as f:
            f.write(str(record))

    # 5) DIBUJAR
    pantalla.fill((10, 10, 15))

    for segmento in serpiente:
        dibujar_celda(segmento, (0, 220, 60))

    # Manzana normal
    dibujar_celda(manzana, (230, 40, 40))

    # Manzana dorada si existe
    if manzana_dorada is not None:
        dibujar_celda(manzana_dorada, (255, 215, 0))

    # Mostrar puntos y récord en el título
    pygame.display.set_caption(
        f"Puntos: {puntos} | Récord: {record}"
    )

    pygame.display.flip()

    # Velocidad de la serpiente
    reloj.tick(10)


pygame.quit()

print(f"Fin del juego. Puntos: {puntos}")

sys.exit()