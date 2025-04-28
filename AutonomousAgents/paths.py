import pygame
import random

def define_path(num_segments, radius, WIDTH, HEIGHT):

    segments = []
    offset = WIDTH / num_segments
    end_x, end_y = -1, -1

    for i in range(num_segments):
        if end_x != -1 and end_y != -1:
            start_x = end_x
            start_y = end_y
        else:
            start_x = i*offset
            start_y = random.randint(0, HEIGHT)
        end_x = (i+1)*offset
        end_y = max(50, min(HEIGHT - 50, random.randint(start_y - 20, start_y + 20))) 

        segment = Segment(start_x, start_y, end_x, end_y, radius=radius)
        segments.append(segment)
    
    return segments

class Segment():
    def __init__(self, start_x: int, start_y: int, end_x: int, end_y: int,  polygon_points: list = None, radius: int = 10):
        self.start_pos = pygame.Vector2(start_x, start_y)
        self.end_pos = pygame.Vector2(end_x, end_y)
        self.direction = self.end_pos - self.start_pos

        if polygon_points:
            self.polygon_points = polygon_points
        else:
            normal = pygame.Vector2(-self.direction.y, self.direction.x).normalize()
            offset = normal * radius
            self.polygon_points = [
                self.start_pos + offset,
                self.end_pos + offset,
                self.end_pos - offset,
                self.start_pos - offset
            ]
        
    def contains_point(self, point: pygame.Vector2) -> bool:
        """
        I'm just gonna believe this works for now
        """
        def sign(p1, p2, p3):
            return (p1.x - p3.x) * (p2.y - p3.y) - (p2.x - p3.x) * (p1.y - p3.y)

        b1 = sign(point, self.polygon_points[0], self.polygon_points[1]) < 0.0
        b2 = sign(point, self.polygon_points[1], self.polygon_points[2]) < 0.0
        b3 = sign(point, self.polygon_points[2], self.polygon_points[3]) < 0.0
        b4 = sign(point, self.polygon_points[3], self.polygon_points[0]) < 0.0

        return (b1 == b2 == b3 == b4)

    def draw_polygon(self, screen):
        pygame.draw.polygon(screen, (100, 100, 255), self.polygon_points)

    def draw_line(self, screen):
        pygame.draw.line(screen, (255, 255, 255), self.start_pos, self.end_pos, 2)

class Path():
    def __init__(self, segments: Segment):
        self.segments = segments
        self.intra_segments = []
        self.define_intra_segments()
    
    def define_intra_segments(self):
        for i in range(len(self.segments) - 1):
            polygon_points = [self.segments[i].polygon_points[1], self.segments[i+1].polygon_points[0], self.segments[i].polygon_points[2],self.segments[i+1].polygon_points[3]]
            self.intra_segments.append(Segment(self.segments[i].end_pos[0], self.segments[i].end_pos[1], 
                                               self.segments[i].end_pos[0], self.segments[i].end_pos[1], polygon_points=polygon_points))

    def is_rectangle_contained(self, point):
        """
        Checks if a rectangle (its center) lies inside any of the segments.
        If not, returns the nearest segment based on distance to the polygon.
        """
        closest_segment = None
        closest_distance = float('inf')

        for segment in self.segments:
            if segment.contains_point(point):
                return True, segment

            # If not inside, calculate the minimum distance to the polygon
            # but only the polygons after the rect current position, to simulate
            # a car following a path
            for polygon_point in segment.polygon_points:
                if segment.start_pos.x > point.x:
                    dist = (point - polygon_point).length()
                    if dist < closest_distance:
                        closest_distance = dist
                        closest_segment = segment

        return False, closest_segment

    def draw(self, screen):
        for segment in self.segments + self.intra_segments:
            segment.draw_polygon(screen)
        
        for segment in self.segments:
            segment.draw_line(screen)

