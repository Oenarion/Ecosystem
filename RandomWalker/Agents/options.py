import pygame
import graphical_components as gc

# Options Menu Class
class OptionsMenu:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.background_color = (50, 50, 50)
        
        # Create slider
        self.walkers_slider = gc.Slider(
            width // 2 - 200,  # x position
            height // 2,       # y position
            400,               # width
            20,                # height
            2,                 # min value
            100,               # max value
            30                 # initial value
        )
        
        # Create back button
        self.back_button = gc.Button(
            width // 2 - 100, 
            height - 100, 
            200, 50, 
            "Back", 
            font_size=24
        )
    
    def draw(self, screen):
        # Draw semi-transparent background
        s = pygame.Surface((self.width, self.height))
        s.set_alpha(200)
        s.fill(self.background_color)
        screen.blit(s, (0,0))
        
        # Draw title
        font = pygame.font.Font(None, 36)
        title = font.render("Options", True, (255, 255, 255))
        title_rect = title.get_rect(center=(self.width // 2, 100))
        screen.blit(title, title_rect)
        
        # Draw max walkers text
        font = pygame.font.Font(None, 24)
        max_walkers_text = font.render("Max Walkers", True, (255, 255, 255))
        max_walkers_rect = max_walkers_text.get_rect(center=(self.width // 2, self.height // 2 - 50))
        screen.blit(max_walkers_text, max_walkers_rect)
        
        # Draw slider
        self.walkers_slider.draw(screen)
        
        # Draw back button
        self.back_button.draw(screen)
    
    def handle_event(self, event):
        self.back_button.handle_event(event)
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_button.is_hovered(event.pos):
                return "BACK"
        
        # Handle slider events
        self.walkers_slider.handle_event(event)
        
        return None