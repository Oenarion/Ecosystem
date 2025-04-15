import pygame
import random

class Particle():
    def __init__(self, x: int, y: int, color: tuple, 
                 radius: int, velocity = None, acceleration = None):
        
        self.color = color
        self.lifespan = 255
        self.radius = radius
        self.rect = pygame.Rect(x - radius, y - radius, radius*2, radius*2)

        # this are all pygame Vectors
        self.position = pygame.Vector2(x, y)
        self.velocity = velocity if velocity is not None else pygame.Vector2(0, 0)
        self.acceleration = acceleration if acceleration is not None else pygame.Vector2(0, 0)
        
    def apply_force(self, force: pygame.Vector2):
        """
        Applies a force on the Mover object (i.e. gravity), follows Newton's formula F = m x A

        Args:
            - force -> force to be applied
        """
        self.acceleration += force

    def update_position(self):
        """
        Updates the position of the mover, used after a force is applied via apply_force().
        """
        self.velocity += self.acceleration
        self.position += self.velocity
        self.acceleration *= 0 
        self.rect = pygame.Rect(self.position.x - self.radius, self.position.y - self.radius, self.radius*2, self.radius*2)

    def draw(self, screen):
        """
        Draw the object on the canvas.
        """
        alpha = max(0, min(255, self.lifespan))
        temp_surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        faded_color = (*self.color, alpha) 
        pygame.draw.circle(temp_surface, faded_color, (self.radius, self.radius), self.radius)
        screen.blit(temp_surface, (self.rect.x, self.rect.y))
        self.lifespan -= 3

    def is_dead(self):
        """
        Checks whether the particle is still alive.
        It's used when we want to get rid of a particle.
        """
        return self.lifespan < 0
    
    def run(self, force: pygame.Vector2, screen):
        self.apply_force(force)
        self.update_position()
        self.draw(screen)

class Emitter():
    def __init__(self, origin_x, origin_y):
        self.origin_position = pygame.Vector2(origin_x, origin_y)
        self.particles = []

    def add_particle(self):
        """
        Add a new particle to the emitter
        """
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.particles.append(Particle(self.origin_position.x, self.origin_position.y, color, 
                                       4, velocity=pygame.Vector2(random.randint(-2, 2), random.randint(-4, 0))))
        
    def run(self, force, screen):
        """
        Apply force and draw the particles on the screen
        """
        for i in range(len(self.particles) - 1, -1, -1):
            self.particles[i].run(force, screen)
            if self.particles[i].is_dead():
                self.particles.pop(i)
