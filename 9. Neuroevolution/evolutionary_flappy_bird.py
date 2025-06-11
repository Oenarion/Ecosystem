import pygame
import time
from flappy_objects import BirdPopulation, PipeGenerator

WIDTH = 640
HEIGHT = 420
BACKGROUND_COLOR = (0, 0, 0)
TIME = time.time()
NUM_BIRDS = 30



def main():
    
    pygame.init()
    clock = pygame.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.fill(BACKGROUND_COLOR)
    FONT = pygame.font.Font(None, 24)
    flappy_birds = BirdPopulation(NUM_BIRDS, 50, HEIGHT//2)
    pipe_generator = PipeGenerator(100, HEIGHT, WIDTH, 120)
    running = True

    pygame.display.set_caption("Flappy Bird")
    while running:
        screen.fill(BACKGROUND_COLOR)
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 

        restart_simulation = flappy_birds.run(pipe_generator.pipes, HEIGHT, WIDTH)        
        if restart_simulation:
            pipe_generator = PipeGenerator(100, HEIGHT, WIDTH, 120)
            
        pipe_generator.delete_old_pipes()
        pipe_generator.update()

        pipe_generator.draw(screen)
        flappy_birds.draw(screen)

        # Update display
        pygame.display.update()
        clock.tick(30)



if __name__ == "__main__":
    main()