import pygame
import time
import vehicles
import paths
import random

WIDTH = 640
HEIGHT = 420
BACKGROUND_COLOR = (0, 0, 0)
TIME = time.time()

def create_new_simulation():
    segments = paths.define_path(20, 10, WIDTH, HEIGHT)
    vehicle = vehicles.Vehicle(0, segments[0].start_pos.y, 20, (250, 50, 50), pygame.Vector2(1, 2))
    path = paths.Path(segments)

    return vehicle, path

def main():
    
    pygame.init()
    clock = pygame.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    vehicle, path = create_new_simulation()
    screen.fill(BACKGROUND_COLOR)

    running = True
    point_to_follow = None
    pygame.display.set_caption("My Own Behaviour")
    while running:
        screen.fill(BACKGROUND_COLOR)
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 

        
        center = pygame.Vector2(vehicle.rect.centerx, vehicle.rect.centery)
        is_contained, segment = path.is_rectangle_contained(center)
        if not is_contained and segment is not None:
            point_to_follow = vehicle.seek_segment(segment)
        print(f"IS RECTANGLE CONTAINED? {is_contained}")
        vehicle.update()
        path.draw(screen)
        vehicle.draw(screen)
        if point_to_follow is not None:
            pygame.draw.circle(screen, (0, 255, 0), point_to_follow, 2)

        if vehicle.position.x > WIDTH + 20:
            vehicle, path = create_new_simulation()

        # Update display
        pygame.display.update()
        clock.tick(60)



if __name__ == "__main__":
    main()