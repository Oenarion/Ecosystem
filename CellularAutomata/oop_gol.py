import pygame
import time
import random
import objects

WIDTH = 640
HEIGHT = 420
BACKGROUND_COLOR = (0, 0, 0)
CELL_ALIVE_COLOR = (255, 255, 255)
RECT_DIM = 5
TIME = time.time()


def restart_simulation(rows: int, cols: int) -> list:
    grid = objects.Grid(rows, cols, RECT_DIM)
    return grid

def main():
    
    pygame.init()
    clock = pygame.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    rows, cols = HEIGHT // RECT_DIM, WIDTH // RECT_DIM
    grid = objects.Grid(rows, cols, RECT_DIM)

    screen.fill(BACKGROUND_COLOR)

    running = True

    pygame.display.set_caption("OOP Game of life")
    while running:
        screen.fill(BACKGROUND_COLOR)
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    grid = restart_simulation(rows, cols)

        grid.update_grid()
        grid.draw(screen)
        # Update display
        pygame.display.update()
        clock.tick(30)



if __name__ == "__main__":
    main()