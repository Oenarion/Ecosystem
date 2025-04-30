import pygame
import math
import random
from perlin_noise import PerlinNoise

class Vehicle():
    def __init__(self, x: int, y: int, dim:int, color: tuple,velocity = None, acceleration = None, max_speed = 8, max_force = 0.4):

        self.rect = pygame.Rect(x, y, dim, dim)
        self.color = color
        self.position = pygame.Vector2(x, y)
        self.velocity = velocity if velocity is not None else pygame.Vector2(0, 0)
        self.acceleration = acceleration if acceleration is not None else pygame.Vector2(0, 0)
        self.max_speed = max_speed
        self.max_force = max_force
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

    def out_of_x_bounds(self, WIDTH):
        """
        checks if vehicle is out of bounds on the x axis
        """
        if self.position.x + self.rect.width > WIDTH or self.position.x < 0:
            return True

        return False

    def separate(self, vehicles):
        """
        Separate each vehicle from the others by taking the avg diff vector
        of the vehicle in a certain radius.

        Args:
            - vehicles: array of the other vehicles
        """
        # bigger vehicle, bigger radius
        separation_distance = self.rect.width * 2
        count = 0
        sum_vector = pygame.Vector2(0,0)

        for vehicle in vehicles:
            distance = self.position.distance_to(vehicle.position)
            if vehicle.rect != self.rect and distance < separation_distance:
                diff_vector = self.position.copy() - vehicle.position.copy()
                # the closer the faster the escape velocity
                diff_vector.scale_to_length(1 / distance)
                
                sum_vector += diff_vector
                count += 1
        if count > 0:
            sum_vector.scale_to_length(self.max_speed)
            steer = sum_vector - self.velocity
            steer.scale_to_length(self.max_force)
            self.apply_force(steer)

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
    

