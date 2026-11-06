"""Dibujo del mundo: terreno, edificios, objetos, personajes y efectos.
Solo dibuja: no cambia las reglas del juego. El panel inferior y los menus
estan en dibujo_panel.py."""
import math
import pygame

import mapa
from mapa import ANCHO, TW, TH
import interiores
import efectos
import escenario
from combate import alcance, distancia, tiro_valido
from enemigo import TIPOS
from pantalla import (lienzo, texto, vertice_superior, rombo, fuente_chica, fuente_media,
                      fuente_etiqueta, fuente_puerta, PANEL_Y)


def _sprite(celda, tipo, variante=0, jugador_rect=None):
    """Dibuja un PNG del juego anclado a su casilla (ver escenario.dibujar)."""
    escenario.dibujar(lienzo, vertice_superior, celda, tipo, variante, jugador_rect)


def dibujar_terreno(celda, hover, g):
    col,row=celda
    if mapa.EN_INTERIOR:
        tipo = mapa.TIPO_INTERIOR
        paleta = {0:(177,192,177),1:(177,155,126),2:(181,140,112),
                  3:(148,140,124),4:(187,184,173)}[tipo]
        base = tuple(max(0,v-10) if (col+row)%2 else v for v in paleta)
        if celda in mapa.MUROS:
            base = tuple(max(0, int(v*.69)) for v in base)
        if celda == hover and celda not in mapa.MUROS:
            base = tuple(min(255,int(v*.7+70)) for v in base)
        rombo(celda,base,(91,91,78))
        x,y=vertice_superior(celda)
        if (row*3+col)%4==0:
            pygame.draw.line(lienzo,(120,112,101),(x-5,y+13),(x+3,y+20),1)
        if celda == interiores.ENTRADA:
            pygame.draw.circle(lienzo,(54,167,164),(x,y+TH//2),18,3)
        return
    (f0,f1),(c0,c1)=mapa.CALLES
    road = f0 <= row <= f1 or c0 <= col <= c1
    vereda = f0-1 <= row <= f1+1 or c0-1 <= col <= c1+1
    if road:
        base=(66,70,69) if (col+row)%3 else (69,73,71)
    elif vereda:
        base=(119,116,103) if (col+row)%2 else (125,121,107)
    else:
        base=mapa.PASTO[0] if (col*3+row)%3 else mapa.PASTO[1]
    if celda==hover and celda not in mapa.MUROS:
        base=tuple(min(255,int(v*.65+110*.35)) for v in base)
    rombo(celda,base)
    x,y=vertice_superior(celda)
    if not road and vereda:
        if col in (c0-1,c1+1) or row in (f0-1,f1+1):
            pygame.draw.line(lienzo,(167,158,130),(x-15,y+TH//2),(x+15,y+TH//2),2)
        if (col+row)%3==0:
            pygame.draw.line(lienzo,(91,89,82),(x-7,y+11),(x+2,y+17),1)
    if road and (row==mapa.LINEA[0] or col==mapa.LINEA[1]):
        if (col+row)%3==0:
            pygame.draw.line(lienzo,(198,169,99),(x-9,y+TH//2),(x+9,y+TH//2),3)
    if (col*7+row*11)%17==0:
        pygame.draw.line(lienzo,(44,50,48),(x-11,y+10),(x-2,y+16),2)
        pygame.draw.line(lienzo,(44,50,48),(x-2,y+16),(x+3,y+14),1)
    if (col*17+row*13)%29==0:
        pygame.draw.circle(lienzo,(112,54,49),(x+6,y+17),3)
    if celda == mapa.REFUGIO:
        pygame.draw.polygon(lienzo,(31,105,77),[(x,y+1),(x+TW//2-3,y+TH//2),(x,y+TH-2),(x-TW//2+3,y+TH//2)])
        pygame.draw.polygon(lienzo,(152,221,156),[(x,y+1),(x+TW//2-3,y+TH//2),(x,y+TH-2),(x-TW//2+3,y+TH//2)],2)
    if celda in mapa.PUERTAS:
        pygame.draw.polygon(lienzo,(35,124,130),[(x,y+3),(x+TW//2-2,y+TH//2),(x,y+TH-3),(x-TW//2+2,y+TH//2)])
        pygame.draw.polygon(lienzo,(134,237,221),[(x,y+3),(x+TW//2-2,y+TH//2),(x,y+TH-3),(x-TW//2+2,y+TH//2)],2)


_RECORTES = {}

def _sprite_recortado(nombre, escala=1.0):
    """Sprite recortado a su parte visible: el borde inferior del PNG son los pies.
    (Los PNG traen margen transparente debajo; sin recortarlo el personaje levita.)
    El resultado se guarda para no recortar ni escalar en cada fotograma."""
    clave = (nombre, escala)
    if clave not in _RECORTES:
        imagen = escenario.IMAGENES[nombre]
        imagen = imagen.subsurface(imagen.get_bounding_rect()).copy()
        if escala != 1.0:
            imagen = pygame.transform.smoothscale(
                imagen, (round(imagen.get_width() * escala), round(imagen.get_height() * escala)))
        _RECORTES[clave] = imagen
    return _RECORTES[clave]


ASPECTO_JUGADOR = {'sprite': 'jugador', 'escala': 1.0, 'ritmo': 350.0}


def dibujar_personaje(celda, tipo='jugador', z=None, g=None):
    """Sprite propio con respiracion, balanceo leve y paso al moverse.

    El aspecto de cada tipo (sprite, escala, ritmo) sale de escenario.ASPECTO_ENEMIGO.
    Los pies quedan siempre apoyados en el centro de la baldosa: al caminar el
    cuerpo da un saltito hacia arriba (nunca se hunde) y la sombra queda fija."""
    if not escenario.IMAGENES:
        escenario.cargar()
    aspecto = escenario.ASPECTO_ENEMIGO.get(tipo, ASPECTO_JUGADOR)
    sprite = aspecto['sprite']
    if z is not None and not z['armadura'] and 'sprite_roto' in aspecto:
        sprite = aspecto['sprite_roto']                  # armadura rota: otro sprite
    imagen = _sprite_recortado(f'personaje_{sprite}', aspecto['escala'])
    x, y = vertice_superior(celda)
    t = pygame.time.get_ticks()
    hasta = z.get('caminar_hasta', 0) if z is not None else (g or {}).get('caminar_hasta', 0)
    andando = t < hasta
    fase = t / (95.0 if andando else aspecto['ritmo'])
    if andando:
        salto = round(3 * abs(math.sin(fase)))           # paso: sube y vuelve al suelo
        balanceo = round(3 * math.sin(fase))
    else:
        salto = 0
        balanceo = round(1.1 * math.sin(fase))
        # Respiracion: el torso se estira un par de pixeles sin separar los pies del suelo.
        extra = round(1.5 * (1 + math.sin(fase)) / 2)
        imagen = pygame.transform.scale(imagen, (imagen.get_width(), imagen.get_height() + extra))
    suelo = y + TH // 2                                   # centro de la baldosa
    sombra = pygame.Surface((46, 14), pygame.SRCALPHA)
    pygame.draw.ellipse(sombra, (8, 14, 14, 130), sombra.get_rect())
    lienzo.blit(sombra, sombra.get_rect(center=(x, suelo)))
    destino = imagen.get_rect(midbottom=(x + balanceo, suelo + 3 - salto))
    lienzo.blit(imagen, destino)
    if z is not None and z['armadura']:                  # punto azul: todavia tiene armadura
        pygame.draw.circle(lienzo, (108, 191, 225), (x+26, destino.top + 20), 6)

def barra_enemigo(z):
    """Barra individual de vida, tipo de enemigo y estado de armadura."""
    aspecto = escenario.ASPECTO_ENEMIGO[z['tipo']]
    x, y = vertice_superior(z['pos'])
    y += TH // 2
    ancho = aspecto['barra']
    x0 = x - ancho//2
    alto = y - round(86 * aspecto['escala'] + (4 if aspecto['escala'] > 1 else 0))
    pygame.draw.rect(lienzo, (28, 33, 35), (x0-1, alto-1, ancho+2, 8))
    color = aspecto['color']
    pygame.draw.rect(lienzo, color, (x0, alto, round(ancho*max(0, z['vida'])/z['vida_max']), 6))
    nombre = TIPOS[z['tipo']]['nombre']
    if z['armadura']: nombre += ' *'
    rotulo = fuente_etiqueta.render(nombre.upper(), True, color)
    rc = rotulo.get_rect(center=(x, alto-9))
    # Fondo oscuro: el nombre se lee aunque quede delante de un edificio claro (Palacio, farmacia).
    fondo = pygame.Surface((rc.width + 8, rc.height + 2), pygame.SRCALPHA)
    pygame.draw.rect(fondo, (12, 18, 20, 175), fondo.get_rect(), border_radius=4)
    lienzo.blit(fondo, fondo.get_rect(center=rc.center))
    lienzo.blit(rotulo, rc)


def marcar_jugador(celda):
    """Marcador corto P1, sin aro en el suelo que distraiga."""
    x, y = vertice_superior(celda)
    base = y + TH // 2
    punta = base - 86
    pygame.draw.polygon(lienzo, (111, 230, 216),
                        [(x - 5, punta - 8), (x + 5, punta - 8), (x, punta)])
    etiqueta = fuente_chica.render('P1', True, (17, 32, 35))
    rec = pygame.Rect(0, 0, 40, 23)
    rec.midbottom = (x, punta - 10)
    pygame.draw.rect(lienzo, (128, 234, 219), rec, border_radius=5)
    lienzo.blit(etiqueta, (rec.centerx - etiqueta.get_width() // 2, rec.y + 3))

def marcar_suministros(g):
    """Resalta discretamente la casilla de suministros mientras siga pendiente."""
    if g['suministros'] or mapa.SUMINISTROS is None:
        return
    x, y = vertice_superior(mapa.SUMINISTROS)
    t = pygame.time.get_ticks() / 350.0
    alpha = 47 + round(17 * (1 + math.sin(t)))
    brillo = pygame.Surface((ANCHO, PANEL_Y), pygame.SRCALPHA)
    pygame.draw.polygon(brillo, (245, 189, 61, alpha), [
        (x, y + 4), (x + TW // 2 - 3, y + TH // 2),
        (x, y + TH - 3), (x - TW // 2 + 3, y + TH // 2)])
    pygame.draw.polygon(brillo, (247, 207, 87, 135), [
        (x, y + 4), (x + TW // 2 - 3, y + TH // 2),
        (x, y + TH - 3), (x - TW // 2 + 3, y + TH // 2)], 2)
    lienzo.blit(brillo, (0, 0))


def marcar_refugio(g):
    """Cuando ya hay suministros, la casilla del refugio late en verde (suelo)."""
    if not g['suministros'] or mapa.REFUGIO is None:
        return
    x, y = vertice_superior(mapa.REFUGIO)
    alpha = 55 + round(25 * (1 + math.sin(pygame.time.get_ticks() / 300.0)))
    brillo = pygame.Surface((ANCHO, PANEL_Y), pygame.SRCALPHA)
    rombo_puntos = [(x, y + 1), (x + TW // 2 - 1, y + TH // 2), (x, y + TH - 1), (x - TW // 2 + 1, y + TH // 2)]
    pygame.draw.polygon(brillo, (110, 235, 150, alpha), rombo_puntos)
    pygame.draw.polygon(brillo, (170, 250, 190, 190), rombo_puntos, 2)
    lienzo.blit(brillo, (0, 0))


def flecha_refugio(g):
    """Flecha que rebota sobre el cartel del refugio cuando ya se puede volver."""
    if not g['suministros'] or mapa.REFUGIO is None:
        return
    _, rect = escenario.rectangulo(vertice_superior, mapa.REFUGIO, 'refugio')
    rebote = round(3 * math.sin(pygame.time.get_ticks() / 200.0))
    x, punta = rect.centerx, rect.top - 6 + rebote
    pygame.draw.polygon(lienzo, (28, 33, 35), [(x - 9, punta - 15), (x + 9, punta - 15), (x, punta + 2)])
    pygame.draw.polygon(lienzo, (130, 240, 160), [(x - 7, punta - 13), (x + 7, punta - 13), (x, punta - 1)])


def rotulo_suministros(g):
    """El rotulo se dibuja por encima de sprites, para no quedar oculto."""
    if g['suministros'] or mapa.SUMINISTROS is None:
        return
    x, y = vertice_superior(mapa.SUMINISTROS)
    # Anclaje corregido: la tapa queda a 46 px sobre el CENTRO del terreno.
    arriba = y - 49
    rotulo = fuente_chica.render('SUMINISTROS', True, (48, 35, 15))
    caja = pygame.Rect(0, 0, rotulo.get_width() + 16, 25)
    caja.midbottom = (x, arriba)
    pygame.draw.rect(lienzo, (235, 184, 68), caja, border_radius=5)
    pygame.draw.rect(lienzo, (110, 76, 28), caja, width=2, border_radius=5)
    lienzo.blit(rotulo, (caja.x + 8, caja.y + 4))
    pygame.draw.polygon(lienzo, (235, 184, 68), [
        (x - 5, caja.bottom + 2), (x + 5, caja.bottom + 2), (x, caja.bottom + 9)])


def _info_interior(g):
    """Plataforma del interior y panel de exploracion a la derecha."""
    # Losetas interiores sobre una plataforma con sombra y un panel de exploracion.
    cx, cy = mapa.ORIGEN
    pygame.draw.polygon(lienzo, (5, 9, 10), [(cx,cy-6),(cx+240,cy+111),
        (cx,cy+255),(cx-240,cy+111)])
    pygame.draw.polygon(lienzo, (40, 53, 52), [(cx,cy-2),(cx+231,cy+114),
        (cx,cy+237),(cx-231,cy+114)], 3)
    info = pygame.Rect(895, 137, 330, 284)
    pygame.draw.rect(lienzo,(28,42,43),info,border_radius=13)
    pygame.draw.rect(lienzo,(75,119,113),info,2,border_radius=13)
    texto('EXPLORANDO',info.x+20,info.y+20,(146,221,193),fuente_media)
    texto(mapa.NOMBRE[:21],info.x+20,info.y+67,(237,213,149),fuente_chica)
    texto(f'Zombis adentro: {len(g["enemigos"])}',info.x+20,info.y+103,fuente=fuente_chica)
    texto(f'Botiquines: {len(g["botiquines_suelo"])}  Balas: {len(g["municion"])}',info.x+20,info.y+128,fuente=fuente_chica)
    texto('E: entrar/salir por la puerta',info.x+20,info.y+178,fuente=fuente_chica)
    texto('Cada puerta cuesta 1 PA.',info.x+20,info.y+202,fuente=fuente_chica)
    texto('Los objetos NO reaparecen.',info.x+20,info.y+226,fuente=fuente_chica)


def dibujar_mundo(g, hover):
    """Terreno, objetos, personajes, efectos y barras de vida (todo menos el panel inferior)."""
    lienzo.fill((13, 21, 23))
    if mapa.EN_INTERIOR:
        _info_interior(g)

    # Terreno sin cuadricula permanente: calles, veredas y vegetacion.
    for row in range(mapa.TAMANO):
        for col in range(mapa.TAMANO):
            dibujar_terreno((col,row),hover,g)
    # Mostrar permanentemente alcance del arma elegida (solo casillas caminables).
    reach = alcance(g['arma'])
    layer = pygame.Surface((ANCHO, PANEL_Y), pygame.SRCALPHA)
    for rr in range(mapa.TAMANO):
        for cc in range(mapa.TAMANO):
            celda = (cc, rr)
            if celda == g['jugador'] or celda in mapa.MUROS or distancia(g['jugador'],celda)>reach:
                continue
            valid = tiro_valido(g['arma'], g['jugador'], celda)
            x,y=vertice_superior(celda)
            color = (67,205,121,44) if valid else (217,82,70,32)
            pygame.draw.polygon(layer,color,[(x,y),(x+TW//2,y+TH//2),(x,y+TH),(x-TW//2,y+TH//2)])
    lienzo.blit(layer,(0,0))
    marcar_suministros(g)
    marcar_refugio(g)
    # Marcas tacticas discretas solo al pasar el raton o al apuntar a zombis.
    if hover is not None and hover not in mapa.MUROS:
        rombo(hover,(105,125,92),(181,196,138))
    for z in g['enemigos']:
        celda=z['pos']
        reach=alcance(g['arma'])
        if distancia(g['jugador'],celda)<=reach:
            x,y=vertice_superior(celda)
            good=tiro_valido(g['arma'], g['jugador'], celda)
            pygame.draw.circle(lienzo,(79,185,129) if good else (204,82,78),(x,y+TH//2),16,2)
    # Los edificios tienen una base fisica de 2x2 y no se generan uno por baldosa.
    for pos, variante in mapa.EDIFICIOS:
        escenario.cimientos(lienzo, vertice_superior, pos)

    # Todo lo que se dibuja sobre el terreno va en una lista ordenada por profundidad:
    # edificios, autos, escombros, objetos, zombis y jugador (lo de atras se dibuja primero).
    objects = [(sum(c) + 2, 0, 'edificio', c, variante) for c, variante in mapa.EDIFICIOS]
    objects += [(sum(c), 0, 'auto', c, variante) for c, variante in mapa.AUTOS]
    objects += [(sum(c), 0, 'escombros', c, None) for c in mapa.ESCOMBROS]
    objects += [(sum(c), 0, 'botiquin', c, None) for c in g['botiquines_suelo']]
    objects += [(sum(c), 0, 'municion', c, None) for c in g['municion']]
    if mapa.EN_INTERIOR:
        objects += [(sum(c), 0, 'mueble', c, nombre) for c, nombre in mapa.MUEBLES.items()]
        objects += [(sum(interiores.ENTRADA), 0, 'salida', interiores.ENTRADA, None)]
    else:
        for celda, nombre in mapa.DECORACION:
            objects.append((sum(celda), 0, 'decoracion', celda, nombre))
        for celda, (edificio, tipo) in mapa.PUERTAS.items():
            objects.append((sum(celda), 0, 'puerta', celda, (edificio, tipo)))
    if not g['suministros'] and mapa.SUMINISTROS is not None:
        objects.append((sum(mapa.SUMINISTROS), 0, 'suministros', mapa.SUMINISTROS, None))
    if mapa.REFUGIO is not None:
        objects.append((sum(mapa.REFUGIO), 0, 'refugio', mapa.REFUGIO, None))
    # Zombis y jugador entran en la MISMA lista ordenada por profundidad:
    # asi un zombi detras de un auto queda tapado por el auto, y uno delante lo tapa.
    objects += [(sum(z['pos']), 1, 'zombi', z['pos'], z) for z in g['enemigos']]
    objects.append((sum(g['jugador']), 1, 'jugador', g['jugador'], None))
    px, py = vertice_superior(g['jugador'])
    jugador_rect = pygame.Rect(px - 23, py + TH // 2 - 57, 46, 83)

    for _, _, tipo, celda, data in sorted(objects, key=lambda o: (o[0], o[1], o[3][1])):
        x, y = vertice_superior(celda)
        if tipo == 'edificio':
            _sprite(celda, 'edificio', data, jugador_rect)
        elif tipo == 'auto':
            _sprite(celda, 'auto', data)
        elif tipo == 'escombros':
            _sprite(celda, 'escombros')
        elif tipo == 'suministros':
            _sprite(celda, 'suministros')
        elif tipo == 'refugio':
            _sprite(celda, 'refugio')
        elif tipo == 'zombi':
            dibujar_personaje(celda, data['tipo'], data)
        elif tipo == 'jugador':
            dibujar_personaje(celda, g=g)
        elif tipo == 'mueble':
            _sprite(celda, f'mueble_{data}')
        elif tipo == 'decoracion':
            _sprite(celda, data)
        elif tipo in ('puerta', 'salida'):
            aviso = 'SALIDA  [E]' if tipo == 'salida' else 'ENTRAR [E]'
            # Rotulo discreto a nivel de suelo: puerta siempre localizable.
            etiqueta = fuente_puerta.render(aviso,True,(235,248,229))
            rc = etiqueta.get_rect(midbottom=(x, y - 4))
            pygame.draw.rect(lienzo,(29,94,95),rc.inflate(9,5),border_radius=3)
            lienzo.blit(etiqueta,rc)
        elif tipo == 'municion':
            pygame.draw.rect(lienzo,(221,181,69),(x-12,y+6,24,14),border_radius=3)
            pygame.draw.rect(lienzo,(89,73,40),(x-12,y+6,24,14),2,border_radius=3)
            for dx in (-7,0,7):pygame.draw.rect(lienzo,(245,227,154),(x+dx-2,y+7,4,7))
        elif tipo == 'botiquin':
            pygame.draw.rect(lienzo, (225, 227, 215), (x - 11, y + 2, 22, 17), border_radius=3)
            pygame.draw.rect(lienzo, (184, 45, 48), (x - 2, y + 4, 4, 13))
            pygame.draw.rect(lienzo, (184, 45, 48), (x - 7, y + 9, 14, 4))

    # Capa de interfaz sobre el mundo: barras de vida y marcador P1 siempre visibles.
    for z in g['enemigos']:
        barra_enemigo(z)
    marcar_jugador(g['jugador'])
    rotulo_suministros(g)
    flecha_refugio(g)
    efectos.dibujar_efectos(lienzo, texto, fuente_chica)
    if g.get('fogonazo',0)>0:
        x,y=vertice_superior(g['jugador'])
        pygame.draw.circle(lienzo,(255,214,92),(x+23,y-24),5+g['fogonazo']//2)
        g['fogonazo']-=1
    if g.get('golpe',0)>0:
        x,y=vertice_superior(g['jugador'])
        pygame.draw.arc(lienzo,(222,192,133),(x-30,y-65,62,65),-.9,1.6,5)
        g['golpe']-=1
    if g.get('herido',0)>0:
        veil=pygame.Surface((ANCHO,PANEL_Y),pygame.SRCALPHA)
        veil.fill((180,28,35,60 if g['herido']%4<2 else 20))
        lienzo.blit(veil,(0,0))
        g['herido']-=1
    if g.get('destello'):
        celda, frames = g['destello']
        x,y=vertice_superior(celda)
        pygame.draw.circle(lienzo,(243,203,89),(x,y-15),max(3,frames*2),3)
        g['destello'] = (celda,frames-1) if frames>1 else None
