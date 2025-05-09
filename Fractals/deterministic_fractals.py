import pygame
import time
import graphical_components as gc
import math

WIDTH = 640
HEIGHT = 420
BACKGROUND_COLOR = (0, 0, 0)
TIME = time.time()

def cantor(screen, start_pos: pygame.Vector2, end_pos: pygame.Vector2, variation = False, type = 0):

    curve = end_pos - start_pos

    if curve.magnitude() < 1:
        return
    
    segment = curve / 3

    p1 = start_pos
    p2 = start_pos + segment
    p3 = start_pos + segment * 2
    p4 = end_pos

    normal = pygame.Vector2(-segment.y, segment.x)
    normal.scale_to_length(20)

    pygame.draw.line(screen, (255, 255, 255), p1, p2, 2)
    
    pygame.draw.line(screen, (255, 255, 255), p3, p4, 2)


    if variation and curve.magnitude() / 3 >= 1:
        padding = 5
        line_length = 10

        normal_copy = normal.copy()
        normal_copy.normalize_ip()

        seg1 = p2 - p1
        seg2 = p4 - p3

        # 1/3 and 2/3 of the segments
        line_points = [
            p1 + seg1 * (1/6),
            p1 + seg1 * (5/6),
            p3 + seg2 * (1/6),
            p3 + seg2 * (5/6)
        ]

        for point in line_points:
            # Upper line
            pygame.draw.line(screen, (255, 255, 255), point + normal_copy * padding, point + normal_copy * (padding + line_length))
            # Below line
            pygame.draw.line(screen, (255, 255, 255), point - normal_copy * padding, point - normal_copy * (padding + line_length))
        
        #Circles between lines
        pygame.draw.circle(screen, (255, 255, 255), (p2 + p3) / 2, segment.magnitude()/2, width=1)
        pygame.draw.circle(screen, (255, 255, 255), (p2 + p3) / 2, segment.magnitude()/3, width=1)
        pygame.draw.circle(screen, (255, 255, 255), (p2 + p3) / 2, segment.magnitude()/6, width=1)

    if type == 1 or type == 0:
        cantor(screen, p1+normal, p2+normal, variation, 1)
        cantor(screen, p3+normal, p4+normal, variation, 1)

    if type == 2 or type == 0:
        cantor(screen, p1-normal, p2-normal, variation, 2)
        cantor(screen, p3-normal, p4-normal, variation, 2)

def main_menu():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("")
    clock = pygame.time.Clock()

    simulation1_button = gc.Button(WIDTH // 2 - 150, HEIGHT // 2 - 150, 300, 50, "Cantor Set")
    simulation2_button = gc.Button(WIDTH // 2 - 150, HEIGHT // 2 - 75, 300, 50, "Koch Curve")
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
    start_pos, end_pos = pygame.Vector2(0,HEIGHT//2), pygame.Vector2(WIDTH, HEIGHT//2)

    center = pygame.Vector2(WIDTH // 2, HEIGHT // 2)
    half_len = WIDTH // 2
    angle_step = 1
    angle = 0

    variation = False
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

                if event.key == pygame.K_n:
                    angle_step = 1 - angle_step

                if event.key == pygame.K_r:
                    angle = 0
        
        angle += angle_step

        # direction vector to rotate the cantor set
        dir_vec = pygame.Vector2(half_len, 0).rotate(angle) 
        start_pos = center - dir_vec
        end_pos = center + dir_vec

        cantor(screen, start_pos, end_pos, variation)

        # Update display
        pygame.display.update()
        clock.tick(60)
    main_menu()

def simulation2_main():
    
    pygame.init()
    clock = pygame.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    screen.fill(BACKGROUND_COLOR)

    running = True

    pygame.display.set_caption("Koch Curve")
    while running:
        screen.fill(BACKGROUND_COLOR)
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 

        # Update display
        pygame.display.update()
        clock.tick(30)
    main_menu()

if __name__ == "__main__":
    main_menu()