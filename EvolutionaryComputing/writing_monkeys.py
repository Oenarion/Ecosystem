import pygame
import time
import random
from DNA import DNA
import numpy as np

WIDTH = 640
HEIGHT = 420
BACKGROUND_COLOR = (0, 0, 0)
TIME = time.time()

population_length = 160
 
TARGET = "CACATO NEL PUZZONG"

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

def change_mutation_factor(phrases, mutation_factor):
    """
    Change mutation factor in a range between 1 and 100
    
    Args:
        - phrases: the DNA object that we want to change
        - mutation_factor: the mutation factor
    """

    for i in range(len(phrases)):
        phrases[i].mutation_factor = mutation_factor


def main():
    
    pygame.init()
    clock = pygame.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.fill(BACKGROUND_COLOR)
    FONT = pygame.font.Font(None, 24)
    evolve = True
    population = []
    mutation_factor = 1
    generations = 0
    for _ in range(population_length):
        population.append(DNA(len(TARGET), mutation_factor))

    running = True

    pygame.display.set_caption("Writing Monkeys")
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PLUS:
                    mutation_factor += 1 
                    if mutation_factor > 100:
                        mutation_factor = 100
                    change_mutation_factor(population, mutation_factor)
                if event.key == pygame.K_MINUS:
                    mutation_factor -= 1
                    if mutation_factor < 1:
                        mutation_factor = 1
                    change_mutation_factor(population, mutation_factor)

        if evolve:
            scores = []
            screen.fill(BACKGROUND_COLOR)
            # compute fitness
            for i, phrase in enumerate(population):
                phrase.fitness_score(TARGET)
                scores.append((phrase.score, i))
            
            scores.sort(reverse=True)
            top_phrases = []
            for i in range(14):
                top_phrases.append(population[scores[i][1]])

            avg_score = np.mean(scores)
            # stop evolution if we got the phrase correctly
            if scores[0][0] == 1.0:

                evolve = False
                draw(screen, top_phrases, generations, avg_score, mutation_factor, FONT)

            # create mating pool
            mating_pool = []
            for phrase in population:
                n = int(phrase.score * 100)
                for _ in range(n):
                    mating_pool.append(phrase)

            # create children
            for i in range(population_length):
                parentA = mating_pool[random.randint(0, len(mating_pool)-1)]
                parentB = mating_pool[random.randint(0, len(mating_pool)-1)]

                # we don't want identical parents
                while parentA == parentB:
                    parentB = mating_pool[random.randint(0, len(mating_pool)-1)]

                child = parentA.crossover(parentB)
                child.mutate()

                population[i] = child
            
            # profit
            draw(screen, top_phrases, generations, avg_score, mutation_factor, FONT)
            generations += 1
            # Update display
            pygame.display.update()
        clock.tick(30)



if __name__ == "__main__":
    main()