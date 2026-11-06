"""Sprites originales de Dead Zone generados por codigo, sin material externo.

Para recrear: python -m pip install Pillow; python herramientas/generar_personajes.py
"""
from pathlib import Path
from PIL import Image, ImageDraw

OUT = Path(__file__).resolve().parent.parent / 'recursos'
OUT.mkdir(exist_ok=True)


def humano(nombre, piel, remera, pantalon, detalle, pose=0):
    im = Image.new('RGBA', (80, 96), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    dark = (25, 33, 34, 255)
    # Botas y piernas disparejas por silueta y pose.
    d.polygon([(31, 61), (40, 64), (38 + pose, 84), (30 + pose, 85), (27, 78)], fill=pantalon, outline=dark)
    d.polygon([(42, 62), (50, 60), (54 - pose, 83), (46 - pose, 86), (42, 78)], fill=pantalon, outline=dark)
    d.ellipse((26 + pose, 80, 40 + pose, 87), fill=(42, 39, 34), outline=dark)
    d.ellipse((44 - pose, 80, 57 - pose, 87), fill=(43, 40, 33), outline=dark)
    d.polygon([(27, 38), (34, 33), (48, 34), (55, 40), (52, 66), (29, 65)], fill=remera, outline=dark)
    d.polygon([(35, 35), (43, 38), (48, 36), (43, 49), (36, 49)], fill=tuple(min(255,x+18) for x in remera), outline=dark)
    d.line([(28, 44), (20 - pose, 60), (16 - pose, 65)], fill=piel, width=8)
    d.line([(52, 43), (60 + pose, 55), (65 + pose, 61)], fill=piel, width=8)
    d.ellipse((29, 12, 52, 39), fill=piel, outline=dark, width=2)
    d.ellipse((31, 28, 50, 39), fill=tuple(max(0,x-22) for x in piel))
    if nombre == 'jugador':
        # Chaleco, mochila, gorra, pistola, rasguños.
        d.polygon([(29, 39), (35, 35), (39, 47), (33, 61), (28, 57)], fill=(53, 84, 72), outline=dark)
        d.polygon([(52, 40), (47, 36), (43, 47), (49, 61), (55, 56)], fill=(49, 86, 80), outline=dark)
        d.rectangle((35, 54, 48, 62), fill=(110, 81, 52), outline=(45, 34, 28))
        d.rectangle((18, 55, 28, 59), fill=(57, 55, 51), outline=dark)
        d.rectangle((17, 54, 21, 67), fill=(54, 51, 46))
        d.polygon([(27, 17), (32, 9), (47, 9), (53, 19), (49, 22), (29, 22)], fill=(57, 72, 65), outline=dark)
        d.line((33, 22, 55, 23), fill=(38, 49, 46), width=4)
        d.ellipse((33, 26, 36, 29), fill=(28, 32, 31))
        d.ellipse((44, 26, 47, 29), fill=(28, 32, 31))
        d.line((37, 35, 47, 35), fill=(93, 54, 43), width=2)
    else:
        # Ojos infectados y heridas; marcas en la ropa.
        d.ellipse((33, 25, 38, 30), fill=(238, 68, 64), outline=(87, 36, 29))
        d.ellipse((44, 25, 49, 30), fill=(238, 68, 64), outline=(87, 36, 29))
        d.line((36, 34, 46, 33), fill=(95, 45, 42), width=2)
        d.polygon([(34, 49), (47, 46), (45, 53), (35, 56)], fill=(134, 48, 48))
        d.line((35, 60, 42, 65), fill=(92, 41, 39), width=2)
        if nombre == 'corredor':
            d.polygon([(30, 35), (50, 34), (53, 39), (28, 41)], fill=(220, 128, 65), outline=dark)
            d.line((19, 58, 11, 46), fill=piel, width=6)
            d.line((62, 57, 69, 45), fill=piel, width=6)
            d.line((33, 15, 48, 13), fill=(47, 30, 28), width=5)
        elif nombre == 'blindado':
            # Casco, visor, placa balistica con remaches.
            d.polygon([(27, 21), (27, 13), (33, 6), (49, 6), (55, 14), (55, 24)], fill=(45, 76, 97), outline=dark)
            d.rectangle((29, 20, 53, 28), fill=(43, 51, 60), outline=(17, 25, 28), width=2)
            d.line((32, 22, 50, 22), fill=(91, 174, 193), width=2)
            d.polygon([(28, 38), (53, 38), (55, 60), (29, 61)], fill=(53, 78, 91), outline=(22, 31, 37))
            d.rectangle((32, 42, 49, 55), fill=(78, 104, 113), outline=(30, 49, 60), width=2)
            for x, y in [(32, 42), (49, 42), (32, 55), (49, 55)]:
                d.ellipse((x-1, y-1, x+1, y+1), fill=(180, 194, 184))
        elif nombre == 'escupidor':
            d.ellipse((27, 30, 55, 45), fill=(119, 150, 65), outline=(47, 64, 38), width=2)
            d.ellipse((33, 33, 49, 41), fill=(93, 39, 126), outline=(69, 24, 83))
            d.ellipse((47, 37, 57, 48), fill=(154, 214, 61))
            d.ellipse((59, 37, 69, 47), fill=(144, 220, 64))
            d.line((55, 44, 63, 42), fill=(172, 247, 86), width=3)
            d.ellipse((30, 46, 37, 56), fill=(145, 221, 81))
        elif nombre == 'jefe':
            d.polygon([(27, 38), (33, 28), (51, 30), (57, 42), (57, 62), (26, 65)], fill=(102, 59, 59), outline=dark, width=2)
            d.line((23, 40, 13, 34), fill=(125, 48, 47), width=8)
            d.polygon([(30, 16), (26, 6), (35, 11), (43, 3), (48, 12), (57, 5), (53, 20)], fill=(68, 49, 43), outline=dark)
            d.ellipse((38, 48, 46, 58), fill=(230, 81, 57))
    im.save(OUT / f'personaje_{nombre}.png')
    if nombre == 'blindado':
        # Variante con visor quebrado y placa arrancada tras un golpe de bate.
        roto = im.copy()
        rd = ImageDraw.Draw(roto)
        rd.polygon([(31,43),(52,44),(48,60),(28,60)],fill=(93,104,78),outline=dark)
        rd.line([(30,19),(47,26),(35,31),(51,34)],fill=(238,183,114),width=3)
        rd.line([(45,44),(34,52),(44,56)],fill=(174,70,70),width=3)
        rd.polygon([(47,38),(56,46),(57,58),(50,57)],fill=(51,75,86))
        roto.save(OUT/'personaje_blindado_roto.png')

humano('jugador', (215, 175, 132), (68, 116, 126), (45, 49, 53), (90, 130, 115))
humano('comun', (143, 169, 113), (95, 111, 75), (55, 61, 52), (134, 54, 55))
humano('corredor', (170, 147, 102), (158, 86, 49), (69, 59, 54), (215, 147, 79), pose=4)
humano('blindado', (128, 157, 127), (48, 76, 87), (46, 58, 64), (79, 156, 187))
humano('escupidor', (151, 173, 94), (105, 63, 116), (55, 45, 66), (178, 219, 85))
humano('jefe', (151, 83, 78), (95, 54, 54), (55, 41, 39), (211, 81, 72))
print('Generados seis sprites de personajes originales en', OUT)
