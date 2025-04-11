import pygame
import math
import random
import time

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
        # print(self.angle_acceleration, self.acceleration.magnitude())
        self.angle_velocity += self.angle_acceleration
        self.angle_velocity = min(0.1, max(-0.1, self.angle_velocity))
        # print(self.angle_velocity, math.degrees(self.angle_velocity))
        self.angle_position += math.degrees(self.angle_velocity)
        self.angle_position %= 360
        
        self.acceleration *= 0 
        self.angle_acceleration = 0

        # print(self.angle_position)


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

        # lifes of the spaceship and how much invulnerability we have after a hit.
        self.lifes = 3
        self.invulnerability_seconds = 1.5
        self.start_invulnerability_timer = -1
        self.is_invulnerable = False

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

    def update_position(self, WIDTH, HEIGHT):
        """
        Updates the spaceship's position based on velocity.
        """

        self.position += self.velocity
        self.rect = pygame.Rect(self.position.x, self.position.y, self.w, self.h)
        self.keep_spaceship_in_bounds( WIDTH, HEIGHT)

    def keep_spaceship_in_bounds(self, WIDTH, HEIGHT):
        """
        Keeps the spaceship in bounds. Since the spaceship will always be oriented
        in a certain way when hitting walls, he have to check that it doesn't surpass
        the value of height of the spaceship.

        Args:
            - WIDTH -> width of the canvas.
            - HEIGHT -> height of the canvas.
        """
        if self.position.x < self.h:
            self.position.x = self.h
        if self.position.x > WIDTH - self.h:
            self.position.x = WIDTH - self.h
        if self.position.y < self.h:
            self.position.y = self.h
        if self.position.y > HEIGHT - self.h:
            self.position.y = HEIGHT - self.h
        
    def hit(self):
        """
        Spaceship gets hit by an asteroid, update all the meaningful variables.
        """
        self.lifes -= 1
        self.is_invulnerable = True
        self.start_invulnerability_timer = time.time()

    def invulnerability_timer(self):
        """
        Checks whether the spaceship is still invulnerable or not.
        """
        if self.is_invulnerable:
            passed_time = time.time() - self.start_invulnerability_timer
            if passed_time > self.invulnerability_seconds:
                self.is_invulnerable = False
                self.start_invulnerability_timer = -1

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

    def modify_rect_pos(self, offset_x, offset_y):
        """
        Modify the rect position.
        Used in the shake_screen method after getting hit.
        """
        self.rect = pygame.Rect(self.position.x + offset_x, self.position.y + offset_y, self.w, self.h)

class Asteroid():
    
    def __init__(self, x: int, y: int, w: int, h: int, color: tuple,
                velocity = None, angle_position = 0, angle_velocity = 0):
                
        self.color = color
        self.w = w
        self.h = h
        self.rect = pygame.Rect(x, y, w, h)

        self.position = pygame.Vector2(x, y)
        self.velocity = velocity if velocity is not None else pygame.Vector2(0, 0)

        self.angle_position = angle_position
        self.angle_velocity = angle_velocity

        self.is_in_bounds = False
        self.kill = False

    def update_position(self):
        """
        Updates the position of the mover, used after a force is applied via apply_force().
        The update takes into account also angle acceleration (rotation of the object).
        """
        self.position += self.velocity
        self.rect = pygame.Rect(self.position.x, self.position.y, self.w, self.h)
        
        self.angle_position += math.degrees(self.angle_velocity)
        self.angle_position %= 360

    def in_bounds(self, WIDTH: int, HEIGHT: int):
        """
        Checks if the asteroid is in the bounds of the canvas.
        It is useful to handle the termination of the asteroid, i.e. falls out of the canvas.
        Since the asteroid spawns out of the canvas we need to check that it enters it before dying.

        Args:
            - WIDTH -> width of the canvas
            - HEIGHT -> height of the canvas

        """
        in_canvas = False
        if self.position.x >= 0 and self.position.x <= WIDTH and self.position.y >= 0 and self.position.y <= HEIGHT:
            in_canvas = True

        if in_canvas and not self.is_in_bounds:
            self.is_in_bounds = True

        if not in_canvas and self.is_in_bounds:
            self.kill = True

    def check_death(self):
        """
        Checks if the asteroid is to be killed or not.
        Returns a boolean to handle it's death state.
        """
        return self.kill
    
    def check_collision(self, spaceship_rect):
        """
        Checks if the asteroid collided with the rect or not.

        Args:
            - spaceship_rect -> the rect containing the spaceship

        Returns a boolean
        """
        
        if self.rect.colliderect(spaceship_rect):
            self.kill = True
            return True

        return False

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

    def explode(self):
        """
        Animation to make the asteroid explode.
        Need to be used after an impact with the spaceship
        """
        return
    
    def modify_rect_pos(self, offset_x, offset_y):
        """
        Modify the rect position.
        Used in the shake_screen method after getting hit.
        """
        self.rect = pygame.Rect(self.position.x + offset_x, self.position.y + offset_y, self.w, self.h)
   
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

