import pygame
import time
import random

WIDTH = 640
HEIGHT = 420
BACKGROUND_COLOR = (0, 0, 0)
CELL_ALIVE_COLOR = (255, 255, 255)
RECT_DIM = 10
TIME = time.time()

def create_ruleset():
    """
    create a random ruleset for each new generation.
    Since we are dealing with 1d CA, we have at most 3 cells for each rule,
    meaning we have 8 different scenarios.
    Avoid scenarios in which the ruleset is either all zeros or all ones.
    """
    ruleset = []
    for _ in range(8):
        ruleset.append(random.choice([0,1]))
    
    while sum(ruleset) == 1 or sum(ruleset) == 0:
        ruleset = create_ruleset()

    print(f"NEW RULESET -> {ruleset}")
    return ruleset

def apply_ruleset(left, curr, right, ruleset):
    """
    Computes the new cell value according to the ruleset
    """
    bin_idx = int(str(left) + str(curr) + str(right), 2)
    new_val = ruleset[bin_idx]
    return new_val

def restart_simulation(rows, cols):
    grid = [[0 for _ in range(cols)] for _ in range(rows)]
    for i in range(len(grid[0])):
        grid[0][i] = random.choice([0, 1])
    ruleset = create_ruleset()

    return grid, ruleset

def draw(screen, grid):
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
    for i in range(len(grid[0])):
        grid[0][i] = random.choice([0, 1])
        
    print(f"NEW GRID CREATED -> ROWS: {len(grid)}, COLS: {len(grid[0])}")
    
    ruleset = create_ruleset()

    screen.fill(BACKGROUND_COLOR)

    running = True

    pygame.display.set_caption("1D CA")
    while running:
        screen.fill(BACKGROUND_COLOR)
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    grid, ruleset = restart_simulation(rows, cols)

        new_generation_line = []
        for i in range(len(grid[0])):
            left_neighbour = grid[0][i-1]
            cell = grid[0][i]
            right_neighbour = grid[0][(i+1)%len(grid[0])]

            new_cell = apply_ruleset(left_neighbour, cell, right_neighbour, ruleset)
            new_generation_line.append(new_cell)
        
        for i in range(len(grid)-1, 0, -1):
            grid[i] = grid[i-1]

        grid[0] = new_generation_line
        draw(screen, grid)
        # Update display
        pygame.display.update()
        clock.tick(10)



if __name__ == "__main__":
    main()