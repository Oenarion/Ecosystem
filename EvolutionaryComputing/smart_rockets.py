import pygame
import time
import random
from DNA import DNA, Rocket, Population
import numpy as np
import math

WIDTH = 640
HEIGHT = 420
BACKGROUND_COLOR = (0, 0, 0)
TIME = time.time()
lifespan = 500
population_length = 40
 

def draw(screen, phrases, generations, avg_score, mutation_factor, font):
    start_x = (WIDTH // 2) + 50
    start_y = 10

    counter = 0
    for i in range(len(phrases)-1, -1, -1):
        text = font.render(phrases[i].get_phrase(), True, (255, 255, 255))
        screen.blit(text, (start_x, start_y + 30*counter))
        counter += 1
    
    best_text = font.render("Best phrase", True, (0, 255, 0))  # verde brillante
    screen.blit(best_text, (10, 50))

    best_font = pygame.font.Font(None, 40)
    best_text = best_font.render(phrases[0].get_phrase(), True, (0, 255, 0))  # verde brillante
    screen.blit(best_text, (10, 100))

    curr_generations = font.render(f"Total generations: {generations}", True, (255, 255, 255))
    screen.blit(curr_generations, (10, 200))

    curr_fitness = font.render(f"Average score: {avg_score}", True, (255, 255, 255))
    screen.blit(curr_fitness, (10, 230))

    curr_mutation = font.render(f"Mutation factor: {mutation_factor}", True, (255, 255, 255))
    screen.blit(curr_mutation, (10, 260))

    curr_mutation = font.render(f"Press +/- to increase/decrease mutation", True, (255, 255, 255))
    screen.blit(curr_mutation, (10, 390))



def main():
    
    pygame.init()
    clock = pygame.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.fill(BACKGROUND_COLOR)
    FONT = pygame.font.Font(None, 24)
    lifespan = 90
    life_passed = 0
    mutation_factor = 1
    target = Rocket(WIDTH//2, 20, 10, 100)
    population = Population(population_length, WIDTH//2, HEIGHT - 10, lifespan, mutation_factor, target)
    running = True

    pygame.display.set_caption("Writing Monkeys")
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 
            
        screen.fill(BACKGROUND_COLOR)    
        if life_passed < lifespan:
            life_passed += 1
            population.live()
        else:
            population.fitness()
            population.normalize_fitness()
            population.reproduction()
            life_passed = 0

        target.draw(screen)
        population.draw(screen)
        # Update display
        pygame.display.update()
        clock.tick(30)



if __name__ == "__main__":
    main()