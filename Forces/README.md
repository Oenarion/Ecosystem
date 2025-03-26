# FORCES
This chapter is focussed on forces, which are mainly gravity, drag force, friction and gravitational force.
In this file you will find for now **3 different simulations**.
### Liquid simulation
Two things were mainly tested in this simulation:
  - **The drag force**, exerted by the liquid which makes the mover object fall more slowly to the ground (works on the y axis).
  - **The friction force**, exerted by the floor on the mover, making resistance when trying to move the object on the x axis.

Two additional forces were used just to give a more realistic feel to the simulation:
  - **Gravity**, which pulls the movers down.
  - **Wind force**, can be applied with the mouse and moves the movers on the x axis (to the right for now)

## Gravitational force simulation
This simulation tests the gravitational force, by using the movers and a new object, the attractor.
The attractor(s) is fixed in place and pulls the movers to him.

During the simulation new movers and new attractors can be added and at the same time movers will "die" if they go out of bounds (out of the canvas) or attractors will be removed. 
This ensures that the simulation feels more real and not static.

## N-body problem
Still under construction...

TO DO:
  - Liquid simulation:
    - [ ] Try adding different liquids and different densities (maybe some liquid keeps the object on the surface) and also give them a specific color (water blue, oil yellow, etc).
    - [ ] Modify the wind force such that it moves the object away from the mouse position (i.e. if the object is to the right of the mouse it will be moved to the right).
    - [ ] New type of gravity force which forces the object down if the liquid keeps pulling it up.
    - [ ] Gravity force pulling the  objects to the mouse position.
    - [ ] Add a tab menu to explain how to use the forces.
    
  - In the gravitational simulation:
    - [x] Instead of deleting an attractor right away, let's delete by slowly shrinking it, like it's losing all of its energy.
    - [x] The spawning of new attractors and new movers must be without any collision, so no mover could spawn inside another attractor or attractors inside other attractors.
    - [ ] Add space like background to beautify.
    
  - N-body problem:
    - [ ] Create the simulation.  
