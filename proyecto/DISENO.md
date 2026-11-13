# Dead Zone: Uruguay — Documento de diseño

**Entrega:** Taller de Videojuegos 2D (TVJ2D 2026), opción 2: RPG isométrico.  
**Versión:** 2.0 — tres niveles, habitaciones, enemigos especiales y nuevo arte.  
**Integrante:** Luis Andrada.

## 1. Idea, objetivo y ambientación

Juego de supervivencia táctica por turnos, ambientado en un Montevideo ficticio invadido por zombis. El protagonista debe **eliminar enemigos de misión, obtener suministros y volver al refugio**. Hay Farmashop, almacenes, panaderías, viviendas, carteles de calles reales, contenedores de basura, taxis, ómnibus y un tercer nivel protagonizado por el Palacio Legislativo.

El arte usa una perspectiva isométrica de rombos con coordenadas convertidas por el módulo original del curso (se usan `grid_to_iso` e `iso_to_grid`), **sin modificar `engine/iso_tools.py`**.

## 2. Reglas y decisiones

| Decisión | Motivo y efecto en la partida |
|---|---|
| **4 PA por turno** | Avanzar una casilla cuesta 1 PA; atacar 2; curarse 1; abrir una puerta 1. El jugador planifica qué sacrificar y cuándo terminar el turno. |
| **Pistola (daño 4, alcance 4, munición limitada)** | Permite eliminar amenazas antes de que lleguen; requiere línea de disparo despejada. |
| **Bate (daño 3, alcance 1, sin munición)** | Permite luchar sin balas; **es la única herramienta que rompe la armadura** de un blindado (primer golpe = romper armadura, sin bajar PV). |
| **Corredor (4 PV, avanza 3 casillas)** | Castiga quedarse quieto o esperar demasiado. |
| **Común (6 PV, 2 casillas)** | Enemigo básico, sirve de referencia. |
| **Blindado (9 PV, 1 casilla)** | Obliga al cambio de arma, vuelve indispensable el bate. Su sprite cambia cuando pierde el blindaje. |
| **Escupidor (5 PV, 1 casilla)** | Puede atacar hasta a **3 casillas con línea de tiro libre**, obliga a usar coberturas. |
| **Jefe (14 PV, 1 casilla)** | Amenaza única en interior del Palacio, con 3 PV de daño por ataque y barra de vida mayor. |
| **Habitaciones 6×6 con puertas (1 PA)** | Ofrecen decisiones de exploración, recursos y combates opcionales. En nivel 2 y 3 alojan los suministros necesarios. |
| **Enemigos y objetos persistentes en habitaciones** | Evita reiniciar el botín o duplicar enemigos tras entrar/salir. |
| **Enemigos interiores opcionales** | Permite terminar niveles sin visitar todos los edificios; el jefe de nivel 3 sí es obligatorio. |
| **Tres niveles con recursos entre niveles** | Permite tutorial, desafío de distancias y jefe final. La vida aumenta hasta +4 PV y se agregan +6 balas entre niveles. |
| **Música ambiental sintetizada** | Se genera en código sin audio de terceros; la música cambia para calle, interiores y Palacio. |
| **Identidad visual uruguaya** | Edificios identificables, medios de transporte urbanos, carteles y contenedores. |

La IA usa búsqueda BFS en una cuadrícula, moviéndose hasta el rango de ataque de cada tipo. La pistola y la escupida respetan bloqueos de línea. Los zombis pueden atacar **como máximo una vez por turno**.

## 3. Los niveles

### Nivel 1: Barrio infectado

- Tablero exterior de 12×12 casillas y tres zombis (2 comunes, 1 corredor).
- Suministros en el exterior; refugio en la esquina opuesta.
- Farmashop, panadería y casa. Los interiores ofrecen reabastecimiento opcional.

### Nivel 2: Avenida bloqueada

- Cinco zombis: escupidor, blindado, corredor y comunes.
- Suministros dentro del **Farmashop**, en el interior 6×6. Se usan puertas y exploración.
- Edificios: almacén, farmacia, casa y panadería.

### Nivel 3: Palacio Legislativo

- Tres zombis en el exterior, incluyendo blindado y escupidor.
- Al entrar al **Palacio Legislativo**, se enfrenta un **jefe** de 14 PV. Los suministros de misión están dentro.
- La victoria exige tanto derrotar al jefe como eliminar los enemigos exteriores, recoger suministros y llegar al refugio.
- Hay otros locales para hallar recursos antes del combate final.

## 4. Arquitectura

