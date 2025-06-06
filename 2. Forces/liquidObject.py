import pygame


class Liquid():

    def __init__(self, x: int, y: int, w: int, h: int, color: tuple, c=0.2):
        self.liquid_rect = pygame.Rect(x, y, w, h)
        self.color = color
        self.c = c
        

    def contains_object(self, obj: pygame.Rect):
        """
        Checks if the given object is inside the liquid.

        """
        if self.liquid_rect.colliderect(obj):
            return True
    
        return False
    
    def compute_drag_force(self, velocity: pygame.Vector2, sur_area: int, mass: float):
        """
        Computes the drag force for the given object.

        Args:
            - velocity -> velocity vector of the object.
            - sur_area -> surface area of the object.

        Returns the drag force.
        """

        speed = velocity.magnitude_squared()
        drag_magnitude = speed * self.c * sur_area
        drag_force = velocity.copy()
        drag_force.normalize_ip()
        drag_force *= -1
        drag_force *= drag_magnitude

        buoyant_force = pygame.Vector2(0, -mass * 0.3)
        
        return drag_force, buoyant_force
    
    def get_draw_attributes(self):
        """
        Returns attributes for drawing, i.e. rect and color
        """

        return [self.liquid_rect, self.color]