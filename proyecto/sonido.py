"""Efectos y musica sintetizados sin archivos externos."""
import pygame, random, math, array
SONIDOS = {}
MUSICA_ACTUAL = None
MUSICAS = {}
ZONA_ACTUAL = 'calle'
silenciado = False

def crear_sonido(tipo, duration, volume=0.4):
    if not pygame.mixer.get_init():
        return None
    rate, fmt, channels = pygame.mixer.get_init()
    count = int(rate * duration)
    samples = array.array('h')
    rng = random.Random(48 + len(tipo))
    for i in range(count):
        t = i / rate
        decay = (1 - i / count) ** 1.5
        noise = rng.uniform(-1, 1)
        if tipo == 'pistola':
            v = (noise * .85 + math.sin(2*math.pi*(110-50*t)*t)*.15) * decay**4
        elif tipo == 'bate':
            v = (math.sin(2*math.pi*95*t)*.65 + noise*.35) * decay**2
        elif tipo == 'herida':
            v = (math.sin(2*math.pi*(210-110*t)*t) + noise*.3) * decay
        elif tipo == 'zombi':
            v = (math.sin(2*math.pi*(75+10*math.sin(2*math.pi*8*t))*t) + noise*.25) * decay
        elif tipo == 'escupitajo':
            v = (.42*noise + .58*math.sin(2*math.pi*(285-95*t)*t)) * decay
        elif tipo == 'paso':
            v = noise * decay**5
        elif tipo == 'recoger':
            v = math.sin(2*math.pi*(500+700*t)*t)*decay
        else:
            v = math.sin(2*math.pi*570*t)*decay
        value = max(-32767, min(32767, int(v * 25000 * volume)))
        if channels == 2:
            samples.extend((value,value))
        else:
            samples.append(value)
    return pygame.mixer.Sound(buffer=samples.tobytes())

def iniciar_audio():
    global MUSICA_ACTUAL
    if not pygame.mixer.get_init():
        return
    for name, seconds in [('pistola',.33),('bate',.25),('herida',.35),('zombi',.48),('paso',.09),('recoger',.3),('clic',.1),('escupitajo',.3),('puerta',.23)]:
        SONIDOS[name] = crear_sonido(name, seconds)
    # Melodia ambiental lenta, tonal, sin ruido blanco ni estatica.
    # 16 pulsos (4 compases de 4 tiempos) a 72 BPM, acordes menores y notas suaves.
    rate, fmt, channels = pygame.mixer.get_init()
    beat = 60 / 72
    duration = 16 * beat
    frames = int(rate * duration)
    data = array.array('h')
    progression = [(110.0, 130.81, 164.81), (98.0, 123.47, 146.83),
                   (87.31, 110.0, 130.81), (98.0, 123.47, 146.83)]
    melody = [220.0, 0, 196.0, 0, 174.61, 0, 196.0, 0,
              164.81, 0, 146.83, 0, 174.61, 0, 196.0, 0]
    for i in range(frames):
        t = i / rate
        beat_index = min(15, int(t / beat))
        chord = progression[beat_index // 4]
        # Ataque y salida suaves de cada nota; bucle sin chasquidos.
        local = (t / beat) % 1
        env = min(1.0, local * 8) * min(1.0, (1-local)*3)
        pad = sum(math.sin(2*math.pi*f*t) for f in chord) / 3
        note = melody[beat_index]
        lead = (math.sin(2*math.pi*note*t) + .25*math.sin(2*math.pi*2*note*t))*env if note else 0
        global_fade = min(1.0,t/.12,(duration-t)/.12)
        v = int(3100 * max(0,global_fade) * (.43*pad + .30*lead))
        if channels == 2: data.extend((v,v))
        else: data.append(v)
    MUSICA_ACTUAL = pygame.mixer.Sound(buffer=data.tobytes())
    pygame.mixer.set_num_channels(12)
    MUSICA_ACTUAL.set_volume(.42)
    MUSICAS['calle'] = MUSICA_ACTUAL
    MUSICAS['interior'] = _musica_sintetizada((146.83, 174.61, 220.0), 62)
    MUSICAS['palacio'] = _musica_sintetizada((82.41, 110.0, 146.83), 104)
    MUSICA_ACTUAL.play(loops=-1)

def reproducir(name):
    if not silenciado and SONIDOS.get(name):
        SONIDOS[name].play()

def pitido():
    """Sonido corto al pulsar botones."""
    reproducir('clic')


def _musica_sintetizada(tonos, bpm):
    """Tema ambiental original con 8 tiempos. Cada interior tiene otra armonia."""
    if not pygame.mixer.get_init():
        return None
    rate, fmt, canales = pygame.mixer.get_init()
    beat = 60.0 / bpm
    duracion = beat * 8
    data = array.array('h')
    total = int(rate * duracion)
    for i in range(total):
        t = i / rate
        pulso = int(t / beat)
        atenuacion = min(1.0, (t/beat % 1)*7) * min(1.0, (1-t/beat % 1)*5)
        fundamental = tonos[pulso % len(tonos)]
        fondo = sum(math.sin(2*math.pi*f*t) for f in tonos) / len(tonos)
        nota = math.sin(2*math.pi*fundamental*t) * atenuacion
        bajo = math.sin(2*math.pi*(fundamental/2)*t) * .35
        fade = min(1.0, t/.14, (duracion-t)/.14)
        n = int(3000 * max(0, fade) * (.45*fondo + .26*nota + .25*bajo))
        if canales == 2:
            data.extend((n,n))
        else:
            data.append(n)
    return pygame.mixer.Sound(buffer=data.tobytes())


def actualizar_volumen():
    if MUSICA_ACTUAL:
        MUSICA_ACTUAL.set_volume(0 if silenciado else (.37 if ZONA_ACTUAL != 'palacio' else .48))


def cambiar_ambiente(zona):
    """Cambia de musica al entrar/salir; no deja varias pistas superpuestas."""
    global MUSICA_ACTUAL, ZONA_ACTUAL
    if zona not in MUSICAS or MUSICAS[zona] is None:
        return
    if ZONA_ACTUAL == zona and MUSICA_ACTUAL is MUSICAS[zona]:
        actualizar_volumen()
        return
    if MUSICA_ACTUAL:
        MUSICA_ACTUAL.stop()
    ZONA_ACTUAL = zona
    MUSICA_ACTUAL = MUSICAS[zona]
    actualizar_volumen()
    MUSICA_ACTUAL.play(loops=-1)
