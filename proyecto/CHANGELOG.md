# Historial de versiones — Dead Zone: Uruguay

## 2.1.1 — 06/11/2026: retoques visuales
- El contenedor con el rótulo "RES" ahora es un tacho de basura verde sin texto (`generar_uruguay.py: tacho()`), y ya no queda detrás del refugio.
- Los tachos de los tres niveles se movieron a casillas donde no los tapa ningún edificio, y varían de un nivel a otro.
- El refugio mantiene su diseño original (solo el cartel).
- Con los suministros recogidos, la casilla del refugio late en verde y aparece una flecha sobre el cartel.
- Las etiquetas de los zombis tienen fondo oscuro para leerse delante de edificios claros.
- Cartel "BVAR ARTIGAS" corregido a "BV. ARTIGAS"; el nivel 3 usa un cartel distinto.

## 2.1 — 06/11/2026: reorganización del código
- `main.py` dividido en `pantalla`, `entrada`, `acciones` y el bucle; `dibujo` dividido en `dibujo_mundo` y `dibujo_panel`.
- Datos de los niveles separados en `niveles.py` (incluye la decoración de calle); `mapa.py` solo guarda la escena activa. La validación ya no se ejecuta al importar: se llama con `niveles.validar_todos()` al iniciar y en las pruebas.
- `navegacion.py` fusionado en `combate.py` (distancia), `jugador.py` (vecinos) y `enemigo.py` (BFS).
- Una sola `nueva_partida(nivel, previo)`; `acciones.py` sin funciones de una línea.
- Nombres unificados en español (funciones, constantes y claves del estado de la partida).
- `herramientas/comun.py` con lo compartido por los generadores con Pygame; eliminado `auto()` de `generar_uruguay.py` (ya no se usaba). Los PNG regenerados son idénticos a los incluidos.
- Documentación reducida: `PRUEBA_MANUAL.md` pasó al README y el diario de avances a este historial.
- Verificación: 136 capturas y mensajes de una partida guiada son idénticos píxel a píxel a los de la versión anterior; 18 pruebas en verde.

## 2.0 — 05/11/2026: versión completa
- Tres niveles: Barrio infectado, Avenida bloqueada y Palacio Legislativo (con jefe obligatorio).
- Enemigos especiales: común, corredor, blindado (armadura rompible solo con el bate), escupidor (ataque a distancia) y jefe.
- Interiores 6×6 en todos los edificios, con puertas de 1 PA, muebles, botiquines, munición y enemigos; los recursos y enemigos persisten al salir y volver a entrar.
- Edificios de inspiración uruguaya (Farmashop, almacén, panadería, casa, Palacio), taxis, ómnibus, contenedores y carteles.
- Personajes que respiran y se balancean, con los pies apoyados en la baldosa (se corrigió que levitaran).
- Música sintetizada distinta para calle, edificios y Palacio.
