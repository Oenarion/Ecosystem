import random
from perlin_noise import PerlinNoise

class Walker():
    """
    Walker class, performs either:
    - random walk, choosing a random step from -1 to 1.
    - random walk with perlin noise, with a given starting noise and step.
    """
    def __init__(self, x, y, color, mode, width, height, starting_noise_x = None, starting_noise_y = None, step = None):
        self.x = x
        self.y = y
        self.color = color
        self.mode = mode
        self.positions = []
        self.width = width
        self.height = height

        #Perlin noise variant
        self.noise_x = starting_noise_x
        self.noise_y = starting_noise_y
        self.step = step
        self.noise_generator = PerlinNoise()

    def randomWalk(self, WIDTH, HEIGHT):
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
            self.x = WIDTH - self.width
        if self.y < 0:
            self.y = 0
        if self.y > HEIGHT:
            self.y = HEIGHT - self.height

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
        return [self.positions, self.color, self.width, self.height]
