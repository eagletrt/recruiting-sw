# Project 1

We've already set a part of the project. You can find some sources with the basic setup to open a window.

## Task
Using [ImGui](https://github.com/ocornut/imgui) create a basic application. You are free to choose the task of the application but you must at least implement the following:
- User login.
- Global state of the application.

### User login
Use ImGui to allow a user to login. You could setup different login types (Admin, Maintainer, Basic User), or simply logged or not.  
Based on the login state, change the attitude of your application, maybe locking some functionalities.

### Global State
Define with some programming thechnique a way to access to the same data across multiple files/classes. For example if the login happened then the whole application should know the new login state.

## Building
The build system that we use is cmake, get used to it.
~~~bash
mkdir -p build
cmake ..
make -j$(nproc)
~~~
This will build the executable that will be located in bin directory.

## Prerequisites
As it is the project requires some prerequisites:
- OpenGl
- GLEW
- GLFW3

OpenGl should already be installed. to install GLEW and GLFW use your package manager. For debian:
~~~bash
sudo apt install libglfw3-dev libglew-dev
~~~