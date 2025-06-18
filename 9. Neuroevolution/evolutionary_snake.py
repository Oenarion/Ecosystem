import pygame
import time
from snake_objects import Snake, SnakePopulation
import os


WIDTH = 400
HEIGHT = 400
DIM = 10
BACKGROUND_COLOR = (0, 0, 0)
TIME = time.time()
snake_population = 500
move_map = {
    0: 'A',
    1: 'W',
    2: 'D',
    3: 'S'
}

def check_illegal_move(new_move, last_move):
    if (new_move == 'D' and last_move == 'A') or (new_move == 'A' and last_move == 'D') \
        or (new_move == 'W' and last_move == 'S') or (new_move == 'S' and last_move == 'W'):
        return True
    return False

def main():
    
    pygame.init()
    clock = pygame.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.fill(BACKGROUND_COLOR)
    FONT = pygame.font.Font(None, 24)
    running = True
    run_number = 0
    last_moves = ['D' for _ in range(snake_population)]
    start_x, start_y = 31, 21
    snakes = SnakePopulation(snake_population, start_x, start_y, WIDTH, HEIGHT, DIM)
    for snake in snakes.snakes:
        snake.grid.grid[31][21] = 'S'
        snake.grid.add_food()


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
        clock.tick(30)



if __name__ == "__main__":
    main()