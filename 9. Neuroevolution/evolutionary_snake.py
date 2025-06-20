import pygame
import time
from snake_objects import SnakePopulation
import os
import sys


DIM = 10
BACKGROUND_COLOR = (0, 0, 0)
TIME = time.time()
snake_population = 200
move_map = {
    0: 'A',
    1: 'W',
    2: 'D',
    3: 'S'
}

def main(WIDTH, HEIGHT):
    
    pygame.init()
    clock = pygame.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.fill(BACKGROUND_COLOR)
    FONT = pygame.font.Font(None, 24)
    running = True
    run_number = 0
    last_moves = ['D' for _ in range(snake_population)]
    start_x, start_y = 10, 10
    snakes = SnakePopulation(snake_population, start_x, start_y, WIDTH, HEIGHT, DIM)
    for snake in snakes.snakes:
        snake.grid.grid[start_x][start_y] = 'S'
        snake.grid.add_food(avoid_row = start_x)


    pygame.display.set_caption("Evolutionary Snake")
    while running:
        screen.fill(BACKGROUND_COLOR)
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 

        restart = snakes.run(start_x, start_y, WIDTH, HEIGHT, DIM, last_moves, screen, run_number)
        if restart:
            run_number += 1
        score_text = FONT.render(f"RUN: {run_number}", True, (200, 255, 0))
        screen.blit(score_text, (WIDTH//2 - 20, 10))

        # Update display
        pygame.display.update()
        clock.tick(60)



if __name__ == "__main__":
    if len(sys.argv) > 1:
        WIDTH = int(sys.argv[1])
        HEIGHT = int(sys.argv[2])
        print(WIDTH, HEIGHT)
    else:
        WIDTH = 200
        HEIGHT = 200
    main(WIDTH, HEIGHT)