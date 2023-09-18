# Steering Wheel Recruitment Project

## Setup the environment

Follow these instructions to clone and build the steering wheel dashboard simulator.

```bash
git clone git@github.com:eagletrt/sw-fenice-evo-steering-wheel.git --recurse-submodules steering-wheel
cd steering-wheel/Core/UI/
# If this fails it is because you miss some dependencies. Please install them.
cmake -S . -B build
cd build
# The first time this could take some time
make -j4
./SteeringSimulator
```

## The task

You should implement a new tab that show the state of the shutdown circuit. As you see from [the result image](./result.png), around each component of the shutdown circuit you have to render a rectangle. It must be red if the shutdown circuit component is open and green if closed.

It will be handled by can messages, but for the purposes of this project you can use keyboard controls to turn each one on and off.


