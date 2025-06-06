import pygame
import math
import random

class CantorSet():
    def __init__(self, start_pos, end_pos, center, half_len, angle, variation=False):
        self.lines = []  
        self.center = center
        self.half_len = half_len
        self.angle = angle
        self.variation_lines = []
        self.variation = variation
        self.add_segment(start_pos, end_pos)

    def add_segment(self, start_pos, end_pos, line_type=0):
        curve = end_pos - start_pos

        if curve.magnitude() < 1:
            return
        
        segment = curve / 3

        p1 = start_pos
        p2 = start_pos + segment
        p3 = start_pos + segment * 2
        p4 = end_pos

        normal = pygame.Vector2(-segment.y, segment.x)
        normal.scale_to_length(20)

        # Salvo linee base
        self.lines.append(Line(p1, p2))
        self.lines.append(Line(p3, p4))

        if self.variation and curve.magnitude() / 3 >= 1:
            padding = 5
            line_length = 10

            normal_copy = normal.copy()
            normal_copy.normalize_ip()

            seg1 = p2 - p1
            seg2 = p4 - p3

            # Punti 1/6 e 5/6 sui segmenti estremi
            line_points = [
                p1 + seg1 * (1/6),
                p1 + seg1 * (5/6),
                p3 + seg2 * (1/6),
                p3 + seg2 * (5/6)
            ]

            for point in line_points:
                up1 = point + normal_copy * padding
                up2 = point + normal_copy * (padding + line_length)
                down1 = point - normal_copy * padding
                down2 = point - normal_copy * (padding + line_length)
                self.variation_lines.append(("line", up1, up2))
                self.variation_lines.append(("line", down1, down2))
            
            center = (p2 + p3) / 2
            radius = segment.magnitude()
            self.variation_lines.append(("circle", center, radius / 2))
            self.variation_lines.append(("circle", center, radius / 3))
            self.variation_lines.append(("circle", center, radius / 6))

        # Ricorsione
        if line_type == 1 or line_type == 0:
            self.add_segment(p1 + normal, p2 + normal, 1)
            self.add_segment(p3 + normal, p4 + normal, 1)

        if line_type == 2 or line_type == 0:
            self.add_segment(p1 - normal, p2 - normal, 2)
            self.add_segment(p3 - normal, p4 - normal, 2)

    def rotate(self, angle_step):
        self.angle += angle_step
        dir_vec = pygame.Vector2(self.half_len, 0).rotate(self.angle) 
        self.start_pos = self.center - dir_vec
        self.end_pos = self.center + dir_vec
        self.lines = []
        self.variation_lines = []
        self.add_segment(self.start_pos, self.end_pos)

    def draw(self, screen):
        for line in self.lines:
            line.draw(screen)

        for item in self.variation_lines:
            if item[0] == "line":
                pygame.draw.line(screen, (255, 255, 255), item[1], item[2], 2)
            elif item[0] == "circle":
                pygame.draw.circle(screen, (255, 255, 255), item[1], item[2], width=1)

class KochCurve():
    def __init__(self, start_pos, end_pos, depth, rotation_sign = -1):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.depth = depth
        self.rotation_sign = rotation_sign
        self.lines = []
        self.add_segment(start_pos, end_pos, depth)

    
    def add_segment(self, start_pos, end_pos, depth):
        """
        Adds segments to the Koch curve.
        """
        if depth == 0:
            self.lines.append(Line(start_pos, end_pos))
            return
        
        curve = end_pos - start_pos
        segment = curve / 3

        # get the 4 vertices
        a = start_pos
        b = start_pos + segment
        d = start_pos + segment * 2
        e = end_pos 

        #compute the koch "tooth", the fifth vertix
        direction = d - b
        angle = math.radians(self.rotation_sign * 60)
        rotated = pygame.Vector2(
            direction.x * math.cos(angle) - direction.y * math.sin(angle),
            direction.x * math.sin(angle) + direction.y * math.cos(angle)
        )
        c = b + rotated

        # recursion
        self.add_segment(a, b, depth - 1)
        self.add_segment(b, c, depth - 1)
        self.add_segment(c, d, depth - 1)
        self.add_segment(d, e, depth - 1)

    def draw(self, screen):
        for line in self.lines:
            line.draw(screen)

class Line():
    def __init__(self, start_pos, end_pos, width = 2):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.width = width

    def draw(self, screen):
        pygame.draw.line(screen, (255, 255, 255), self.start_pos, self.end_pos, self.width)

