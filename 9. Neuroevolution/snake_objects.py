import pygame
import random
from brains import SnakeBrain
import torch
import math

move_map = {
    0: 'A',
    1: 'W',
    2: 'D',
    3: 'S'
}

dir_map = {
    "A": 0.0, 
    "W": 0.25, 
    "D": 0.5, 
    "S": 0.75,
    "": 0.0
}

class Grid():
    def __init__(self, WIDTH, HEIGHT, DIM):
        self.rows = WIDTH // DIM
        self.cols = HEIGHT // DIM
        self.dim = DIM
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.food_position = ()

    def update_grid(self, head_position, last_position,  eaten = False):
        """
        Update grid values, last position is removed only if no food has been encountered
        """
        self.grid[head_position[0]][head_position[1]] = 'S'
        if not eaten:
            self.grid[last_position[0]][last_position[1]] = 0

    def add_food(self):
        rand_x, rand_y = random.randint(0, self.rows - 1), random.randint(0, self.cols - 1)
        while self.grid[rand_x][rand_y] == 'S':
            rand_x, rand_y = random.randint(0, self.rows - 1), random.randint(0, self.cols - 1)
        
        self.grid[rand_x][rand_y] = 'F'
        self.food_position = (rand_x, rand_y)

    def draw(self, screen):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                if self.grid[i][j] == 'S': 
                    pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(i*self.dim, j*self.dim, self.dim, self.dim))
                elif self.grid[i][j] == 'F':
                    pygame.draw.rect(screen, (200, 100, 0), pygame.Rect(i*self.dim, j*self.dim, self.dim, self.dim))

class Snake():
    def __init__(self, start_x, start_y, grid, brain=None):
        self.x = start_x
        self.y = start_y
        self.positions = [(start_x, start_y)]
        self.last_position = (start_x, start_y)
        self.grid = grid
        if brain:
            self.brain = brain
        else:
            self.brain = SnakeBrain()
            self.mutate(mutation_rate=1.0, mutation_strength=1.0)
        self.fitness = 0
        self.is_alive = True
        self.same_move_counter = 0
        self.steps_since_food = 0

    def think(self, last_direction):
        """
        Thinking next move, inputs are:
        - position of snakes head (x, y)
        - position of food (x, y)
        - distance from food (x, y)
        - last direction the snake is following (A: 0, W:0.25, D: 0.5, S: 0.75)
        
        Returns the next direction:
        -> 0: A, 1: W, 2: D, 3: S
        """

        rows, cols = len(self.grid.grid), len(self.grid.grid[0])
        food_x, food_y = self.grid.food_position
        head_x, head_y = self.positions[0]
        inputs = torch.tensor([
            head_x / cols,
            head_y / rows,
            food_x / cols,
            food_y / rows,
            head_x - food_x / cols,
            head_y - food_y / rows,
            math.sqrt( ((food_x - head_x) / cols)**2 + ((food_y - head_y) / rows)**2 ),
            dir_map[last_direction]
            ], dtype=torch.float32)

        with torch.no_grad():
            output = self.brain(inputs)

        item_num = torch.argmax(output).item()

        return item_num

    def crossover(self, brain2: SnakeBrain, start_x, start_y, WIDTH, HEIGHT, DIM):
        """
        Child is created as a crossover between two parents.
        """
        brain1_parameters = list(self.brain.parameters())
        brain2_parameters = list(brain2.parameters())

        child_brain = SnakeBrain()
        for p_child, p1, p2 in zip(child_brain.parameters(), brain1_parameters, brain2_parameters):
            mask = torch.rand_like(p1) > 0.5
            p_child.data.copy_(torch.where(mask, p1.data, p2.data))
        child = Snake(start_x, start_y, Grid(WIDTH, HEIGHT, DIM), child_brain)
        return child

    def mutate(self, mutation_rate = 0.4, mutation_strength = 0.3):
        for param in self.brain.parameters():
            if len(param.shape) == 2:  # matrices
                mask = torch.rand_like(param) < mutation_rate
                noise = torch.randn_like(param) * mutation_strength
                param.data += mask * noise
            else:  # bias 
                mask = torch.rand_like(param) < mutation_rate
                noise = torch.randn_like(param) * mutation_strength
                param.data += mask * noise

    def move(self, command):
        """
        Update all positions of the array
        """
        self.last_position = self.positions[-1]
        for i in range(len(self.positions)-1, 0, -1):
            self.positions[i] = self.positions[i-1]

        x, y = self.positions[0]
        if command == "W":
            if y-1 < 0:
                y = self.grid.cols
            self.positions[0] = (x, y-1)
        elif command == "A":
            if x-1 < 0:
                x = self.grid.rows
            self.positions[0] = (x-1, y)
        elif command == "S":
            if y+1 > self.grid.cols-1:
                y = -1
            self.positions[0] = (x, y+1)
        else:
            if x+1 > self.grid.rows-1:
                x = -1
            self.positions[0] = (x+1, y)

    def snake_growth(self):
        """
        Snake has eaten something, it grows larger.
        """
        self.positions.append(self.last_position)

    def eat(self):
        """
        Check if snake is eating or not.
        """
        head_position = self.positions[0]
        if self.grid.grid[head_position[0]][head_position[1]] == 'F':
            self.snake_growth()
            return True
        return False

    def check_hit(self):
        """
        This check is done after we moved every position in the array but
        before we updated this values in the matrix.

        If is_alive is set to False then it's game over.
        """
        head_position = self.positions[0]
        if self.grid.grid[head_position[0]][head_position[1]] == 'S':
            self.is_alive = False

