# Dead Zone: Uruguay — RPG isométrico postapocalíptico

Juego táctico de supervivencia hecho en **Python y Pygame**, con **tres niveles**, exploración de interiores, enemigos especiales y ambientación uruguaya. Usa del motor de clase (`engine/iso_tools.py`, sin modificar) las conversiones `grid_to_iso` e `iso_to_grid`.

## Cómo ejecutarlo en Windows

1. Descomprimí el ZIP completo, incluida la carpeta `recursos`.
2. Abrí **PowerShell** dentro de `Tarea_videojuego_2d` (donde está `main.py`).
3. Ejecutá:

   ```powershell
   py -m pip install -r requirements.txt
   py main.py
   ```

   Si usás `python` en vez de `py`: `python -m pip install -r requirements.txt` y `python main.py`.

4. Arranca en **pantalla completa**; presioná `F11` para alternar a ventana.

Para hacer las pruebas automáticas de lógica (no requieren Pygame):

```powershell
py -m unittest discover -s pruebas -v
```

## Objetivo y progresión

Por turno contás con **4 puntos de acción** (PA). La misión es derrotar a los zombis obligatorios, conseguir suministros y regresar al refugio verde.

- **Nivel 1 — Barrio infectado:** conocés las mecánicas y enfrentás comunes y un corredor. Los suministros están en la calle.
- **Nivel 2 — Avenida bloqueada:** aparecen escupidores y blindados. **Los suministros están dentro de Farmashop**: llegá a su puerta turquesa y pulsá `E`.
- **Nivel 3 — Palacio Legislativo:** escenario uruguayo final. Los suministros están **dentro del Palacio**, protegidos por un **jefe**. Tenés que derrotarlo antes de completar la misión.

Los recursos de interiores opcionales ayudan, pero sus zombis opcionales no bloquean el refugio. En el tercer nivel **sí** es obligatorio derrotar al jefe del Palacio. La vida, munición y botiquines se conservan entre niveles con una bonificación de +4 PV (máximo 12) y +6 balas.

## Controles

| Acción | Tecla o control |
|---|---|
| Moverse 1 casilla, cuesta 1 PA | `WASD` o flechas; también clic en una casilla vecina |
| Atacar a un zombi, cuesta 2 PA | Clic sobre el zombi cuando está al alcance |
| Elegir pistola (4 casillas, 4 daño) | `1` o botón **PISTOLA** |
| Elegir bate (1 casilla, 3 daño) | `2` o botón **BATE** |
| Usar botiquín (1 PA, cura 5) | `H` o botón |
| Terminar turno (avanzan los zombis) | `ESPACIO` |
| **Entrar/salir de un edificio (1 PA)** | Pararse sobre el marcador **ENTRAR [E] / SALIDA [E]** y pulsar `E` o clicar la misma casilla |
| Cambiar pantalla completa/ventana | `F11` |
| Activar o silenciar audio | `M` |
| Reiniciar nivel / menú | `R` / `ESC` |

### Los enemigos especiales

| Tipo | Vida | Movimiento / ataque | Consejo |
|---|---:|---|---|
| **Común** | 6 | 2 pasos, muerde a 1 casilla | Evitá quedarte cerca al terminar turno |
| **Corredor** | 4 | **3 pasos por turno**, muerde a 1 casilla | Disparale antes de que te alcance |
| **Blindado** | 9 | 1 paso, mordida fuerte | Las balas no hacen nada hasta que **un golpe del bate rompa la armadura**; después cambia de aspecto |
| **Escupidor** | 5 | 1 paso, **ataque a distancia hasta 3 casillas**, si tiene línea de tiro | Aprovechá obstáculos y acercate desde otro ángulo |
| **Jefe** | 14 | 1 paso, golpe fuerte | Reservá balas y botiquines para el Palacio |

Cada tipo tiene sprite y barra de vida propios, con respiración y balanceo animados. Hay partículas, números de daño, sombras y efectos de impacto.

