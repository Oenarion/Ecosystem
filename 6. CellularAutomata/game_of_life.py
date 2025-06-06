import pygame
import time
import random

WIDTH = 640
HEIGHT = 420
BACKGROUND_COLOR = (0, 0, 0)
CELL_ALIVE_COLOR = (255, 255, 255)
RECT_DIM = 5
TIME = time.time()

def get_neighbours_sum(i: int, j: int, grid: list) -> int:
    """
    Computes the sum of the neighbours of the current cell.
    It's used to later evaluate the current cell to alive or dead.

    Args:
        - i -> x index of the cell
        - j -> y index of the cell
        - grid -> the whole grid

    Returns the sum of the neighbours, i.e. alive neighbours
    """
    neighbours_sum = 0
    for z in range(i-1, i+2):
        for t in range(j-1, j+2):
            if (z == i and t == j) or z < 0 or z >= len(grid) or t < 0 or t >= len(grid[0]):
                continue
            neighbours_sum += grid[z][t]

    return neighbours_sum


def restart_simulation(rows: int, cols: int) -> list:
    grid = [[0 for _ in range(cols)] for _ in range(rows)]
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if random.randint(0, 100) < 10:
                grid[i][j] = 1
            else:
                grid[i][j] = 0

    return grid

def update_grid(grid: list) -> list:
    """
    updates the grid in the correct way, had issues with updating the same variable twice.

    Args:
        - grid -> grid of values.
    """
    rows, cols = len(grid), len(grid[0])
    new_grid = [[0 for _ in range(cols)] for _ in range(rows)]
    
    for i in range(rows):
        for j in range(cols):
            cell = grid[i][j]
            neighbours = get_neighbours_sum(i, j, grid)
            if cell == 1:
                if 2 <= neighbours <= 3:
                    new_grid[i][j] = 1
            else:
                if neighbours == 3:
                    new_grid[i][j] = 1
    return new_grid

def draw(screen, grid: list) -> None:
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            color = CELL_ALIVE_COLOR if grid[i][j] == 1 else BACKGROUND_COLOR
            pygame.draw.rect(screen, color, pygame.Rect(j*RECT_DIM, i*RECT_DIM, RECT_DIM, RECT_DIM))

def main():
    
    pygame.init()
    clock = pygame.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    rows, cols = HEIGHT // RECT_DIM, WIDTH // RECT_DIM
    grid = [[0 for _ in range(cols)] for _ in range(rows)]

    # generate randomly the first iteration
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if random.randint(0, 100) < 10:
                grid[i][j] = 1
            else:
                grid[i][j] = 0

    screen.fill(BACKGROUND_COLOR)

    running = True

    pygame.display.set_caption("Game of life")
    while running:
        screen.fill(BACKGROUND_COLOR)
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    grid = restart_simulation(rows, cols)

        grid = update_grid(grid)

        draw(screen, grid)
        # Update display
        pygame.display.update()
        clock.tick(30)



if __name__ == "__main__":
    main()