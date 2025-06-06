# Cellular Automata

This directory explores the fundamentals of Cellular Automata[^1] (CA), with its most iconic example: Conway’s *Game of Life*[^2].

## Main files

- **1d_CA.py**  
  A basic 1D cellular automaton, where each cell’s next state depends on itself and its two immediate neighbors.  
  In this simulation, a new ruleset (composed of 2<sup>3</sup> rules) is randomly generated for each generation.  
  Each generation is stacked vertically, providing a sense of time evolution.  
  After several iterations, the system often reaches a stable or repetitive state.  

- **game_of_life.py**  
  A straightforward implementation of Conway’s Game of Life.

- **oop_gol.py**  
  An object-oriented implementation of Game of Life.  
  Adds visual feedback through color transitions, indicating state changes.  
  Pressing `C` toggles a mode where temporal information is embedded—cells gradually fade or light up over time.

- **gol_variation.py**  
  A variation where multiple Game of Life instances run simultaneously across different regions of the canvas.  
  Each region evolves independently, creating a layered dynamic across the grid.

Press `R` to reset each simulation.
---

## Footnotes

[^1]: [Cellular Automata](https://en.wikipedia.org/wiki/Cellular_automaton)  
[^2]: [Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life)
