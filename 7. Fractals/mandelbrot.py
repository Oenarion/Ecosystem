import pygame
import complexNumbers
import time
import numpy as np
import matplotlib.pyplot as plt

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
    

def compute_fractal(plane, func, const=None):
    iter_map = np.zeros((HEIGHT, WIDTH // 2), dtype=np.uint16)
    for j in range(HEIGHT):
        for i in range(WIDTH // 2):
            z = plane.screen_to_complex((i, j))
            iter_map[j, i] = func(z, const, MAX_ITER) if const is not None else func(z, MAX_ITER)
    return iter_map



def main():
    
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mandelbrot & Julia")

    scale = 100

    right_plane = complexNumbers.ComplexPlane(screen, WIDTH // 2, HEIGHT, center=0+0j, scale=scale)
    left_plane = complexNumbers.ComplexPlane(screen, WIDTH // 2, HEIGHT, center=0+0j, scale=scale)

    clock = pygame.time.Clock()
    running = True
    prev_c = None
    stop_mouse_position = False

    start = time.time()
    mandelbrot_data = compute_fractal(right_plane, mandelbrot)
    end = time.time()
    print(f"Time taken to compute Mandelbrot: {end - start:.2f}s")

    # let's use matplotlib
    cmap = plt.get_cmap("inferno")
    colors = (np.array([cmap(i / MAX_ITER)[:3] for i in range(MAX_ITER + 1)]) * 255).astype(np.uint8)

    julia_data = np.zeros((HEIGHT, WIDTH // 2, 3), dtype=np.uint8)
    mandelbrot_rgb = colors[mandelbrot_data]

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    stop_mouse_position = not stop_mouse_position

                if event.key == pygame.K_r:
                    right_plane = complexNumbers.ComplexPlane(screen, WIDTH // 2, HEIGHT, center=0+0j, scale=scale)
                    left_plane = complexNumbers.ComplexPlane(screen, WIDTH // 2, HEIGHT, center=0+0j, scale=scale)
                    mandelbrot_data = compute_fractal(left_plane, mandelbrot)
                    mandelbrot_rgb = colors[mandelbrot_data]
                    if prev_c is not None:
                        julia_data = compute_fractal(right_plane, julia_set, prev_c)
                        julia_data = colors[julia_data]
                    else:
                        julia_data = np.zeros((HEIGHT, WIDTH // 2, 3), dtype=np.uint8)

            if event.type == pygame.MOUSEWHEEL:
                zoom_factor = 1.1 if event.y > 0 else 0.9
                mouse_x, mouse_y = pygame.mouse.get_pos()

                if mouse_x < WIDTH // 2:
                    left_plane.zoom_at((mouse_x, mouse_y), zoom_factor)
                    mandelbrot_data = compute_fractal(left_plane, mandelbrot)
                    mandelbrot_rgb = colors[mandelbrot_data]
                else:
                    right_plane.zoom_at((mouse_x - WIDTH // 2, mouse_y), zoom_factor)
                    if prev_c:
                        julia_data = compute_fractal(right_plane, julia_set, prev_c)
                        julia_data = colors[julia_data]

        x, y = pygame.mouse.get_pos()
        if 0 <= x < WIDTH // 2:
            c = left_plane.screen_to_complex((x, y))
            if c != prev_c and not stop_mouse_position:
                prev_c = c
                for j in range(HEIGHT):
                    for i in range(WIDTH // 2):
                        z = left_plane.screen_to_complex((i, j))
                        m = julia_set(z, c, MAX_ITER)
                        julia_data[j, i] = colors[m]

        combined = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
        combined[:, :WIDTH//2] = mandelbrot_rgb
        combined[:, WIDTH//2:] = julia_data

        pygame.surfarray.blit_array(screen, combined.swapaxes(0, 1))
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()