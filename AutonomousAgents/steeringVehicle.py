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
    escape_target = vehicles.EscapingTarget(WIDTH//2, HEIGHT//2, 10, 0)
    vehicle = vehicles.Vehicle(random.randint(0, WIDTH), random.randint(0, HEIGHT), 
                               20, (50, 50, 200), pygame.Vector2(1, 2))
    screen.fill(BACKGROUND_COLOR)

    running = True

    pygame.display.set_caption("Steering behaviour")
    while running:
        screen.fill(BACKGROUND_COLOR)
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 

        if random.randint(1, 1000) == 1:
            print("CHANGING MODE")
            vehicle.change_mode()

        if random.randint(0, 1000) < 2:
            escape_target.invert_direction()
        
        if vehicle.pursuit:
            vehicle.seek(escape_target.next_position())
        else:
            vehicle.seek(escape_target.position)
        vehicle.update()
        escape_target.update_position()
        
        escape_target.draw(screen)
        vehicle.draw(screen)

        # Update display
        pygame.display.update()
        clock.tick(60)



if __name__ == "__main__":
    main()