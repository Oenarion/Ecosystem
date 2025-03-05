import pygame
import time
import math

## SLIDER CLASS
class Slider:
    def __init__(self, x, y, width, height, min_val, max_val, initial_val):
        """
        Create a slider for selecting a value between min and max
        
        Args:
        x, y: Position of slider
        width, height: Dimensions of slider area
        min_val, max_val: Range of values
        initial_val: Starting value
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.min_val = min_val
        self.max_val = max_val
        
        # Slider handle
        self.handle_width = 20
        self.handle_height = 40
        self.handle_color = (200, 200, 200)
        self.handle_hover_color = (230, 230, 230)
        
        # Set initial value
        self.current_val = initial_val
        self.calculate_handle_position()
        
        # Dragging state
        self.is_dragging = False
    
    def calculate_handle_position(self):
        """
        Calculate the x position of the slider handle based on current value
        """
        # Map current value to slider width
        normalized = (self.current_val - self.min_val) / (self.max_val - self.min_val)
        # Computes new slider positions and ensures it is in bounds with the slider
        self.handle_x = self.rect.x + normalized * (self.rect.width - self.handle_width)
        # Create the corresponding rect
        self.handle_rect = pygame.Rect(
            self.handle_x, 
            self.rect.y - (self.handle_height - self.rect.height) // 2, 
            self.handle_width, 
            self.handle_height
        )
    
    def draw(self, screen):
        """
        Draw the slider on the screen
        """
        # Draw slider track
        pygame.draw.rect(screen, (100, 100, 100), self.rect)
        
        # Draw handle
        pygame.draw.rect(screen, self.handle_color, self.handle_rect)
        
        # Draw value text
        font = pygame.font.Font(None, 24)
        text = font.render(str(int(self.current_val)), True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.rect.centerx, self.rect.bottom + 30))
        screen.blit(text, text_rect)
    
    def handle_event(self, event):
        """
        Handle mouse events for the slider
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.handle_rect.collidepoint(event.pos):
                self.is_dragging = True
        
        elif event.type == pygame.MOUSEBUTTONUP:
            self.is_dragging = False
        
        elif event.type == pygame.MOUSEMOTION:
            if self.is_dragging:
                # Calculate new handle position
                mouse_x = max(self.rect.x, min(event.pos[0], self.rect.right - self.handle_width))
                
                # Map mouse position to slider value
                normalized = (mouse_x - self.rect.x) / (self.rect.width - self.handle_width)
                self.current_val = self.min_val + normalized * (self.max_val - self.min_val)
                
                # Snap to integer
                self.current_val = round(self.current_val)

                # # Recalculate handle position
                self.calculate_handle_position()
        
        return int(self.current_val)


## BUTTON CLASS
class Button:
    def __init__(self, x, y, width, height, text, font_size=32, 
                 text_color=(255, 255, 255), 
                 normal_color=(100, 100, 100), 
                 hover_color=(150, 150, 150)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font_size = font_size
        self.text_color = text_color
        self.normal_color = normal_color
        self.hover_color = hover_color
        self.current_color = normal_color
        
        # Create font
        self.font = pygame.font.Font(None, font_size)
    
    def draw(self, screen):
        # Draw button rectangle
        pygame.draw.rect(screen, self.current_color, self.rect)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)  # White border
        
        # Render text
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
    
    def is_hovered(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            if self.is_hovered(event.pos):
                self.current_color = self.hover_color
            else:
                self.current_color = self.normal_color


## LOADING CIRCLE CLASS
class LoadingCircle:
    def __init__(self, x, y, radius=10, duration=1.0, color=(255, 255, 255)):
        """
        Initialize the loading circle
        
        Args:
        x, y: Center coordinates of the circle
        radius: Radius of the circle
        duration: Time to complete the loading (in seconds)
        color: Color of the loading segment
        background_color: Color of the background circle
        """
        self.x = x
        self.y = y
        self.radius = radius
        self.duration = duration
        self.color = color
        
        # Tracking variables
        self.start_time = 0
        self.is_loading = False
    
    def start_loading(self):
        """
        Start the loading timer
        """
        self.start_time = time.time()
        self.is_loading = True
    
    def stop_loading(self):
        """
        Stop the loading timer
        """
        self.is_loading = False
    
    def draw(self, screen):
        """
        Draw the loading circle
        
        Args:
        screen: Pygame screen surface to draw on
        """
        if not self.is_loading:
            return
        
        # Calculate progress
        elapsed_time = time.time() - self.start_time
        progress = min(elapsed_time / self.duration, 1.0)

        # Draw loading segment
        if progress > 0:
            # Draw arc from 3 o'clock position (0 degrees)
            pygame.draw.arc(
                screen, 
                self.color, 
                (self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2),
                math.pi/2,  # Start from top
                math.pi/2 + (progress * 2 * math.pi),  # End position based on progress
                width=5  # Thickness of the arc
            )