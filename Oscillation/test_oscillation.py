import pygame
import rotatingMover
import random

WIDTH = 640
HEIGHT = 420
BACKGROUND_COLOR = (0, 0, 0)

def update_screen(screen, movers: rotatingMover.RotatingMover):
    
    for mover in movers:
        mover.draw(screen)

def main():

    pygame.init()
    clock = pygame.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    screen.fill(BACKGROUND_COLOR)

    rotating_movers = []
    num_movers = 1

    for _ in range(num_movers):
        size = random.randint(5, 30)
        h, w = size, size
        x = random.randint(0, WIDTH - w)
        y = random.randint(0, HEIGHT - h)
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        rot_mover = rotatingMover.RotatingMover(x, y, w, h, color)
        rotating_movers.append(rot_mover)

    running = True

    gravity = pygame.Vector2(0, 0.001)

    pygame.display.set_caption("n-body Simulation")
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False # Quit simulation

        for mover in rotating_movers:
            mover.apply_force(gravity)
            mover.update_position()

        screen.fill(BACKGROUND_COLOR)
        update_screen(screen, rotating_movers)
        # Update display
        pygame.display.update()
        clock.tick(60)



if __name__ == "__main__":
    main()