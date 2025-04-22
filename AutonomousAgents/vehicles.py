import pygame
import math

class Vehicle():
    def __init__(self, x: int, y: int, dim:int, color: tuple,velocity = None, acceleration = None):

        self.rect = pygame.Rect(x, y, dim, dim)
        self.color = color
        self.position = pygame.Vector2(x, y)
        self.velocity = velocity if velocity is not None else pygame.Vector2(0, 0)
        self.acceleration = acceleration if acceleration is not None else pygame.Vector2(0, 0)
        self.max_speed = 8
        self.pursuit = False
    
    def change_mode(self):
        """
        Change mode, either pursuit, i.e. follow object next position
        or not, i.e. follow object current position
        """
        self.pursuit = not self.pursuit

    def apply_force(self, force):
        """
        Applies force to the acceleration vector
        """
        self.acceleration += force

    def update(self):
        """
        Updates position of the vehicle
        """
        self.velocity += self.acceleration
        
        if self.velocity.magnitude() > self.max_speed:
            self.velocity.normalize_ip()
            self.velocity *= self.max_speed
        
        self.position += self.velocity
        self.acceleration *= 0
        #update rect position
        self.rect.center = self.position

    def seek(self, target):
        """
        The vehicle seeks the target, implementing a steering force.

        Args:
            - target: the target object, with the position attribute
        """
        if self.pursuit:
            target_pos = target.next_position()
        else:
            target_pos = target.position
        
        desired_speed = target_pos - self.position 
        desired_speed.normalize_ip()
        desired_speed *= self.max_speed
        steer = desired_speed - self.velocity
        # keep velocity in check
        if steer.magnitude() > self.max_speed:
            steer.normalize_ip()
            steer *= self.max_speed

        self.apply_force(steer)

    def draw(self, screen):
        """
        Draws the rect.
        """
        pygame.draw.rect(screen, self.color, self.rect)



class EscapingTarget():
    def __init__(self, x: int, y: int, radius: int, angle = 0, scale = 100):
        self.angle = angle
        self.radius = radius
        self.center = pygame.Vector2(x, y)
        self.position = pygame.Vector2(x, y)
        self.angle_increase = 3
        self.scale = scale

    def next_position(self):
        """
        Compute x and y next position 
        """
        x = self.scale * 2*math.sin(math.radians(self.angle))
        y = self.scale * math.sin(math.radians(2*self.angle))
        final_x, final_y = self.center.x + x, self.center.y + y
        return final_x, final_y

    def update_position(self):
        """
        Updates the position of the target, it follows the
        Lemniscate of Bernoulli, i.e. the infinity symbol
        """
        self.angle += self.angle_increase
        x, y = self.next_position()
        self.position = pygame.Vector2(x, y)
        
    def invert_direction(self):
        """
        Inverts the direction of the target
        """
        self.angle_increase *= -1

    def draw(self, screen):
        """
        Draws the object.
        """
        pygame.draw.circle(screen, (200, 100, 60), self.position, self.radius + 3)
        pygame.draw.circle(screen, (200, 200, 200), self.position, self.radius)