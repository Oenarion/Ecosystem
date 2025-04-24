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
        end_y = random.randint(0, HEIGHT) 

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

    def draw(self, screen):
        for segment in self.segments + self.intra_segments:
            segment.draw_polygon(screen)
        
        for segment in self.segments:
            segment.draw_line(screen)

