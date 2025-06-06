import pygame
import moverObject
import time

class Attractor():
    def __init__(self, x: int, y: int, color: tuple, radius: int, mass = 1):

        self.G = 1
        self.mass = mass        
        self.color = color
        self.position = pygame.Vector2(x, y)
        self.rect = pygame.Rect(x - radius, y - radius, radius*2, radius*2)
        self.radius = radius 

        # will be used for the spawn and death update
        self.total_radius = radius

        self.start_time_spawn = -1
        self.start_time_of_death = -1
        
        self.spawn_timer = 1
        self.death_timer = 2

    def attract(self, mover: moverObject.Mover) -> pygame.Vector2:
        """
        Computes the gravitational force between the attractor and a mover with the formula
        Fg = (G * m1 * m2) / r*r, where G is the gravitational constant, m1 is the mass of the mover,
        m2 is the mass of the attractor and r*r is the distance squared between the two objects.

        Args:
            - mover -> mover object

        Returns a pygame.Vector2 which is the gravitational force.
        """
        
        force = self.position - mover.position  # Inverti l'ordine della sottrazione
        distance = force.magnitude()

        # add a limit to the distance so that the force is never too weak or too strong.
        # the distance is now between 20 and 500
        # the higher the numbers the lower the power of the force

        distance = max(20, min(distance, 500))

        magnitude = (self.G * mover.mass * self.mass) / distance**2

        force.normalize_ip()
        force *= magnitude

        return force
    
    def get_draw_attributes(self):
        """
        Returns attributes for drawing, i.e. rect and color
        """
        return [self.radius, self.position, self.color]
    

    def death_of_attractor(self):
        """
        Start the death timer.

        This will invoke a constant update which shrinks the attractor until it dies.
        Also if the attractor was spawning (i.e. growing), it will stop that routine
        and start the death routine instead.
        """
        self.start_time_of_death = time.time()
        self.start_time_alive = -1

    def check_death_update(self):
        """
        Updates the dimensions of the attractor untile the death timer is met.
        The attractor will shrink until it is no more.

        Returns a boolean, True -> the attractor died, False -> it's still shrinking
        """
        if self.start_time_of_death != -1:
            passed_time = time.time() - self.start_time_of_death

            if passed_time > self.death_timer:
                return True
            
            # (self.death_timer - passed_time) / self.death_timer will give me the % of how close
            # we are w.r.t. the death timer, i.e. the closer we are (smaller number) the smaller the radius
            self.radius = ((self.death_timer - passed_time) / self.death_timer) * self.total_radius
            self.mass = self.radius * 2        
            self.rect = pygame.Rect(self.position.x - self.radius, self.position.y - self.radius, self.radius*2, self.radius*2)

        return False
    
    def birth_of_attractor(self):
        """
        Starts the spawning of the attractor.

        This will invoke a constant update which enlarges the attractor
        until it reaches it's full dimension.
        """
        self.start_time_spawn = time.time()
    
    def check_spawn_update(self):
        """
        It's the exact opposite of the check_death_update function, it updates the dimensions
        of the attractor until it reaches it's full capacity. While the attractor is growing it's
        still possible to kill it.

        Returns a boolean, True -> the attractor reached it's max dimension, False -> it's still getting bigger
        """
        if self.start_time_spawn != -1:
            passed_time = time.time() - self.start_time_spawn
            
            if passed_time > self.spawn_timer:
                return True
            
            # (1 - (self.alive_timer - passed_time) / self.alive_timer) will give me the % of how close
            # we are w.r.t. the alive timer, i.e. the closer we are (bigger number) the bigger the radius
            self.radius = (1 - ((self.spawn_timer - passed_time) / self.spawn_timer)) * self.total_radius
            self.mass = self.radius * 2        
