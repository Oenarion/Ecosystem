import pygame
import random


class Grid():
    def __init__(self, WIDTH, HEIGHT, DIM):
        self.rows = WIDTH // DIM
        self.cols = HEIGHT // DIM
        self.dim = DIM
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

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

    def draw(self, screen):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                if self.grid[i][j] == 'S': 
                    pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(i*self.dim, j*self.dim, self.dim, self.dim))
                elif self.grid[i][j] == 'F':
                    pygame.draw.rect(screen, (200, 100, 0), pygame.Rect(i*self.dim, j*self.dim, self.dim, self.dim))

class Snake():
    def __init__(self, start_x, start_y, grid):
        self.x = start_x
        self.y = start_y
        self.positions = [(start_x, start_y)]
        self.last_position = (start_x, start_y)
        self.grid = grid

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

        If true is returned then it's game over.
        """
        head_position = self.positions[0]
        if self.grid.grid[head_position[0]][head_position[1]] == 'S':
            return True
        return False


