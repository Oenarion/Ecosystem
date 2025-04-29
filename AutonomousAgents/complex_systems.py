import pygame
import time
import vehicles
import random
import graphical_components as gc

WIDTH = 640
HEIGHT = 420
BACKGROUND_COLOR = (0, 0, 0)
TIME = time.time()

def main_menu():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("")
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
    vehicle = vehicles.OwnBehaviourVehicle(random.randint(0, WIDTH), random.randint(0, HEIGHT), 
                               20, (50, 50, 200), pygame.Vector2(1, 2))
    x, y = random.randint(100, WIDTH - 100), random.randint(100, HEIGHT - 100)
    w, h = random.randint(50, WIDTH - x - 10), random.randint(50, HEIGHT - y - 10)
    rect = pygame.Rect(x, y, w, h)
    screen.fill(BACKGROUND_COLOR)

    running = True

    pygame.display.set_caption("Separation")
    while running:
        screen.fill(BACKGROUND_COLOR)
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 

        vehicle.compute_new_velocity(rect)
        vehicle.update()

        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(rect.left, rect.top, w, 1), 5)
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(rect.right, rect.top, 1, h), 5)
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(rect.left, rect.bottom, w, 1), 5)
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(rect.left, rect.top, 1, h), 5)
        vehicle.draw(screen)

        # Update display
        pygame.display.update()
        clock.tick(60)


def simulation2_main():
    
    pygame.init()
    clock = pygame.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    vehicle = vehicles.OwnBehaviourVehicle(random.randint(0, WIDTH), random.randint(0, HEIGHT), 
                               20, (50, 50, 200), pygame.Vector2(1, 2))
    x, y = random.randint(100, WIDTH - 100), random.randint(100, HEIGHT - 100)
    w, h = random.randint(50, WIDTH - x - 10), random.randint(50, HEIGHT - y - 10)
    rect = pygame.Rect(x, y, w, h)
    screen.fill(BACKGROUND_COLOR)

    running = True

    pygame.display.set_caption("Path Following with separation")
    while running:
        screen.fill(BACKGROUND_COLOR)
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 

        vehicle.compute_new_velocity(rect)
        vehicle.update()

        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(rect.left, rect.top, w, 1), 5)
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(rect.right, rect.top, 1, h), 5)
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(rect.left, rect.bottom, w, 1), 5)
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(rect.left, rect.top, 1, h), 5)
        vehicle.draw(screen)

        # Update display
        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main_menu()