import pygame
import particles
import random
import math
import time

WIDTH = 640
HEIGHT = 420
BACKGROUND_COLOR = (0, 0, 0)
TIME = time.time()
MIN_PARTICLES = 10
MAX_PARTICLES = 200



def main():
    
    pygame.init()
    FONT =  pygame.font.Font(None, 24)
    clock = pygame.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    screen.fill(BACKGROUND_COLOR)
    first_emitter = particles.Emitter(WIDTH//2, 50, 
                                      random.randint(MIN_PARTICLES, MAX_PARTICLES))
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
                new_emitter = particles.Emitter(pos[0], pos[1], 
                                                random.randint(MIN_PARTICLES, MAX_PARTICLES))
                emitters.append(new_emitter)

        for i in range(len(emitters)-1, -1, -1):
            emitters[i].add_particle()
            emitters[i].apply_force(gravity)
            emitters[i].run(screen)
            if emitters[i].is_dead():
                emitters.pop(i)
        
        # Update display
        pygame.display.update()
        clock.tick(60)



if __name__ == "__main__":
    main()