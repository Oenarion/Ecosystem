import pygame

class Mover():
    def __init__(self, x: int, y: int, color: tuple, h: int, w: int, elastiticy = -0.9, mass = 1, 
                velocity = None, acceleration = None):
        
        
        self.color = color
        self.h = h
        self.w = w
        self.__mass = mass
        
        self.__elastiticy = elastiticy
        # this are all pygame Vectors
        self.__position = pygame.Vector2(x, y)
        self.__velocity = velocity if velocity is not None else pygame.Vector2(0, 0)
        self.__acceleration = acceleration if acceleration is not None else pygame.Vector2(0, 0)


    def apply_force(self, force: pygame.Vector2):
        """
        Applies a force on the Mover object (i.e. gravity), follows Newton's formula F = m x A

        Args:
            - force -> force to be applied
        """
        force_copy = force.copy()
        f = force_copy / self.__mass  
        self.__acceleration += f 

    def update_position(self):
        """
        Updates the position of the mover, used after a force is applied via apply_force().
        """
        self.__velocity += self.acceleration
        self.__position += self.velocity
        self.__acceleration *= 0 


    def check_edges(self, WIDTH: int, HEIGHT: int) -> None:
        """
        Objects bounce of walls, this functions checks if a wall is hit (note that the floor is not considered a wall).
        If a wall is hit the velocity direction is inverted, and the position reset to wall's position.

        Args:
            - WIDTH -> width of the canvas
            - HEIGHT -> height of the canvas
        """

        if self.__position.x > (WIDTH - self.w):
            self.__position.x = WIDTH - self.w
            self.__velocity.x *= self.__elastiticy  
        elif self.__position.x < 0:
            self.__position.x = 0
            self.__velocity.x *= self.__elastiticy  

        if self.__position.y < 0:
            self.__position.y = 0
            self.__velocity.y *= self.__elastiticy  
        elif self.__position.y > (HEIGHT - self.h):
            self.__position.y = HEIGHT - self.h
            self.__velocity.y *= self.__elastiticy
        
        
    def check_floor(self, HEIGHT: int) -> bool:
        """
        Checks if floor is hit.

        Args:
            - HEIGHT -> height of the canvas in which objects are drawn

        Returns True if floor is hit, False otherwise
        """
        if self.__position.y >= (HEIGHT - self.h):
            return True 
        return False

    def get_mover_attributes(self):
        """
        Returns position and color of object, used mainly to draw the walker at each iteration.
        """
        return [self.__position, self.__velocity, self.__acceleration, self.color, self.h, self.w] 


    # GETTERS
    @property
    def mass(self):
        """
        Returns the mover's mass
        """
        return self.__mass

    @property
    def velocity(self):
        """
        Returns the mover's velocity
        """
        return self.__velocity
    
    @property
    def acceleration(self):
        """
        Returns the mover's acceleration
        """
        return self.__acceleration