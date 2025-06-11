import pygame
import time
from flappy_objects import BirdPopulation, PipeGenerator

WIDTH = 640
HEIGHT = 420
BACKGROUND_COLOR = (0, 0, 0)
TIME = time.time()
NUM_BIRDS = 100

def render_text(screen, generation, best_score, curr_score, font, start_time):
    elapsed_time = int(time.time() - start_time)
    hours = elapsed_time // 3600
    minutes = (elapsed_time % 3600) // 60
    seconds = elapsed_time % 60
    time_text = f"Time: {hours:02}:{minutes:02}:{seconds:02}"
    time_surface = font.render(time_text, True, (0, 255, 0))
    screen.blit(time_surface, (WIDTH - 150, 5))
    error_text = font.render(f"GENERATION: {generation}", True, (0, 255, 0))
    screen.blit(error_text, (10, 5))
    score_text = font.render(f"BEST SCORE: {best_score}", True, (0, 255, 0))
    screen.blit(score_text, (10, 15))
    score_text = font.render(f"CURRENT SCORE: {curr_score}", True, (0, 255, 0))
    screen.blit(score_text, (10, 25))


def main():
    
    pygame.init()
    clock = pygame.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.fill(BACKGROUND_COLOR)
    FONT = pygame.font.Font(None, 20)
    flappy_birds = BirdPopulation(NUM_BIRDS, 50, HEIGHT//2)
    pipe_generator = PipeGenerator(100, HEIGHT, WIDTH, 120)
    running = True
    pause_visualization = False
    pygame.display.set_caption("Flappy Bird")
    start_time = time.time()

    best_score = 0
    curr_score = 0
    generation = 0
    last_seen_score_idx = -1
    while running:
        screen.fill(BACKGROUND_COLOR)
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 

            if event.type ==  pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pause_visualization = not pause_visualization

        # run the birds
        restart_simulation = flappy_birds.run(pipe_generator.pipes, HEIGHT, WIDTH)        
        # if all birds are dead restart
        if restart_simulation:
            generation += 1
            curr_score = 0
            last_seen_score_idx = -1
            pipe_generator = PipeGenerator(100, HEIGHT, WIDTH, 120)
        
        # get first alive bird
        alive_bird = None
        for bird in flappy_birds.birds:
            if bird.alive:
                alive_bird = bird
                break
        
        if alive_bird:
            # check if it surpassed the pipe, update score
            for pipe in pipe_generator.pipes:
                if pipe.top_pipe.x + pipe.pipe_dim < alive_bird.rect.x and pipe.id != last_seen_score_idx:
                    curr_score += 1 
                    last_seen_score_idx = pipe.id
                    if curr_score > best_score:
                        best_score = curr_score
                    break

        # delete useless pipes and update positions
        pipe_generator.delete_old_pipes()
        pipe_generator.update()

        # faster simulation if needed
        if pause_visualization:
            screen.fill(BACKGROUND_COLOR)
            render_text(screen, generation, best_score, curr_score, FONT, start_time)
            pygame.display.update()
            clock.tick(0)
        else:
            pipe_generator.draw(screen)
            flappy_birds.draw(screen)
            render_text(screen, generation, best_score, curr_score, FONT, start_time)
            pygame.display.update()
            clock.tick(100)
        




if __name__ == "__main__":
    main()