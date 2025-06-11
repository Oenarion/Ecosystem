import pygame
import random
from bird_brain import BirdBrain
import torch

class Bird():
    def __init__(self, x, y, brain=None, color=None):
        """
        The bird moves only on the y axis.
        """
        self.x = x
        self.y = y
        self.radius = 7
        self.color = color if color != None else (255, 200, 0)

        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius*2, self.radius*2)

        self.velocity = 0
        self.gravity = 0.5
        self.flap_force = -10

        if brain:
            self.brain = brain
        else:
            self.brain = BirdBrain()

        self.alive = True
        self.fitness = 0

    def think(self, pipes, height, width):
        """
        Runs the neural network to know if the bird has to flap or not.
        Returns the idx of the next pipe to compute collisions afterwards.
        """
        idx = -1
        
        for i, pipe in enumerate(pipes):
            if pipe.top_pipe.x + pipe.top_pipe.w > self.rect.x:
                idx = i
                break
        
        # surpassed the current pipe
        if idx > 0:
            self.fitness += 10

        inputs = torch.tensor([self.y / height,
                  self.velocity / height,
                  pipes[idx].bottom_pipe.y / height,
                  (pipes[idx].bottom_pipe.x + pipes[idx].bottom_pipe.w) / width],
                  dtype=torch.float32)
        
        with torch.no_grad():
            output = self.brain(inputs)

        if torch.argmax(output).item() == 0:
            self.flap()

        return idx

    def crossover(self, brain2: BirdBrain, height):
        """
        Child is created as a crossover between two parents.
        """
        brain1_parameters = list(self.brain.parameters())
        brain2_parameters = list(brain2.parameters())

        child_brain = BirdBrain()
        for p_child, p1, p2 in zip(child_brain.parameters(), brain1_parameters, brain2_parameters):
            mask = torch.rand_like(p1) > 0.5
            p_child.data.copy_(torch.where(mask, p1.data, p2.data))
        child = Bird(self.x, height//2, child_brain)
        return child

    def mutate(self, mutation_rate = 0.1, mutation_strength = 0.2):
        for param in self.brain.parameters():
            if len(param.shape) == 2:  # matrices
                mask = torch.rand_like(param) < mutation_rate
                noise = torch.randn_like(param) * mutation_strength
                param.data += mask * noise
            else:  # bias 
                mask = torch.rand_like(param) < mutation_rate
                noise = torch.randn_like(param) * mutation_strength
                param.data += mask * noise

    def flap(self):
        self.velocity += self.flap_force
        

    def update(self, HEIGHT):
        self.velocity += self.gravity
        self.y += self.velocity

        self.velocity *= 0.95

        if self.y > HEIGHT - self.radius:
            self.y = HEIGHT - self.radius
            self.velocity = 0
        if self.y - self.radius < 0:
            self.y = self.radius

        self.rect.y = self.y - self.radius

        #update fitness function
        self.fitness += 1

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
        pygame.draw.circle(screen, self.color, (self.x + 5, self.y), 3)


class BirdPopulation():
    def __init__(self, num_birds, x, y):
        self.birds = []
        for _ in range(num_birds):
            self.birds.append(Bird(x, y))
        self.best_fitness = 0

    def check_bird_are_dead(self):
        for bird in self.birds:
            if bird.alive:
                return False
        return True
    
    def weighted_selection(self):
        """
        Select the parent for the next child.
        In this case we take a random point from 0 to 1 and progressively remove 
        the fitness score of the current rocket. Since fitness scores are normalized
        in the worst case scenario we will pick the last element.
        """
        start = random.uniform(0, 1)
        idx = 0
        while start > 0:
            start -= self.birds[idx].fitness
            idx += 1
        
        idx -= 1
        return self.birds[idx]

    def normalize_fitness(self):
        fitness_sum = 0
        for bird in self.birds:
            fitness_sum += bird.fitness

        for bird in self.birds:
            bird.fitness /= fitness_sum 

    def run(self, pipes, height, width):
        if self.check_bird_are_dead():
            new_birds = []
            self.normalize_fitness()
            self.birds.sort(key=lambda b: b.fitness, reverse=True)
            elite = self.birds[:10]  # keep ten best performing birds
            new_birds = elite.copy() 

            best_bird = elite[0]
            if best_bird.fitness > self.best_fitness:
                self.best_fitness = best_bird.fitness
                best_bird.brain.save("weights\\best_brain.pth")

            for _ in range(len(self.birds)-len(new_birds)):
                parentA = self.weighted_selection()
                parentB = self.weighted_selection()
                child = parentA.crossover(parentB.brain, height)
                child.mutate()
                new_birds.append(child)
            self.birds = new_birds
            return True
        else:
            for bird in self.birds:
                if bird.alive:
                    idx = bird.think(pipes, height, width)
                    collision, _ = pipes[idx].collision(bird.rect)
                    if collision:
                        bird.alive = False
                        bird.fitness -= 10
                    else:
                        bird.update(height)
            return False

    def draw(self, screen):
        for bird in self.birds:
            if bird.alive:
                bird.draw(screen)

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
        self.velocity = -3

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