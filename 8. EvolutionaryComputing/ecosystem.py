import pygame
import time
from bloops import World

WIDTH = 640
HEIGHT = 420
BACKGROUND_COLOR = (0, 0, 0)
TIME = time.time()
NUM_BLOOPS = 50
NUM_FOOD = 40


def main():
    
    pygame.init()
    clock = pygame.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.fill(BACKGROUND_COLOR)
    world = World(NUM_BLOOPS, WIDTH, HEIGHT, NUM_FOOD)
    running = True

    pygame.display.set_caption("Ecosystem")
    while running:
        # Handle events
        screen.fill(BACKGROUND_COLOR)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 

        world.run(screen)
        # Update display
        pygame.display.update()
        clock.tick(60)



if __name__ == "__main__":
    main()