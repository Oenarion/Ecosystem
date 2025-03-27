import pygame
import math

class RotatingMover():

    def __init__(self, x: int, y: int, w: int, h: int, color: tuple,
                 mass = 1, velocity = None, acceleration = None,
                 angle_position = 0, angle_velocity = 0, angle_acceleration = 0):
                
        self.color = color
        self.mass = mass
        self.w = w
        self.h = h
        self.rect = pygame.Rect(x, y, w, h)

        self.position = pygame.Vector2(x, y)
        self.velocity = velocity if velocity is not None else pygame.Vector2(0, 0)
        self.acceleration = acceleration if acceleration is not None else pygame.Vector2(0, 0)

        self.angle_position = angle_position
        self.angle_velocity = angle_velocity
        self.angle_acceleration = angle_acceleration


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
        The update takes into account also angle acceleration (rotation of the object).
        """
        self.velocity += self.acceleration
        self.position += self.velocity
        self.rect = pygame.Rect(self.position.x, self.position.y, self.w, self.h)
        
        self.angle_acceleration = self.acceleration.magnitude()
        print(self.angle_acceleration, self.acceleration.magnitude())
        self.angle_velocity += self.angle_acceleration
        self.angle_velocity = min(0.1, max(-0.1, self.angle_velocity))
        print(self.angle_velocity, math.degrees(self.angle_velocity))
        self.angle_position += math.degrees(self.angle_velocity)
        self.angle_position %= 360
        
        self.acceleration *= 0 
        self.angle_acceleration = 0

        print(self.angle_position)


    def draw(self, screen):
        """
        Draws the rotated rectangle on the screen
        """

        # Create a surface with the same size as the rect
        rect_surf = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        rect_surf.fill(self.color)

        # Rotate the surface
        rotated_surf = pygame.transform.rotate(rect_surf, self.angle_position)  # Negative to match Pygame rotation
        rotated_rect = rotated_surf.get_rect(center=self.rect.center)

        # Blit the rotated surface
        screen.blit(rotated_surf, rotated_rect.topleft)