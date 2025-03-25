import pygame

class Mover():
    def __init__(self, x: int, y: int, color: tuple, radius: int, elastiticy = -0.9, friction_coef = 0.7,
                 mass = 1, velocity = None, acceleration = None):
        
        
        self.color = color
        self.radius = radius
        self.__mass = mass
        self.rect = pygame.Rect(x - radius, y - radius, self.radius*2, self.radius*2)

        self.__elastiticy = elastiticy
        self.friction_coef = friction_coef
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
        self.rect = pygame.Rect(self.__position.x - self.radius, self.__position.y - self.radius, self.radius*2, self.radius*2)


    def check_edges(self, WIDTH: int, HEIGHT: int) -> None:
        """
        Objects bounce of walls, this functions checks if a wall is hit (note that the floor is not considered a wall).
        If a wall is hit the velocity direction is inverted, and the position reset to wall's position.

        Args:
            - WIDTH -> width of the canvas
            - HEIGHT -> height of the canvas
        """

        if self.__position.x > (WIDTH - self.radius):
            self.__position.x = WIDTH - self.radius
            self.__velocity.x *= self.__elastiticy  
        elif self.__position.x < 0:
            self.__position.x = 0
            self.__velocity.x *= self.__elastiticy  

        if self.__position.y < 0:
            self.__position.y = 0
            self.__velocity.y *= self.__elastiticy  
        elif self.__position.y > (HEIGHT - self.radius):
            self.__position.y = HEIGHT - self.radius
            self.__velocity.y *= self.__elastiticy
        
        
    def check_floor(self, HEIGHT: int) -> bool:
        """
        Checks if floor is hit.

        Args:
            - HEIGHT -> height of the canvas in which objects are drawn

        Returns True if floor is hit, False otherwise
        """
        if self.__position.y >= (HEIGHT - self.radius):
            return True 
        return False

    def get_mover_attributes(self):
        """
        Returns position and color of object, used mainly to draw the walker at each iteration.
        """
        return [self.__position, self.__velocity, self.__acceleration, self.color, self.radius] 

    def get_draw_attributes(self):
        """
        Returns attributes for drawing, i.e. rect and color
        """

        return [self.radius, self.__position, self.rect, self.color]

    def compute_friction(self):
        """
        Computes friction, where F = -1*μ*N*v.
        This method is now encapsulated into the mover's class because each mover could have a different friction coefficient, friction is now computed on the x axis.

        Args:
            - mover -> the mover object which we need to apply friction to

        Returns the friction force.
        """
        normal = self.mass

        # If velocity is very small, don't apply friction
        if abs(self.__velocity.x) < 0.05:
            self.__velocity.x = 0
            return pygame.Vector2(0, 0)

        # Apply a small damping factor when the velocity is very small
        if abs(self.__velocity.x) < 0.1:
            print("reducing friction coef")
            self.friction_coef = self.friction_coef * 0.5  # Reduce friction when moving slowly

        # Calculate friction magnitude
        friction_magnitude = self.friction_coef * normal

        # Apply friction in the opposite direction of velocity
        friction_vector = pygame.Vector2(-1 * self.__velocity.x, 0)  # Only in x direction
        friction_vector.normalize_ip()
        friction_vector *= friction_magnitude
        
        return friction_vector


    # GETTERS - just to test that you can actually do it
    # getters are not needed in python most of the times
    @property
    def position(self):
        """
        Returns the mover's mass
        """
        return self.__position

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