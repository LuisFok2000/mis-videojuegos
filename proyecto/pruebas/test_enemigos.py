"""Pruebas de reglas sin Pygame: python -m unittest discover -s pruebas -v"""
import unittest
import niveles
import enemigo
import combate
import jugador


def silencio(*args, **kwargs):
    pass

class PruebasEnemigos(unittest.TestCase):
    def test_niveles_e_interiores_validos(self):
        niveles.validar_todos()

    def test_tipos_y_vida(self):
        for clase, config in enemigo.TIPOS.items():
            z = enemigo.crear_enemigos([((3,3), clase)])[0]
            self.assertEqual(z['vida'], config['vida'])
            self.assertEqual(z['armadura'], clase == 'blindado')

    def test_blindaje_requiere_bate(self):
        g = jugador.crear(jugador.atributos_iniciales())
        g.update({'enemigos': [], 'botiquines_suelo': set(), 'mensaje': '', 'turno': 1, 'modo': 'juego', 'nivel': 0})
        g['jugador'] = (0, 5)
        z = enemigo.crear_enemigos([((1,5), 'blindado')])[0]
        g['enemigos'] = [z]
        g['arma'] = 'pistola'
        balas = g['balas']
        combate.atacar(g, z['pos'], silencio, silencio, silencio)
        self.assertEqual(z['vida'], 9)
        self.assertTrue(z['armadura'])
        self.assertEqual(g['balas'], balas - 1)
        g['arma'] = 'bate'
        combate.atacar(g, z['pos'], silencio, silencio, silencio)
        self.assertFalse(z['armadura'])
        self.assertEqual(z['vida'], 9)
        g['pa'] = 4
        g['arma'] = 'pistola'
        combate.atacar(g, z['pos'], silencio, silencio, silencio)
        self.assertEqual(z['vida'], 5)

    def test_corredor_avanza_tres(self):
        g = jugador.crear(jugador.atributos_iniciales())
        g.update({'enemigos': [], 'botiquines_suelo': set(), 'mensaje': '', 'turno': 1, 'modo': 'juego', 'nivel': 0})
        g['jugador'] = (0, 6)
        g['enemigos'] = enemigo.crear_enemigos([((0, 1), 'corredor')])
        inicial = g['enemigos'][0]['pos']
        enemigo.turno_enemigos(g, silencio, silencio, silencio)
        self.assertEqual(abs(inicial[1]-g['enemigos'][0]['pos'][1]), 3)

    def test_escupidor_dispara_desde_tres(self):
        g = jugador.crear(jugador.atributos_iniciales())
        g.update({'enemigos': [], 'botiquines_suelo': set(), 'mensaje': '', 'turno': 1, 'modo': 'juego', 'nivel': 0})
        g['jugador'] = (0, 6)
        g['enemigos'] = enemigo.crear_enemigos([((0, 3), 'escupidor')])
        hp = g['vida']
        enemigo.turno_enemigos(g, silencio, silencio, silencio)
        self.assertEqual(g['vida'], hp - 2)
        self.assertEqual(g['enemigos'][0]['pos'], (0, 3))

if __name__ == '__main__':
    unittest.main()
