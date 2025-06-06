import pygame
import time
import graphical_components as gc
import math

WIDTH = 640
HEIGHT = 420
BACKGROUND_COLOR = (0, 0, 0)
TIME = time.time()

def generate_circle(screen, x, y, r):
    color = min(255, int((r * 255) / 200))
    pygame.draw.circle(screen, (0, color, color), 
                                (x, y), r, width=1)
    if r > 2:
        
        r *= 0.75

        generate_circle(screen, x, y, r)

def generate_4_circles(screen, x, y, r):
    color = min(255, int((r * 255) / 200))
    pygame.draw.circle(screen, (color, color, color), 
                                (x + (r//2), y), r, width=1)
    pygame.draw.circle(screen, (color, color, color), 
                                (x - (r//2), y), r, width=1)
    pygame.draw.circle(screen, (color, color, color), 
                                (x, y + (r//2)), r, width=1)
    pygame.draw.circle(screen, (color, color, color), 
                                (x, y - (r//2)), r, width=1)
    if r > 20:
        
        r *= 0.5

        generate_4_circles(screen, x + (r//2), y, r)
        generate_4_circles(screen, x - (r//2), y, r)
        generate_4_circles(screen, x, y + (r//2), r)
        generate_4_circles(screen, x, y - (r//2), r)

def main_menu():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("")
    clock = pygame.time.Clock()

    simulation1_button = gc.Button(WIDTH // 2 - 150, HEIGHT // 2 - 150, 300, 50, "Circle zoom")
    simulation2_button = gc.Button(WIDTH // 2 - 150, HEIGHT // 2 - 75, 300, 50, "Quadruple circle fractal")
    exit_button = gc.Button(WIDTH // 2 - 150, HEIGHT // 2, 300, 50, "Exit")

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
                    pygame.quit()
                    simulation1_main()
                
                if simulation2_button.is_hovered(event.pos):
                    pygame.quit()
                    simulation2_main()

                if exit_button.is_hovered(event.pos):
                    running = False
                
        simulation1_button.draw(screen)
        simulation2_button.draw(screen)
        exit_button.draw(screen)

        pygame.display.update()
        clock.tick(60)

    pygame.quit()

def simulation1_main():
    
    pygame.init()
    clock = pygame.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    start_r_value = 600
    r = start_r_value

    screen.fill(BACKGROUND_COLOR)

    running = True

    pygame.display.set_caption("Zoom Circle fractal")
    while running:
        screen.fill(BACKGROUND_COLOR)
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 

        generate_circle(screen, 160, 210, r)
        r = (r + 10)
        if r == start_r_value//0.75:
            r = start_r_value

        # Update display
        pygame.display.update()
        clock.tick(60)
    main_menu()

def simulation2_main():
    
    pygame.init()
    clock = pygame.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    
    start_r_value = 700
    r = start_r_value
    zoom_speed = 0.02  # più piccolo = più lento
    time_elapsed = 0

    screen.fill(BACKGROUND_COLOR)

    running = True

    pygame.display.set_caption("Quadruple Circle Fractal")
    while running:
        screen.fill(BACKGROUND_COLOR)
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 

        r = start_r_value * (0.5 + 0.5 * math.cos(time_elapsed))
        generate_4_circles(screen, WIDTH//2, HEIGHT//2, r)
        
        time_elapsed += zoom_speed
        # Update display
        pygame.display.update()
        clock.tick(30)
    main_menu()

if __name__ == "__main__":
    main_menu()