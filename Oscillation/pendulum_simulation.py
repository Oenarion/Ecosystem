import pygame
import oscillators as oscillators
import graphical_components as gc
import random
import math
import time

WIDTH = 640
HEIGHT = 420
BACKGROUND_COLOR = (0, 0, 0)

def main_menu():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Forces Simulation")
    clock = pygame.time.Clock()

    simulation1_button = gc.Button(WIDTH // 2 - 150, HEIGHT // 2 - 150, 300, 50, "Pendulum")
    simulation2_button = gc.Button(WIDTH // 2 - 150, HEIGHT // 2 - 75, 300, 50, "Double Pendulum")
    exit_button = gc.Button(WIDTH // 2 - 150, HEIGHT // 2, 300, 50, "Exit")

    running = True
    while running:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            # exit
            if event.type == pygame.QUIT:
                return False 

            simulation1_button.handle_event(event)
            simulation2_button.handle_event(event)
            exit_button.handle_event(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if simulation1_button.is_hovered(event.pos):
                    pygame.quit()
                    simulation1_main()
                
                if simulation2_button.is_hovered(event.pos):
                    pygame.quit()
                    simulation2_main()

                
                if exit_button.is_hovered(event.pos):
                    pygame.quit()
                    return False  # Exit application
                
        simulation1_button.draw(screen)
        simulation2_button.draw(screen)
        exit_button.draw(screen)

        pygame.display.update()
        clock.tick(60)

def simulation1_main():
    pygame.init()
    clock = pygame.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    screen.fill(BACKGROUND_COLOR)
    pendulum = oscillators.Pendulum(WIDTH//2, 50, 200, 90, 0, 0, 20)
    gravity = pygame.Vector2(0, 40)
    running = True

    pygame.display.set_caption("Oscillation")
    while running:
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False # Quit simulation

        pendulum.update(gravity)
        screen.fill(BACKGROUND_COLOR)
        pendulum.draw(screen)
        # Update display
        pygame.display.update()
        clock.tick(60)

    main_menu()

def simulation2_main():
    pygame.init()
    clock = pygame.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    screen.fill(BACKGROUND_COLOR)
    double_pendulum = oscillators.DoublePendulum(WIDTH//2, HEIGHT//2, 100, angle1=random.randint(0, 90), angle2=random.randint(-90, 90))
    gravity = pygame.Vector2(0, random.uniform(0.5, 2))
    running = True

    pygame.display.set_caption("Oscillation")
    while running:
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False # Quit simulation

        double_pendulum.update(gravity)
        screen.fill(BACKGROUND_COLOR)
        double_pendulum.draw(screen)
        # Update display
        pygame.display.update()
        clock.tick(60)

    main_menu()

if __name__ == "__main__":
    main_menu()