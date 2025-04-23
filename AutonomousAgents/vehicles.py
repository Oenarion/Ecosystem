import pygame
import math
import random

class Vehicle():
    def __init__(self, x: int, y: int, dim:int, color: tuple,velocity = None, acceleration = None):

        self.rect = pygame.Rect(x, y, dim, dim)
        self.color = color
        self.position = pygame.Vector2(x, y)
        self.velocity = velocity if velocity is not None else pygame.Vector2(0, 0)
        self.acceleration = acceleration if acceleration is not None else pygame.Vector2(0, 0)
        self.max_speed = 8
        self.max_force = 0.4
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
        if desired_speed.magnitude() < 100:
            # scale the speed according to the distance
            # the closer the slower, i.e. the vehicle is slowing down
            percentage = desired_speed.magnitude() / 100
        else:
            percentage = 1.0

        desired_speed.normalize_ip()
        desired_speed *= (self.max_speed * percentage)
        steer = desired_speed - self.velocity
        # keep velocity in check
        if steer.magnitude() > self.max_force:
            steer.normalize_ip()
            steer *= self.max_force

        self.apply_force(steer)

    def draw(self, screen):
        """
        Draws the rect.
        """
        pygame.draw.rect(screen, self.color, self.rect)


class OwnBehaviourVehicle():
    """
    The own behaviour vehicle should simulate the behaviour of moving towards a random point 
    of a rectangle once it's out of its bounds. This is done by first picking the closest side
    of the rectangle, and then picking a random point on it, which will give us the direction.
    """
    def __init__(self, x: int, y: int, dim:int, color: tuple, velocity=None, acceleration=None):
        self.rect = pygame.Rect(x, y, dim, dim)
        self.color = color
        self.position = pygame.Vector2(x, y)
        self.velocity = velocity if velocity is not None else pygame.Vector2(0, 0)
        self.acceleration = acceleration if acceleration is not None else pygame.Vector2(0, 0)
        self.max_speed = 8
        self.max_force = 0.4
        self.last_point_seen = None
        self.offset = 30  # distance from after which the vehicle will try to go again inside the rectangle

    def is_outside_with_offset(self, rect):
        """
        Checks if the vehicle is out of bounds, considering a minimum offset.
        Returns True if completely outside with offset, False otherwise.
        """
        out_left   = self.position.x < rect.left   - self.offset
        out_right  = self.position.x > rect.right  + self.offset
        out_top    = self.position.y < rect.top    - self.offset
        out_bottom = self.position.y > rect.bottom + self.offset
        return out_left or out_right or out_top or out_bottom

    def closest_side_point(self, rect):
        """
        Finds the closest side (with offset ignored here) and returns a random point on that side.
        """
        distances = {
            "left": abs(self.position.x - rect.left),
            "right": abs(self.position.x - rect.right),
            "top": abs(self.position.y - rect.top),
            "bottom": abs(self.position.y - rect.bottom)
        }

        closest_dist = 100000
        closest = None
        for key, dist in distances.items():
            # this prevents the wrong side to be chosen, i.e. top
            # side is always chosen because y is closer even tho we
            # would like to choose the right or left side.
            if dist < self.offset:
                continue
            if dist < closest_dist:
                closest_dist = dist
                closest = key

        if closest == "left":
            return pygame.Vector2(rect.left, random.randint(rect.top, rect.bottom))
        elif closest == "right":
            return pygame.Vector2(rect.right, random.randint(rect.top, rect.bottom))
        elif closest == "top":
            return pygame.Vector2(random.randint(rect.left, rect.right), rect.top)
        else:  # bottom
            return pygame.Vector2(random.randint(rect.left, rect.right), rect.bottom)

    def seek(self, target):
        desired = target - self.position
        distance = desired.length()

        if distance < 5:
            self.last_point_seen = None
            return

        desired.normalize_ip()
        desired *= self.max_speed

        steer = desired - self.velocity
        if steer.length() > self.max_force:
            steer.scale_to_length(self.max_force)

        self.apply_force(steer)

    def compute_new_velocity(self, rect):
        if self.is_outside_with_offset(rect):
            if self.last_point_seen is None:
                self.last_point_seen = self.closest_side_point(rect)
        else:
            self.last_point_seen = None

        if self.last_point_seen:
            self.seek(self.last_point_seen)

    def apply_force(self, force):
        self.acceleration += force

    def update(self):
        self.velocity += self.acceleration
        if self.velocity.length() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)
        self.position += self.velocity
        self.acceleration *= 0
        self.rect.center = self.position

    def draw(self, screen):
        if self.last_point_seen:
            pygame.draw.circle(screen, (128, 128, 128), self.last_point_seen, 4)
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