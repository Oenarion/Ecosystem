import pygame

class ComplexPlane:
    def __init__(self, screen, width, height, center=0+0j, scale=100):
        self.screen = screen
        self.width = width
        self.height = height
        self.center = center
        self.scale = scale  # pixels per unit

    def complex_to_screen(self, z):
        """Convert complex number to screen coordinates"""
        x = self.width // 2 + (z.real - self.center.real) * self.scale
        y = self.height // 2 - (z.imag - self.center.imag) * self.scale
        return int(x), int(y)
    
    def screen_to_complex(self, px):
        """Convert screen coordinates to complex number"""
        z_real = ((px[0] - self.width // 2) / self.scale) + self.center.real
        z_imag = -((px[1] - self.height // 2) / self.scale) + self.center.imag

        return complex(z_real, z_imag)

    def draw_pixel(self, x, y, color=(0, 0, 0), radius = 3):
        pygame.draw.circle(self.screen, color, (x, y), radius)

    def draw_point(self, z, color=(0, 0, 0), radius=3):
        x, y = self.complex_to_screen(z)
        pixel_center = self.complex_to_screen(self.center)
        pygame.draw.line(self.screen, color, pixel_center, (x, y))
        pygame.draw.circle(self.screen, color, (x, y), radius)

    def draw_axes(self, color=(200, 200, 200)):
        pygame.draw.line(self.screen, color, (0, self.height//2), (self.width, self.height//2))  # x-axis
        pygame.draw.line(self.screen, color, (self.width//2, 0), (self.width//2, self.height))  # y-axis

    def zoom_at(self, px, zoom_factor):
        """Zooms toward a pixel coordinate by adjusting scale and center."""
        before = self.screen_to_complex(px)
        self.scale *= zoom_factor
        after = self.screen_to_complex(px)
        self.center += before - after  # Shift center to keep zoom target fixed
