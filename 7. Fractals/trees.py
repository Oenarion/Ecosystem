import pygame
import time
import graphical_components as gc
import deterministic_objects as do

WIDTH = 640
HEIGHT = 500
BACKGROUND_COLOR = (0, 0, 0)
TIME = time.time()

def main_menu():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Main menu")
    clock = pygame.time.Clock()

    simulation1_button = gc.Button(WIDTH // 2 - 150, HEIGHT // 2 - 150, 300, 50, "Deterministic Tree")
    simulation2_button = gc.Button(WIDTH // 2 - 150, HEIGHT // 2 - 75, 300, 50, "Step by step Tree")
    simulation3_button = gc.Button(WIDTH // 2 - 150, HEIGHT // 2, 300, 50, "Random Tree")
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
                    pygame.quit()
                    simulation1_main()
                
                if simulation2_button.is_hovered(event.pos):
                    pygame.quit()
                    simulation2_main()
                
                if simulation3_button.is_hovered(event.pos):
                    pygame.quit()
                    simulation3_main()

                if exit_button.is_hovered(event.pos):
                    running = False
                
        simulation1_button.draw(screen)
        simulation2_button.draw(screen)
        simulation3_button.draw(screen)
        exit_button.draw(screen)

        pygame.display.update()
        clock.tick(60)

    pygame.quit()

def simulation1_main():
    
    pygame.init()
    clock = pygame.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    FONT =  pygame.font.Font(None, 24)
    angle_slider = gc.Slider(x=10, y=40, width=120, height=10, min_val=0, max_val=180, initial_val=5, toggle=True, interval=1, label="Angle")
    decay_slider = gc.Slider(x=10, y=80, width=120, height=10, min_val=0.1, max_val=0.9, initial_val=0.7, toggle=True, interval=0.1, label="Length decay")
    depth_slider = gc.Slider(x=10, y=120, width=120, height=10, min_val=2, max_val=15, initial_val=10, toggle=True, interval=1, label="Max depth")

    tree = do.Tree(pygame.Vector2(WIDTH//2, 400), pygame.Vector2(WIDTH//2, 300), 
                   decay_rate=decay_slider.current_val, angle=angle_slider.current_val, max_depth=depth_slider.current_val)

    angle = angle_slider.current_val
    decay = decay_slider.current_val
    depth = depth_slider.current_val

    screen.fill(BACKGROUND_COLOR)

    running = True

    pygame.display.set_caption("Deterministic Tree")
    while running:
        screen.fill(BACKGROUND_COLOR)
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False    

            angle_slider.handle_event(event)
            decay_slider.handle_event(event)
            depth_slider.handle_event(event)
        
        if decay != decay_slider.current_val:
            decay = decay_slider.current_val
            tree = do.Tree(pygame.Vector2(WIDTH//2, 400), pygame.Vector2(WIDTH//2, 300), 
                           decay_rate=decay, angle=angle_slider.current_val, max_depth=depth_slider.current_val)

        if angle != angle_slider.current_val:
            angle = angle_slider.current_val
            tree = do.Tree(pygame.Vector2(WIDTH//2, 400), pygame.Vector2(WIDTH//2, 300), 
                           decay_rate=decay_slider.current_val, angle=angle, max_depth=depth_slider.current_val)

        if depth != depth_slider.current_val:
            depth = depth_slider.current_val
            tree = do.Tree(pygame.Vector2(WIDTH//2, 400), pygame.Vector2(WIDTH//2, 300), 
                           decay_rate=decay_slider.current_val, angle=angle_slider.current_val, max_depth=depth)

        tree.draw(screen)
        angle_slider.draw(screen, FONT)
        decay_slider.draw(screen, FONT)
        depth_slider.draw(screen, FONT)
        # Update display
        pygame.display.update()
        clock.tick(60)
    main_menu()

def simulation2_main():
    pygame.init()
    clock = pygame.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    tree = do.SlowTree(pygame.Vector2(WIDTH//2, 400), pygame.Vector2(WIDTH//2, 300), decay_rate=0.8, angle=60, width=7)

    screen.fill(BACKGROUND_COLOR)
    
    running = True

    pygame.display.set_caption("Slow generating tree")
    while running:
        screen.fill(BACKGROUND_COLOR)
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 

        tree.update()
        tree.draw(screen)

        # Update display
        pygame.display.update()
        clock.tick(60)
    main_menu()


def simulation3_main():
    pygame.init()
    clock = pygame.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    tree = do.RandomTree(pygame.Vector2(WIDTH//2, 400), pygame.Vector2(WIDTH//2, 300), decay_rate=0.8)

    screen.fill(BACKGROUND_COLOR)
    
    running = True

    pygame.display.set_caption("Random tree")
    while running:
        screen.fill(BACKGROUND_COLOR)
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 

        tree.draw(screen)
        tree.generate_new_tree()
        # Update display
        pygame.display.update()
        clock.tick(60)
    main_menu()

if __name__ == "__main__":
    main_menu()