class SnakePopulation():
    def __init__(self, population_size, start_x, start_y, WIDTH, HEIGHT, DIM):
        self.snakes = [Snake(start_x, start_y, Grid(WIDTH, HEIGHT, DIM)) for _ in range(population_size)]
        self.best_fitness = 0
        self.max_steps = 4000
        self.max_steps_no_food = 200
        self.curr_steps = 0

    def check_snakes_are_dead(self):
        for snake in self.snakes:
            if snake.is_alive:
                return False
        return True
    
    def check_illegal_move(self, new_move, last_move):
        if (new_move == 'D' and last_move == 'A') or (new_move == 'A' and last_move == 'D') \
            or (new_move == 'W' and last_move == 'S') or (new_move == 'S' and last_move == 'W'):
            return True
        return False
    
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
            start -= self.snakes[idx].fitness
            idx += 1
        
        idx -= 1
        return self.snakes[idx]
    
    def normalize_fitness(self):
        fitness_sum = 0
        for snakes in self.snakes:
            fitness_sum += snakes.fitness

        if fitness_sum == 0:
            for snakes in self.snakes:
                snakes.fitness = 1.0 / len(self.snakes)
        else:
            for snakes in self.snakes:
                snakes.fitness /= fitness_sum

    def run(self, start_x, start_y, WIDTH, HEIGHT, DIM, last_moves, screen, num_run):
        self.curr_steps += 1
        already_drawn = False
        if self.check_snakes_are_dead() or self.curr_steps > self.max_steps:
            self.curr_steps = 0
            new_snakes = []
            self.normalize_fitness()
            self.snakes.sort(key=lambda b: b.fitness, reverse=True)
            elite = self.snakes[:50]  # keep ten best performing snakes
            new_snakes = elite.copy() 

            best_snake = elite[0]
            if best_snake.fitness > self.best_fitness:
                print(f"New Best fitness! {self.best_fitness}")
                self.best_fitness = best_snake.fitness
                best_snake.brain.save("weights\\best_snake_brain.pth")

            for _ in range(len(self.snakes)-len(new_snakes)):
                parentA = self.weighted_selection()
                parentB = self.weighted_selection()
                child = parentA.crossover(parentB.brain, start_x, start_y, WIDTH, HEIGHT, DIM)
                mutation_rate = max(0.1, 1.0 - (num_run / 300))
                mutation_strength = max(0.05, 0.8 - (num_run / 500))
                child.mutate(mutation_rate=mutation_rate, mutation_strength=mutation_strength)
                child.grid.add_food()
                new_snakes.append(child)
            self.snakes = new_snakes

            return True
        else:
            for i, snake in enumerate(self.snakes):
                if snake.is_alive:
                    new_move = snake.think(last_moves[i])
                    new_direction = move_map[new_move]
                    if last_moves[i] == new_direction:
                        snake.same_move_counter += 1
                    else:
                        snake.same_move_counter = 0
                    
                    if snake.same_move_counter > 30:
                        snake.fitness -= 2
                    if not self.check_illegal_move(new_direction, last_moves[i]):
                        last_moves[i] = new_direction
                    else:
                        snake.fitness -= 5
                    snake.move(last_moves[i])
                    eaten = snake.eat()
                    snake.check_hit()
                    distance_x = abs(snake.positions[0][0] - snake.grid.food_position[0])
                    distance_y = abs(snake.positions[0][1] - snake.grid.food_position[1])
                    distance_to_food = distance_x + distance_y 

                    if eaten:
                        snake.fitness += 100  
                        snake.grid.add_food()
                        snake.steps_since_food = 0
                    else:
                        snake.fitness += -0.1 * distance_to_food  
                        snake.fitness += 0.5  
                        snake.steps_since_food += 1

                    if snake.steps_since_food > self.max_steps_no_food:
                        snake.is_alive = False
                        snake.steps_since_food = 0

                    snake.grid.update_grid(snake.positions[0], snake.last_position, eaten)
                    if not already_drawn:
                        # print(f"NEW DIRECTION: {new_direction}")
                        # print(f"LAST MOVES: {last_moves[i]}")
                        print(f"STEPS: {self.curr_steps}")
                        snake.grid.draw(screen)
                        already_drawn = True
            return False

    def draw(self, screen):
        for snake in self.snakes:
            if snake.is_alive:
                snake.grid.draw(screen)