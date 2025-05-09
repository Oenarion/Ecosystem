import pygame
import math

import pygame

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
    def __init__(self, start_pos, end_pos, depth):
        self.lines = []
        self.add_segment(start_pos, end_pos, depth)

    def compute_line_points(self):
        """
        Function used to compute the five points of the koch curve.
        """
        curve = self.end_pos - self.start_pos
        segment = curve / 3

        a = self.start_pos
        b = self.start_pos + segment
        d = self.start_pos + segment * 2
        e = self.end_pos 

        # to compute c
        direction = d - b
        angle = math.radians(-60)
        rotated = pygame.Vector2(
            direction.x * math.cos(angle) - direction.y * math.sin(angle),
            direction.x * math.sin(angle) + direction.y * math.cos(angle)
        )
        
        c = b + rotated

        return [a, b, c, d, e]
    
    def add_segment(self, start_pos, end_pos, depth):
        """
        Funzione ricorsiva che costruisce la Koch curve.
        """
        if depth == 0:
            self.lines.append(Line(start_pos, end_pos))
            return
        
        # Calcola i 5 punti della curva di Koch
        curve = end_pos - start_pos
        segment = curve / 3

        a = start_pos
        b = start_pos + segment
        d = start_pos + segment * 2
        e = end_pos 

        # Calcolo del punto c tramite rotazione
        direction = d - b
        angle = math.radians(-60)
        rotated = pygame.Vector2(
            direction.x * math.cos(angle) - direction.y * math.sin(angle),
            direction.x * math.sin(angle) + direction.y * math.cos(angle)
        )
        c = b + rotated

        # Ricorsione sui 4 sottosegmenti
        self.add_segment(a, b, depth - 1)
        self.add_segment(b, c, depth - 1)
        self.add_segment(c, d, depth - 1)
        self.add_segment(d, e, depth - 1)

    def draw(self, screen):
        for line in self.lines:
            line.draw(screen)


class Line():
    def __init__(self, start_pos, end_pos):
        self.start_pos = start_pos
        self.end_pos = end_pos

    def draw(self, screen):
        pygame.draw.line(screen, (255, 255, 255), self.start_pos, self.end_pos, 2)