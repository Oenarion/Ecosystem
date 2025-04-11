import pygame
import oscillators as oscillators
import random
import math
import time

WIDTH = 640
HEIGHT = 420
BACKGROUND_COLOR = (0, 0, 0)



def main():
    pygame.init()
    clock = pygame.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    screen.fill(BACKGROUND_COLOR)
    pendulum = oscillators.Pendulum(WIDTH//2, 50, 200, 90, 0, 0, 20)
    gravity = pygame.Vector2(0, 40)
    running = True

    pygame.display.set_caption("Oscillation")
    while running:
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False # Quit simulation

        pendulum.update(gravity)
        screen.fill(BACKGROUND_COLOR)
        pendulum.draw(screen)
        # Update display
        pygame.display.update()
        clock.tick(60)



if __name__ == "__main__":
    main()