# Project 1

> ⚠️ This document is fairly technical to maintain brevity, if you have **any** questions ask your recruiter or come visit us at floor -2 of Povo 2.

## Abstract

Create a desktop application using [ImGui](https://github.com/ocornut/imgui). You are free to choose the task of the application but you must at least implement the following:

- User login.
- Global state of the application.
- Parse and plot a CSV file.

The application mus be organized with multiple tabs, each in a different source file.
Keep the project clean, setup it for scalability, allowing for new features implementations.
Try using some thirdparty libraries to add functionalities to your application.

### User login

Use ImGui to allow a user to login. You could setup different login types (Admin, Maintainer, Basic user), or simply logged or not.
Based on the login state, change the attitude of your application, maybe locking some functionalities.

### Global State

Define with some programming thechnique a way to access to the same data across multiple files/classes. For example if the login happened then the whole application should know the new login state.

### CSV file

Implement a parser for a CSV file, use your interface to select the path or the file to load.
Use the login type to change the way the data is plotted.

CSV files are in csv_samples folder, you have 2 files, one of a acceleration test and the other of a skidpad.

## Getting started

### Prerequisites

- `git` and a [GitHub](https://github.com) account
- C/C++ toolchain, with CMake
- OpenGL
- GLEW
- GLFW3

For Debian / Ubuntu you can use:

```bash
sudo apt install build-essential cmake libglfw3-dev libglew-dev mesa-utils
```

### Setup

- Download the project files [here](https://download-directory.github.io/?url=https%3A%2F%2Fgithub.com%2Feagletrt%2Frecruiting-sw%2Ftree%2Fmaster%2Ftelemetry%2Fproject_1)
- Create a new GitHub repository and upload the project files via git
- Start working on the task, creating git commits as you make progress
- When it's time to deliver, please send your recruiter a link to your github repository

## Building

The build system that we use is cmake.

```bash
mkdir -p build
cmake ..
make -j$(nproc)
```

This will build the executable that will be located in `./bin` directory.
