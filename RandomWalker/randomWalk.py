import pygame
import random
import graphical_components as gc
import walker
import options as opt
import time

WIDTH = 640
HEIGHT = 420
WALKER_WIDTH = 2
WALKER_HEIGHT = 2
MAX_WALKERS = 50

mode_map = {
    0: 'random',
    1: 'perlin',
    2: 'gaussian'
}


def main_menu():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Random Walker Simulation")
    clock = pygame.time.Clock()

    # Create menu buttons
    start_button = gc.Button(WIDTH // 2 - 100, HEIGHT // 2 - 75, 200, 50, "Start")
    options_button = gc.Button(WIDTH // 2 - 100, HEIGHT // 2, 200, 50, "Options")
    exit_button = gc.Button(WIDTH // 2 - 100, HEIGHT // 2 + 75, 200, 50, "Exit")

    # Options menu
    options_menu = opt.OptionsMenu(WIDTH, HEIGHT)
    show_options = False

    running = True
    while running:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            # exit
            if event.type == pygame.QUIT:
                return False 
            
            # options
            if show_options:
                options_result = options_menu.handle_event(event)
                if options_result == "BACK":
                    show_options = False
            # main menu
            else:
                start_button.handle_event(event)
                options_button.handle_event(event)
                exit_button.handle_event(event)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if start_button.is_hovered(event.pos):
                        # Start the simulation with current max walkers setting from slider
                        main(int(options_menu.walkers_slider.current_val))
                    
                    if options_button.is_hovered(event.pos):
                        show_options = True
                    
                    if exit_button.is_hovered(event.pos):
                        return False  # Exit application

        # Draw menu or options
        if show_options:
            options_menu.draw(screen)
        else:
            # Draw menu buttons
            start_button.draw(screen)
            options_button.draw(screen)
            exit_button.draw(screen)

        pygame.display.update()
        clock.tick(60)

def update_screen(screen, walkers):
    """
    Updates the screen with all the walkers next step

    Args:
        - walkers(Walker) -> objects to draw.
    """
    for walker in walkers:
        positions, color, w_width, w_height = walker.get_walker_attributes()
        for x, y in positions:
            rect = pygame.Rect(x, y, w_width, w_height)
            pygame.draw.rect(screen, color, rect)

def create_new_walker():
    """
    Creates a new walker with random attributes.

    Returns:
        The walker object.
    """
    rand_color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
    walker_x = random.randint(0, WIDTH)
    walker_y = random.randint(0, HEIGHT)
    mode = mode_map[random.choice([0,1,2])]
    if mode == 'perlin':
        starting_noise_x1 = random.uniform(0, 100)
        starting_noise_y1 = random.uniform(0, 100)
        starting_jump = 0.01
        temp_walker = walker.PerlinWalker(walker_x, walker_y, rand_color, mode, WALKER_WIDTH, WALKER_HEIGHT, starting_noise_x1, starting_noise_y1, starting_jump)
    elif mode == 'random':
        temp_walker = walker.RandomWalker(walker_x, walker_y, rand_color, mode, WALKER_WIDTH, WALKER_HEIGHT)
    else:
        temp_walker = walker.GaussianWalker(walker_x, walker_y, rand_color, mode, WALKER_WIDTH, WALKER_HEIGHT)

    return temp_walker



def main(num_walkers):
    pygame.init()
    clock = pygame.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    #Creating walkers
    print(f"Created {num_walkers} walkers!")
    walkers = []
    num_perlin = 0
    num_random = 0
    num_gaussian = 0

    for _ in range(num_walkers):
        temp_walker = create_new_walker()
        if temp_walker.get_walker_mode() == 'random':
            num_random += 1
        elif temp_walker.get_walker_mode() == 'perlin':
            num_perlin += 1
        else:
            num_gaussian += 1
        walkers.append(temp_walker)

    background_color = (0, 0, 0)  # Black
    
    print(f"We have {num_random} Random walkers!")
    print(f"We have {num_perlin} Perlin walkers!")
    print(f"We have {num_random} Gaussian walkers!")  

    screen.fill(background_color)

    update_step = 0

    update_screen(screen, walkers)

    loading_circle = gc.LoadingCircle(10, 10)  # Top-left corner
    
    # Font for instructions
    esc_pressed = False
    running = True

    pygame.display.set_caption("Random Walk Simulation")
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return  # Quit simulation

        keys = pygame.key.get_pressed()
        
        # ESC key handling
        if keys[pygame.K_ESCAPE]:
            if not esc_pressed:
                # First time pressing ESC
                loading_circle.start_loading()
                esc_pressed = True
        else:
            # Reset if ESC is released
            loading_circle.stop_loading()
            esc_pressed = False

        for walker in walkers:
            walker.randomWalk(WIDTH, HEIGHT)
            if walker.get_walker_mode() == 'perlin' and update_step > 100:
                walker.update_step(0.01)
  
        update_step += 1
        screen.fill(background_color)
        update_screen(screen, walkers)
        loading_circle.draw(screen)

        if loading_circle.is_loading and time.time() - loading_circle.start_time >= loading_circle.duration:
            running = False
        
        if len(walkers) < MAX_WALKERS:
            walker_generator_chance = random.randint(0,1000)
            # 1 in 1000 chance to generate a new random walker at each step
            if walker_generator_chance > 999:
                temp_walker = create_new_walker()
                walkers.append(temp_walker)
                print(f"A new {walkers[-1].get_walker_mode()} walker appeared!")

        # Update display
        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main_menu()
    pygame.quit()