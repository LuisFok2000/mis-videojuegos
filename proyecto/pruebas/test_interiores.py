"""Pruebas de jugabilidad de interiores, niveles y continuidad de estado.
Ejecutar: python -m unittest discover -s pruebas -v
"""
import unittest
import mapa
import niveles
import transiciones
import partida
import jugador
import combate


def silencio(*_args):
    pass


class TestInteriores(unittest.TestCase):
    def tearDown(self):
        mapa.cargar_nivel(0)

    def test_tres_niveles_completables_geometricamente(self):
        self.assertEqual(len(mapa.NIVELES), 3)
        niveles.validar_todos()

    def test_puerta_cuesta_un_pa(self):
        g = partida.nueva_partida(1)
        puerta = (5, 4)
        g['jugador'] = puerta
        self.assertTrue(transiciones.interactuar(g, silencio))
        self.assertEqual(g['pa'], 3)
        self.assertEqual(g['escena'], 'interior')
        self.assertEqual(mapa.TAMANO, 6)
        self.assertEqual(g['jugador'], (2, 5))
        self.assertEqual(mapa.NOMBRE, 'FARMASHOP')

    def test_salir_restaurar_calle_y_consume_pa(self):
        g = partida.nueva_partida(1)
        g['jugador'] = (5, 4)
        exteriores = g['enemigos']
        self.assertTrue(transiciones.interactuar(g))
        self.assertTrue(transiciones.interactuar(g))
        self.assertEqual(g['pa'], 2)
        self.assertEqual(g['escena'], 'calle')
        self.assertIs(g['enemigos'], exteriores)
        self.assertEqual(mapa.TAMANO, 12)
        self.assertEqual(g['jugador'], (5, 4))

    def test_no_se_puede_interactuar_lejos_de_la_puerta(self):
        g = partida.nueva_partida(0)
        self.assertFalse(transiciones.interactuar(g))
        self.assertEqual(g['pa'], 4)
        self.assertEqual(g['escena'], 'calle')

    def test_recursos_interior_no_reaparecen(self):
        g = partida.nueva_partida(1)
        g['jugador'] = (5, 4)
        transiciones.interactuar(g)
        self.assertIn((3, 4), g['botiquines_suelo'])
        self.assertIn((2, 1), g['municion'])
        g['botiquines_suelo'].remove((3, 4))
        g['municion'].remove((2, 1))
        g['enemigos'].clear()
        transiciones.interactuar(g)
        g['pa'] = 4
        transiciones.interactuar(g)
        self.assertNotIn((3, 4), g['botiquines_suelo'])
        self.assertNotIn((2, 1), g['municion'])
        self.assertEqual(len(g['enemigos']), 0)

    def test_farmashop_nivel_dos_tiene_suministros(self):
        g = partida.nueva_partida(1)
        self.assertIsNone(mapa.SUMINISTROS)
        g['jugador'] = (5, 4)
        transiciones.interactuar(g)
        self.assertEqual(mapa.SUMINISTROS, (4, 1))
        self.assertFalse(g['suministros'])
        g['jugador'] = (3, 1)
        jugador.mover(g, (4, 1), silencio, silencio)
        self.assertTrue(g['suministros'])
        transiciones.interactuar(g)  # Todavia lejos de la salida: se rechaza.
        self.assertEqual(g['escena'], 'interior')
        g['jugador'] = (2, 5)
        transiciones.interactuar(g)
        self.assertTrue(g['suministros'])

    def test_palacio_jefe_es_obligatorio(self):
        g = partida.nueva_partida(2)
        self.assertEqual(transiciones.enemigos_pendientes(g), 4)
        g['enemigos'].clear()
        self.assertEqual(transiciones.enemigos_pendientes(g), 1)
        g['jugador'] = mapa.REFUGIO
        g['suministros'] = True
        # Sin derrotar al jefe la llegada al refugio no puede dar victoria.
        g['jugador'] = (10, 11)
        jugador.mover(g, (11, 11), silencio, silencio)
        self.assertEqual(g['modo'], 'juego')
        self.assertIn('jefe', g['mensaje'])

    def test_jefe_persiste_hasta_derrotarlo(self):
        g = partida.nueva_partida(2)
        g['jugador'] = (5, 3)
        transiciones.interactuar(g)
        self.assertEqual(g['enemigos'][0]['tipo'], 'jefe')
        self.assertEqual(mapa.TAMANO, 6)
        jefe = g['enemigos'][0]
        jefe['vida'] = 6
        transiciones.interactuar(g)
        g['pa'] = 4
        transiciones.interactuar(g)
        self.assertIs(g['enemigos'][0], jefe)
        self.assertEqual(jefe['vida'], 6)

    def test_entrada_bloqueada_sin_pa(self):
        g = partida.nueva_partida(0)
        g['jugador'] = (3, 3)
        g['pa'] = 0
        self.assertFalse(transiciones.interactuar(g))
        self.assertEqual(g['escena'], 'calle')

    def test_rango_escupidor_en_interior_obstaculo(self):
        g = partida.nueva_partida(2)
        g['jugador'] = (5, 3)
        transiciones.interactuar(g)
        self.assertTrue((4, 3) in mapa.MUROS)
        self.assertFalse(combate.linea_libre((3, 3),(5, 3)))

    def test_armadura_sigue_rota_al_regresar(self):
        g = partida.nueva_partida(1)
        # Dentro de Farmashop hay enemigo comun. El blindado del exterior permanece.
        blindado = next(z for z in g['enemigos'] if z['tipo'] == 'blindado')
        blindado['armadura'] = False
        g['jugador'] = (5, 4)
        transiciones.interactuar(g)
        transiciones.interactuar(g)
        self.assertFalse(blindado['armadura'])

    def test_reinicio_restaurar_nivel_exterior(self):
        g = partida.nueva_partida(2)
        g['jugador'] = (5, 3)
        transiciones.interactuar(g)
        ng = partida.reintentar(g)
        self.assertEqual(ng['escena'], 'calle')
        self.assertEqual(mapa.TAMANO, 12)
        self.assertEqual(len(ng['enemigos']), 3)

    def test_salida_solo_tras_objetivos(self):
        g = partida.nueva_partida(2)
        g['enemigos'].clear()
        g['salas'][(4, 1)]['enemigos'].clear()
        g['suministros'] = True
        g['jugador'] = (10, 11)
        jugador.mover(g, (11, 11), silencio, silencio)
        self.assertEqual(g['modo'], 'victoria')


if __name__ == '__main__':
    unittest.main()
