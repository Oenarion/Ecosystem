import pygame
import random

class Cell():
    def __init__(self, x: int, y: int, w: int, state: int):
        self.x = x
        self.y = y
        self.w = w
        self.state = state
        self.previous = state
        self.next_state = state


    def draw(self, screen):
        if self.state == 1 and self.previous == 0:
            color = (200, 200, 0)
        elif self.state == 1 and self.previous == 1:
            color = (255, 255, 255)
        elif self.state == 0 and self.previous == 1:
            color = (0, 50, 50)
        else:
            color = (0, 0, 0)

        pygame.draw.rect(screen, color, pygame.Rect(self.x, self.y, self.w, self.w))

class Grid():
    def __init__(self, rows: int, cols: int, w: int):
        self.rows = rows
        self.cols = cols
        self.w = w
        self.grid = []

        for row in range(self.rows):
            row_grid = []
            for col in range(self.cols):
                row_grid.append(Cell(col*self.w, row*self.w, self.w, random.choice([0, 1])))
            self.grid.append(row_grid)


    def get_neighbours_sum(self, i: int, j: int, grid: list) -> int:
        """
        Computes the sum of the neighbours of the current cell.
        It's used to later evaluate the current cell to alive or dead.

        Args:
            - i -> x index of the cell
            - j -> y index of the cell
            - grid -> the whole grid

        Returns the sum of the neighbours, i.e. alive neighbours
        """
        neighbours_sum = 0
        for z in range(i-1, i+2):
            for t in range(j-1, j+2):
                if (z == i and t == j) or z < 0 or z >= len(grid) or t < 0 or t >= len(grid[0]):
                    continue
                neighbours_sum += grid[z][t].state

        return neighbours_sum
    
    def update_grid(self):
        for row in range(len(self.grid)):
            for col in range(len(self.grid[0])):
                cell = self.grid[row][col]
                neighbours_sum = self.get_neighbours_sum(row, col, self.grid)
                if cell.state == 1 and (neighbours_sum >= 4 or neighbours_sum <= 1):
                    cell.next_state = 0
                if cell.state == 0 and neighbours_sum == 3:    
                    cell.next_state = 1

        for row in self.grid:
            for cell in row:
                cell.previous = cell.state
                cell.state = cell.next_state
                

    
    def draw(self, screen):
        for row in range(len(self.grid)):
            for col in range(len(self.grid[0])):
                self.grid[row][col].draw(screen)
