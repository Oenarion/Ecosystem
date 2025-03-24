import pygame
import moverObject

class Attractor():
    def __init__(self, x: int, y: int, color: tuple, h: int, w: int, mass = 1):

        #self.h = h
        #self.w = w
        self.G = 0.5
        self.mass = mass        
        self.color = color
        self.position = pygame.Vector2(x, y)
        self.attractor_rect = pygame.Rect(x, y, w, h)

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

        # Evita divisione per zero e imposta un limite minimo alla distanza
        distance = max(distance, 5)

        magnitude = (self.G * mover.mass * self.mass) / distance**2

        force.normalize_ip()
        force *= magnitude

        return force
    
    def get_draw_attributes(self):
        """
        Returns attributes for drawing, i.e. rect and color
        """
        return [self.attractor_rect, self.color]