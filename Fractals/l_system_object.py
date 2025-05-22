import pygame
import math

class L_System():
    def __init__(self, starting_string, rules, generation_limit, length, angle):
        """
        Rules is intended to be a map of the type
            {
            'char' : 'generating string'
            }
        if char is not present the char remains unchanged
        """
        self.string = starting_string
        self.rules = rules
        self.generation_limit = generation_limit
        self.length = length
        self.angle = angle
        
    
    def generate_string(self):
        for _ in range(self.generation_limit):
            current_string = ""
            for char in self.string:
                if char in self.rules:
                    current_string += self.rules[char]
                else:
                    current_string += char
            self.string = current_string
    
    def draw(self, screen, WIDTH, HEIGHT, time):
        curr_point = (WIDTH // 2, HEIGHT)
        angle = -90  # pointing up
        stack = []

        amplitude = 15  
        frequency = 0.002  
        angle_offset = amplitude * math.sin(frequency * time)

        for char in self.string:
            if char == 'F':
                # Move forward and draw
                dx = math.cos(math.radians(angle)) * self.length
                dy = math.sin(math.radians(angle)) * self.length
                next_point = (curr_point[0] + dx, curr_point[1] + dy)
                pygame.draw.line(screen, (40, 255, 200), curr_point, next_point, 1)
                curr_point = next_point
            elif char == 'G':
                # Move forward without drawing
                dx = math.cos(math.radians(angle)) * self.length
                dy = math.sin(math.radians(angle)) * self.length
                curr_point = (curr_point[0] + dx, curr_point[1] + dy)
            elif char == '+':
                # Rotate right
                angle += self.angle + angle_offset
            elif char == '-':
                # Rotate left
                angle -= self.angle + angle_offset
            elif char == '[':
                # Save current state
                stack.append((curr_point, angle))
            elif char == ']':
                # Restore last state
                curr_point, angle = stack.pop()