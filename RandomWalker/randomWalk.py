import pygame
import random
from perlin_noise import PerlinNoise

WIDTH = 640
HEIGHT = 420
WALKER_WIDTH = 2
WALKER_HEIGHT = 2

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
            walk_x = random.uniform(-1, 1)
            walk_y = random.uniform(-1, 1)

            self.x += walk_x
            self.y += walk_y
        else:
            #print(self.noise_generator(self.noise_x), self.noise_generator(self.noise_y))
            self.x += self.noise_generator(self.noise_x)
            self.y += self.noise_generator(self.noise_y)
            self.noise_x += self.step
            self.noise_y += self.step

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

def main():
    pygame.init()
    clock = pygame.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    #Creating walkers
    num_walkers = random.randint(2, 15)
    print(f"Created {num_walkers} walkers!")
    walkers = []
    num_perlin = 0
    num_random = 0
    for _ in range(num_walkers):
        rand_color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        walker_x = random.randint(0, WIDTH)
        walker_y = random.randint(0, HEIGHT)
        mode = mode_map[random.choice([0,1])]
        if mode == 'perlin':
            starting_noise_x1 = random.uniform(0, 10)
            starting_noise_y1 = random.uniform(0, 10)
            starting_jump = 0.01
            temp_walker = Walker(walker_x, walker_y, rand_color, mode, starting_noise_x1, starting_noise_y1, starting_jump)
            num_perlin += 1
        else:
            temp_walker = Walker(walker_x, walker_y, rand_color, mode)
            num_random += 1

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
        
        # Update display
        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main()
    pygame.quit()