import pygame
import oscillators as oscillators
import random
import math
import time

WIDTH = 640
HEIGHT = 420
BACKGROUND_COLOR = (0, 0, 0)
TIME = time.time()
SPAWN_MAX = 300
asteroids_added_velocity = 0.1
ASTEROIDS_MAX_ADDED_VELOCITY = 20

spawn_side = {
    0: [-1, -40],
    1: [-1, HEIGHT + 40],
    2: [-40, -1],
    3: [WIDTH + 40, -1]
}



def update_screen(screen, spaceship, asteroids):
    
    spaceship.draw(screen)

    for asteroid in asteroids:
        asteroid.draw(screen)

def update_text(text, font, pos, screen):
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=pos)

    screen.blit(text_surface, text_rect)

def spawn_rate_handle(spawn_rate, spawn_limit):
    global TIME, asteroids_added_velocity, SPAWN_MAX, ASTEROIDS_MAX_ADDED_VELOCITY
    passed_time = time.time() - TIME

    if passed_time > 10:
        TIME = time.time()
        spawn_limit -= 1
        spawn_limit = max(spawn_limit, SPAWN_MAX)
        asteroids_added_velocity += 0.1
        asteroids_added_velocity = min(asteroids_added_velocity, ASTEROIDS_MAX_ADDED_VELOCITY)
        print(spawn_limit, asteroids_added_velocity)
    if random.randint(0, spawn_limit) < spawn_rate:
        return True
    return False

def asteroid_spawn_handle(asteroids_added_velocity, asteroids, spaceship):

    curr_spawn_side = spawn_side[random.randint(0, 3)]
    if curr_spawn_side[0] == -1:
        x = random.randint(0, WIDTH)
    else:
        x = curr_spawn_side[0]
    
    if curr_spawn_side[1] == -1:
        y = random.randint(0, HEIGHT)
    else:
        y = curr_spawn_side[1]

    size = random.randint(5, 40)
    velocity = 10 / math.sqrt(size)
    dist_vector = spaceship.position - pygame.Vector2(x, y)
    dist_vector.normalize_ip()
    asteroid_velocity = dist_vector * velocity
    asteroid_velocity += pygame.Vector2(asteroids_added_velocity, asteroids_added_velocity)
    print("new asteroid!")
    asteroid = oscillators.Asteroid(x, y, size, size, (128, 128, 128), velocity=asteroid_velocity, angle_velocity= velocity / 10)
    asteroids.append(asteroid)

def main():
    
    pygame.init()
    FONT =  pygame.font.Font(None, 24)
    clock = pygame.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    screen.fill(BACKGROUND_COLOR)
    spaceship = oscillators.Spaceship(300, 100, 20, 10, (128, 255, 0), pygame.Vector2(0, 1), angle=90)
    running = True

    turning_left = False
    turning_right = False
    thrust = False
    score = 0

    spawn_rate = 5
    spawn_limit = 500
    asteroids = []
    paused = False

    pygame.display.set_caption("Oscillation")
    while running:
        # if the game ends
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    paused = False
                    pygame.quit()

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

        if spawn_rate_handle(spawn_rate, spawn_limit):
            asteroid_spawn_handle(asteroids_added_velocity, asteroids, spaceship)

        idx_to_rmv = []
        idx_hit_spaceship = []
        for i, asteroid in enumerate(asteroids):
            asteroid.in_bounds(WIDTH, HEIGHT)
            collided = asteroid.check_collision(spaceship.rect)
            if collided:
                print("spaceship hit")
                spaceship.hit()
                idx_hit_spaceship.append(i)
            asteroid.update_position()
            if asteroid.check_death():
                idx_to_rmv.append(i)

        idx_to_rmv = idx_to_rmv[::-1]
        for idx in idx_to_rmv:
            asteroids.pop(idx)
            if idx != idx_hit_spaceship:
                score += 1

        spaceship.invulnerability_timer()
        spaceship.update_position(WIDTH, HEIGHT)

        screen.fill(BACKGROUND_COLOR)

        text = f"SCORE: {score}"
        update_text(text, FONT, (WIDTH//2 , 20),screen)

        text = f"LIVES: {spaceship.lifes}"
        update_text(text, FONT, (40 , 20),screen)

        update_screen(screen, spaceship, asteroids)

        if spaceship.lifes == 0:
            paused = True

        # Update display
        pygame.display.update()
        clock.tick(60)



if __name__ == "__main__":
    main()