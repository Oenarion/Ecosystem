import pygame
import time
import random
import objects

WIDTH = 500
HEIGHT = 500
BACKGROUND_COLOR = (0, 0, 0)
CELL_ALIVE_COLOR = (255, 255, 255)
RECT_DIM = 5
TIME = time.time()


def restart_simulation(rows: int, cols: int, num_of_grids_x, num_of_grids_y) -> list:
    grid = objects.MacroGrid(rows, cols, RECT_DIM, num_of_grids_x, num_of_grids_y)
    return grid

def main():
    
    pygame.init()
    clock = pygame.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    num_of_grids_x, num_of_grids_y = 5, 5 
    rows, cols = HEIGHT // (num_of_grids_y*RECT_DIM), WIDTH // (num_of_grids_x*RECT_DIM)
    macro_grid = objects.MacroGrid(rows, cols, RECT_DIM, num_of_grids_x, num_of_grids_y)

    screen.fill(BACKGROUND_COLOR)

    running = True

    pygame.display.set_caption("CA inside CA")
    while running:
        screen.fill(BACKGROUND_COLOR)
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    macro_grid = restart_simulation(rows, cols, num_of_grids_x, num_of_grids_y)

        macro_grid.update_grid()
        macro_grid.draw(screen)
        # Update display
        pygame.display.update()
        clock.tick(30)



if __name__ == "__main__":
    main()