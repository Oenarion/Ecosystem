import pygame
import time
import l_system_object as lo
import graphical_components as gc

WIDTH = 640
HEIGHT = 500
BACKGROUND_COLOR = (0, 0, 0)
TIME = time.time()


def main():
    
    pygame.init()
    clock = pygame.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    FONT =  pygame.font.Font(None, 24)
    screen.fill(BACKGROUND_COLOR)
    angle_slider = gc.Slider(x=10, y=40, width=120, height=10, min_val=0, max_val=90, initial_val=25, toggle=True, interval=1, label="Angle")
    angle = angle_slider.current_val

    running = True
    axiom = "F"
    rules = {
        "F": "F[+F]F[-F]F"
    }
    l_system = lo.L_System(starting_string=axiom, rules=rules, generation_limit=4, length=5, angle=angle)
    l_system.generate_string()
    pygame.display.set_caption("L-System")

    while running:
        screen.fill(BACKGROUND_COLOR)
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False    
            angle_slider.handle_event(event)

        if angle != angle_slider.current_val:
            angle = angle_slider.current_val
            l_system.angle = angle

        current_time = pygame.time.get_ticks()
        l_system.draw(screen, WIDTH, HEIGHT, current_time)
        angle_slider.draw(screen, FONT)
        # Update display
        pygame.display.update()
        clock.tick(60)



if __name__ == "__main__":
    main()