import pygame
import random
from perlin_noise import PerlinNoise

WIDTH = 640
HEIGHT = 420
WALKER_WIDTH = 2
WALKER_HEIGHT = 2
MAX_WALKERS = 50

mode_map = {
    0: 'random',
    1: 'perlin'
}

class Walker():
    """
    Walker class, performs either:
    - random walk, choosing a random step from -1 to 1.
    - random walk with perlin noise, with a given starting noise and step.
    """
    def __init__(self, x, y, color, mode, starting_noise_x = None, starting_noise_y = None, step = None):
        self.x = x
        self.y = y
        self.color = color
        self.mode = mode
        self.positions = []

        #Perlin noise variant
        self.noise_x = starting_noise_x
        self.noise_y = starting_noise_y
        self.step = step
        self.noise_generator = PerlinNoise()

    def randomWalk(self):
        """
        Updates the position of the walker following the chosen mode.
        """
        if self.mode == "random":
            walk_x = random.uniform(-2, 2)
            walk_y = random.uniform(-2, 2)

            self.x += walk_x
            self.y += walk_y
        else:
            # Add scale to make movements more pronounced
            noise_scale = 5.0
            
            noise_x_value = self.noise_generator(self.noise_x) * noise_scale
            noise_y_value = self.noise_generator(self.noise_y) * noise_scale
            
            # Occasionally add a random "kick" to break patterns
            if random.random() < 0.05:  # 5% chance of a random kick
                noise_x_value += random.uniform(-2, 2)
                noise_y_value += random.uniform(-2, 2)
            
            # Add a second noise to create more variation
            # This variations were introduced because the perlin walkers, seemed pretty "still" in the movement
            second_scale = 2.0
            noise_x_value += self.noise_generator(self.noise_x * 2.5) * second_scale
            noise_y_value += self.noise_generator(self.noise_y * 2.5) * second_scale
            
            self.x += noise_x_value
            self.y += noise_y_value
            
            self.noise_x += self.step
            self.noise_y += self.step
        
            # Occasionally change direction in noise space
            if random.random() < 0.01:
                self.step = -self.step


        # Keep walker in bounds
        if self.x < 0:
            self.x = 0
        if self.x > WIDTH:
            self.x = WIDTH - WALKER_WIDTH
        if self.y < 0:
            self.y = 0
        if self.y > HEIGHT:
            self.y = HEIGHT - WALKER_HEIGHT

        self.positions.append([self.x, self.y])
        if len(self.positions) > 100:
            self.positions.pop(0)  

    def update_step(self, step_update):
        """
        For Perlin walkers only, updates the step size.
        """
        self.step += step_update

    def get_walker_mode(self):
        """
        Return the walker mode, used mainly to check if we want to use update_step().
        """
        return self.mode

    def get_walker_attributes(self):
        """
        Returns position and color of walker, used mainly to draw the walker at each iteration.
        """
        return [self.positions, self.color]


def update_screen(screen, walkers):
    """
    Updates the screen with all the walkers next step

    Args:
        - walkers(Walker) -> objects to draw.
    """
    for walker in walkers:
        positions, color = walker.get_walker_attributes()
        for x, y in positions:
            rect = pygame.Rect(x, y, WALKER_WIDTH, WALKER_HEIGHT)
            pygame.draw.rect(screen, color, rect)

def create_new_walker():
    rand_color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
    walker_x = random.randint(0, WIDTH)
    walker_y = random.randint(0, HEIGHT)
    mode = mode_map[random.choice([0,1])]
    if mode == 'perlin':
        starting_noise_x1 = random.uniform(0, 100)
        starting_noise_y1 = random.uniform(0, 100)
        starting_jump = 0.01
        temp_walker = Walker(walker_x, walker_y, rand_color, mode, starting_noise_x1, starting_noise_y1, starting_jump)
    else:
        temp_walker = Walker(walker_x, walker_y, rand_color, mode)

    return temp_walker

def main():
    pygame.init()
    clock = pygame.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    #Creating walkers
    num_walkers = random.randint(2, 30)
    print(f"Created {num_walkers} walkers!")
    walkers = []
    num_perlin = 0
    num_random = 0

    for _ in range(num_walkers):
        temp_walker = create_new_walker()
        if temp_walker.get_walker_mode() == 'random':
            num_random += 1
        else:
            num_perlin += 1
        walkers.append(temp_walker)

    background_color = (0, 0, 0)  # Black
    
    print(f"We have {num_perlin} Perlin walkers!")
    print(f"We have {num_random} Random walkers!")

    screen.fill(background_color)

    update_step = 0

    update_screen(screen, walkers)

    pygame.display.set_caption("Random Walk Simulation")
    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return  # Quit simulation

        for walker in walkers:
            walker.randomWalk()
            if walker.get_walker_mode() == 'perlin' and update_step > 100:
                walker.update_step(0.01)

        update_step += 1
        screen.fill(background_color)
        update_screen(screen, walkers)
        
        if len(walkers) < 50:
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
    main()
    pygame.quit()