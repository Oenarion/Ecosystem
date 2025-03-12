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

def main():
    pygame.init()
    clock = pygame.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    num_movers = random.randint(1, 10)
    #Creating walkers
    print(f"Created {num_movers} movers!")
    movers = []

    for _ in range(num_movers):
        h, w = 20, 20
        x, y = random.randint(0, WIDTH - w), random.randint(0, HEIGHT - h)
        rand_color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        curr_mover = moverObject.Mover(x, y, rand_color, h, w)
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
            mover.apply_force(gravity)
            if is_wind_blowing:
                mover.apply_force(wind)

            # position, velocity, acceleration, _, _, _ = mover.get_mover_attributes()
            # print(f"mover_{i} position: {position}, velocity: {velocity}, acceleration: {acceleration}")
            mover.update_position()
            mover.check_edges(WIDTH, HEIGHT)

        screen.fill(BACKGROUND_COLOR)
        update_screen(screen, movers)
        
        # Update display
        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()