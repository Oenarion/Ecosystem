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
        self.same_value_time = 0
        
    def update_value_time(self):
        if self.state == self.previous:
            self.same_value_time += 1
        else:
            self.same_value_time = 0

    def draw(self, screen, progression_display, no_bg = False):
        if not progression_display:
            if self.state == 1 and self.previous == 0:
                color = (200, 200, 0)
            elif self.state == 1 and self.previous == 1:
                color = (255, 255, 255)
            elif self.state == 0 and self.previous == 1:
                color = (0, 50, 50)
            else:
                color = (0, 0, 0)
        else:
            if self.state == 1:
                color = (min(255, 50 + (self.same_value_time*5)), min(255, 50 + (self.same_value_time*5)), 200)
            else:
                color = (0, max(0, 200 - (self.same_value_time*5)), max(0, 200 - (self.same_value_time*5)))
        if no_bg and color == (0, 0, 0):
            return
        pygame.draw.rect(screen, color, pygame.Rect(self.x, self.y, self.w, self.w))

class Grid():
    def __init__(self, rows: int, cols: int, w: int, offset_x = 0, offset_y = 0, progression_display = False):
        self.rows = rows
        self.cols = cols
        self.w = w
        self.grid = []
        self.progression_display = progression_display

        for row in range(self.rows):
            row_grid = []
            for col in range(self.cols):
                row_grid.append(Cell(offset_x + (col*self.w),offset_y + (row*self.w), self.w, random.choice([0, 1])))
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
                cell.update_value_time()
                
    def grid_change_sum(self):
        """
        Checks the number of changes in the grid, 
        the yellow/blue-ish squares to be clear. 
        """
        total_sum = 0
        for row in self.grid:
            for cell in row:
                if cell.state != cell.previous:
                    total_sum += 1
        
        return total_sum

    def draw(self, screen):
        for row in range(len(self.grid)):
            for col in range(len(self.grid[0])):
                self.grid[row][col].draw(screen, self.progression_display)


class MacroGrid():
    def __init__(self, rows, cols, dim, num_of_grids_x, num_of_grids_y):
        self.rows = rows
        self.cols = cols
        self.dim = dim
        self.macro_grid = []
        self.macro_grid_values = []
        self.times_dead_or_alive = []
        for i in range(num_of_grids_x):
            for j in range(num_of_grids_y):
                self.macro_grid.append(Grid(rows, cols, dim, i*(dim*rows), j*(dim*cols), True))
                # start as "alive"
                self.macro_grid_values.append(1)
                self.times_dead_or_alive.append(0)

    def kill_grid(self, grid):
        """
        Set all cells value to 0.

        Args:
            - grid -> the grid which we want to kill.
        """
        for row in grid.grid:
            for cell in row:
                cell.state = 0
                cell.previous = 1
                cell.next_state = 0

    def restart_grid(self, grid):
        """
        Restarts the grid by giving random values to each cell.
        
        Args:
            - grid -> the grid which we want to kill.
        """
        for row in grid.grid:
            for cell in row:
                choice = random.choice([0, 1])
                cell.state = 1-choice
                cell.previous = choice
                cell.next_state = choice

    def update_grid(self):
        for i, grid in enumerate(self.macro_grid):
            grid.update_grid()
            total_sum = grid.grid_change_sum()

            if total_sum < 20:
                if self.macro_grid_values[i] == 1:
                    self.times_dead_or_alive[i] = 0
                else:
                    self.times_dead_or_alive[i] += 1
                self.macro_grid_values[i] = 0
            
            if total_sum > 30:
                if self.macro_grid_values[i] == 0:
                    self.times_dead_or_alive[i] = 0
                else:
                    self.times_dead_or_alive[i] += 1
                self.macro_grid_values[i] = 1

            if self.times_dead_or_alive[i] > 200:
                self.kill_grid(self.macro_grid[i])

            if self.times_dead_or_alive[i] > 300:
                self.restart_grid(self.macro_grid[i])

    def draw(self, screen):
        for grid in self.macro_grid:
            grid.draw(screen)
