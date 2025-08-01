import pygame
import time
from snake_objects import Snake, Grid
import os


WIDTH = 400
HEIGHT = 400
DIM = 10
BACKGROUND_COLOR = (0, 0, 0)
TIME = time.time()




def main():
    
    pygame.init()
    clock = pygame.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.fill(BACKGROUND_COLOR)
    FONT = pygame.font.Font(None, 24)
    running = True
    score = 0
    grid = Grid(WIDTH, HEIGHT, DIM)
    last_seen_move = ''
    direction_chosen = False
    snake = Snake(31, 21, grid)
    grid.grid[31][21] = 'S'
    grid.add_food()

    pygame.display.set_caption("Snake")
    while running:
        screen.fill(BACKGROUND_COLOR)
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 
            
            if event.type == pygame.KEYDOWN:
                if not direction_chosen:
                    if (event.key == pygame.K_w or event.key == pygame.K_UP) and last_seen_move != 'S':
                        last_seen_move = "W"
                        direction_chosen = True
                    if (event.key == pygame.K_a or event.key == pygame.K_LEFT)and last_seen_move != 'D':
                        last_seen_move = "A"
                        direction_chosen = True
                    if (event.key == pygame.K_s or event.key == pygame.K_DOWN)and last_seen_move != 'W':
                        last_seen_move = "S"
                        direction_chosen = True
                    if (event.key == pygame.K_d or event.key == pygame.K_RIGHT) and last_seen_move != 'A':
                        last_seen_move = "D"
                        direction_chosen = True

        # for i in range(len(grid)):
        #     for j in range(len(grid[0])):
        #         pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(i*DIM, j*DIM, DIM, DIM), width = 1)

        direction_chosen = False
        snake.move(last_seen_move)
        eaten = snake.eat()
        snake.check_hit()
        if not snake.is_alive:
            print("GAME OVER")
            running = False
        if eaten:
            score += 1
            grid.add_food()
        grid.update_grid(snake.positions[0], snake.last_position, eaten)
        grid.draw(screen, snake.positions[0])

        score_text = FONT.render(f"SCORE: {score}", True, (200, 255, 0))
        screen.blit(score_text, (WIDTH//2 - 50, 10))

        # Update display
        pygame.display.update()
        clock.tick(30)



if __name__ == "__main__":
    main()