class Pendulum():
    def __init__(self, x, y, r, angle, angle_velocity, angle_acceleration, bob_radius = 5):
        """
        The pendulum object is composed of a pivot and a bob, the bob position is 
        """
        self.r = r
        self.angle = angle
        self.pivot_position = pygame.Vector2(x, y)
        self.bob_position = pygame.Vector2(x + (r * math.sin(math.radians(angle))), y + (r * math.cos(math.radians(angle))))
        self.bob_radius = bob_radius
        self.angle_velocity = angle_velocity
        self.angle_acceleration = angle_acceleration
        self.damping = 0.999


    def update(self, gravity):  
        """
        Updates position of the bob using gravity and the tension
        """
        self.angle_acceleration = - 1 * gravity.magnitude() * math.sin(math.radians(self.angle)) / self.r
        self.angle_velocity += self.angle_acceleration
        self.angle += self.angle_velocity
        self.angle_velocity *= self.damping
        self.bob_position = pygame.Vector2(self.pivot_position.x + (self.r * math.sin(math.radians(self.angle))),
                                            self.pivot_position.y + (self.r * math.cos(math.radians(self.angle))))

    def draw(self, screen):
        pygame.draw.line(screen, (255, 255, 255), self.pivot_position, self.bob_position)
        pygame.draw.circle(screen, (60, 200, 200), self.bob_position, self.bob_radius + 3)
        pygame.draw.circle(screen, (200, 200, 200), self.bob_position, self.bob_radius)


class DoublePendulum:
    def __init__(self, x, y, r, angle1, angle2, v1=0, v2=0, bob_radius=5):

        self.origin = pygame.Vector2(x, y)
        self.r = r  
        self.m = 1 

        # Angles and angular velocities/accelerations (in radians)
        self.theta1 = math.radians(angle1)
        self.theta2 = math.radians(angle2)
        self.v1 = v1
        self.v2 = v2
        self.a1 = 0
        self.a2 = 0

        self.bob_radius = bob_radius
        self.damping = 0.999  # Friction

        # Position of bobs
        self.bob1 = pygame.Vector2()
        self.bob2 = pygame.Vector2()

        self.MAX_VELOCITY = 50

        self.trails = []

    def update_positions(self):
        """Update bob positions based on current angles"""
        x1 = self.origin.x + self.r * math.sin(self.theta1)
        y1 = self.origin.y + self.r * math.cos(self.theta1)

        x2 = x1 + self.r * math.sin(self.theta2)
        y2 = y1 + self.r * math.cos(self.theta2)

        self.bob1 = pygame.Vector2(x1, y1)
        self.bob2 = pygame.Vector2(x2, y2)

        if len(self.trails) > 1500:
            self.trails.pop(0)
        self.trails.append(self.bob2)

    def update(self, gravity):
        """
        Update pendulum motion using real physics,
        i'm no physicist this equations are copied lol
        """
        g = gravity.magnitude()

        # Intermediate values to simplify the expression
        sin1 = math.sin(self.theta1)
        sin2 = math.sin(self.theta2)
        cos1 = math.cos(self.theta1)
        sin12 = math.sin(self.theta1 - self.theta2)
        cos12 = math.cos(self.theta1 - self.theta2)

        # Equations for angular acceleration (assuming m1 = m2, r1 = r2)
        num1 = -g * (2 * sin1 + sin2)
        num2 = -self.v2 ** 2 * self.r * sin12
        num3 = -self.v1 ** 2 * self.r * sin12 * cos12
        denom = self.r * (2 - math.cos(2 * (self.theta1 - self.theta2)))

        self.a1 = (num1 + num2 + num3) / denom

        num1 = 2 * sin12
        num2 = self.v1 ** 2 * self.r + g * cos1 + self.v2 ** 2 * self.r * cos12
        self.a2 = num1 * num2 / denom

        # Update velocities and angles
        self.v1 += self.a1
        self.v2 += self.a2
        self.v1 = max(min(self.v1, self.MAX_VELOCITY), -self.MAX_VELOCITY)
        self.v2 = max(min(self.v2, self.MAX_VELOCITY), -self.MAX_VELOCITY)
        self.v1 *= self.damping
        self.v2 *= self.damping
        self.theta1 += self.v1
        self.theta2 += self.v2

        # Update bob positions
        self.update_positions()

    def draw(self, screen):
        # Draw arms
        pygame.draw.line(screen, (255, 255, 255), self.origin, self.bob1, 2)
        pygame.draw.line(screen, (255, 255, 255), self.bob1, self.bob2, 2)

        # Draw bobs
        pygame.draw.circle(screen, (60, 200, 200), self.bob1, self.bob_radius + 2)
        pygame.draw.circle(screen, (200, 200, 200), self.bob1, self.bob_radius)
        pygame.draw.circle(screen, (60, 200, 200), self.bob2, self.bob_radius + 2)
        pygame.draw.circle(screen, (200, 200, 200), self.bob2, self.bob_radius)

        for trail in self.trails:
            pygame.draw.rect(screen, (200, 0, 0), pygame.Rect(trail.x, trail.y, 1, 1))