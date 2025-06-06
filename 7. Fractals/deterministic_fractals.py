import pygame
import time
import graphical_components as gc
import deterministic_objects as do
import math

WIDTH = 640
HEIGHT = 500
BACKGROUND_COLOR = (0, 0, 0)
TIME = time.time()

def main_menu():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Main menu")
    clock = pygame.time.Clock()

    simulation1_button = gc.Button(WIDTH // 2 - 150, HEIGHT // 2 - 150, 300, 50, "Cantor Set")
    simulation2_button = gc.Button(WIDTH // 2 - 150, HEIGHT // 2 - 50, 300, 50, "Koch Curve")
    simulation3_button = gc.Button(WIDTH // 2 - 150, HEIGHT // 2 + 50, 300, 50, "Koch Snowflake")
    exit_button = gc.Button(WIDTH // 2 - 150, HEIGHT // 2 + 150, 300, 50, "Exit")

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
    
    start_pos, end_pos = pygame.Vector2(0,HEIGHT//2), pygame.Vector2(WIDTH, HEIGHT//2)
    center = pygame.Vector2(WIDTH // 2, HEIGHT // 2)
    half_len = WIDTH // 2
    angle_step = 1
    angle = 0
    variation = False

    cantor_set = do.CantorSet(start_pos, end_pos, center, half_len, angle, variation)

    screen.fill(BACKGROUND_COLOR)

    running = True

    pygame.display.set_caption("Cantor Set")
    while running:
        screen.fill(BACKGROUND_COLOR)
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False    

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    variation = not variation
                    cantor_set = do.CantorSet(start_pos, end_pos, center, half_len, cantor_set.angle, variation)

                if event.key == pygame.K_n:
                    angle_step = 1 - angle_step

                if event.key == pygame.K_r:
                    cantor_set.angle = 0
        
        
        cantor_set.rotate(angle_step)
        cantor_set.draw(screen)
        # Update display
        pygame.display.update()
        clock.tick(60)
    main_menu()

def simulation2_main():
    pygame.init()
    FONT =  pygame.font.Font(None, 24)
    clock = pygame.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    screen.fill(BACKGROUND_COLOR)
    depth_slider = gc.Slider(x=10, y=40, width=120, height=10, min_val=1, max_val=5, initial_val=1, toggle=True, interval=1, label="Depth")
    depth = depth_slider.current_val
    old_depth_val = depth_slider.current_val
    start_pos, end_pos = pygame.Vector2(0,HEIGHT//2), pygame.Vector2(WIDTH, HEIGHT//2)

    koch = do.KochCurve(start_pos, end_pos, depth)
    running = True

    pygame.display.set_caption("Koch Curve")
    while running:
        screen.fill(BACKGROUND_COLOR)
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 

            depth_slider.handle_event(event)

        depth = depth_slider.current_val
        # print(depth, old_depth_val)
        if depth != old_depth_val:
            koch = do.KochCurve(start_pos, end_pos, depth)
            old_depth_val = depth

        koch.draw(screen)
        # koch_curve(screen, start_pos, end_pos, depth)

        depth_slider.draw(screen, FONT)
        # Update display
        pygame.display.update()
        clock.tick(30)
    main_menu()

def simulation3_main():
    pygame.init()
    FONT =  pygame.font.Font(None, 24)
    clock = pygame.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    screen.fill(BACKGROUND_COLOR)
    depth_slider = gc.Slider(x=10, y=40, width=120, height=10, min_val=1, max_val=5, initial_val=1, toggle=True, interval=1, label="Depth")
    depth = depth_slider.current_val
    old_depth_val = depth_slider.current_val
    start_pos, end_pos = pygame.Vector2(WIDTH//3,HEIGHT*2//3), pygame.Vector2(WIDTH*2//3, HEIGHT*2//3)

    direction = end_pos - start_pos
    angle = math.radians(-60)
    rotated = pygame.Vector2(
        direction.x * math.cos(angle) - direction.y * math.sin(angle),
        direction.x * math.sin(angle) + direction.y * math.cos(angle)
    )
    third_pos = start_pos + rotated

    kochs = [do.KochCurve(start_pos, end_pos, depth, 1), 
             do.KochCurve(start_pos, third_pos, depth), 
             do.KochCurve(third_pos, end_pos, depth)]
    running = True

    pygame.display.set_caption("Koch Curve")
    while running:
        screen.fill(BACKGROUND_COLOR)
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 

            depth_slider.handle_event(event)

        depth = depth_slider.current_val
        if depth != old_depth_val:
            kochs_array = []
            for koch in kochs:
                kochs_array.append(do.KochCurve(koch.start_pos, koch.end_pos, depth, koch.rotation_sign))
            old_depth_val = depth
            kochs = kochs_array

        for koch in kochs:
            koch.draw(screen)

        depth_slider.draw(screen, FONT)
        # Update display
        pygame.display.update()
        clock.tick(30)
    main_menu()

if __name__ == "__main__":
    main_menu()