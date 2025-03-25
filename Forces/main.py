import pygame
import random
import moverObject
import liquidObject
import attractorObject
import graphical_components as gc

WIDTH = 640
HEIGHT = 420
BACKGROUND_COLOR = (0, 0, 0) # black

MAX_MOVERS = 10

def update_screen(screen: pygame.display, movers: list, liquid: liquidObject.Liquid, attractors):
    """
    Updates the screen by visualizing all the objects in it.

    Args:
        - screen -> screen of the application
        - movers -> array of objects to be displayed
    """

    if liquid:
        rect, color = liquid.get_draw_attributes()
        pygame.draw.rect(screen, color, rect)

    if attractors is not None and attractors != []:
        for attractor in attractors:
            radius, position, color = attractor.get_draw_attributes()
            pygame.draw.circle(screen, color, (position.x, position.y), radius)

    for mover in movers:
        radius, position, rect, color = mover.get_draw_attributes()
        
        pygame.draw.rect(screen, color, rect)
        pygame.draw.circle(screen, (0,0,0), (position.x, position.y), radius)

    
def main_menu():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Forces Simulation")
    clock = pygame.time.Clock()

    simulation1_button = gc.Button(WIDTH // 2 - 150, HEIGHT // 2 - 75, 300, 50, "Liquid Simulation")
    simulation2_button = gc.Button(WIDTH // 2 - 150, HEIGHT // 2, 300, 50, "Gravitational Attraction")
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
            exit_button.handle_event(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if simulation1_button.is_hovered(event.pos):
                    simulation1_main()
                
                if simulation2_button.is_hovered(event.pos):
                    simulation2_main()
                
                if exit_button.is_hovered(event.pos):
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

    num_movers = 1
    print(f"Created {num_movers} movers!")
    movers = []
    
    liquid = liquidObject.Liquid(0, 300, WIDTH, HEIGHT, (128, 128, 128))
    for i in range(num_movers):
        radius = random.randint(5, 20)
        x, y = random.randint(100, WIDTH - 100), 100
        mass = random.randint(1, 5)
        rand_color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        friction_coef = random.uniform(0,0.5)
        print(f"Friction coef of mover {i} is: {friction_coef}")
        curr_mover = moverObject.Mover(x, y, rand_color, radius, mass=mass, friction_coef=friction_coef)
        movers.append(curr_mover)

    screen.fill(BACKGROUND_COLOR)

    update_screen(screen, movers, liquid, None)

    running = True

    gravity = pygame.Vector2(0, 0.1)
    wind = pygame.Vector2(0.5, 0)
    is_wind_blowing = False

    pygame.display.set_caption("Liquid Simulation")
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False # Quit simulation

            # wind blows if users clicks on the screen
            if event.type == pygame.MOUSEBUTTONDOWN:
                is_wind_blowing = True
            if event.type == pygame.MOUSEBUTTONUP:
                is_wind_blowing = False

        # movers are now subject to gravity
        for i, mover in enumerate(movers):

            if mover.check_floor(HEIGHT) and abs(mover.velocity.y) < 0.1:
                mover.velocity.y = 0
            else:
                # scale the gravity by the mover's mass
                mover.apply_force(gravity * mover.mass)

            if liquid.contains_object(mover.rect) and abs(mover.velocity.y) > 0.01:
                drag_force = liquid.compute_drag_force(mover.velocity, mover.radius)
                # add a limit so that the item doesn't bounce off the liquid.
                if drag_force.magnitude_squared() > mover.velocity.magnitude_squared():
                    limit_drag_force = pygame.Vector2(0, - mover.velocity.y + 0.3) 
                    mover.apply_force(limit_drag_force)
                else:
                    mover.apply_force(drag_force)

            if is_wind_blowing:
                mover.apply_force(wind)

            if mover.check_floor(HEIGHT):
                friction = mover.compute_friction()
                mover.apply_force(friction)
            #     print(f"Friction: {friction}")
            print(f"Mover's velocity: {mover.velocity}")

            
            mover.update_position()
        
            mover.check_edges(WIDTH, HEIGHT)

            

        screen.fill(BACKGROUND_COLOR)
        update_screen(screen, movers, liquid, None)
        
        # Update display
        pygame.display.update()
        clock.tick(60)


def simulation2_main():
    pygame.init()
    clock = pygame.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    num_movers = random.randint(5, 20)
    print(f"Created {num_movers} movers!")
    movers = []
    attractors = []
    
    attractor_1 = attractorObject.Attractor(500, 200, (255, 255, 0), 15, 150)
    attractor_2 = attractorObject.Attractor(100, 200, (255, 0, 255), 15, 150)
    attractor_3 = attractorObject.Attractor(300, 200, (0, 255, 255), 15, 150)

    attractors.append(attractor_1)
    attractors.append(attractor_2)
    attractors.append(attractor_3)

    for _ in range(num_movers):
        radius = random.randint(2, 10)
        x, y = random.randint(100, WIDTH - 100), random.randint(100, HEIGHT - 100)
        mass = radius * 2
        rand_color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        curr_mover = moverObject.Mover(x, y, rand_color, radius, mass=mass)
        movers.append(curr_mover)

    screen.fill(BACKGROUND_COLOR)

    update_screen(screen, movers, None, attractors)

    running = True

    pygame.display.set_caption("Gravitational Force Simulation")
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False # Quit simulation

        # movers are now subject to gravity
        for i, mover in enumerate(movers):

            if mover.check_floor(HEIGHT) and abs(mover.velocity.y) < 0.1:
                mover.velocity.y = 0

            for i, attractor in enumerate(attractors):
                grav_force = attractor.attract(mover)
                distance = (attractor.position - mover.position).magnitude()
                print(f"ATTRACTOR {i}: Distance = {distance}, Force = {grav_force.magnitude()}")
                mover.apply_force(grav_force)

            mover.update_position()

            

        screen.fill(BACKGROUND_COLOR)
        update_screen(screen, movers, None, attractors)
        
        # Update display
        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main_menu()