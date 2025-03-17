import pygame
import random
import moverObject

WIDTH = 640
HEIGHT = 420
BACKGROUND_COLOR = (0, 0, 0) # black

MAX_MOVERS = 10

def update_screen(screen: pygame.display, movers: list):
    """
    Updates the screen by visualizing all the objects in it.

    Args:
        - screen -> screen of the application
        - movers -> array of objects to be displayed
    """

    for mover in movers:
        position, _, _, color, w_width, w_height = mover.get_mover_attributes()
        rect = pygame.Rect(position.x, position.y, w_width, w_height)
        pygame.draw.rect(screen, color, rect)

def compute_friction(mover):
    """
    Computes friction, where F = -1*μ*N*v.

    Args:
        - mover -> the mover object which we need to apply friction to

    Returns the friction force.
    """

    c = 0.7  # Friction coefficient
    normal = 1  # Normal force

    vel_y = mover.velocity.y

    # If velocity is very small, don't apply friction
    if abs(vel_y) < 0.01:
        return pygame.Vector2(0, 0)

    friction_magnitude = c * normal
    friction_vector = pygame.Vector2(0, -1 * vel_y)  # Only in y direction

    # Normalize and scale
    friction_vector.normalize_ip()
    friction_vector *= friction_magnitude
    
    return friction_vector


def main():
    pygame.init()
    clock = pygame.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    num_movers = 1
    #Creating walkers
    print(f"Created {num_movers} movers!")
    movers = []

    for _ in range(num_movers):
        h, w = 20, 20
        x, y = random.randint(100, WIDTH - 100), random.randint(100, HEIGHT - 100)
        mass = random.randint(1, 5)
        rand_color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        curr_mover = moverObject.Mover(x, y, rand_color, h, w, mass=mass)
        movers.append(curr_mover)

    screen.fill(BACKGROUND_COLOR)

    update_screen(screen, movers)

    running = True

    gravity = pygame.Vector2(0, 0.1)
    wind = pygame.Vector2(0.1, 0)
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

            # scale the gravity by the mover's mass
            mover.apply_force(gravity * mover.mass)

            if is_wind_blowing:
                mover.apply_force(wind)

            if mover.check_floor(HEIGHT) and abs(mover.velocity.y) > 0.01:
                friction = compute_friction(mover)
                mover.apply_force(friction)

            mover.update_position()
        
            mover.check_edges(WIDTH, HEIGHT)

            

        screen.fill(BACKGROUND_COLOR)
        update_screen(screen, movers)
        
        # Update display
        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()