"""Arte 100% original del barrio uruguayo, creado con Pillow.

Uso: python herramientas/generar_uruguay.py
Produce edificios (farmacia, almacen, panaderia y casa), contenedores, carteles y muebles interiores.
Los vehiculos los genera generar_autos.py y el Palacio Legislativo generar_palacio.py.
No utiliza archivos de imagen de terceros ni requiere conexion a internet.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent / 'recursos'
ROOT.mkdir(parents=True, exist_ok=True)
INK = (27, 36, 40, 255)

def poly(d, pts, fill, outline=INK, width=3):
    d.polygon(pts, fill=fill)
    d.line(pts + [pts[0]], fill=outline, width=width, joint='curve')

def fuente(size=12):
    try:
        return ImageFont.truetype('DejaVuSans-Bold.ttf', size)
    except OSError:
        return ImageFont.load_default()

def letrero(d, cuadro, texto, color=(255,255,240), size=12):
    d.rounded_rectangle(cuadro, radius=2, fill=(30,66,66), outline=INK, width=2)
    f = fuente(size)
    x1,y1,x2,y2=cuadro
    bbox=d.textbbox((0,0),texto,font=f)
    x=(x1+x2-(bbox[2]-bbox[0]))//2
    # Centrar por caja real sin que las letras salgan de la marquesina.
    d.text((x, (y1+y2-(bbox[3]-bbox[1]))//2-bbox[1]), texto, font=f, fill=color)

def edificio(tipo):
    W,H=192,216
    im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
    mid=W//2; base=H-1
    # geometria del isometrico: una base 2x2 de 145x60 aproximadamente
    L,R=mid-73,mid+73
    Q=(R,base-34); S=(mid,base); T=(L,base-34)
    altura={0:116,1:88,2:105,3:101}[tipo]
    c={0:((222,229,215),(171,190,175)),1:((211,185,145),(156,126,93)),
       2:((187,125,100),(140,84,75)),3:((206,188,148),(152,135,112))}[tipo]
    izq,der=c
    poly(d,[(L,base-34-altura),(mid,base-altura),S,T],izq)
    poly(d,[(mid,base-altura),(R,base-34-altura),Q,S],der)
    # franjas / bloques en cada cara
    for offset in (25,52,80):
        if offset<altura-6:
            d.line([(L+4,base-34-offset),(mid-1,base-offset)],fill=(69,76,72,75),width=2)
            d.line([(mid+1,base-offset),(R-3,base-34-offset)],fill=(53,55,60,70),width=2)
    roof=[(L-7,base-35-altura),(mid,base-68-altura),(R+7,base-35-altura),(mid,base+2-altura)]
    if tipo==0: roofcolor=(53,138,102)
    elif tipo==1: roofcolor=(104,87,70)
    elif tipo==2: roofcolor=(122,63,62)
    elif tipo==3: roofcolor=(74,96,96)
    else: roofcolor=(122,129,117)
    poly(d,roof,roofcolor,width=4)
    # Fachada derecha con ventanas inclinadas y puerta
    for k in range(2):
        for xx in (mid+15,mid+47):
            yy=round(base-altura-((xx-mid)/73)*34+24+k*36)
            poly(d,[(xx,yy),(xx+19,yy-8),(xx+19,yy+14),(xx,yy+22)],(41,71,84),width=2)
            d.line([(xx+8,yy-3),(xx+8,yy+19)],fill=(206,215,204),width=2)
            d.line([(xx,yy+11),(xx+19,yy+3)],fill=(188,215,212),width=1)
    # Puerta de ingreso iluminada en fachada frontal
    poly(d,[(mid+12,base-47),(mid+41,base-61),(mid+41,base-19),(mid+12,base-6)],(41,62,61),width=2)
    d.line([(mid+33,base-31),(mid+35,base-32)],fill=(237,209,109),width=3)
    if tipo==0: # farmacia cruz verde
        letrero(d,(mid+5,base-70,mid+68,base-52),'FARMASHOP',size=8)
        d.rounded_rectangle((mid-50,base-80,mid-27,base-54),3,fill=(238,247,236),outline=(46,129,86),width=2)
        d.rectangle((mid-43,base-75,mid-36,base-58),fill=(38,174,95))
        d.rectangle((mid-48,base-69,mid-31,base-64),fill=(38,174,95))
        d.line((L+3,base-45,mid-2,base-77),fill=(45,172,111),width=6)
    elif tipo==1:
        letrero(d,(mid+5,base-70,mid+68,base-52),'ALMACEN',size=10)
        d.polygon([(L+4,base-73),(mid-5,base-99),(mid-5,base-86),(L+4,base-60)],fill=(201,106,67))
        for i in range(6):d.line([(L+5+i*11,base-73-i*4),(L+5+i*11,base-60-i*4)],fill=(247,203,138),width=4)
    elif tipo==2:
        letrero(d,(mid-1,base-78,mid+70,base-59),'PANADERIA',size=9)
        # Toldito a rayas sobre escaparate
        for i in range(7):
            x=mid+4+i*9
            d.line((x,base-59+i*3,x+1,base-47+i*3), fill=(222,188,128) if i%2 else (143,59,56), width=7)
        d.ellipse((mid-51,base-76,mid-28,base-59),fill=(227,190,111),outline=INK,width=2)
        d.line((mid-45,base-64,mid-35,base-70),fill=(161,107,65),width=2)
    elif tipo==3:
        d.polygon([(L+7,base-71),(mid-9,base-94),(mid-9,base-68),(L+7,base-45)],fill=(84,117,110),outline=INK)
        d.line([(L+8,base-69),(mid-12,base-93)],fill=(184,226,194),width=2)
        letrero(d,(mid+12,base-67,mid+61,base-53),'CASA',size=11)
    im.save(ROOT/f'edificio_{tipo}.png')

def tacho():
    """Tacho de basura de calle (verde, como los de Montevideo), sin texto.
    Se ancla por el centro de su base: el centro de la elipse inferior queda 12 px
    sobre el borde de abajo del PNG."""
    im=Image.new('RGBA',(60,80));d=ImageDraw.Draw(im)
    cx,base,tope=30,67,28                      # centro x, centro de la base, centro de la boca
    verde,verde_osc,verde_claro=(46,120,86),(32,86,64),(72,156,112)
    gris,gris_claro=(86,94,92),(132,142,138)
    # cuerpo: tronco de cono (mas angosto abajo)
    d.ellipse((cx-14,base-6,cx+14,base+6),fill=verde_osc,outline=INK,width=2)
    d.polygon([(cx-18,tope),(cx+18,tope),(cx+14,base),(cx-14,base)],fill=verde)
    d.polygon([(cx+4,tope),(cx+18,tope),(cx+14,base),(cx+4,base)],fill=verde_osc)   # lado en sombra
    d.ellipse((cx-14,base-6,cx+14,base+6),fill=verde)
    d.polygon([(cx-18,tope),(cx+18,tope),(cx+14,base),(cx-14,base)],fill=verde)
    d.polygon([(cx+5,tope),(cx+18,tope),(cx+14,base),(cx+5,base+1)],fill=verde_osc)
    d.line([(cx-18,tope),(cx-14,base)],fill=INK,width=2)
    d.line([(cx+18,tope),(cx+14,base)],fill=INK,width=2)
    d.arc((cx-14,base-6,cx+14,base+6),0,180,fill=INK,width=2)
    # nervaduras verticales y franja de reciclaje
    for k in (-9,-3,3,9):
        d.line([(cx+k*1.25,tope+6),(cx+k*0.95,base-1)],fill=verde_claro if k<5 else verde_osc,width=1)
    d.polygon([(cx-17,tope+15),(cx+17,tope+15),(cx+16,tope+21),(cx-16,tope+21)],fill=(226,230,214))
    for k in (-8,0,8):                          # tres flechitas de reciclaje (puntos), sin letras
        d.polygon([(cx+k,tope+16),(cx+k+3,tope+19),(cx+k-3,tope+19)],fill=(46,120,86))
    # aro superior y tapa
    d.ellipse((cx-19,tope-6,cx+19,tope+6),fill=gris,outline=INK,width=2)
    d.ellipse((cx-17,tope-9,cx+17,tope+3),fill=gris_claro,outline=INK,width=2)
    d.ellipse((cx-5,tope-8,cx+5,tope-3),fill=gris,outline=INK,width=1)               # manija
    # un papel que se asoma por el borde
    d.polygon([(cx+9,tope+1),(cx+17,tope-2),(cx+16,tope+4)],fill=(232,226,200),outline=INK)
    im.save(ROOT/'contenedor.png')


def decoraciones():
    tacho()
    for i,calle in enumerate(('18 DE JULIO','AGRACIADA','BV. ARTIGAS')):
        im=Image.new('RGBA',(120,125));d=ImageDraw.Draw(im)
        d.line((57,111,57,24),fill=(170,176,165),width=6)
        d.ellipse((53,105,62,116),fill=(74,79,74))
        d.rounded_rectangle((9,9,113,37),radius=5,fill=(37,120,79),outline=(223,230,205),width=2)
        d.text((15,16),calle,font=fuente(10),fill=(238,246,229))
        d.line((50,39,66,39),fill=(216,226,201),width=3)
        im.save(ROOT/f'cartel_{i}.png')


def muebles():
    colores={'estante':((103,72,51),(167,138,95)), 'mostrador':((110,89,70),(172,143,110)),
             'horno':((81,90,96),(172,179,172)), 'mesa':((116,91,67),(179,143,100)),
             'armario':((83,79,69),(136,123,98)), 'columna':((130,135,132),(217,211,191))}
    for tipo,(oscuro,claro) in colores.items():
        im=Image.new('RGBA',(78,94));d=ImageDraw.Draw(im)
        poly(d,[(9,66),(37,52),(69,67),(40,83)],oscuro)
        poly(d,[(9,66),(40,83),(40,91),(9,75)],oscuro)
        poly(d,[(40,83),(69,67),(69,75),(40,91)],claro)
        if tipo=='columna':
            d.rectangle((23,11,55,65),fill=claro,outline=INK,width=3)
            d.rectangle((17,8,61,17),fill=(217,217,208),outline=INK,width=2)
            d.rectangle((19,63,59,72),fill=oscuro,outline=INK,width=2)
            for x in (28,37,46,54):d.line((x,18,x,62),fill=(126,125,113),width=2)
        elif tipo=='mesa':
            for x in (19,56):d.line((x,46,x,73),fill=oscuro,width=5)
            poly(d,[(9,43),(38,28),(70,43),(40,60)],claro)
        else:
            poly(d,[(8,20),(35,8),(66,22),(40,37)],claro)
            poly(d,[(8,20),(40,37),(40,76),(8,59)],oscuro)
            poly(d,[(40,37),(66,22),(66,60),(40,76)],claro)
            for y in (36,53):
                d.line((10,y,38,y+16),fill=(46,50,49),width=3)
                d.line((42,y+15,65,y+2),fill=(66,69,62),width=3)
            if tipo=='estante':
                for xx,yy,cc in ((14,31,(221,94,92)),(25,39,(224,203,111)),(45,48,(121,180,117)),(50,66,(210,180,98))):
                    d.rectangle((xx,yy,xx+7,yy+7),fill=cc)
            if tipo=='horno':
                d.rectangle((17,36,38,55),fill=(37,50,60),outline=(199,210,214))
                d.ellipse((23,18,29,24),fill=(240,144,72))
        im.save(ROOT/f'mueble_{tipo}.png')

if __name__ == '__main__':
    for tipo in range(4): edificio(tipo)   # el Palacio (4) lo genera herramientas/generar_palacio.py
    # Los vehiculos los genera herramientas/generar_autos.py (python herramientas/generar_autos.py)
    decoraciones()   # tacho de basura (contenedor.png) y 3 carteles
    muebles()
    print('Generados 4 edificios (el Palacio lo genera generar_palacio.py), tacho, 3 carteles y 6 muebles originales.')
