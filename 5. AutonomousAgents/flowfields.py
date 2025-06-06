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
    vehicles_array = []
    
    first_vehicle = vehicles.Vehicle(WIDTH//2, HEIGHT//2, 
                               20, (50, 50, 200), pygame.Vector2(1, 2))
    
    flow_field_type = random.randint(0,3)
    flow_field = vehicles.FlowField(WIDTH, HEIGHT, 20, flow_field_type)
    screen.fill(BACKGROUND_COLOR)

    vehicles_array.append(first_vehicle)
    running = True

    pygame.display.set_caption("Flow Fields")
    while running:
        screen.fill(BACKGROUND_COLOR)
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 

            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                new_vehicle = vehicles.Vehicle(pos[0], pos[1], 
                               20, (50, 50, 200), pygame.Vector2(1, 2))
                vehicles_array.append(new_vehicle)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_0: 
                    if flow_field_type != 0:
                        flow_field_type = 0
                        flow_field = vehicles.FlowField(WIDTH, HEIGHT, 20, flow_field_type)
                
                if event.key == pygame.K_1: 
                    if flow_field_type != 1:
                        flow_field_type = 1
                        flow_field = vehicles.FlowField(WIDTH, HEIGHT, 20, flow_field_type)

                if event.key == pygame.K_2: 
                    if flow_field_type != 2:
                        flow_field_type = 2
                        flow_field = vehicles.FlowField(WIDTH, HEIGHT, 20, flow_field_type)
                
                if event.key == pygame.K_3: 
                    if flow_field_type != 3:
                        flow_field_type = 3
                        flow_field = vehicles.FlowField(WIDTH, HEIGHT, 20, flow_field_type)


        flow_field.draw(screen)

        remove_idx = []

        for i, vehicle in enumerate(vehicles_array):
            vehicle.follow(flow_field)
            vehicle.update()
            vehicle.draw(screen)
            if vehicle.position.x < 0 or vehicle.position.x > WIDTH or vehicle.position.y < 0 or vehicle.position.y > HEIGHT:
                remove_idx.append(i)

        remove_idx = remove_idx[::-1]
        for idx in remove_idx:
            vehicles_array.pop(idx)

        # Update display
        pygame.display.update()
        clock.tick(60)



if __name__ == "__main__":
    main()