import pygame
import complexNumbers
import time
import numpy as np

WIDTH = 800
HEIGHT = 400
MAX_ITER = 100

# computing the mandelbrot
def mandelbrot(c, max_iter):
    z = 0
    for n in range(max_iter):
        if abs(z) > 2:
            return n
        z = z*z + c
    return max_iter

def julia_set(z, c, max_iter):
    """
    computes the julia set.

    Args:
        - z: complex number of the current pixel point examined.
        - c: position of the mouse.
        - max_iter: maximum number of iterations.
    """
    for n in range(max_iter):
        if abs(z) > 2:
            return n
        z = z*z + c
    return max_iter

def compute_fractal(plane, width, height, func, const=None):
    data = np.zeros((height, width, 3), dtype=np.uint8)
    for i in range(width):
        for j in range(height):
            z = plane.screen_to_complex((i, j))
            iter_count = func(z, const, MAX_ITER) if const else func(z, MAX_ITER)
            color = 255 - int(iter_count * 255 / MAX_ITER)
            data[j, i] = [0, 0, color]
    return data

def main():
    
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    left_plane = complexNumbers.ComplexPlane(screen, WIDTH // 2, HEIGHT, center=0+0j, scale=100)
    right_plane = complexNumbers.ComplexPlane(screen, WIDTH // 2, HEIGHT, center=0+0j, scale=100)

    clock = pygame.time.Clock()
    running = True
    prev_c = None

    start = time.time()
    mandelbrot_data = compute_fractal(left_plane, WIDTH // 2, HEIGHT, mandelbrot)
    end = time.time()
    print(f"Time taken to compute Mandelbrot: {end - start:.2f}s")

    mandelbrot_surface = pygame.surfarray.make_surface(np.transpose(mandelbrot_data, (1, 0, 2)))
    julia_surface = pygame.Surface((WIDTH // 2, HEIGHT))

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.blit(mandelbrot_surface, (0, 0))

        x, y = pygame.mouse.get_pos()
        if 0 <= x < WIDTH // 2:
            c = left_plane.screen_to_complex((x, y))

            # Ricrea solo se cambia posizione
            if c != prev_c:
                julia_data = compute_fractal(right_plane, WIDTH // 2, HEIGHT, julia_set, c)
                julia_surface = pygame.surfarray.make_surface(np.transpose(julia_data, (1, 0, 2)))
                prev_c = c

        screen.blit(julia_surface, (WIDTH // 2, 0))
        pygame.display.flip()
        clock.tick(10)

    pygame.quit()


if __name__ == "__main__":
    main()