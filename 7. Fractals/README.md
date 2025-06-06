# Fractals
This directory explores the fundamentals of Fractals [^1]. It goes from simple Fractal such as the Cantor Set[^2], Koch Curve (Koch Snowflake)[^3] to more advanced ones like the Mandelbrot Set[^4] and the Julia Set[^5], ending with a simulation of L-systems[^6].

# Main files
- **circles.py**

  Contains two simulations of testing backtracking stuff with circles.

- **deterministic_fractals.py**

  Contains the first "fractals" simulations. Starting with the **Cantor Set** simulation, in which the set rotates because it was boring otherwise. This simulation has some extra "features", `R` can be used to reset the simulation, `N` to stop the rotation and `C` to display a variation of the Cantor set, with, you guessed it, **circles**!
  
  The other simulation displays a **Koch Curve** the amount of backtracking steps can be changed using a slider.
  
  Finally the last simulation displays the **Koch Snowflake**, and again the amount of backtracking steps can be changed.
- **mandelbrot.py**

  The name is pretty self explanatory, or is it? The actual simulation is divided in two parts, the left part of the screen has the **Mandelbrot Set**, which is constant. On the right however, the **Julia Set** is displayed! Julia Sets can be generated starting from a certain point of the Mandelbrot set, by simply taking the current mouse position (if it's in the left part of the screen) the corresponding Julia set will be displayed.
  
  By using `mouse wheel` it is possible to zoom on the half of the screen in which the mouse is currently, by pressing `P` you can pause the updates of the Julia set, so that it's easier to zoom in or zoom out. Finally with `R` you can reset the simulation.

  I didn't watch the optimization part, so the code runs pretty slowly, deal with it.
- **trees.py**

  This program contains three simulation, each one generating different types of **Fractal Trees[^7]**. The first one contains a plain Fractal Tree, by using sliders you can change the angle of each new branch, the decay length of each branch and also the number of total backpropagation steps.

  The second simulation just shows the backpropragation process, by constructing the tree in branch call order.

  Finally the final simulation is a Random Fractal Tree, which changes at each frame, the effect it creates made me laugh (total chaos tree) so it remained unchanged.

- **l_systems.py**

  Finally the last simulation contains the **L-systems**, again with a slider it's possible to change the angle by which a rotated branch gets created. I used a standard rule system and the simulation is deterministic.

  The system also oscillates by using a simple periodic function, it should remind an algae being moved by currents. 

## Footnotes
[^1]: [Fractal](https://en.wikipedia.org/wiki/Fractal)
[^2]: [Cantor Set](https://en.wikipedia.org/wiki/Cantor_set)
[^3]: [Koch Curve](https://en.wikipedia.org/wiki/Koch_snowflake)
[^4]: [Mandelbrot Set](https://en.wikipedia.org/wiki/Mandelbrot_set)
[^5]: [Julia Set](https://en.wikipedia.org/wiki/Julia_set)
[^6]: [L-systems](https://en.wikipedia.org/wiki/L-system)
[^7]: [Fractal Trees](https://en.wikipedia.org/wiki/Fractal_canopy)
