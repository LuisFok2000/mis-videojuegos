import pygame
from engine.game_loop import GameLoop

ANCHO, ALTO = 800, 600


class SpaceInvaders(GameLoop):
    def __init__(self):
        super().__init__(ANCHO, ALTO, "Space Invaders", 60)
        self.nave = pygame.Rect(ANCHO // 2 - 30, ALTO - 60, 60, 30)
        self.balas = []
        self.enemigos = [pygame.Rect(x, y, 40, 30)
                         for x in range(40, ANCHO - 40, 60)
                         for y in range(30, 150, 40)]
        self.direccion = 1
        self.puntos = 0
        self.vidas = 3
        self.invulnerable_hasta = 0
        self.resultado = None
        self.fuente = pygame.font.Font(None, 36)

    def handle_specific_events(self, evento):
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE and self.resultado is None:
                self.balas.append(pygame.Rect(self.nave.centerx - 2, self.nave.y, 4, 12))
            if evento.key == pygame.K_ESCAPE:
                self.running = False

    def update_game_logic(self):
        if self.resultado is not None:
            return

        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]:
            self.nave.x -= 6
        if teclas[pygame.K_RIGHT]:
            self.nave.x += 6
        self.nave.x = max(0, min(ANCHO - self.nave.width, self.nave.x))

        for bala in self.balas[:]:
            bala.y -= 8
            if bala.bottom < 0:
                self.balas.remove(bala)

        if any(e.right >= ANCHO or e.left <= 0 for e in self.enemigos):
            self.direccion *= -1
            for enemigo in self.enemigos:
                enemigo.y += 20
        for enemigo in self.enemigos:
            enemigo.x += 3 * self.direccion

        for bala in self.balas[:]:
            for enemigo in self.enemigos[:]:
                if bala.colliderect(enemigo):
                    self.balas.remove(bala)
                    self.enemigos.remove(enemigo)
                    self.puntos += 10
                    break

        if not self.enemigos:
            self.resultado = "¡Ganaste!"
            return

        ahora = pygame.time.get_ticks()
        for enemigo in self.enemigos:
            if enemigo.bottom >= ALTO:
                self.resultado = "Perdiste"
                return
            if enemigo.colliderect(self.nave) and ahora >= self.invulnerable_hasta:
                self.vidas -= 1
                self.invulnerable_hasta = ahora + 1000
                if self.vidas == 0:
                    self.resultado = "Perdiste"
                break

    def draw_game_elements(self):
        self.screen.fill((10, 10, 20))
        ahora = pygame.time.get_ticks()
        # Mientras está protegida, la nave aparece y desaparece.
        if ahora >= self.invulnerable_hasta or (ahora // 100) % 2 == 0:
            pygame.draw.rect(self.screen, (0, 255, 120), self.nave)
        for bala in self.balas:
            pygame.draw.rect(self.screen, (255, 255, 100), bala)
        for enemigo in self.enemigos:
            pygame.draw.rect(self.screen, (255, 80, 80), enemigo)
        marcador = self.fuente.render(f"Puntos: {self.puntos}    Vidas: {self.vidas}", True, (255, 255, 255))
        self.screen.blit(marcador, (15, ALTO - 40))
        if self.resultado:
            mensaje = self.fuente.render(self.resultado, True, (255, 255, 255))
            self.screen.blit(mensaje, mensaje.get_rect(center=(ANCHO // 2, ALTO // 2)))


if __name__ == "__main__":
    SpaceInvaders().run()
