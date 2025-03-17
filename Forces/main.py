import pygame
import random
import moverObject
import liquidObject

WIDTH = 640
HEIGHT = 420
BACKGROUND_COLOR = (0, 0, 0) # black

MAX_MOVERS = 10

def update_screen(screen: pygame.display, movers: list, liquid: liquidObject.Liquid):
    """
    Updates the screen by visualizing all the objects in it.

    Args:
        - screen -> screen of the application
        - movers -> array of objects to be displayed
    """

    rect, color = liquid.get_draw_attributes()
    pygame.draw.rect(screen, color, rect)

    for mover in movers:
        rect, color = mover.get_draw_attributes()
        pygame.draw.rect(screen, color, rect)

    


def main():
    pygame.init()
    clock = pygame.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    num_movers = 1
    #Creating walkers
    print(f"Created {num_movers} movers!")
    movers = []
    
    liquid = liquidObject.Liquid(0, 300, WIDTH, HEIGHT, (128, 128, 128))
    for i in range(num_movers):
        h, w = 20, 20
        x, y = random.randint(100, WIDTH - 100), 100
        mass = random.randint(1, 5)
        rand_color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        friction_coef = random.uniform(0,1)
        print(f"Friction coef of mover {i} is: {friction_coef}")
        curr_mover = moverObject.Mover(x, y, rand_color, h, w, mass=mass, friction_coef=friction_coef)
        movers.append(curr_mover)

    screen.fill(BACKGROUND_COLOR)

    update_screen(screen, movers, liquid)

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

            if mover.check_floor(HEIGHT) and abs(mover.velocity.y) < 0.01:
                mover.velocity.y = 0

            if liquid.contains_object(mover.rect) and abs(mover.velocity.y) > 0.01:
                print(mover.velocity.y)
                drag_force = liquid.compute_drag_force(mover.velocity)
                print(f"DRAG FORCE: {drag_force}")
                mover.apply_force(drag_force)

            # scale the gravity by the mover's mass
            mover.apply_force(gravity * mover.mass)

            if is_wind_blowing:
                mover.apply_force(wind)

            if mover.check_floor(HEIGHT) and abs(mover.velocity.x) > 0.01:
                friction = mover.compute_friction()
                mover.apply_force(friction)

            
            mover.update_position()
        
            mover.check_edges(WIDTH, HEIGHT)

            

        screen.fill(BACKGROUND_COLOR)
        update_screen(screen, movers, liquid)
        
        # Update display
        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()