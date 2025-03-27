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
    num_movers = random.randint(1, 10)

    for _ in range(num_movers):
        size = random.randint(5, 30)
        h, w = size, size
        x = random.randint(0, WIDTH - w)
        y = random.randint(0, HEIGHT - h)
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        rot_mover = rotatingMover.RotatingMover(x, y, w, h, color)
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



if __name__ == "__main__":
    main()