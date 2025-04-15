import pygame
import particles
import random
import math
import time

WIDTH = 640
HEIGHT = 420
BACKGROUND_COLOR = (0, 0, 0)
TIME = time.time()



def main():
    
    pygame.init()
    FONT =  pygame.font.Font(None, 24)
    clock = pygame.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    screen.fill(BACKGROUND_COLOR)
    first_emitter = particles.Emitter(WIDTH//2, 50)
    gravity = pygame.Vector2(0, 0.1)
    running = True
    
    emitters = [first_emitter]

    pygame.display.set_caption("Particle System")
    while running:
        screen.fill(BACKGROUND_COLOR)
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 

            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                new_emitter = particles.Emitter(pos[0], pos[1])
                emitters.append(new_emitter)

        for emitter in emitters:
            emitter.add_particle()
            emitter.run(gravity, screen)
        
        # Update display
        pygame.display.update()
        clock.tick(60)



if __name__ == "__main__":
    main()