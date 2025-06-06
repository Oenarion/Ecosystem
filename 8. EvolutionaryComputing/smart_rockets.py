import pygame
import time
import graphical_components as gc
from DNA import Population, SmartPopulation, Target, Obstacle
import numpy as np

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


def main_menu():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("")
    clock = pygame.time.Clock()

    simulation1_button = gc.Button(WIDTH // 2 - 150, 25, 300, 50, "Smart Rockets")
    simulation2_button = gc.Button(WIDTH // 2 - 150, 100, 300, 50, "Smarter Rockets 1")
    simulation3_button = gc.Button(WIDTH // 2 - 150, 175, 300, 50, "Smarter Rockets 2")
    simulation4_button = gc.Button(WIDTH // 2 - 150, 250, 300, 50, "Smarter Rockets 3")
    exit_button = gc.Button(WIDTH // 2 - 150, 325, 300, 50, "Exit")

    running = True
    while running:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            # exit
            if event.type == pygame.QUIT:
                return False 

            simulation1_button.handle_event(event)
            simulation2_button.handle_event(event)
            simulation3_button.handle_event(event)
            simulation4_button.handle_event(event)
            exit_button.handle_event(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if simulation1_button.is_hovered(event.pos):
                    pygame.quit()
                    simulation1_main()
                
                if simulation2_button.is_hovered(event.pos):
                    pygame.quit()
                    simulation2_main()

                if simulation3_button.is_hovered(event.pos):
                    pygame.quit()
                    simulation3_main()

                if simulation4_button.is_hovered(event.pos):
                    pygame.quit()
                    simulation4_main()
                
                if exit_button.is_hovered(event.pos):
                    pygame.quit()
                    return False  # Exit application
                
        simulation1_button.draw(screen)
        simulation2_button.draw(screen)
        simulation3_button.draw(screen)
        simulation4_button.draw(screen)
        exit_button.draw(screen)

        pygame.display.update()
        clock.tick(60)

def simulation1_main():
    
    pygame.init()
    clock = pygame.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.fill(BACKGROUND_COLOR)
    FONT = pygame.font.Font(None, 24)
    lifespan = 60
    life_passed = 0
    generation = 0
    mutation_factor = 5
    target = Target(WIDTH//2, 20, 10)
    population = Population(population_length, WIDTH//2, HEIGHT - 10, lifespan, mutation_factor, target)
    running = True

    pygame.display.set_caption("Smart Rockets")
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 

            if event.type == pygame.MOUSEBUTTONUP:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                target = Target(mouse_x, mouse_y, 10)
            
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
        draw(screen, generation, lifespan - life_passed, FONT)
        # Update display
        pygame.display.update()
        clock.tick(30)
    main_menu()

def simulation2_main():
    
    pygame.init()
    clock = pygame.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.fill(BACKGROUND_COLOR)
    FONT = pygame.font.Font(None, 24)
    lifespan = 120
    life_passed = 0
    generation = 0
    mutation_factor = 10
    obstacles = [Obstacle(280, 300, 60, 10, (255, 0, 0))]
    target = Obstacle(WIDTH//2-5, 20, 10, 10, (0, 255, 0))
    population = SmartPopulation(population_length, WIDTH//2, HEIGHT - 10, lifespan, mutation_factor, target, obstacles)
    running = True

    pygame.display.set_caption("Smarter Rockets 1")
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
    main_menu()

def simulation3_main():
    
    pygame.init()
    clock = pygame.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.fill(BACKGROUND_COLOR)
    FONT = pygame.font.Font(None, 24)
    lifespan = 150
    life_passed = 0
    generation = 0
    mutation_factor = 10
    obstacles = [Obstacle(280, 300, 60, 10, (255, 0, 0)), Obstacle(200, 150, 60, 10, (255, 0, 0)), Obstacle(360, 150, 60, 10, (255, 0, 0))]
    target = Obstacle(WIDTH//2-5, 20, 10, 10, (0, 255, 0))
    population = SmartPopulation(population_length, WIDTH//2, HEIGHT - 10, lifespan, mutation_factor, target, obstacles)
    running = True

    pygame.display.set_caption("Smarter Rockets 2")
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
    main_menu()

def simulation4_main():
    
    pygame.init()
    clock = pygame.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.fill(BACKGROUND_COLOR)
    FONT = pygame.font.Font(None, 24)
    lifespan = 180
    life_passed = 0
    generation = 0
    mutation_factor = 10
    obstacles = [Obstacle(280, 300, 60, 10, (255, 0, 0)), Obstacle(200, 150, 60, 10, (255, 0, 0)), Obstacle(360, 150, 60, 10, (255, 0, 0)),
                 Obstacle(WIDTH//2 - 30, 0, 10, 50, (255, 0, 0)), Obstacle(WIDTH//2 + 20, 0, 10, 50, (255, 0, 0))]
    target = Obstacle(WIDTH//2-5, 20, 10, 10, (0, 255, 0))
    population = SmartPopulation(population_length, WIDTH//2, HEIGHT - 10, lifespan, mutation_factor, target, obstacles)
    running = True

    pygame.display.set_caption("Smarter Rockets 3")
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
    main_menu()


if __name__ == "__main__":
    main_menu()