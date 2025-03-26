import pygame

class Body():
    def __init__(self, x: int, y: int, color: tuple, radius: int, mass = 1, velocity = None, acceleration = None):
        """
        A fusion between both mover and attractor, it exerts a gravitational force but
        can also be attracted by it.
        """

        self.G = 1
        self.mass = mass        
        self.color = color

        self.rect = pygame.Rect(x - radius, y - radius, radius*2, radius*2)
        self.radius = radius 

        self.position = pygame.Vector2(x, y)
        self.velocity = velocity if velocity is not None else pygame.Vector2(0, 0)
        self.acceleration = acceleration if acceleration is not None else pygame.Vector2(0, 0)

    def attract(self, body) -> pygame.Vector2:
        """
        Computes the gravitational force between two Bodies with the formula
        Fg = (G * m1 * m2) / r*r, where G is the gravitational constant, m1 is the mass of the mover,
        m2 is the mass of the attractor and r*r is the distance squared between the two objects.

        Args:
            - mover -> mover object

        Returns a pygame.Vector2 which is the gravitational force.
        """
        
        force = self.position - body.position  # Inverti l'ordine della sottrazione
        distance = force.magnitude()

        # add a limit to the distance so that the force is never too weak or too strong.
        # the distance is now between 20 and 500
        # the higher the numbers the lower the power of the force

        distance = max(20, min(distance, 500))

        magnitude = (self.G * body.mass * self.mass) / distance**2

        force.normalize_ip()
        force *= magnitude

        return force
    
    def get_draw_attributes(self):
        """
        Returns attributes for drawing, i.e. rect and color
        """
        return [self.radius, self.position, self.rect, self.color]
    
    def apply_force(self, force: pygame.Vector2):
        """
        Applies a force on the Body object (i.e. gravity), follows Newton's formula F = m x A

        Args:
            - force -> force to be applied
        """
        force_copy = force.copy()
        f = force_copy / self.mass  
        self.acceleration += f 

    def update_position(self):
        """
        Updates the position of the Body, used after a force is applied via apply_force().
        """
        self.velocity += self.acceleration
        self.position += self.velocity
        self.acceleration *= 0 
        self.rect = pygame.Rect(self.position.x - self.radius, self.position.y - self.radius, self.radius*2, self.radius*2)