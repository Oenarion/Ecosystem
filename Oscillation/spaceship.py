import pygame
import Oscillation.oscillators as oscillators
import random

WIDTH = 640
HEIGHT = 420
BACKGROUND_COLOR = (0, 0, 0)

def update_screen(screen, movers):
    
    for mover in movers:
        mover.draw(screen)

def main():

    pygame.init()
    clock = pygame.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    screen.fill(BACKGROUND_COLOR)
    spaceship = oscillators.Spaceship(300, 100, 20, 10, (128, 255, 0), pygame.Vector2(0, 1), angle=90)
    running = True

    turning_left = False
    turning_right = False
    thrust = False

    pygame.display.set_caption("Oscillation")
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False # Quit simulation

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    turning_left = True
                    spaceship.turn("LEFT")

                if event.key == pygame.K_RIGHT:
                    turning_right = True
                    

                if event.key == pygame.K_z:
                    thrust = True
                    spaceship.apply_thrust()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    turning_left = False

                if event.key == pygame.K_RIGHT:
                    turning_right = False

                if event.key == pygame.K_z:
                    thrust = False
        
        if turning_left:
            spaceship.turn("LEFT")

        if turning_right:
            spaceship.turn("RIGHT") 

        if thrust:
            spaceship.apply_thrust()
        else:
            spaceship.decrease_speed()


        spaceship.update_position()
        screen.fill(BACKGROUND_COLOR)
        update_screen(screen, [spaceship])
        # Update display
        pygame.display.update()
        clock.tick(60)



if __name__ == "__main__":
    main()