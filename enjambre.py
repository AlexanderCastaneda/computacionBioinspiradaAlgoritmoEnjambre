## pip install pygame

import pygame
import random
import math

# ----------------------- Configuración Inicial -----------------------
ANCHO, ALTO = 800, 600
NUM_PECES = 30
RADIO_VISION = 100
VELOCIDAD_MAXIMA = 2
DISTANCIA_SEPARACION = 20
DISTANCIA_HUIDA = 100  # Distancia para detectar al "tiburón"

# ---------------------- Clase Pez ----------------------
class Pez:
    def __init__(self, x, y):
        # Posición y velocidad inicial agrupada
        self.pos = pygame.Vector2(x, y)
        self.vel = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))

    def actualizar(self, peces, tiburon_pos):
        # Variables de comportamiento del enjambre
        cohesion = pygame.Vector2(0, 0)
        separacion = pygame.Vector2(0, 0)
        alineacion = pygame.Vector2(0, 0)
        total = 0

        # Regla de evasión del tiburón (el mouse)
        evadir = pygame.Vector2(0, 0)
        distancia_al_tiburon = self.pos.distance_to(tiburon_pos)

        if distancia_al_tiburon < DISTANCIA_HUIDA:
            # Huir del tiburón
            evadir = self.pos - tiburon_pos
            evadir.scale_to_length(VELOCIDAD_MAXIMA * 2)

        # Reglas de comportamiento del cardumen
        for otro in peces:
            if otro == self:
                continue
            distancia = self.pos.distance_to(otro.pos)
            if distancia < RADIO_VISION:
                cohesion += otro.pos
                alineacion += otro.vel
                if distancia < DISTANCIA_SEPARACION:
                    separacion -= (otro.pos - self.pos)
                total += 1

        if total > 0:
            cohesion = (cohesion / total - self.pos) * 0.05
            alineacion = (alineacion / total - self.vel) * 0.05
            separacion *= 0.1

        # Velocidad resultante
        self.vel += cohesion + alineacion + separacion + evadir

        # Limitar la velocidad
        if self.vel.length() > VELOCIDAD_MAXIMA:
            self.vel.scale_to_length(VELOCIDAD_MAXIMA)

        self.pos += self.vel

        # Evitar salir de la pantalla
        self.pos.x = max(0, min(ANCHO, self.pos.x))
        self.pos.y = max(0, min(ALTO, self.pos.y))

    def dibujar(self, pantalla):
        pygame.draw.circle(pantalla, (0, 150, 255), self.pos, 5)


# ---------------------- Función Principal ----------------------
def main():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Simulación de Cardumen Bioinspirado 🐟🦈")

    # Inicializar peces agrupados en el centro
    centro = pygame.Vector2(ANCHO / 2, ALTO / 2)
    peces = [Pez(centro.x + random.uniform(-30, 30), centro.y + random.uniform(-30, 30)) for _ in range(NUM_PECES)]

    reloj = pygame.time.Clock()
    corriendo = True

    while corriendo:
        pantalla.fill((25, 25, 25))  # Fondo

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False

        tiburon_pos = pygame.Vector2(pygame.mouse.get_pos())

        # Dibujar el tiburón (mouse)
        pygame.draw.circle(pantalla, (255, 0, 0), tiburon_pos, 10)

        # Actualizar y dibujar peces
        for pez in peces:
            pez.actualizar(peces, tiburon_pos)
            pez.dibujar(pantalla)

        pygame.display.flip()
        reloj.tick(60)

    pygame.quit()

# ---------------------- Ejecutar ----------------------
if __name__ == "__main__":
    main()