class Boid():
    def __init__(self, x: int, y: int, radius: int, color: tuple, separation_distance: int, id_boid: int, mass:int = 1, velocity = None, acceleration = None, max_speed = 3, max_force = 0.2):
        self.position = pygame.Vector2(x, y)
        self.radius = radius
        self.color = color
        self.mass = mass
        self.separation_distance = separation_distance
        self.id_boid = id_boid
        self.velocity = velocity if velocity is not None else pygame.Vector2(0,0)
        self.acceleration = acceleration if acceleration is not None else pygame.Vector2(0,0)
        self.max_speed = max_speed
        self.max_force = max_force
        self.fov_points = ()
        self.mode = 1
        self.show_fov = False

    def fov(self):
        fov_vector = self.velocity.copy()
        fov_vector.scale_to_length(50)
        fov_vector_pos = self.position + fov_vector
        fov_oblique_pos_1 = fov_vector.rotate(45) + self.position
        fov_oblique_pos_2 = fov_vector.rotate(-45) + self.position
        fov_points = (self.position, fov_oblique_pos_1, fov_vector_pos, fov_oblique_pos_2)
        self.fov_points = fov_points

    def contains_point(self, point: pygame.Vector2) -> bool:
        """
        I'm just gonna believe this works for now.

        Checks if another boid is inside the field of view.
        """
        def sign(p1, p2, p3):
            return (p1.x - p3.x) * (p2.y - p3.y) - (p2.x - p3.x) * (p1.y - p3.y)

        b1 = sign(point, self.fov_points[0], self.fov_points[1]) < 0.0
        b2 = sign(point, self.fov_points[1], self.fov_points[2]) < 0.0
        b3 = sign(point, self.fov_points[2], self.fov_points[3]) < 0.0
        b4 = sign(point, self.fov_points[3], self.fov_points[0]) < 0.0

        return (b1 == b2 == b3 == b4)
    
    def apply_force(self, force: pygame.Vector2):
        """
        Applies a force on the object (i.e. gravity), follows Newton's formula F = m x A

        Args:
            - force -> force to be applied
        """
        force_copy = force.copy()
        f = force_copy / self.mass  
        self.acceleration += f

    def pac_man_effect(self, WIDTH, HEIGHT):
        """
        Let the boid spawn on the other side of the canvas once the borders are reached.
        """
        if self.position.x > WIDTH:
            self.position.x = 0
        if self.position.x < 0:
            self.position.x = WIDTH - self.radius
        if self.position.y > HEIGHT:
            self.position.y = 0
        if self.position.y < 0:
            self.position.y = HEIGHT - self.radius

    def separate(self, boids):
        """
        Separate each boid from the others by taking the avg diff vector
        of the boid in a certain radius.

        Args:
            - boids: array of the other boids

        Returns steer velocity applying Reynold's formula or 0 if no boid is close enough.
        """
        count = 0
        sum_vector = pygame.Vector2(0,0)

        for boid in boids:
            if boid.id_boid == self.id_boid:
                continue

            distance = self.position.distance_to(boid.position)
            if self.mode == 0:
                if self.contains_point(boid.position):
                    diff_vector = self.position.copy() - boid.position.copy()
                    if diff_vector.length_squared() == 0:
                        # If boids are overlapped, avoids random errors
                        diff_vector = pygame.Vector2(random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5)).normalize() * 0.1
                    # the closer the faster the escape velocity
                    diff_vector.scale_to_length(1 / (distance+0.01))
                    sum_vector += diff_vector
                    count += 1
            else:
                if distance < self.separation_distance:
                    diff_vector = self.position.copy() - boid.position.copy()
                    if diff_vector.length_squared() == 0:
                        # If boids are overlapped, avoids random errors
                        diff_vector = pygame.Vector2(random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5)).normalize() * 0.1
                    # the closer the faster the escape velocity
                    diff_vector.scale_to_length(1 / (distance+0.01))
                    sum_vector += diff_vector
                    count += 1

        if count > 0:
            sum_vector.scale_to_length(self.max_speed)
            steer = sum_vector - self.velocity
            if steer.length_squared() < 1e-5:
                # If steer has length 0
                steer = pygame.Vector2(random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5)).normalize() * 0.1
            steer.scale_to_length(self.max_force)
            return steer 
        else:
            return pygame.Vector2(0, 0)

    def align(self, boids):
        """
        Align the boid to the average velocity of the other boids

        Args:
            - boids: array of the other boids

        Returns steer velocity applying Reynold's formula.
        """
        sum_velocity = pygame.Vector2(0, 0)
        count = 0

        for boid in boids:
            if boid.id_boid == self.id_boid:
                continue
            if self.mode == 0:
                if self.contains_point(boid.position):
                    sum_velocity += boid.velocity
                    count += 1
            else:
                distance = self.position.distance_to(boid.position)
                if distance < self.separation_distance:
                    sum_velocity += boid.velocity
                    count += 1
            

        if count > 0:
            sum_velocity /= count
            if sum_velocity.length_squared() < 1e-5:
                sum_velocity = pygame.Vector2(random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5)).normalize() * 0.1
            sum_velocity.scale_to_length(self.max_speed)
            steer = sum_velocity - self.velocity
            if steer.length_squared() < 1e-5:
                # If steer has length 0
                steer = pygame.Vector2(random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5)).normalize() * 0.1
            steer.scale_to_length(self.max_force)
            return steer
        else:
            return pygame.Vector2(0, 0)
    
    def cohesion(self, boids):
        """
        Align the boid to the average position of the other boids

        Args:
            - boids: array of the other boids

        Returns steer velocity applying Reynold's formula.
        """
        sum_position = pygame.Vector2(0, 0)
        count = 0

        for boid in boids:
            if boid.id_boid == self.id_boid:
                continue

            if self.mode == 0:
                if self.contains_point(boid.position):
                    sum_position += boid.position
                    count += 1
            else:
                distance = self.position.distance_to(boid.position)
                if distance < self.separation_distance:
                    sum_position += boid.position
                    count += 1
                
        if count > 0:
            sum_position /= count
            if sum_position.length_squared() < 1e-5:
                sum_position = pygame.Vector2(random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5)).normalize() * 0.1
            steer = sum_position - self.velocity
            if steer.length_squared() < 1e-5:
                # If steer has length 0
                steer = pygame.Vector2(random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5)).normalize() * 0.1
            steer.scale_to_length(self.max_force)
            return steer
        else:
            return pygame.Vector2(0, 0)

    def update(self):
        """
        Updates position of the object.
        """
        self.velocity += self.acceleration
        
        if self.velocity.magnitude() > self.max_speed:
            self.velocity.normalize_ip()
            self.velocity *= self.max_speed
        
        self.position += self.velocity
        self.acceleration *= 0

    def draw(self, screen):
        if self.show_fov and self.mode == 1:
            pygame.draw.polygon(screen, (255, 0, 0), self.fov_points)
        pygame.draw.circle(screen, (255, 255, 255), self.position, self.radius + 2)
        pygame.draw.circle(screen, self.color, self.position, self.radius)
        