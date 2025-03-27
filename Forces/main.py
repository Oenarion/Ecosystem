import pygame
import random
import moverObject
import liquidObject
import attractorObject
import bodyObject
import graphical_components as gc

WIDTH = 640
HEIGHT = 420
BACKGROUND_COLOR = (0, 0, 0) # black
OIL_COLOR = (200, 200, 0) # yellow
WATER_COLOR = (0, 128, 255)  # blue

MAX_MOVERS = 20
MAX_ATTRACTORS = 15
MAX_BODIES = 100

def update_screen(screen: pygame.display, movers: list, liquids: liquidObject.Liquid, attractors: attractorObject.Attractor):
    """
    Updates the screen by visualizing all the objects in it.

    Args:
        - screen -> screen of the application
        - movers -> array of objects to be displayed
    """

    if liquids is not None and liquids != []:
        for liquid in liquids:
            rect, color = liquid.get_draw_attributes()
            pygame.draw.rect(screen, color, rect)

    if attractors is not None and attractors != []:
        for attractor in attractors:
            radius, position, color = attractor.get_draw_attributes()
            pygame.draw.circle(screen, color, (position.x, position.y), radius)
            if radius > 5:
                pygame.draw.circle(screen, (255, 255, 255), (position.x, position.y), radius - 5)

    for mover in movers:
        radius, position, _, color = mover.get_draw_attributes()
        pygame.draw.circle(screen, color, (position.x, position.y), radius)


def out_of_bounds(mover):
    """
    Checks if the mover is out of bounds.

    Returns a boolean.
    """
    if mover.position.x < -20 or mover.position.x > WIDTH + 20 \
        or mover.position.y < -20 or mover.position.y > HEIGHT + 20:
            return True

    return False

def create_new_mover(attractors):
    """
    Creates new mover object with random values initialization, if the mover overlaps for more than
    20 times with an existing attractor the object won't be created.

    Returns the new mover.
    """
    overlap = True
    counter = 0

    while overlap:
        mov_radius = random.randint(2, 10)
        mov_x, mov_y = random.choice([10, WIDTH - 10]), random.choice([10, HEIGHT - 10])
        mov_mass = mov_radius * 2
        mov_rand_color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        mov_rect = pygame.Rect(mov_x - mov_radius, mov_y - mov_radius, mov_radius*2, mov_radius*2)  
        if check_spawn_collision(mov_rect, attractors):
            curr_mover = moverObject.Mover(mov_x, mov_y, mov_rand_color, mov_radius, mass=mov_mass)
            overlap = False
        counter += 1
        
        if counter > 20:
            print("Couldn't create a suitable position for the mover")
            return None
        
    return curr_mover

def create_new_body():
    """
    Creates a new body with random values.

    Returns the new body.
    """
    mov_radius = random.randint(2, 20)
    mov_x, mov_y = random.randint(10, WIDTH - 10), random.randint(10, HEIGHT - 10)
    mov_mass = mov_radius * 2
    mov_rand_color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
    curr_body = bodyObject.Body(mov_x, mov_y, mov_rand_color, mov_radius, mass=mov_mass)

    return curr_body

def create_new_attractor(attractors):
    """
    Creates new attractor with random values initialization, if the attractor overlaps for more than
    20 times with an existing attractor the object won't be created.

    Returns the new attractor.
    """
    overlap = True
    counter = 0

    while overlap:
        att_x, att_y = random.randint(100, WIDTH - 100), random.randint(100, HEIGHT - 100)
        att_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        att_radius = random.randint(10, 20)
        att_mass = random.randint(40, 150)
        att_rect = pygame.Rect(att_x - att_radius, att_y - att_radius, att_radius*2, att_radius*2)  
        if check_spawn_collision(att_rect, attractors):
            new_attractor = attractorObject.Attractor(att_x, att_y, att_color, att_radius, att_mass)
            overlap = False
        
        counter += 1
        if counter > 20:
            print("Couldn't create a suitable position for the mover")
            return None
        
    return new_attractor

def check_spawn_collision(new_obj: pygame.Rect, attractors: list[attractorObject.Attractor]):
    """
    Checks whether the new object collides with any of the new attractor present in the simulation.

    Args:
        - new_obj -> rect of the mover or the attractor to be created.
        - attractors -> array of attractors objects.

    Returns a boolean.
    """
    for attractor in attractors:
        if new_obj.colliderect(attractor):
            return False

    return True