### Entrar y explorar edificios

Los edificios tienen puertas señalizadas en **turquesa**. Para entrar o salir hacen falta **1 PA**. Los interiores son mapas de **6×6** casillas con estanterías, muebles, botiquines, paquetes de +5 balas y, a veces, enemigos. Se muestran pistas en el panel derecho. Los enemigos derrotados y los recursos recogidos **no reaparecen** al salir y volver a entrar.

## Estructura del proyecto

- `main.py`: punto de entrada y bucle principal.
- `pantalla.py`, `entrada.py`, `acciones.py`: ventana y coordenadas, teclado y ratón, y conexión de las reglas con sonido y efectos.
- `dibujo_mundo.py`, `dibujo_panel.py`, `escenario.py`, `interfaz.py`, `efectos.py`: dibujo del mundo (terreno, edificios, personajes), del panel inferior y de los menús; sprites, botones y partículas.
- `niveles.py`, `mapa.py`, `interiores.py`, `transiciones.py`, `partida.py`: datos de los niveles y su validación, escena activa (calle o habitación), puertas y cambios de escena, y estado de la partida.
- `jugador.py`, `enemigo.py`, `combate.py`: reglas tácticas e inteligencia artificial.
- `sonido.py`: efectos y música ambiental sintetizados por código (calle, edificios y Palacio).
- `engine/iso_tools.py`: motor del curso (sin modificar).
- `recursos/*.png`: recursos gráficos incluidos, **sin necesidad de generarlos para jugar**.
- `herramientas/`: generadores de los PNG (`generar_uruguay.py` y `generar_personajes.py` usan **Pillow**; `generar_autos.py` y `generar_palacio.py` usan Pygame y comparten `comun.py`). Solo hacen falta para regenerar los recursos.
- `pruebas/`: pruebas de reglas, colisiones, enemigos e interiores (18 casos).
- `DISENO.md`: decisiones de diseño, arquitectura y procedencia de recursos. `CHANGELOG.md`: historial de versiones.

## Pruebas

Las pruebas automáticas (`py -m unittest discover -s pruebas -v`) cubren la lógica y no necesitan abrir el juego. Lo que solo se ve jugando (resolución, superposiciones y audio) se comprueba a mano con `py main.py`:

- [ ] El juego inicia en pantalla completa y `F11` alterna ventana y pantalla completa.
- [ ] Se ven Farmashop, panadería y casa en el nivel 1; taxis, ómnibus, contenedores y carteles sin piezas flotando.
- [ ] P1 se mueve con flechas y WASD, y el panel actualiza los PA (4 por turno).
- [ ] La pistola necesita línea de tiro y consume munición; el bate no consume balas.
- [ ] El corredor avanza hasta 3 casillas al terminar el turno; el escupidor ataca a distancia.
- [ ] El blindado bloquea balas; después del bate cambia el sprite y las balas empiezan a dañarlo.
- [ ] Todos los enemigos muestran etiqueta y barra de vida; los personajes respiran y se balancean al moverse.
- [ ] Pararse sobre `ENTRAR [E]` y pulsar `E` consume 1 PA y cambia al interior de 6×6, con muebles sólidos y algún enemigo.
- [ ] Recoger balas suma +5 y los botiquines se agregan al inventario.
- [ ] Salir y reingresar: los recursos recogidos y los enemigos derrotados no reaparecen.
- [ ] La música cambia al entrar y salir; en el Palacio suena otro tema; `M` silencia o reactiva.
- [ ] Nivel 2: los suministros están dentro de Farmashop. Nivel 3: entrar al Palacio, vencer al jefe de 14 PV, recoger suministros y volver al refugio.
- [ ] `R` dentro de un interior reinicia el nivel en la calle; menú, derrota, transición de nivel y victoria funcionan.

> Si algo visual falla, sacá una captura y anotá el texto de la consola.
