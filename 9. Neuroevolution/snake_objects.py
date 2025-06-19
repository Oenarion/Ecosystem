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

    def clear_food(self):
        if self.food_position != ():
            self.grid[self.food_position[0]][self.food_position[1]] = ''


    def add_food(self, snake_positions=None, avoid_row=None):
        """
        snake_positions: list of tuples with all the snake positions [(x1, y1), (x2, y2), ...]
        avoid_row: row to avoid
        """
        while True:
            rand_x = random.randint(0, self.rows - 1)
            rand_y = random.randint(0, self.cols - 1)

            if avoid_row is not None and rand_x == avoid_row:
                continue

            if snake_positions and (rand_x, rand_y) in snake_positions:
                continue

            # Tutto ok, piazza il cibo
            self.grid[rand_x][rand_y] = 'F'
            self.food_position = (rand_x, rand_y)
            break


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
        self.steps_since_food = 500

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
        
        dx = food_x - head_x
        dy = food_y - head_y
        
        # Normalized distances
        dx_norm = dx / rows
        dy_norm = dy / cols
        
        food_left = 1.0 if dx < 0 else 0.0    # food is on the left
        food_right = 1.0 if dx > 0 else 0.0   # food is on the right
        food_up = 1.0 if dy < 0 else 0.0      # food is upwards
        food_down = 1.0 if dy > 0 else 0.0    # food is downwards
        
        # Check collisions with himself
        danger_left = self.check_collision_in_direction(head_x, head_y, 'A')
        danger_up = self.check_collision_in_direction(head_x, head_y, 'W')  
        danger_right = self.check_collision_in_direction(head_x, head_y, 'D')
        danger_down = self.check_collision_in_direction(head_x, head_y, 'S')
        
        inputs = torch.tensor([
            head_x / rows,        # head position
            head_y / cols,
            food_x / rows,        # food position 
            food_y / cols,
            dx_norm,              # distance normalized
            dy_norm,
            food_left,            # binary direction of food
            food_right,
            food_up, 
            food_down,
            danger_left,          # danger in the 4 positions
            danger_up,
            danger_right,
            danger_down,
            len(self.positions) / (rows * cols),  # length snake
            dir_map[last_direction]  # last direction
        ], dtype=torch.float32)

        with torch.no_grad():
            output = self.brain(inputs)
        
        probabilities = torch.softmax(output, dim=0)
        
        if random.random() < 0.9:  # choose best option 90% of the time
            item_num = torch.argmax(output).item()
        else:  # little bit of randomicity 10% of the times
            item_num = torch.multinomial(probabilities, 1).item()
        
        return item_num

    def check_collision_in_direction(self, x, y, direction):
        """
        Check if there's a collision in the next step
        """
        rows, cols = len(self.grid.grid), len(self.grid.grid[0])
        
        if direction == 'A':
            next_x = (x - 1) % rows
            next_y = y
        elif direction == 'W':
            next_x = x
            next_y = (y - 1) % cols
        elif direction == 'D':
            next_x = (x + 1) % rows
            next_y = y
        else:  # 'S'
            next_x = x
            next_y = (y + 1) % cols
    
        return 1.0 if (next_x, next_y) in self.positions else 0.0

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
        self.max_steps = 1000
        self.max_steps_no_food = 500
        self.curr_steps = 0

    def check_snakes_are_dead(self):
        for snake in self.snakes:
            if snake.is_alive:
                return False
        return True
    
    def check_illegal_move(self, new_move, last_move):
        return (new_move == 'D' and last_move == 'A') or (new_move == 'A' and last_move == 'D') \
            or (new_move == 'W' and last_move == 'S') or (new_move == 'S' and last_move == 'W')
    
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
            for i in range(len(new_snakes)):
                new_snakes[i] = Snake(start_x, start_y, Grid(WIDTH, HEIGHT, DIM), new_snakes[i].brain)
                new_snakes[i].grid.add_food(new_snakes[i].positions, avoid_row=start_x)

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
                child.grid.add_food(child.positions, avoid_row=start_x)
                new_snakes.append(child)
            self.snakes = new_snakes

            return True
        else:
            for i, snake in enumerate(self.snakes):
                if snake.is_alive:
                    new_move = snake.think(last_moves[i])
                    new_direction = move_map[new_move]
                    
                    # distance before movement
                    old_distance = abs(snake.positions[0][0] - snake.grid.food_position[0]) + \
                                abs(snake.positions[0][1] - snake.grid.food_position[1])
                    
                    if self.check_illegal_move(new_direction, last_moves[i]):
                        # if it does an illegal move we don't kill him but choose the best move
                        # also give him penalty
                        valid_moves = ['A', 'W', 'D', 'S']
                        opposite = self.get_opposite_move(last_moves[i])
                        valid_moves.remove(opposite)
                        
                        best_move = self.choose_best_move_toward_food(snake, valid_moves)
                        new_direction = best_move
                        snake.fitness -= 10  # Penalità ridotta
                    
                    last_moves[i] = new_direction
                    snake.move(last_moves[i])
                    eaten = snake.eat()
                    snake.check_hit()
                    
                    # computes distance after movement
                    new_distance = abs(snake.positions[0][0] - snake.grid.food_position[0]) + \
                                abs(snake.positions[0][1] - snake.grid.food_position[1])
                    
                    
                    if eaten:
                        snake.fitness += 100  # big rewards if it eats
                        snake.grid.add_food(snake.positions)
                        snake.steps_since_food = self.max_steps_no_food
                    else:
                        # reward if he gets close, penalty if he gets away
                        if new_distance < old_distance:
                            snake.fitness += 2  
                        elif new_distance > old_distance:
                            snake.fitness -= 1  
                        
                        snake.fitness += 0.1  # reward for survival
                        snake.steps_since_food -= 1

                    if snake.steps_since_food < 0:
                        snake.is_alive = False
                        snake.steps_since_food = self.max_steps_no_food

                    snake.grid.update_grid(snake.positions[0], snake.last_position, eaten)
                    
                    if not already_drawn:
                        print(f"STEPS: {self.curr_steps}")
                        snake.grid.draw(screen)
                        already_drawn = True
            return False

    def get_opposite_move(self, move):
        """
        Get the opposite (illegal) move
        """
        opposites = {'A': 'D', 'D': 'A', 'W': 'S', 'S': 'W'}
        return opposites.get(move, '')

    def choose_best_move_toward_food(self, snake, valid_moves):
        head_x, head_y = snake.positions[0]
        food_x, food_y = snake.grid.food_position
        rows, cols = len(snake.grid.grid), len(snake.grid.grid[0])
        
        best_move = valid_moves[0]
        best_distance = float('inf')
        
        for move in valid_moves:
            if move == 'A':
                next_x = (head_x - 1) % rows
                next_y = head_y
            elif move == 'W':
                next_x = head_x
                next_y = (head_y - 1) % cols
            elif move == 'D':
                next_x = (head_x + 1) % rows
                next_y = head_y
            else:  # 'S'
                next_x = head_x
                next_y = (head_y + 1) % cols
            
            distance = abs(next_x - food_x) + abs(next_y - food_y)
            
            if (next_x, next_y) not in snake.positions and distance < best_distance:
                best_distance = distance
                best_move = move
        
        return best_move

    def draw(self, screen):
        for snake in self.snakes:
            if snake.is_alive:
                snake.grid.draw(screen)