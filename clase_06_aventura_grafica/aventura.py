import sys
import pygame

pygame.init()

ANCHO, ALTO = 900, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Aventura en la Selva")

reloj = pygame.time.Clock()
fuente = pygame.font.SysFont("arial", 26)

# =========================
# HISTORIA
# =========================

historia = {
    "inicio": {
        "texto": "Estás en la selva. Escuchás un ruido entre los árboles.",
        "opciones": [
            ("Ir a investigar", "cueva"),
            ("Seguir el sendero", "rio")
        ],
    },

    "cueva": {
        "texto": "Dentro de la cueva hay un cofre dorado. Un mono lo custodia.",
        "opciones": [
            ("Hablar con el mono", "mono"),
            ("Abrir el cofre a escondidas", "cofre")
        ],
    },

    "rio": {
        "texto": "Llegás a un río. Junto a la orilla encontrás una banana.",
        "opciones": [
            ("Recoger la banana", "banana"),
            ("Volver a la selva", "inicio")
        ],
    },

    "banana": {
        "texto": "Recogiste la banana. Quizás pueda servirte más adelante.",
        "opciones": [
            ("Ir hacia la cueva", "cueva"),
            ("Volver al río", "rio")
        ],
    },

    "mono": {
        "texto": "El mono habla: '¡Dame una banana y el tesoro será tuyo!'",
        "opciones": [
            ("Negarme", "inicio")
        ],
    },

    "cofre": {
        "texto": "Intentás abrir el cofre, pero el mono te descubre y te echa de la cueva.",
        "opciones": [
            ("Volver a intentarlo", "inicio")
        ],
    },

    "tesoro": {
        "texto": "¡Le diste la banana al mono y ganaste el tesoro legendario de la selva! Fin.",
        "opciones": [],
    }
}

# =========================
# INVENTARIO
# =========================

tiene_banana = False
escena = "inicio"


def obtener_opciones():
    opciones = list(historia[escena]["opciones"])

    # Si estamos hablando con el mono y tenemos la banana,
    # aparece una opción nueva.
    if escena == "mono" and tiene_banana:
        opciones.insert(0, ("Dar la banana", "tesoro"))

    return opciones


# =========================
# COLORES SEGÚN ESCENA
# =========================

def obtener_color_fondo():
    if escena in ["cueva", "mono", "cofre", "tesoro"]:
        return (45, 45, 45)

    elif escena in ["rio", "banana"]:
        return (20, 70, 120)

    else:
        return (20, 80, 30)


# =========================
# BOTONES
# =========================

def dibujar_botones(opciones):
    botones = []

    y = ALTO - 40 * len(opciones) - 20

    for texto, _ in opciones:
        rect = pygame.Rect(ANCHO // 2 - 200, y, 400, 34)

        pygame.draw.rect(pantalla, (60, 60, 130), rect)

        pantalla.blit(
            fuente.render(texto, True, (255, 255, 255)),
            (rect.x + 12, rect.y + 4)
        )

        botones.append((rect, texto))
        y += 44

    return botones


# =========================
# TEXTO
# =========================

def dibujar_texto(texto, limite=45):
    palabras = texto.split()

    lineas = []
    actual = ""

    for palabra in palabras:
        if len(actual) + len(palabra) + 1 > limite:
            lineas.append(actual)
            actual = palabra
        else:
            actual = actual + " " + palabra

    if actual:
        lineas.append(actual)

    y = 150

    for linea in lineas:
        pantalla.blit(
            fuente.render(linea, True, (255, 255, 255)),
            (80, y)
        )

        y += 34


# =========================
# BUCLE PRINCIPAL
# =========================

ejecutando = True

while ejecutando:

    opciones = obtener_opciones()

    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            ejecutando = False

        elif evento.type == pygame.MOUSEBUTTONDOWN and opciones:

            mx, my = pygame.mouse.get_pos()

            botones = dibujar_botones(opciones)

            for i, (rect, _) in enumerate(botones):

                if rect.collidepoint(mx, my):

                    nueva_escena = opciones[i][1]

                    # Si elegimos recoger la banana,
                    # la agregamos al inventario.
                    if escena == "rio" and nueva_escena == "banana":
                        tiene_banana = True

                    escena = nueva_escena

                    if not historia[escena]["opciones"]:
                        print("La aventura terminó.")

                    break

    # Fondo diferente dependiendo de la escena
    pantalla.fill(obtener_color_fondo())

    # Título
    pantalla.blit(
        fuente.render(
            "AVENTURA EN LA SELVA",
            True,
            (255, 200, 60)
        ),
        (80, 60)
    )

    # Texto de la escena
    dibujar_texto(historia[escena]["texto"])

    # Mostrar inventario
    if tiene_banana:
        pantalla.blit(
            fuente.render(
                "Inventario: Banana",
                True,
                (255, 255, 255)
            ),
            (80, 100)
        )
    else:
        pantalla.blit(
            fuente.render(
                "Inventario: vacío",
                True,
                (255, 255, 255)
            ),
            (80, 100)
        )

    # Botones
    opciones = obtener_opciones()
    dibujar_botones(opciones)

    pygame.display.flip()
    reloj.tick(30)


pygame.quit()
sys.exit()