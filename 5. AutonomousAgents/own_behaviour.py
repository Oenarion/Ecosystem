import pygame
import time
import vehicles
import random

WIDTH = 640
HEIGHT = 420
BACKGROUND_COLOR = (0, 0, 0)
TIME = time.time()


def main():
    
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

    pygame.display.set_caption("My Own Behaviour")
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
    main()