| Componente | Responsabilidad |
|---|---|
| `main.py` | Punto de entrada y bucle principal: leer entrada, dibujar y presentar. |
| `pantalla.py` | Ventana, lienzo fijo 1280×850, fuentes, transformación de coordenadas (`vertice_superior`, `casilla_bajo_raton`) y escalado al monitor. |
| `entrada.py` | Teclado y ratón: traduce cada evento en una acción de juego o un cambio de pantalla. |
| `acciones.py` | Conecta las reglas (mover, atacar, curar, turno enemigo) con el sonido y los efectos visuales. |
| `dibujo_mundo.py` | Dibujo de la escena activa: terreno, edificios, objetos, personajes, barras de vida y efectos. |
| `dibujo_panel.py` | Panel inferior de la partida y pantallas de menú, victoria y derrota. |
| `niveles.py` | Datos de los tres niveles (edificios, puertas, autos, enemigos, decoración) y su validación, sin dependencias gráficas. |
| `mapa.py` | Escena activa (calle 12×12 o interior 6×6): paredes, tamaño, puertas y carga de calle/interior. |
| `interiores.py` | Diseño determinista de muebles y contenido de las habitaciones (sin dependencia gráfica). |
| `transiciones.py` | Puertas, costo en PA, conservación de estado de la calle/interior y progreso de misión. |
| `partida.py` | Inicialización y progreso de partida, conservación de vida, balas, botiquines y estado interior. |
| `enemigo.py` | Datos por tipo, IA (incluida la búsqueda BFS del siguiente paso), movimiento y ataques según alcance. |
| `combate.py` | Armas, distancia, línea de tiro, daños y mecánica de blindaje. |
| `jugador.py` | Movimiento a casillas vecinas libres, recogida de recursos, curación y victoria. |
| `escenario.py` | Carga de PNG, anclaje isométrico, sombras, transparencia de edificios y aspecto visual de cada tipo de enemigo. |
| `sonido.py` | Efectos y melodías sintetizadas por código. |
| `efectos.py`, `interfaz.py` | Partículas y números de daño; botones e indicadores del panel. |
| `engine/iso_tools.py` | Motor de clase, se mantiene intacto; el juego usa `grid_to_iso` e `iso_to_grid`. |

### Estado entre escenas

Al entrar en una habitación se guarda el estado de la calle (`jugador`, `enemigos`, `botiquines_suelo`, `municion`). Se carga el interior, pero vida, PA, arma, munición global, botiquines y misión pertenecen al mismo jugador. Al salir se preservan los zombis y objetos del interior y se restaura la calle. Una sala visitada se reutiliza sin recrear sus objetos.

Las funciones de `mapa` publican las paredes y la dimensión activa; el movimiento (`jugador.vecinos`) y la IA (`enemigo.paso_hacia`) las leen en cada acción, por lo que cambiar a habitación 6×6 no modifica las reglas del escenario de 12×12.

## 5. Procedencia de assets

| Elemento | Origen / cómo reproducirlo | Derechos |
|---|---|---|
| `edificio_0.png` a `edificio_3.png`: farmacia, almacén, panadería y casa | Generados con dibujo de polígonos y texto en `herramientas/generar_uruguay.py` usando Pillow | Arte original del proyecto; no se descargaron imágenes de otras fuentes. |
| `edificio_4.png`: Palacio Legislativo | Generado con cajas isométricas en `herramientas/generar_palacio.py` usando Pygame | Arte original del proyecto. |
| `auto_0.png` a `auto_2.png`: taxi, ómnibus y vehículo público | `herramientas/generar_autos.py` (Pygame, cajas isométricas); sus versiones invertidas se realizan en tiempo de ejecución | Arte original del proyecto. |
| `contenedor.png`, `cartel_0.png` a `cartel_2.png` | Mismo generador, carteles de 18 de Julio, Agraciada y Bvar. Artigas | Arte original del proyecto. |
| `mueble_*.png` (6 tipos) | Mismo generador, estantes, mesas, horno, armarios, columnas y mostradores | Arte original del proyecto. |
| `personaje_*.png` (jugador, comunes, corredor, blindado, blindado roto, escupidor y jefe) | `herramientas/generar_personajes.py`, con Pillow, siluetas, rostros y equipos dibujados por coordenadas | Arte original del proyecto. |
| `escombros.png`, `refugio.png`, `suministros.png` | Recursos incluidos con la versión inicial del proyecto suministrada por el equipo | Procedencia original **pendiente de confirmar por los autores de la versión inicial**. |
| Terreno, carteles de puertas, barras de vida, botiquines del suelo, cajas de munición, botones, partículas y animaciones | Dibujados con `pygame.draw` y transformaciones en tiempo de ejecución | Propios del proyecto. |
| Música y efectos sonoros | Ondas generadas mediante Python en `sonido.py` | Composiciones/efectos originales sintéticos; no hay audios de terceros. |
| Motor `engine/iso_tools.py` | Archivo original del motor entregado en clase | Material educativo del curso; no modificado. |
| Pygame | Biblioteca externa, instalada con pip | Ver licencia de la distribución de Pygame. |
| Fuente `Consolas` | Fuente del sistema cuando está disponible; Pygame usa alternativa | No se distribuye ningún archivo de fuente. |

Para regenerar PNG propios hay que instalar opcionalmente **Pillow**: `py -m pip install pillow`, ejecutar `py herramientas/generar_uruguay.py` y `py herramientas/generar_personajes.py`. Los PNG ya están incluidos en el ZIP; Pillow **no es requisito para jugar**. Los vehículos se regeneran con `py herramientas/generar_autos.py` y el Palacio con `py herramientas/generar_palacio.py` (ambos usan Pygame, no Pillow) y comparten `herramientas/comun.py`, que toma el tamaño de baldosa de `mapa.py`.

## 6. Pruebas

Pruebas unitarias sin motor gráfico (`py -m unittest discover -s pruebas -v`): creación de tipos, escupidor, corredor, blindaje, validación de los tres niveles y de todos los interiores (`niveles.validar_todos()`), puertas y PA, conservación de objetos al reingresar, suministros interiores, reinicio, obligación de derrotar al jefe, victoria y alcance de obstáculos. 

**Limitación de validación:** las pruebas automáticas verifican la lógica; la ejecución visual y sonora con Pygame debe revisarse en un equipo que lo tenga instalado.
