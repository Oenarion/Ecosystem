import pygame
import random

class Particle():
    def __init__(self, x: int, y: int, color: tuple, 
                 radius: int, mass = 1, velocity = None, acceleration = None):
        
        self.color = color
        self.mass = mass
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
        force_copy = force.copy()
        f = force_copy / self.mass  
        self.acceleration += f 

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
    
    def run(self, screen):
        self.update_position()
        self.draw(screen)

class Emitter():
    def __init__(self, origin_x, origin_y, max_particles):
        self.origin_position = pygame.Vector2(origin_x, origin_y)
        self.particles = []
        self.max_particles = max_particles

    def apply_force(self, force):
        """
        Apply force to all the particles.
        """
        for particle in self.particles:
            particle.apply_force(force)

    def add_particle(self):
        """
        Add a new particle to the emitter
        """
        if self.max_particles > 0:
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            self.particles.append(Particle(self.origin_position.x, self.origin_position.y, color, 
                                        4, velocity=pygame.Vector2(random.randint(-2, 2), random.randint(-4, 0))))
        self.max_particles -= 1


    def run(self, screen):
        """
        Apply force and draw the particles on the screen
        """
        for i in range(len(self.particles) - 1, -1, -1):
            self.particles[i].run(screen)
            if self.particles[i].is_dead():
                self.particles.pop(i)

    def is_dead(self):
        """
        Checks whether the emitter ended it's life cycle.
        The life cycle is given by the number of particles created up to a maxium.
        """
        return self.max_particles <= 0 and len(self.particles) <= 0


class ExplodingBall():
    def __init__(self, x, y, radius, color, velocity = None, acceleration = None):
        self.position = pygame.Vector2(x, y)
        self.radius = radius
        self.color = color
        self.velocity = velocity if velocity is not None else pygame.Vector2(0, 0)
        self.acceleration = acceleration if acceleration is not None else pygame.Vector2(0, 0)
        self.particles = []
        self.dead = False

    def apply_force(self, force: pygame.Vector2):
        """
        Applies a force on the ball object (i.e. gravity), follows Newton's formula F = m x A

        Args:
            - force -> force to be applied
        """
        self.acceleration += force

    def death_animation(self):
        """
        the ball explodes into smaller balls
        """

        for i in range(50):
            self.particles.append(Particle(self.position.x, self.position.y, self.color, random.randint(1, self.radius//2),
                                            1, pygame.Vector2(random.randint(-10, 10), random.randint(-10, 10))))

    def update_position(self, HEIGHT):
        """
        Updates the position of the ball, used after a force is applied via apply_force().
        """
        if not self.dead:
            self.velocity += self.acceleration
            self.position += self.velocity
            self.acceleration *= 0 
            self.rect = pygame.Rect(self.position.x - self.radius, self.position.y - self.radius, self.radius*2, self.radius*2)
            if self.position.y > HEIGHT and not self.dead:
                self.dead = True
                self.death_animation()
        else:
            for particle in self.particles:
                gravity = pygame.Vector2(0, 0.1)
                particle.apply_force(gravity)
                particle.update_position()

    def draw(self, screen):
        """
        Draws the ball on the screen.
        """
        if not self.dead:
            pygame.draw.circle(screen, (128, 128, 128), self.position, self.radius + 2)
            pygame.draw.circle(screen, self.color, self.position, self.radius)
        else:
            #draw particles
            for particle in self.particles:
                pygame.draw.circle(screen, (128, 128, 128), particle.position, particle.radius + 2)
                pygame.draw.circle(screen, particle.color, particle.position, particle.radius)
        