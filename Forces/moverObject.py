import pygame

class Mover():
    def __init__(self, x: int, y: int, color: tuple, h: int, w: int, mass = 1, 
                velocity = None, acceleration = None):
        
        
        self.color = color
        self.h = h
        self.w = w
        self.mass = mass
        
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
        
        f = force / self.mass  
        self.acceleration += f  

    def update_position(self):
        """
        Updates the position of the mover, used after a force is applied via apply_force().
        """
        self.velocity += self.acceleration
        self.position += self.velocity
        self.acceleration *= 0 


    def check_edges(self, WIDTH: int, HEIGHT: int) -> None:
        """
        Objects bounce of walls, this functions checks if a wall is hit.
        If a wall is hit the velocity direction is inverted, and the position reset to wall's position.

        Args:
            - WIDTH -> width of the canvas
            - HEIGHT -> height of the canvas
        """

        if self.position.x > (WIDTH - self.w):
            self.position.x = WIDTH - self.w
            self.velocity.x *= -1  
        elif self.position.x < 0:
            self.position.x = 0
            self.velocity.x *= -1

        if self.position.y > (HEIGHT - self.h):
            self.position.y = HEIGHT - self.h
            self.velocity.y *= -1
        elif self.position.y < 0:
            self.position.y = 0
            self.velocity.y *= -1

    def get_mover_attributes(self):
        """
        Returns position and color of object, used mainly to draw the walker at each iteration.
        """
        return [self.position, self.velocity, self.acceleration, self.color, self.h, self.w] 