import random
import pygame
import math

class DNA_string():
    def __init__(self, length, mutation_factor):
        self.length = length
        self.mutation_factor = mutation_factor
        self.genes = []
        for _ in range(length):
            self.genes.append(self.select_random_character())
        self.score = 0

    def get_phrase(self):
        """
        Get string of the phrase
        """
        return ''.join(self.genes)

    def fitness_score(self, target: list):
        """
        Computes a score based on how close to the target we are.

        Args:
            - target: the target object, in this example another sequence of characters
        """
        score = 0
        for i in range(self.length):
            if target[i] == self.genes[i]:
                score += 1
        
        self.score = score / self.length

    def crossover(self, partner):
        """
        Applies crossover to create the child for the next generation.
        The new sentence will be created by using half of both parents sentence.

        Args:
            - partner: has to be another DNA object.

        Returns a new object containing the child
        """
        child = DNA_string(self.length, self.mutation_factor)

        half = self.length // 2
        new_genes = self.genes[:half] + partner.genes[half:]
        child.genes = new_genes

        return child

    def mutate(self):
        """
        Applies mutation, i.e. a character randomly changes
        """
        for i in range(self.length):
            if random.randint(0, 100) < self.mutation_factor:
                self.genes[i] = self.select_random_character()
                break

    def select_random_character(self):
        """
        Return a lower letter character
        """
        rand = random.randint(1, 27)
        if rand == 27:
            return " "
        start = ord('A') - 1
        char = chr(start + rand)
        return char
    
class DNA():
    def __init__(self, lifespan, max_force, mutation_factor = 1):
        self.max_force = max_force
        self.lifespan = lifespan
        self.max_force = max_force
        self.mutation_factor = mutation_factor
        self.genes = []
        for _ in range(lifespan):
            angle = random.uniform(0, 2 * math.pi)
            # avoid bias towards diagonals by taking polar coordinates
            direction = pygame.Vector2(math.cos(angle), math.sin(angle))
            direction.scale_to_length(1)
            direction *= random.uniform(0.1, self.max_force)
            self.genes.append(direction)

    def crossover(self, partner):
        """
        Applies crossover to create the child for the next generation.
        The new genes will be created by using half of both parents genes.

        Args:
            - partner: has to be another DNA object.

        Returns a new object containing the child
        """
        child = DNA(self.lifespan, self.max_force)

        half = self.lifespan // 2
        new_genes = self.genes[:half] + partner.genes[half:]
        child.genes = new_genes

        return child

    def mutate(self):
        """
        Applies mutation, i.e. a gene randomly changes
        """
        for i in range(self.lifespan):
            if random.randint(0, 100) < self.mutation_factor:
                angle = random.uniform(0, 2 * math.pi)
                direction = pygame.Vector2(math.cos(angle), math.sin(angle))
                direction.scale_to_length(1)
                direction *= random.uniform(0.1, self.max_force)
                break
    
class Rocket():
    def __init__(self, x: int, y: int, radius: int, lifespan: int, max_force = 2, mutation_factor = 1, velocity = None, acceleration = None):
        
        self.radius = radius
        self.rect = pygame.Rect(x - radius, y - radius, radius*2, radius*2)
        self.fitness = 0
        self.dna = DNA(lifespan, max_force, mutation_factor)
        self.gene_counter = 0

        # this are all pygame Vectors
        self.position = pygame.Vector2(x, y)
        self.velocity = velocity if velocity is not None else pygame.Vector2(0, 0)
        self.acceleration = acceleration if acceleration is not None else pygame.Vector2(0, 0)

    def apply_force(self, force: pygame.Vector2):
        """
        Applies a force on the Mover object (i.e. gravity), follows Newton's formula F = m x A

        Args:
            - force -> force to be applied
        """
        force_copy = force.copy()
        self.acceleration += force_copy 

    def update(self):
        """
        Updates the position of the mover, used after a force is applied via apply_force().
        """
        self.velocity += self.acceleration
        self.position += self.velocity
        self.acceleration *= 0 
        self.rect.center = self.position

    def compute_fitness(self, target):
        """
        Computes the fitness score for the object. 
        The score is inversely proportional to the distance.

        Args:
            - target: the target to reach
        """
        dist = (target.position - self.position).magnitude()
        self.fitness = 1 / (dist+0.0001)

    def run(self):
        
        self.apply_force(self.dna.genes[self.gene_counter])
        self.gene_counter += 1
        self.update()

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), self.position, self.radius)

