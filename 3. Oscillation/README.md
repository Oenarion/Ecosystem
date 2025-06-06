# Oscillation
This project explores different simulations related to oscillatory motion and dynamics, built using pygame. Simulations are organized across a few themed files:

## Main Files
  - **test_oscillation.py**: Contains three distinct motion simulations.
  - **spaceship.py**: A simple asteroid-avoidance game.
  - **pendulum_simulation.py**: Includes both single and double pendulum simulations.

## Simulations in test_oscillation.py
### Rotating Objects
A random number of "Movers" are spawned on screen. They rotate and accelerate toward the mouse cursor, both in angle and position.

### Oscillators
This simulation visualizes harmonic motion. Each oscillator moves back and forth with its own frequency and amplitude, creating an elegant oscillatory system.

### Wave Simulation
A dynamic wave is rendered by combining multiple sine waves. The result is a complex wave that travels along both x and y axes, producing rich and fluid motion.

## Spaceship
Control a spaceship and avoid incoming asteroids. The game becomes more challenging over time (though fine-tuning of parameters is still in progress). Core mechanics are in place, but additional game logic is planned.

## Pendulum
Includes two simulations:
  - Single Pendulum: A basic pendulum with damping that gradually reduces velocity.
  - Double Pendulum: A more chaotic system where the second pendulum is attached to the first. The motion reflects the complex behavior of a real double pendulum.

## To Do:
  - Spaceship Simulation:
    - [ ] Add a game over menu
    - [ ] Fine-tune asteroid speed and spawn rate

  - Pendulum Simulation:
    - [ ] Enable repositioning the pendulum with the mouse
    - [ ] Allow dynamic adjustment of the pendulum's length
