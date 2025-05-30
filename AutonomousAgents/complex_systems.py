import pygame
import time
import vehicles
import random
import graphical_components as gc
import paths

WIDTH = 640
HEIGHT = 420
BACKGROUND_COLOR = (0, 0, 0)
TIME = time.time()

def create_new_simulation(num_vehicles = 20):
    segments = paths.define_path(20, 10, WIDTH, HEIGHT)
    vehicles_array = []
    for _ in range(num_vehicles):
        vehicle = vehicles.Vehicle(random.randint(0, 50), segments[0].start_pos.y, 5, (250, 50, 50), pygame.Vector2(1, 2))
        vehicles_array.append(vehicle)
    path = paths.Path(segments)

    return vehicles_array, path

def update_text(text, font, pos, screen):
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=pos)

    screen.blit(text_surface, text_rect)

def main_menu():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("")
    clock = pygame.time.Clock()

    simulation1_button = gc.Button(WIDTH // 2 - 150, HEIGHT // 2 - 150, 300, 50, "Separation")
    simulation2_button = gc.Button(WIDTH // 2 - 150, HEIGHT // 2 - 75, 300, 50, "PF w Separation")
    simulation3_button = gc.Button(WIDTH // 2 - 150, HEIGHT // 2, 300, 50, "Flocking")
    exit_button = gc.Button(WIDTH // 2 - 150, HEIGHT // 2 + 75, 300, 50, "Exit")

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
                
                if exit_button.is_hovered(event.pos):
                    pygame.quit()
                    return False  # Exit application
                
        simulation1_button.draw(screen)
        simulation2_button.draw(screen)
        simulation3_button.draw(screen)
        exit_button.draw(screen)

        pygame.display.update()
        clock.tick(60)

def simulation1_main():
    
    pygame.init()
    clock = pygame.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    num_of_vehicles = random.randint(20, 30)
    vehicles_array = []
    for _ in range(num_of_vehicles):
        vehicle = vehicles.Vehicle(random.randint(0, WIDTH), random.randint(0, HEIGHT), 
                                random.randint(10, 30), (200, 100, 60), 
                                pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)),
                                max_speed = 5, max_force=0.2)
        vehicles_array.append(vehicle)

    screen.fill(BACKGROUND_COLOR)

    running = True

    pygame.display.set_caption("Separation")
    while running:
        screen.fill(BACKGROUND_COLOR)
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 

        for vehicle in vehicles_array:
            vehicle.separate(vehicles_array)
            vehicle.update()
            vehicle.draw(screen)

        # Update display
        pygame.display.update()
        clock.tick(60)

    pygame.quit()
    main_menu()


def simulation2_main():
    
    pygame.init()
    clock = pygame.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    num_of_vehicles = 20
    vehicles_array, path = create_new_simulation(num_of_vehicles)
    screen.fill(BACKGROUND_COLOR)

    running = True
    point_to_follow = None
    pygame.display.set_caption("Path Following with separation")
    while running:
        screen.fill(BACKGROUND_COLOR)
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 

        path.draw(screen)
        for vehicle in vehicles_array:
            center = pygame.Vector2(vehicle.rect.centerx, vehicle.rect.centery)
            is_contained, segment = path.is_rectangle_contained(center)
            if not is_contained and segment is not None:
                point_to_follow = vehicle.seek_segment(segment)
            print(f"IS RECTANGLE CONTAINED? {is_contained}")
            vehicle.separate(vehicles_array)
            vehicle.update()
            vehicle.draw(screen)

        if point_to_follow is not None:
            pygame.draw.circle(screen, (0, 255, 0), point_to_follow, 2)
        
        out_of_bounds = 0
        for vehicle in vehicles_array:
            out_of_bounds += vehicle.out_of_x_bounds(WIDTH)
            if out_of_bounds == num_of_vehicles:
                vehicles_array, path = create_new_simulation(num_of_vehicles)

        # Update display
        pygame.display.update()
        clock.tick(60)
    
    pygame.quit()
    main_menu()


def simulation3_main():
    
    pygame.init()
    FONT =  pygame.font.Font(None, 24)
    
    max_velocity = 3
    max_force = 0.2

    sliders = [
        gc.Slider(10, 40, 120, 10, 0.1, 3, 1, toggle=False, label="Separation Multiplier"),
        gc.Slider(10, 90, 120, 10, 0.1, 3, 1, toggle=False, label="Alignment Multiplier"),
        gc.Slider(10, 140, 120, 10, 0.1, 3, 1, toggle=False, label="Cohesion Multiplier"),
        gc.Slider(WIDTH - 170, 40, 120, 10, 0.1, 10, max_velocity, toggle=False, label="Max velocity"),
        gc.Slider(WIDTH - 170, 90, 120, 10, 0.1, 2, max_force, toggle=False, label="Max force")
    ]

    clock = pygame.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.fill(BACKGROUND_COLOR)
    number_of_boids = random.randint(50, 150)
    boids = []
    for i in range(number_of_boids):
        boid = vehicles.Boid(x = random.randint(WIDTH//2 - 10, WIDTH//2 + 10), 
                             y = random.randint(HEIGHT//2 - 10, HEIGHT//2 + 10), radius = 3, 
                             color = (250, 40, 40), separation_distance = random.randint(50, 200), id_boid = i, 
                             velocity = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)),
                             max_speed = max_velocity, max_force = max_force)
        # prepare boid field of view
        boid.fov()
        boids.append(boid)

    running = True
    pygame.display.set_caption("Flocking")
    while running:
        screen.fill(BACKGROUND_COLOR)
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    for slider in sliders:
                        slider.invert_toggle()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    for boid in boids:
                        boid.show_fov = not boid.show_fov

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    for boid in boids:
                        boid.mode = 1 - boid.mode

        for slider in sliders:
            slider.handle_event(event)

        sep_weight = sliders[0].current_val
        align_weight = sliders[1].current_val
        coh_weight = sliders[2].current_val

        if sliders[3].current_val != max_velocity:
            max_velocity = sliders[3].current_val
            for boid in boids:
                boid.max_speed = max_velocity

        if sliders[4].current_val != max_force:
            max_force = sliders[4].current_val
            for boid in boids:
                boid.max_force = max_force

        for boid in boids:
            
            
            separation_force = boid.separate(boids) * sep_weight
            align_force = boid.align(boids) * align_weight
            cohesion_force = boid.cohesion(boids) * coh_weight
            
            boid.apply_force(separation_force)
            boid.apply_force(align_force)
            boid.apply_force(cohesion_force)
            boid.pac_man_effect(WIDTH, HEIGHT)

            boid.fov()
            boid.draw(screen)
            boid.update()
            
            
            

        for slider in sliders:
            slider.draw(screen, FONT)

        # Update display
        pygame.display.update()
        clock.tick(60)

    pygame.quit()
    main_menu()


if __name__ == "__main__":
    main_menu()