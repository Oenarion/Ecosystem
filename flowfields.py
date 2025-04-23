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
    vehicle = vehicles.Vehicle(random.randint(0, WIDTH), random.randint(0, HEIGHT), 
                               20, (50, 50, 200), pygame.Vector2(1, 2))
    flow_field = vehicles.FlowField(WIDTH, HEIGHT, 20, 0)
    print(flow_field.rows, flow_field.cols)
    print(len(flow_field.array), len(flow_field.array[0]))
    screen.fill(BACKGROUND_COLOR)

    running = True

    pygame.display.set_caption("My Own Behaviour")
    while running:
        screen.fill(BACKGROUND_COLOR)
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 

        vehicle.follow(flow_field)
        vehicle.update()

        flow_field.draw(screen)
        vehicle.draw(screen)
        # Update display
        pygame.display.update()
        clock.tick(60)



if __name__ == "__main__":
    main()