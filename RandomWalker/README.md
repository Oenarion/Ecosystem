# What is this?
"In mathematics, a random walk, sometimes known as a drunkard's walk, is a stochastic process that describes a path that consists of a succession of random steps on some mathematical space."[^1]

# How does it work?
The algorithm is pretty simple, at the start a random number of walkers is generated at a random position between the boundaries, this walker will either be:
- Random walkers, at each iteration they choose a random value from the range (-1, 1) and add it to their x and y, effectively doing a random step.
- Random walkers with perlin noise[^2], the rationale is basically the same but this time the step is decided using a random timestep followed by the computation of the perlin noise for that timestep. Also additional noise is used in the equation to give the walker extra randomicity.

Random walkers will leave footprints of the last 100 steps they've taken, also a new random walker has a 0.0001% chance to spawn at each iteration, so that the simulation feels more diverse.

# TO DO

- [x] Add a user interface
  - #### OPTIONAL
  - [ ] different simulations? (create walls after the walkers trail, etc...)
  - [ ] modify noise parameters?
  - [x] Add exit button with loading circle
- [ ] Add Gaussian Random Walk.
- [ ] Add another file in which AI agents to adapt to the envinroment and try to reach another walker
- [ ] Still thinking...


[^1]: Explanation of random walk [(https://en.wikipedia.org/wiki/Random_walk)].
[^2]: Explanation of Perlin noise [(https://en.wikipedia.org/wiki/Perlin_noise)].
