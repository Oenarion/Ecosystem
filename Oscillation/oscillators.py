import pygame
import math
import random

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
        rotated_surf = pygame.transform.rotate(rect_surf, self.angle_position)
        rotated_rect = rotated_surf.get_rect(center=self.rect.center)

        # Blit the rotated surface
        screen.blit(rotated_surf, rotated_rect.topleft)


class Spaceship():

    def __init__(self, x: int, y: int, w: int, h: int, color: tuple,
                 velocity = None, speed = 1, acceleration = 0.1, angle = 0):
                
        self.color = color
        self.w = w
        self.h = h
        self.rect = pygame.Rect(x, y, w, h)

        self.speed = speed
        self.acceleration = acceleration
        self.position = pygame.Vector2(x, y)
        self.velocity = velocity if velocity is not None else pygame.Vector2(0, 0)
        self.angle = angle
        self.rotation_amount = 5


    def apply_thrust(self):
        """
        Moves the spaceship in the direction of its current angle.
        """

        # Convert angle to radians
        angle_rad = math.radians(self.angle)

        # Compute thrust force vector (small increments)
        thrust_force = pygame.Vector2(
            self.acceleration * math.cos(angle_rad),
            self.acceleration * math.sin(angle_rad)
        )

        # Apply the force without normalizing (to accumulate velocity correctly)
        self.velocity += thrust_force

        # Optional: Limit max speed
        max_speed = 20
        if self.velocity.magnitude() > max_speed:
            self.velocity.scale_to_length(max_speed)

    def decrease_speed(self):
        """
        Decreases the velocity of the spaceship to standard velocity when no thrust is applied.
        """
        # Convert angle to radians
        angle_rad = math.radians(self.angle)

        # Compute thrust force vector (small increments)
        thrust_force = pygame.Vector2(
            self.acceleration * math.cos(angle_rad),
            self.acceleration * math.sin(angle_rad)
        )

        # Apply the force without normalizing (to accumulate velocity correctly)
        self.velocity -= thrust_force

        if self.velocity.magnitude() < self.speed:
            self.velocity.scale_to_length(self.speed)

    def turn(self, direction):
        """
        Rotates the spaceship left or right.
        """
        if direction == "LEFT":
            self.angle = (self.angle - self.rotation_amount) % 360  # Rotate counterclockwise
        elif direction == "RIGHT":
            self.angle = (self.angle + self.rotation_amount) % 360  # Rotate clockwise

        angle_rad = math.radians(self.angle)
        speed_direction = pygame.Vector2(
            self.speed * math.cos(angle_rad),
            self.speed * math.sin(angle_rad)
        )
        speed_direction.normalize_ip()
        self.velocity = speed_direction * self.velocity.magnitude()

    def update_position(self):
        """
        Updates the spaceship's position based on velocity.
        """

        self.position += self.velocity
        self.rect = pygame.Rect(self.position.x, self.position.y, self.w, self.h)
       

    def draw(self, screen):
        """
        Draws the rotated rectangle on the screen.
        """

        # Create a surface with the same size as the rect, with transparency
        rect_surf = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        rect_surf.fill(self.color)

        # Rotate the surface
        rotated_surf = pygame.transform.rotate(rect_surf, -self.angle) 
        rotated_rect = rotated_surf.get_rect(center=(self.position.x, self.position.y))  # Update position

        # Blit the rotated surface to the screen
        screen.blit(rotated_surf, rotated_rect.topleft)


class Oscillator():
    def __init__(self, x: int, y: int, radius: int,angle: float, angle_velocity: pygame.Vector2, amplitude: int, angle_acceleration: pygame.Vector2):
        
        self.x = x
        self.y = y
        self.radius = radius
        self.position = pygame.Vector2(x, y)
        self.angle = angle if angle is not None else pygame.Vector2(0,0)
        self.angle_velocity = angle_velocity if angle_velocity is not None else pygame.Vector2(random.uniform(0, 0.5), random.uniform(0, 0.5))
        self.starting_angle_velocity = self.angle_velocity.copy()
        self.angle_acceleration = angle_acceleration
        self.amplitude = amplitude

    def accelerate(self):
        if self.angle_velocity.magnitude_squared() < 100:
            self.angle_velocity += self.angle_acceleration
            self.angle_velocity.x = min(self.angle_velocity.x, 10)

    def decelerate(self):
        if self.angle_velocity.magnitude() > self.starting_angle_velocity.magnitude():
            self.angle_velocity -= self.angle_acceleration

    def oscillate(self):
        new_x = self.x + (math.sin(math.radians(self.angle.x)) * self.amplitude)
        new_y = self.y + (math.sin(math.radians(self.angle.y)) * self.amplitude)

        self.position = pygame.Vector2(new_x, new_y)
        self.angle += self.angle_velocity

    def draw(self, screen):
        pygame.draw.line(screen, (128, 0, 60), (self.x, self.y), (self.position.x, self.position.y))
        pygame.draw.circle(screen, (60, 200, 200), (self.position.x, self.position.y), self.radius + 3)
        pygame.draw.circle(screen, (200, 200, 200), (self.position.x, self.position.y), self.radius)
        

class Wave():
    def __init__(self, amplitude: int, wavelength: int, delta_angle: float, start_angle):
        self.amplitude = amplitude
        self.wavelength = wavelength
        self.delta_angle = delta_angle
        self.start_angle = start_angle  # Phase shift for animation

    def get_y_offset(self, x):
        """
        Compute the wave's y offset at a given x position.
        """
        angle = self.start_angle + (x / self.wavelength) * 360  # Convert to degrees
        return math.sin(math.radians(angle)) * self.amplitude  # Convert to y offset

    def update_wave(self):
        """
        Update the wave to animate it.
        """
        self.start_angle += self.delta_angle  # Move the wave over time
