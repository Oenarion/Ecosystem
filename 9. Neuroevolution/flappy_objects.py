import pygame
import random

class Bird():
    def __init__(self, x, y):
        """
        The bird moves only on the y axis.
        """
        self.x = x
        self.y = y
        self.radius = 7

        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius*2, self.radius*2)

        self.velocity = 0
        self.gravity = 0.5
        self.flap_force = -10

    def flap(self):
        self.velocity += self.flap_force

    def update(self, HEIGHT):
        self.velocity += self.gravity
        self.y += self.velocity
        self.rect.y = self.y - self.radius

        self.velocity *= 0.95

        if self.y > HEIGHT - self.radius:
            self.y = HEIGHT - self.radius
            self.velocity = 0

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 200, 0), (self.x, self.y), self.radius)


class Pipe():
    def __init__(self, spacing, height, width, id, start_y = None):
        self.height = height
        self.width = width
        self.spacing = spacing
        self.id = id
        self.pipe_dim = 20

        if start_y:
            self.top_pipe_y = start_y
        else:
            self.top_pipe_y = random.randint(50, height - spacing - 50)
        self.bottom_pipe_y = self.top_pipe_y + self.spacing

        self.top_pipe = pygame.Rect((width, 0, self.pipe_dim, self.top_pipe_y))
        self.bottom_pipe = pygame.Rect((width, self.bottom_pipe_y, self.pipe_dim, height))
        self.velocity = -1.5

    def update(self):
        self.top_pipe.x += self.velocity
        self.bottom_pipe.x += self.velocity

    def create_new_pipe(self, id):
        random_dist = random.choice([-1,1]) * random.randint(50, 150)
        new_y = self.top_pipe_y + random_dist
        new_y = min(max(50, new_y), self.height - self.spacing - 50)
        new_pipe = Pipe(self.spacing, self.height, self.width, id, new_y)
        return new_pipe

    def collision(self, rect):
        if self.top_pipe.colliderect(rect) or self.bottom_pipe.colliderect(rect):
            return True, self.id

        return False, -1

    def draw(self, screen):
        pygame.draw.rect(screen, (128, 128, 128), self.top_pipe)
        pygame.draw.rect(screen, (128, 128, 128), self.bottom_pipe)


class PipeGenerator():
    def __init__(self, spacing, height, width, pipe_distance):
        self.pipe_distance = pipe_distance
        self.h = height
        self.w = width
        self.spacing = spacing
        self.pipes = []
        self.global_id = 0
        pipe = Pipe(spacing, height, width, self.global_id)
        self.global_id += 1
        self.pipes.append(pipe)
    
    def update(self):
        if self.w - self.pipes[-1].top_pipe.x > self.pipe_distance:
            self.global_id += 1
            self.pipes.append(self.pipes[-1].create_new_pipe(self.global_id))
        
        for pipe in self.pipes:
            pipe.update()

    def delete_old_pipes(self):
        while len(self.pipes) > 0:
            if self.pipes[0].top_pipe.x + self.pipes[0].pipe_dim < 0:
                self.pipes.pop(0) 
                print("DELETED!")
            else:
                break
    
    def detect_collisions(self, rect):
        for pipe in self.pipes:
            collided, id = pipe.collision(rect)
            if collided:
                return True, id
        return False, -1

    def draw(self, screen):
        for pipe in self.pipes:
            pipe.draw(screen)