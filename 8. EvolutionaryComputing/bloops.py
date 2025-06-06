import pygame
import random
import math
from perlin_noise import PerlinNoise

class DNA():
    def __init__(self, mutation_factor = 1):
        self.gene = random.uniform(0, 1)
        self.mutation_factor = mutation_factor

    def mutate(self):
        """
        Applies mutation, i.e. a gene randomly changes
        """
        if random.randint(0, 100) < self.mutation_factor:
            self.gene = random.uniform(0, 1)

    def copy(self):
        dna = DNA()
        dna.gene = self.gene
        return dna

class Bloop():
    def __init__(self, pos: tuple, dna: DNA):
        self.dna = dna
        self.dim = (self.dna.gene * 20) + 10
        self.speed = (10 - 10*self.dna.gene) + 3
        self.health = 100
        self.pos = pygame.Vector2(pos)
        self.rect = pygame.Rect(pos[0], pos[1], self.dim, self.dim)

        # Perlin noise generator
        self.noise_x = PerlinNoise(octaves=1)
        self.noise_y = PerlinNoise(octaves=1)

        # Offset per il tempo
        self.xoff = random.uniform(0, 1000)
        self.yoff = random.uniform(0, 1000)
        self.noise_step = 0.01

    def move(self):
        # Perlin values between -1 and 1
        dx = self.noise_x(self.xoff)
        dy = self.noise_y(self.yoff)  
        
        # Remap the values
        move_x = dx * self.speed
        move_y = dy * self.speed

        self.pos += pygame.Vector2(move_x, move_y)
        self.rect.center = self.pos
        
        # Update noise
        self.xoff += self.noise_step
        self.yoff += self.noise_step

    def reproduce(self):
        child_DNA = self.dna.copy()
        child_DNA.mutate()
        bloop = Bloop(self.pos.copy(), child_DNA)
        return bloop


    def update(self, foods):
        self.move()
        self.eat(foods)
        self.health -= 0.2

    def eat(self, foods):
        i = 0
        while i < len(foods.pos_array):
            if self.rect.colliderect(foods.rect_array[i]):
                self.health += min(100, self.health + 50)
                foods.pos_array.pop(i)
                foods.rect_array.pop(i)
            else:
                i += 1

    def is_dead(self):
        return self.health <= 0
    
    def run(self, foods):
        self.update(foods)
        return self.is_dead()
    
    def draw(self, screen):
        pygame.draw.circle(screen, (128, 128, 128), self.pos, int(self.dim/2), width=1)

class Food():
    def __init__(self, num_food, WIDTH, HEIGHT):
        self.pos_array = []
        self.rect_array = []
        self.w_screen = WIDTH
        self.h_screen = HEIGHT
        
        for _ in range(num_food):
            self.pos_array.append((random.randint(0, WIDTH), random.randint(0, HEIGHT)))
            self.rect_array.append((pygame.Rect(self.pos_array[-1][0], self.pos_array[-1][1], 10, 10)))

    def run(self, screen):
        if random.randint(1, 500) < 10:
            self.pos_array.append((random.randint(0, self.w_screen), random.randint(0, self.h_screen))) 
            self.rect_array.append((pygame.Rect(self.pos_array[-1][0], self.pos_array[-1][1], 10, 10)))

        self.draw(screen)

    def draw(self, screen):
        for rect in self.rect_array:
            pygame.draw.rect(screen, (255, 100, 0), rect)

class World():
    def __init__(self, num_bloops, WIDTH, HEIGHT, num_food):
        self.bloops = []
        for _ in range(num_bloops):
            dna = DNA()
            pos = (random.randint(0, WIDTH), random.randint(0, HEIGHT))
            self.bloops.append(Bloop(pos, dna))

        self.food = Food(num_food, WIDTH, HEIGHT)


    def run(self, screen):
        i = 0

        while i < len(self.bloops):
            is_dead = self.bloops[i].run(self.food)
            if is_dead:
                self.bloops.pop(i)
            else:
                if random.randint(1, 2000) == 1:
                    new_bloop = self.bloops[i].reproduce()
                    self.bloops.append(new_bloop)
                self.bloops[i].draw(screen)
                i += 1
            

        self.food.run(screen)