import pygame
import oscillators
import random
import graphical_components as gc

WIDTH = 640
HEIGHT = 420
BACKGROUND_COLOR = (0, 0, 0)

def update_screen(screen, movers: oscillators.RotatingMover):
    
    for mover in movers:
        mover.draw(screen)

def main_menu():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Forces Simulation")
    clock = pygame.time.Clock()

    simulation1_button = gc.Button(WIDTH // 2 - 150, HEIGHT // 2 - 150, 300, 50, "Rotating objects")
    simulation2_button = gc.Button(WIDTH // 2 - 150, HEIGHT // 2 - 75, 300, 50, "Oscillators")
    simulation3_button = gc.Button(WIDTH // 2 - 150, HEIGHT // 2, 300, 50, "Wave simulation")
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
                    simulation1_main()
                
                if simulation2_button.is_hovered(event.pos):
                    simulation2_main()

                if simulation3_button.is_hovered(event.pos):
                     simulation3_main()
                
                if exit_button.is_hovered(event.pos):
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

    screen.fill(BACKGROUND_COLOR)

    rotating_movers = []
    num_movers = random.randint(1, 10)

    for _ in range(num_movers):
        size = random.randint(5, 30)
        h, w = size, size
        x = random.randint(0, WIDTH - w)
        y = random.randint(0, HEIGHT - h)
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        rot_mover = oscillators.RotatingMover(x, y, w, h, color)
        rotating_movers.append(rot_mover)

    running = True

    pygame.display.set_caption("Oscillation")
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False # Quit simulation

        for mover in rotating_movers:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            distance_force = pygame.Vector2(mouse_x - mover.position.x, mouse_y - mover.position.y)
            distance_force.normalize_ip()
            distance_force *= 0.1
            mover.apply_force(distance_force)
            mover.update_position()

        screen.fill(BACKGROUND_COLOR)
        update_screen(screen, rotating_movers)
        # Update display
        pygame.display.update()
        clock.tick(60)

def simulation2_main():
    pygame.init()
    clock = pygame.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    screen.fill(BACKGROUND_COLOR)
    oscillators_array = []
    num_oscillators = random.randint(1, 15)

    for _ in range(num_oscillators):
        oscillator = oscillators.Oscillator(WIDTH // 2, HEIGHT // 2, 10, 
                                            pygame.Vector2(random.randint(0, 360), random.randint(0, 360)), 
                                            pygame.Vector2(random.uniform(1, 5), random.uniform(1, 5)), random.randint(20, HEIGHT // 2),
                                            pygame.Vector2(random.uniform(0, 0.8), random.uniform(0, 0.8)))

        oscillators_array.append(oscillator)


    running = True

    accelerate = False

    pygame.display.set_caption("Oscillation")
    while running:
        
        screen.fill(BACKGROUND_COLOR)
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False # Quit simulation

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    accelerate = True
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    accelerate = False

        for oscillator in oscillators_array:
            if accelerate:
                oscillator.accelerate()
            else:
                oscillator.decelerate()

            oscillator.oscillate()
            oscillator.draw(screen)

        # Update display
        pygame.display.update()
        clock.tick(60)

def simulation3_main():
    pygame.init()
    clock = pygame.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    screen.fill(BACKGROUND_COLOR)

    running = True

    wave = oscillators.Wave(x = 0, y = 300, amplitude = 100, wavelength = WIDTH + 20, 
                            inpoint_distance = 20, start_angle = 0, delta_angle = 10, radius = 15)
    pygame.display.set_caption("Wave simulation")
    while running:
        
        screen.fill(BACKGROUND_COLOR)
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False # Quit simulation

        wave.draw(screen)
        # Update display
        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main_menu()