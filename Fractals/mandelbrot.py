import pygame
import complexNumbers
import time

WIDTH = 400
HEIGHT = 400
MAX_ITER = 1000

# computing the mandelbrot
def mandelbrot(c, max_iter):
    z = 0
    for n in range(max_iter):
        if abs(z) > 2:
            return n
        z = z*z + c
    return max_iter

def main():
    
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    plane = complexNumbers.ComplexPlane(screen, WIDTH, HEIGHT, center=0+0j, scale=100)

    clock = pygame.time.Clock()
    running = True

    # yo this is sick!
    surface = pygame.Surface((WIDTH, HEIGHT))
    pixels = pygame.PixelArray(surface)
    start = time.time()

    for i in range(WIDTH):
        for j in range(HEIGHT):
            c = plane.screen_to_complex((i, j))
            m = mandelbrot(c, MAX_ITER) 
            color = 255 - int(m * 255 / MAX_ITER)
            pixels[i][j] = (color, color, color)

    del pixels
    end = time.time()
    print(f"Time taken to compute Mandelbrot: {end - start}s")
    while running:

        screen.blit(surface, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()