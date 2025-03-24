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

def update_screen(screen: pygame.display, movers: list, liquid: liquidObject.Liquid, attractor: attractorObject.Attractor):
    """
    Updates the screen by visualizing all the objects in it.

    Args:
        - screen -> screen of the application
        - movers -> array of objects to be displayed
    """

    if liquid:
        rect, color = liquid.get_draw_attributes()
        pygame.draw.rect(screen, color, rect)

    if attractor:
        rect, color = attractor.get_draw_attributes()
        pygame.draw.rect(screen, color, rect)

    for mover in movers:
        rect, color = mover.get_draw_attributes()
        pygame.draw.rect(screen, color, rect)

    
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

    num_movers = random.randint(0, 10)
    print(f"Created {num_movers} movers!")
    movers = []
    
    liquid = liquidObject.Liquid(0, 300, WIDTH, HEIGHT, (128, 128, 128))
    for i in range(num_movers):
        size = random.randint(10, 50)
        h, w = size, size
        x, y = random.randint(100, WIDTH - 100), 100
        mass = random.randint(1, 5)
        rand_color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        friction_coef = random.uniform(0,1)
        print(f"Friction coef of mover {i} is: {friction_coef}")
        curr_mover = moverObject.Mover(x, y, rand_color, h, w, mass=mass, friction_coef=friction_coef)
        movers.append(curr_mover)

    screen.fill(BACKGROUND_COLOR)

    update_screen(screen, movers, liquid, None)

    running = True

    gravity = pygame.Vector2(0, 0.1)
    wind = pygame.Vector2(0.5, 0)
    is_wind_blowing = False

    pygame.display.set_caption("Forces Simulation")
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

            if liquid.contains_object(mover.rect) and abs(mover.velocity.y) > 0.01:
                drag_force = liquid.compute_drag_force(mover.velocity, mover.w)
                # add a limit so that the item doesn't bounce off the liquid.
                if drag_force.magnitude_squared() > mover.velocity.magnitude_squared():
                    limit_drag_force = pygame.Vector2(0, - mover.velocity.y + 0.1) 
                    mover.apply_force(limit_drag_force)
                else:
                    mover.apply_force(drag_force)

            # scale the gravity by the mover's mass
            mover.apply_force(gravity * mover.mass)

            if is_wind_blowing:
                mover.apply_force(wind)

            if mover.check_floor(HEIGHT) and abs(mover.velocity.x) > 0.1:
                friction = mover.compute_friction()
                mover.apply_force(friction)
            #     print(f"Friction: {friction}")
            # print(f"Mover's velocity: {mover.velocity}")

            
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

    num_movers = 1
    print(f"Created {num_movers} movers!")
    movers = []
    
    attractor = attractorObject.Attractor(300, 200, (128, 128, 0), 30, 30, 100)
    
    for i in range(num_movers):
        size = random.randint(5, 10)
        h, w = size, size
        x, y = random.randint(100, WIDTH - 100), 100
        mass = random.randint(1, 5)
        rand_color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        curr_mover = moverObject.Mover(x, y, rand_color, h, w, mass=mass)
        movers.append(curr_mover)

    screen.fill(BACKGROUND_COLOR)

    update_screen(screen, movers, None, attractor)

    running = True

    gravity = pygame.Vector2(0, 0.1)

    pygame.display.set_caption("Forces Simulation")
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False # Quit simulation

        # movers are now subject to gravity
        for i, mover in enumerate(movers):

            if mover.check_floor(HEIGHT) and abs(mover.velocity.y) < 0.1:
                mover.velocity.y = 0


            # scale the gravity by the mover's mass
            # mover.apply_force(gravity * mover.mass)

            grav_force = attractor.attract(mover)
            print(grav_force)
            mover.apply_force(grav_force)

            mover.update_position()

            

        screen.fill(BACKGROUND_COLOR)
        update_screen(screen, movers, None, attractor)
        
        # Update display
        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main_menu()