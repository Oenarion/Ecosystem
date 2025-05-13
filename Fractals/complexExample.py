import pygame
import complexNumbers
import cmath
import time

WIDTH = 800
HEIGHT = 600

def main():
    
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    plane = complexNumbers.ComplexPlane(screen, WIDTH, HEIGHT, center=0+0j, scale=100)

    clock = pygame.time.Clock()
    running = True

    px = (0, 0)
    z = plane.screen_to_complex(px)
    print(z.real, z.imag)
    px_x, px_y = plane.complex_to_screen(z)
    print(px_x, px_y)

    z = 1 + 1j
    print(type(z))
    z_transformed = cmath.sqrt(z)

    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for i in range(WIDTH):
            for j in range(HEIGHT):
                z = plane.screen_to_complex((i, j))
                if (z.real - plane.center.real)**2 + (z.imag - plane.center.imag)**2 < 4:
                    pygame.draw.rect(screen, (255,0,0), pygame.Rect(i, j, 1, 1))
        
        # x, y = pygame.mouse.get_pos()
        # print(f"Current pixel point: {x, y}")
        # z = plane.screen_to_complex((x, y))
        # print(f"Current complex point: {z}")

        # plane.draw_pixel(x, y, (255, 0, 0))
        # screen.fill((255, 255, 255))
        # plane.draw_axes()

        # Disegna numero originale
        # plane.draw_point(z, color=(255, 0, 0))

        # # Disegna trasformazione
        # plane.draw_point(z_transformed, color=(0, 0, 255))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()