import pygame
import time
import random
from DNA import SmartPopulation, Target, Obstacle
import numpy as np
import math

WIDTH = 640
HEIGHT = 420
BACKGROUND_COLOR = (0, 0, 0)
TIME = time.time()
lifespan = 500
population_length = 40
 

def draw(screen, generation, lifespan, font):
    
    generation_text = font.render(f"Generation: {generation}", True, (255, 255, 255))  # verde brillante
    screen.blit(generation_text, (10, 10))

    lifespan_text = font.render(f"Lifespan left: {lifespan}", True, (255, 255, 255))
    screen.blit(lifespan_text, (10, 40))


def main():
    
    pygame.init()
    clock = pygame.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.fill(BACKGROUND_COLOR)
    FONT = pygame.font.Font(None, 24)
    lifespan = 120
    life_passed = 0
    generation = 0
    mutation_factor = 10
    obstacles = [Obstacle(280, 300, 60, 10, (255, 0, 0)), Obstacle(200, 150, 60, 10, (255, 0, 0)), Obstacle(360, 150, 60, 10, (255, 0, 0))]
    target = Obstacle(WIDTH//2-5, 20, 10, 10, (0, 255, 0))
    population = SmartPopulation(population_length, WIDTH//2, HEIGHT - 10, lifespan, mutation_factor, target, obstacles)
    running = True

    pygame.display.set_caption("Writing Monkeys")
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 

            if event.type == pygame.MOUSEBUTTONUP:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                target = Obstacle(mouse_x, mouse_y, 10, 10, (0, 255, 0))
            
        screen.fill(BACKGROUND_COLOR)    
        if life_passed < lifespan:
            life_passed += 1
            population.live()
        else:
            population.fitness()
            population.normalize_fitness()
            population.reproduction()
            life_passed = 0
            generation += 1

        target.draw(screen)
        population.draw(screen)
        for obstacle in obstacles:
            obstacle.draw(screen)
        draw(screen, generation, lifespan - life_passed, FONT)
        # Update display
        pygame.display.update()
        clock.tick(30)



if __name__ == "__main__":
    main()