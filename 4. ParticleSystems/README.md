# 💨 Particle Systems

This project explores the fundamentals of [particle systems](https://en.wikipedia.org/wiki/Particle_system), a technique widely used in computer graphics and simulations to represent fuzzy phenomena like fire, smoke, explosions, or magical effects.

---

##  Main Files

### 🌪️ `emitters.py`

This script implements a basic **particle emitter** system:

- Emitters spawn a **random number of particles** at creation time.
- Each particle has properties like **lifespan, velocity, size, and transparency** that evolve over time.
- `Left-clicking` on the canvas creates new emitters dynamically.
- The simulation uses additive blending and fading effects to simulate a trail and smooth disappearance.

#### Visual Examples

![Emitters](gifs/emitters.gif)

> Emitters are created dinamically and each one has a different number of particles that can create.

---

### 💥 `ball_death_animation.py`

This script simulates a **destruction effect**:

- A ball drops due to gravity and, upon hitting the ground, **explodes into multiple smaller particles**.
- The resulting "shatter" creates a convincing death or impact animation.

#### Visual Examples

![Death ball](gifs/death_ball_animation.gif)

> Ball exploding into tiny little balls.

---

## 📚 Footnotes

- [Particle Systems (Wikipedia)](https://en.wikipedia.org/wiki/Particle_system)
