import pygame
import time
from flappy_objects import Bird, PipeGenerator
import os


WIDTH = 640
HEIGHT = 420
BACKGROUND_COLOR = (0, 0, 0)
TIME = time.time()




def main():
    
    pygame.init()
    clock = pygame.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.fill(BACKGROUND_COLOR)
    FONT = pygame.font.Font(None, 24)
    flappy_bird = Bird(50, HEIGHT//2)
    enemy_bird = Bird(50, HEIGHT, color=(128, 0, 128))
    if os.path.exists("weights\\best_bird_brain.pth"):
        enemy_bird.brain.load("weights\\best_bird_brain.pth")
    else:
        enemy_bird = None

    print(enemy_bird)
    pipe_generator = PipeGenerator(100, HEIGHT, WIDTH, 120)
    running = True

    last_seen_error_idx = -1
    last_seen_score_idx = -1
    errors = 0
    score = 0

    pygame.display.set_caption("Flappy Bird")
    while running:
        screen.fill(BACKGROUND_COLOR)
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    flappy_bird.flap()

                if event.key == pygame.K_p:
                    if enemy_bird is not None:
                        enemy_bird.alive = not enemy_bird.alive

        flappy_bird.update(HEIGHT)
        collided, id = pipe_generator.detect_collisions(flappy_bird.rect)
        if collided:
            if id != last_seen_error_idx:
                errors += 1
                print(f"Total errors: {errors}")
                last_seen_error_idx = id

        for pipe in pipe_generator.pipes:
            if pipe.top_pipe.x + pipe.pipe_dim < flappy_bird.rect.x and pipe.id != last_seen_error_idx and pipe.id != last_seen_score_idx:
                score += 1 
                last_seen_score_idx = pipe.id
                break
        
        pipe_generator.delete_old_pipes()
        pipe_generator.update()

        pipe_generator.draw(screen)

        if enemy_bird is not None:
            if enemy_bird.alive:
                collided, id = pipe_generator.detect_collisions(enemy_bird.rect)
                if collided:
                    enemy_bird.alive = False
                enemy_bird.think(pipe_generator.pipes, HEIGHT, WIDTH)
                enemy_bird.update(HEIGHT)
                enemy_bird.draw(screen)
                
        flappy_bird.draw(screen)

        error_text = FONT.render(f"ERRORS: {errors}", True, (0, 255, 0))
        screen.blit(error_text, (10, 10))
        score_text = FONT.render(f"SCORE: {score}", True, (0, 255, 0))
        screen.blit(score_text, (10, 30))

        # Update display
        pygame.display.update()
        clock.tick(30)



if __name__ == "__main__":
    main()