class Tree():
    def __init__(self, start_pos: pygame.Vector2, end_pos: pygame.Vector2, decay_rate: float, angle = 5, max_depth = 10, width = 10):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.decay_rate = decay_rate
        self.angle = angle
        self.max_depth = max_depth
        self.width = width
        self.branches = []
        self.generate_tree(start_pos, end_pos, 0, self.width)

    def generate_tree(self, start_pos, end_pos, current_depth, curr_width):
        if current_depth >= self.max_depth:
            return

        self.branches.append(Line(start_pos, end_pos, curr_width))
        curr_width = round(curr_width * 0.7)

        direction = (end_pos - start_pos)
        direction_length = direction.length()
        direction = direction.normalize() * direction_length * self.decay_rate

        rotated_right = direction.rotate(self.angle)
        right_end = end_pos + rotated_right
        self.generate_tree(end_pos, right_end, current_depth + 1, curr_width)

        rotated_left = direction.rotate(-self.angle)
        left_end = end_pos + rotated_left
        self.generate_tree(end_pos, left_end, current_depth + 1, curr_width)

    def draw(self, screen):
        for branch in self.branches:
            branch.draw(screen)
        
class AnimatedLine():
    def __init__(self, start_pos, end_pos, width = 2, percentage = 100):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.width = width
        self.percentage = percentage

    def draw(self, screen):
        current_end = self.start_pos.lerp(self.end_pos, self.percentage)
        pygame.draw.line(screen, (255, 255, 255), self.start_pos, current_end, self.width)

class SlowTree:
    def __init__(self, start_pos: pygame.Vector2, end_pos: pygame.Vector2, decay_rate: float, angle=5, max_depth=10, width=10):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.decay_rate = decay_rate
        self.angle = angle
        self.frames = 20
        self.curr_frame = 0
        self.max_depth = max_depth
        self.width = width
        self.branches = []
        self.to_generate = [(start_pos, end_pos, 0, self.width)]  # Queue of branches to grow

    def update(self):
        """Call this every frame or periodically to grow the tree"""
        if self.to_generate:
            start_pos, end_pos, current_depth, curr_width = self.to_generate.pop(0)
            self.curr_frame += 1
            if current_depth >= self.max_depth:
                return

            if self.curr_frame > 20:
                self.curr_frame = 0
                self.branches.append(Line(start_pos, end_pos, curr_width))
                curr_width = round(curr_width * 0.7)

                direction = (end_pos - start_pos)
                direction_length = direction.length()
                if direction_length == 0:  # Safety check
                    return
                direction = direction.normalize() * direction_length * self.decay_rate

                rotated_right = direction.rotate(self.angle)
                right_end = end_pos + rotated_right
                self.to_generate.append((end_pos, right_end, current_depth + 1, curr_width))

                rotated_left = direction.rotate(-self.angle)
                left_end = end_pos + rotated_left
                self.to_generate.append((end_pos, left_end, current_depth + 1, curr_width))
            else:
                percentage = self.curr_frame / self.frames
                self.branches.append(AnimatedLine(start_pos, end_pos, curr_width, percentage))
                self.to_generate.insert(0, (start_pos, end_pos, current_depth, curr_width))

    def draw(self, screen):
        for branch in self.branches:
            branch.draw(screen)

class RandomTree():
    def __init__(self, start_pos: pygame.Vector2, end_pos: pygame.Vector2, decay_rate: float):
        """
        Yes I know it's not deterministic, I didn't want to create another file just for this class get over it.
        """
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.decay_rate = decay_rate
        self.max_depth = random.randint(3, 10)
        self.branches = []
        self.generate_tree(start_pos, end_pos, 0)

    def generate_tree(self, start_pos, end_pos, current_depth):
        if current_depth >= self.max_depth:
            return

        self.branches.append(Line(start_pos, end_pos))

        direction = (end_pos - start_pos)
        direction_length = direction.length()
        direction = direction.normalize() * direction_length * self.decay_rate

        
        num_of_branches = random.randint(1, 4)

        for _ in range(num_of_branches):
            rotated_branch = direction.rotate(random.randint(-90, 90))
            branch_end = end_pos + rotated_branch
            self.generate_tree(end_pos, branch_end, current_depth + 1)        

    def generate_new_tree(self):
        self.branches = []
        self.generate_tree(self.start_pos, self.end_pos,0)

    def draw(self, screen):
        for branch in self.branches:
            branch.draw(screen)