class SmarterRocket(Rocket):
    def __init__(self, x: int, y: int, radius: int, lifespan: int, max_force = 2, mutation_factor = 1, velocity = None, acceleration = None):
        super().__init__(x, y, radius, lifespan, max_force, mutation_factor, velocity, acceleration)
        self.hit_obstacle = False
        self.best_distance = 99999
        self.hit_target = False
        self.frames_to_reach_target = 0

    def apply_force(self, force: pygame.Vector2):
        """
        Applies a force on the Mover object (i.e. gravity), follows Newton's formula F = m x A

        Args:
            - force -> force to be applied
        """
        force_copy = force.copy()
        self.acceleration += force_copy 

    def update(self):
        """
        Updates the position of the mover, used after a force is applied via apply_force().
        """
        self.velocity += self.acceleration
        self.position += self.velocity
        self.acceleration *= 0 
        self.rect.center = self.position

    def compute_fitness(self):
        """
        Computes the fitness score for the object. 
        The score is inversely proportional to the distance.

        Args:
            - target: the target to reach
        """
        self.fitness = 1 / (self.best_distance * self.frames_to_reach_target)**2

        if self.hit_target:
            self.fitness *= 2

        if self.hit_obstacle:
            self.fitness *= 0.01

    def check_obstacles(self, obstacles):
        """
        Checks if rocket has hit an obstacle
        """
        for obstacle in obstacles:
            if obstacle.contains(self.rect):
                return True
            
        return False
    
    def check_target(self, target):
        """
        Checks if rocket has hit the target.
        """
        if target.contains(self.rect):
            return True
        return False

    def distance_from_target(self, target):
        """
        Computes distance from target and updates best distance (closest).
        """
        target_pos = pygame.Vector2(target.rect.x, target.rect.y)

        dist = (target_pos - self.position).magnitude()

        if dist < self.best_distance:
            self.best_distance = dist

    def run(self, obstacles, target):
        # if obstacle already hit don't update position anymore
        if not self.hit_obstacle:
            if not self.check_obstacles(obstacles):
                # target related stuff
                if self.check_target(target):
                    self.best_distance = 0.001
                    self.hit_target = True
                else:
                    self.distance_from_target(target)
                self.frames_to_reach_target += 1
                # update as usual
                self.apply_force(self.dna.genes[self.gene_counter])
                self.gene_counter += 1
                self.update()
            else:
                self.hit_obstacle = True

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), self.position, self.radius)


class Population():
    def __init__(self, population_len, start_x, start_y, lifespan, mutation_factor, target):
        self.start_x = start_x
        self.start_y = start_y
        self.lifespan = lifespan
        self.target = target
        self.mutation_factor = mutation_factor
        self.population = []
        for _ in range(population_len):
            self.population.append(Rocket(start_x, start_y, 3, lifespan, 1.5, mutation_factor=mutation_factor))

    def fitness(self):
        """
        Computes fitness score.
        """
        for rocket in self.population:
            rocket.compute_fitness(self.target)

    def normalize_fitness(self):
        """
        Normalizes fitness score.
        """
        total_fitness = 0
        for rocket in self.population:
            total_fitness += rocket.fitness
        
        for rocket in self.population:
            rocket.fitness /= total_fitness

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
            start -= self.population[idx].fitness
            idx += 1
        
        idx -= 1
        return self.population[idx].dna

    def reproduction(self):
        """
        Function to create the new spawn of rockets.
        """
        new_population = []
        for i in range(len(self.population)):
            parentA = self.weighted_selection()
            parentB = self.weighted_selection()
            child = parentA.crossover(parentB)
            child.mutate()
            new_rocket = Rocket(self.start_x, self.start_y, 3, self.lifespan, 1.5, mutation_factor=self.mutation_factor)
            new_rocket.dna = child
            new_population.append(new_rocket)

        self.population = new_population

    def live(self):
        for rocket in self.population:
            rocket.run()

    def draw(self, screen):
        for rocket in self.population:
            rocket.draw(screen)


class SmartPopulation(Population):
    def __init__(self, population_len, start_x, start_y, lifespan, mutation_factor, target, obstacles):
        self.start_x = start_x
        self.start_y = start_y
        self.lifespan = lifespan
        self.target = target
        self.mutation_factor = mutation_factor
        self.population = []
        for _ in range(population_len):
            self.population.append(SmarterRocket(start_x, start_y, 3, lifespan, 1.5, mutation_factor=mutation_factor))
        self.obstacles = obstacles

    def reproduction(self):
        """
        Function to create the new spawn of rockets.
        """
        new_population = []
        for i in range(len(self.population)):
            parentA = self.weighted_selection()
            parentB = self.weighted_selection()
            child = parentA.crossover(parentB)
            child.mutate()
            new_rocket = SmarterRocket(self.start_x, self.start_y, 3, self.lifespan, 1.5, mutation_factor=self.mutation_factor)
            new_rocket.dna = child
            new_population.append(new_rocket)

        self.population = new_population

    def fitness(self):
        """
        Computes fitness score.
        """
        for rocket in self.population:
            rocket.compute_fitness()

    def live(self):
        for rocket in self.population:
            rocket.run(self.obstacles, self.target)

    def draw(self, screen):
        for rocket in self.population:
            rocket.draw(screen)


class Target:
    def __init__(self, x, y, radius):
        self.position = pygame.Vector2(x, y)
        self.radius = radius

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), self.position, self.radius)


class Obstacle():
    def __init__(self, x, y, w, h, c):
        self.rect = pygame.Rect((x,y,w,h))
        self.color = c

    def contains(self, rect):
        if self.rect.colliderect(rect):
            return True
        return False
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
    