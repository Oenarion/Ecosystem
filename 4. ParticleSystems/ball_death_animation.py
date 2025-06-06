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
    clock = pygame.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    screen.fill(BACKGROUND_COLOR)
    color = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
    exploding_ball = particles.ExplodingBall(WIDTH//2, 50, 10, color)
    gravity = pygame.Vector2(0, 0.1)
    running = True


    pygame.display.set_caption("Exploding Ball")
    while running:
        screen.fill(BACKGROUND_COLOR)
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 

        exploding_ball.apply_force(gravity)
        exploding_ball.update_position(HEIGHT)
        exploding_ball.draw(screen)

        # Update display
        pygame.display.update()
        clock.tick(60)



if __name__ == "__main__":
    main()