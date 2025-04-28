import pygame
import math
import random
from perlin_noise import PerlinNoise

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

    def seek_segment(self, segment):
        """
        
        """
        # take direction of the segment and normalize it
        direction = segment.direction.copy()
        direction.normalize_ip()

        future = self.velocity.copy()
        # scale velocity to arbitrary value, i.e. future
        future.scale_to_length(25)
        # move curr position to the future
        future += self.position
        # compute the vector from the start to the segment to the future
        a = future - segment.start_pos

        # compute dot product between a vector and direction
        # in this way we get the position of our normal point
        direction_projection_length = a.dot(direction)
        direction.scale_to_length(direction_projection_length)
        
        # compute the normal
        normal_point = segment.start_pos + direction
        segment_length = segment.direction.length()
        
        if direction_projection_length < 0:
            normal_point = segment.start_pos
        elif direction_projection_length > segment_length:
            normal_point = segment.end_pos

        self.seek(normal_point)
        return normal_point

    def seek(self, target_pos):
        """
        The vehicle seeks the target, implementing a steering force.

        Args:
            - target_pos: the target object position
        """
        
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

    def follow(self, flow):
        """
        follows the flow field.
        """
        desired = flow.lookup(self.position)
        # out of the flow field
        if not desired:
            return
        desired *= self.max_speed
        steer = desired - self.velocity
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
        return pygame.Vector2(final_x, final_y)

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

class FlowField():
    def __init__(self, WIDTH: int, HEIGHT: int, cell_size: int, mode: int):
        # mode 0 random, 1 perlin, 2 circular, 3 points to the center 
        self.cell_size = cell_size
        self.rows = HEIGHT // cell_size
        self.cols = WIDTH // cell_size
        self.center = pygame.Vector2(WIDTH//2, HEIGHT//2)
        self.array = []
        self.mode = mode
        self.initialize_array()

    def initialize_array(self):
        if self.mode == 0:
            self.array = [[pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)) for _ in range(self.cols)] for _ in range(self.rows)]
        elif self.mode == 1:
            noise_gen = PerlinNoise(octaves=4)
            scale = 0.1
            self.array = []

            for row in range(self.rows):
                curr_row = []
                for col in range(self.cols):
                    # Genera perlin noise in [0,1], then scale it to [0, 2π]
                    noise_val = noise_gen([col * scale, row * scale])
                    angle = noise_val * math.tau  # 0 to 2π

                    vec = pygame.Vector2(math.cos(angle), math.sin(angle))
                    curr_row.append(vec)
                self.array.append(curr_row)
        elif self.mode == 2:
            for i in range(self.rows):
                curr_arr = []
                for j in range(self.cols):
                    point_x = j * self.cell_size + self.cell_size // 2
                    point_y = i * self.cell_size + self.cell_size // 2
                    angle = math.atan2(self.center.y - point_y, self.center.x - point_x)
                    angle = math.radians(math.degrees(angle)+90)
                    curr_arr.append(pygame.Vector2(math.cos(angle), math.sin(angle)))
                self.array.append(curr_arr) 
        else:
            for i in range(self.rows):
                curr_arr = []
                for j in range(self.cols):
                    point_x = j * self.cell_size + self.cell_size // 2
                    point_y = i * self.cell_size + self.cell_size // 2
                    angle = math.atan2(self.center.y - point_y, self.center.x - point_x)
                    curr_arr.append(pygame.Vector2(math.cos(angle), math.sin(angle)))
                self.array.append(curr_arr) 
 

    def draw(self, screen):
        for row in range(len(self.array)):
            for col in range(len(self.array[0])):
                vector = self.array[row][col]
                angle = math.atan2(vector[1], vector[0])  # Already in radians

                # Center of the cell
                point_x = col * self.cell_size + self.cell_size // 2
                point_y = row * self.cell_size + self.cell_size // 2

                # Offset in the direction of the vector
                offset_length = self.cell_size // 2 - 2  # So the arrow stays inside the cell
                offset_x = math.cos(angle) * offset_length
                offset_y = math.sin(angle) * offset_length

                # Draw line in the direction of the flow
                pygame.draw.line(screen, (255, 255, 255), (point_x - offset_x, point_y - offset_y), (point_x + offset_x, point_y + offset_y), 3)
                pygame.draw.circle(screen, (255, 255, 255), (point_x + offset_x, point_y + offset_y), 3)
    
    def lookup(self, position):
        """
        Searches for the position of the rect is in the flow field right now.

        Args:
            - position: vector of the position of the vehicle

        Returns the force applied by the flow field in that cell.
        """
        col = int(position.x // self.cell_size)
        row = int(position.y // self.cell_size)

        if row > 0 and row < self.rows and col > 0 and col < self.cols:
            return self.array[row][col].copy() 
        return None