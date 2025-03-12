import pygame

class Mover():
    def __init__(self, x: int, y: int, color: tuple, h: int, w: int, elastiticy = -0.9, mass = 1, 
                velocity = None, acceleration = None):
        
        
        self.color = color
        self.h = h
        self.w = w
        self.mass = mass
        
        self.elastiticy = elastiticy
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
        Objects bounce of walls, this functions checks if a wall is hit (note that the floor is not considered a wall).
        If a wall is hit the velocity direction is inverted, and the position reset to wall's position.

        Args:
            - WIDTH -> width of the canvas
            - HEIGHT -> height of the canvas
        """

        if self.position.x > (WIDTH - self.w):
            self.position.x = WIDTH - self.w
            self.velocity.x *= self.elastiticy  
        elif self.position.x < 0:
            self.position.x = 0
            self.velocity.x *= self.elastiticy  

        if self.position.y < 0:
            self.position.y = 0
            self.velocity.y *= self.elastiticy  
        elif self.position.y > (HEIGHT - self.h):
            self.position.y = HEIGHT - self.h
            self.velocity *= self.elastiticy
        
        
    def check_floor(self, HEIGHT: int) -> bool:
        """
        Checks if floor is hit.

        Args:
            - HEIGHT -> height of the canvas in which objects are drawn

        Returns True if floor is hit, False otherwise
        """
        if self.position.y >= (HEIGHT - self.h):
            return True 
        return False

    def get_mover_attributes(self):
        """
        Returns position and color of object, used mainly to draw the walker at each iteration.
        """
        return [self.position, self.velocity, self.acceleration, self.color, self.h, self.w] 
    
    def get_mass(self):
        """
        Returns the mover's mass.
        """
        return self.mass
    
    def get_velocity(self):
        """
        Returns the mover's velocity
        """
        return self.velocity