def main_menu():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Forces Simulation")
    clock = pygame.time.Clock()

    simulation1_button = gc.Button(WIDTH // 2 - 150, HEIGHT // 2 - 150, 300, 50, "Liquid Simulation")
    simulation2_button = gc.Button(WIDTH // 2 - 150, HEIGHT // 2 - 75, 300, 50, "Gravitational Attraction")
    simulation3_button = gc.Button(WIDTH // 2 - 150, HEIGHT // 2, 300, 50, "N-body problem")
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
                    simulation1_main()
                
                if simulation2_button.is_hovered(event.pos):
                    simulation2_main()

                if simulation3_button.is_hovered(event.pos):
                    simulation3_main()
                
                if exit_button.is_hovered(event.pos):
                    return False  # Exit application
                
        simulation1_button.draw(screen)
        simulation2_button.draw(screen)
        simulation3_button.draw(screen)
        exit_button.draw(screen)

        pygame.display.update()
        clock.tick(60)

def simulation1_main():
    pygame.init()
    clock = pygame.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    num_movers = random.randint(1, 5)
    print(f"Created {num_movers} movers!")
    movers = []
    
    

    water = liquidObject.Liquid(0, 300, WIDTH, HEIGHT - 300, WATER_COLOR)
    oil = liquidObject.Liquid(0, 250, WIDTH, 50, OIL_COLOR, 0.5)

    liquids = [water, oil]
    for i in range(num_movers):
        radius = random.randint(5, 20)
        x, y = random.randint(100, WIDTH - 100), 100
        mass = radius * 10
        rand_color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        friction_coef = random.uniform(0.8,0.99)
        print(f"Friction coef of mover {i} is: {friction_coef}")
        curr_mover = moverObject.Mover(x, y, rand_color, radius, mass=mass, friction_coef=friction_coef)
        movers.append(curr_mover)

    screen.fill(BACKGROUND_COLOR)

    update_screen(screen, movers, liquids, None)

    running = True

    gravity = pygame.Vector2(0, 0.1)
    increasing_gravity = pygame.Vector2(0, 0.5)
    max_val_gravity = 25
    apply_increased_gravity = False
    negative_increasing_gravity = pygame.Vector2(0, -0.5)
    apply_negative_increased_gravity = False
    wind = pygame.Vector2(0.5, 0)
    is_wind_blowing = False

    pygame.display.set_caption("Liquid Simulation")
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False # Quit simulation

            # wind blows if users clicks on the screen
            if event.type == pygame.MOUSEBUTTONDOWN:
                is_wind_blowing = True
            if event.type == pygame.MOUSEBUTTONUP:
                is_wind_blowing = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q: 
                    apply_increased_gravity = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_q: 
                    apply_increased_gravity = False
                    increasing_gravity = pygame.Vector2(0, 0.5) 

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w: 
                    apply_negative_increased_gravity = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w: 
                    apply_negative_increased_gravity = False
                    negative_increasing_gravity = pygame.Vector2(0, -0.5) 

        # movers are now subject to gravity
        for i, mover in enumerate(movers):

            if mover.check_floor(HEIGHT) and abs(mover.velocity.y) < 0.1:
                mover.velocity.y = 0
            else:
                # scale the gravity by the mover's mass
                mover.apply_force(gravity * mover.mass)
                if apply_increased_gravity:
                    increasing_gravity += pygame.Vector2(0, 0.001)
                    max_y_vel = min(increasing_gravity[1], max_val_gravity)
                    increasing_gravity = pygame.Vector2(0, max_y_vel)
                    mover.apply_force(increasing_gravity * mover.mass)

            if apply_negative_increased_gravity:
                negative_increasing_gravity += pygame.Vector2(0, -0.001)
                print(negative_increasing_gravity)
                max_y_vel = max(negative_increasing_gravity[1], -max_val_gravity)
                negative_increasing_gravity = pygame.Vector2(0, max_y_vel)
                mover.apply_force(negative_increasing_gravity * mover.mass)

            for liquid in liquids:
                if liquid.contains_object(mover.rect) and abs(mover.velocity.y) > 0.01:
                    drag_force, buoyant_force = liquid.compute_drag_force(mover.velocity, mover.radius, mover.mass)
                    #print(f"drag force: {drag_force}")

                    if drag_force.magnitude_squared() > mover.velocity.magnitude_squared():
                        limit_drag_force = pygame.Vector2(0, - mover.velocity.y*2) 
                        #print(f"Limit drag force: {limit_drag_force}")
                        mover.apply_force(limit_drag_force)
                    else:
                        mover.apply_force(drag_force)

                    # apply this force only if it's oil
                    if liquid.color == OIL_COLOR:
                        mover.apply_force(buoyant_force)

                    #print(f"curr acceleration: {mover.acceleration}")
            if is_wind_blowing:
                mouse_x, _ = pygame.mouse.get_pos()
                if mouse_x < mover.position.x:
                    mover.apply_force(wind)
                else:
                    mover.apply_force(-wind)

            if mover.check_floor(HEIGHT):
                friction = mover.compute_friction()
                mover.apply_force(friction)
            #     print(f"Friction: {friction}")
            #print(f"Mover's velocity: {mover.velocity}")

            
            mover.update_position()
        
            mover.check_edges(WIDTH, HEIGHT)

            

        screen.fill(BACKGROUND_COLOR)
        update_screen(screen, movers, liquids, None)
        
        # Update display
        pygame.display.update()
        clock.tick(60)

def simulation2_main():
    pygame.init()
    clock = pygame.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    num_movers = random.randint(5, 20)
    print(f"Created {num_movers} movers!")
    movers = []
    
    
    attractor_1 = attractorObject.Attractor(500, 200, (255, 0, 0), 15, 150)
    attractor_2 = attractorObject.Attractor(100, 200, (255, 0, 255), 15, 150)
    attractor_3 = attractorObject.Attractor(300, 200, (0, 255, 255), 15, 150)

    attractors = [attractor_1, attractor_2, attractor_3]

    for _ in range(num_movers):
        radius = random.randint(2, 10)
        x, y = random.randint(100, WIDTH - 100), random.randint(100, HEIGHT - 100)
        mass = radius * 2
        rand_color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        curr_mover = moverObject.Mover(x, y, rand_color, radius, mass=mass)
        movers.append(curr_mover)

    screen.fill(BACKGROUND_COLOR)

    update_screen(screen, movers, None, attractors)

    running = True

    pygame.display.set_caption("Gravitational Force Simulation")
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False # Quit simulation

        # movers are now subject to gravity
        for i, mover in enumerate(movers):
            
            if out_of_bounds(mover):
                print("Mover went in the outer space and was never found again!")
                movers.pop(i)

            if mover.check_floor(HEIGHT) and abs(mover.velocity.y) < 0.1:
                mover.velocity.y = 0

            idx_to_remove = []
            for i, attractor in enumerate(attractors):
                grav_force = attractor.attract(mover)
                # distance = (attractor.position - mover.position).magnitude()
                # print(f"ATTRACTOR {i}: Distance = {distance}, Force = {grav_force.magnitude()}")
                mover.apply_force(grav_force)

                attractor.check_spawn_update()
                is_dead = attractor.check_death_update()
                if is_dead:
                    idx_to_remove.append(i)

            for idx in idx_to_remove:
                attractors.pop(idx)

            mover.update_position()

        create_chance = random.randint(0, 1000)
        
        if create_chance > 998:
            remove_or_add = random.randint(0, 1)
            # 1 == True, remove a random attractor
            if remove_or_add and len(attractors) > 1:
                idx = random.randint(0, len(attractors) - 1)
                attractors[idx].death_of_attractor()
                print("Attractor started death timer!")
            # 0 == False, add an attractor
            else:
                if len(attractors) < MAX_ATTRACTORS:
                    new_attractor = create_new_attractor(attractors)
                    new_attractor.birth_of_attractor()
                    new_attractor.check_spawn_update()
                    if new_attractor is not None:
                        attractors.append(new_attractor)
                        print("New attractor!!")

        if create_chance < 10 and len(movers) < MAX_MOVERS:
            new_mover = create_new_mover(attractors)
            if new_mover is not None:
                print("New mover from outer space!")
                movers.append(new_mover)


        screen.fill(BACKGROUND_COLOR)
        update_screen(screen, movers, None, attractors)
        
        # Update display
        pygame.display.update()
        clock.tick(60)

def simulation3_main():
    pygame.init()
    clock = pygame.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    screen.fill(BACKGROUND_COLOR)

    bodies = []

    num_bodies = random.randint(5, 20)

    for _ in range(num_bodies):
        radius = random.randint(2, 10)
        x, y = random.randint(100, WIDTH - 100), random.randint(100, HEIGHT - 100)
        mass = radius * 2
        rand_color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        curr_body = bodyObject.Body(x, y, rand_color, radius, mass=mass)
        bodies.append(curr_body)

    screen.fill(BACKGROUND_COLOR)

    update_screen(screen, bodies, None, None)

    running = True

    pygame.display.set_caption("n-body Simulation")
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False # Quit simulation

        screen.fill(BACKGROUND_COLOR)
        
        for i, body in enumerate(bodies):
            body.check_spawn_update()
            for j, other_body in enumerate(bodies):
                if i != j:
                    grav_force = other_body.attract(body)
                    body.apply_force(grav_force)
            body.update_position()

            if out_of_bounds(body):
                print("Body went out of bounds :c")
                bodies.pop(i)
        
        spawn_chance = random.randint(0, 100)

        if spawn_chance > 99:
            new_body = create_new_body()
            new_body.birth_of_body()
            new_body.check_spawn_update()
            if new_body is not None and len(bodies) < MAX_BODIES:
                bodies.append(new_body)
                print("New body!!")

        update_screen(screen, bodies, None, None)
        # Update display
        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main_menu()