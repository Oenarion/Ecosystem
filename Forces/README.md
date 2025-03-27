# FORCES
This chapter is focussed on forces, which are mainly gravity, drag force, friction and gravitational force.
In this file you will find for now **3 different simulations**.
### Liquid simulation
Two things were mainly tested in this simulation:
  - **The drag force**, exerted by the liquid which makes the mover object fall more slowly to the ground and works on the y axis (can change depending on the liquid). 
  - **The friction force**, exerted by the floor on the mover, making resistance when trying to move the object on the x axis.

Two liquids can be found in the simulation:
  - **Water**, applies a basic drag force following the formula.
  - **Oil**, applies also a bouncy effect that makes movers reach the surface of the liquid if they are not heavy enough.
    
Additional forces were used just to give a more realistic feel to the simulation:
  - **Gravity**, which pushes the movers down, always applied unless the mover is on the floor.
  - **Wind force**, can be applied with **the mouse left click** and moves the movers on the x axis, depending on the mover's position relative to the mouse (mover's to the right w.r.t. the mouse will be pushed right and viceversa).
  - **Increasing gravity force**, can be applied with **Q** and pushes the movers down, it reaches a maximum value which can be set from the code.
  - **Increasing negative gravity force**, can be applied with **W**, does the same thing as the *increasing gravity force*...just in the other way.

## Gravitational force simulation
This simulation tests the gravitational force, by using the movers and a new object, the attractor.
The attractor(s) is fixed in place and pulls the movers to him.

During the simulation there's a small chance during each iteration that a new mover or a new attractor spawns, at the same time there's also a small chance that one of the attractors dies. 
On the other hand the movers will die when they go out of the boundaries (out of the canvas).

**Movers** will come *"from outer space"* (spawn), i.e. from the edges of the canvas, to make it feel like they are coming, as I have just written, from outer space.

**Attractors** will spawn and die by rapidly enlarging or shrinking over time, the *spawn time and death time variable* can be changed in the Attractor class. This makes the attractor feel more real as it is rapidly gaining fuel
or losing it all before vanishing, like it was a real star.

This ensures that the simulation feels more real and not static.

## N-body problem [^1]
The N-body problem simulation just takes what was done from the *Gravitational force simulation* and mixes it up, movers and attractors are now **bodies**, which have the ability to both attract and get attracted.

**Bodies** follow the same spawn method of **attractors** and the same death method of the **movers**. 

Like the other simulation the bodies have a small chance to spawn at each iteration (*1%*), to make the simulation feel more real.



**TO DO** :
  - Liquid simulation:
    - [x] Try adding different liquids and different densities (maybe some liquid keeps the object on the surface) and also give them a specific color (water blue, oil yellow, etc).
    - [x] Modify the wind force such that it moves the object away from the mouse position (i.e. if the object is to the right of the mouse it will be moved to the right).
    - [x] New type of gravity force which forces the object down if the liquid keeps pulling it up.
    
  - In the gravitational simulation:
    - [x] Instead of deleting an attractor right away, let's delete by slowly shrinking it, like it's losing all of its energy.
    - [x] The spawning of new attractors and new movers must be without any collision, so no mover could spawn inside another attractor or attractors inside other attractors.
    
  - N-body problem:
    - [x] Create the simulation.
    - [x] add spawn of new bodies and maybe also some attractors/movers just for the lols.
   
  - [ ] BEATIFY THE SIMULATIONS IF NEEDED!

[^1]: N-body problem explanation [(https://en.wikipedia.org/wiki/N-body_problem)].
