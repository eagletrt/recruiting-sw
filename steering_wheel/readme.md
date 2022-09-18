# Recruiting steering wheel

> ⚠️ This document is fairly technical to maintain brevity, if you have **any** questions ask your recruiter or come visit us at floor -2 of Povo 2.

## Abstract

Create a racing view for a Formula 1 steering wheel ([some examples](https://duckduckgo.com/?q=steering+wheel+formula+1+screen&t=h_&iar=images&iax=images&ia=images)), displaying sensor data, temperatures, speed, RPM, … fetched (and simulated) from a C++ backend.

### Interface

As you can tell by [some examples](https://duckduckgo.com/?q=steering+wheel+formula+1+screen&t=h_&iar=images&iax=images&ia=images), F1 steering wheel UI's are not striving for a beautiful look, instead focusing on functional layout that can be interpreted at a glance by the pilot while racing. Your UI should reflect this principle, using clever graphics to **clearly** display data in a useful manner.

There is no restriction on how you lay down visual components in your view, but you must include at least:

- RPM counter [`rpm`]
- Current speed [`km/h`]
- Power limiter value, which can have values of:
  - 0%
  - 20%
  - 40%
  - 60%
  - 80%
  - 100%
- 4 temperature sensors (of which you know the range):
  - BMS HV Temp [`*C`, `20-40`]: Maximum cell pack temperature of the BMS HV
  - BMS LV Temp [`*C`, `20-50`]: Maximum battery temperature of the BMS LV
  - INVERTER Temp [`*C`, `20-70`]
  - MOTOR Temp [`*C`, `20-80`] 
- 3 additional sensors (of which you know the range):
  - BMS HV Voltage [`V`, `350-460`]: Voltage of all the 108 cells in the BMS HV
  - BMS LV Voltage [`V`, `12-18`]: Voltage of all the 4 cells in the BMS LV
  - BMS LV Current [`A`, `0-30`]: Current output of the BMS LV 

The entire UI, including components needs to be developed using QML, all the sensor data will originate from the backend. Be sure to bookmark the official [wiki](https://doc.qt.io/qt-5/qmlapplications.html).

#### Some hints

- Temperature sensor ranges are indicative so temperatures above and below the range could occur and are considered critical.
- You can think of the power limiter value as a sort of gear (_don't tell anyone about this_)
- The BMS HV Voltage represents the remaining charge of the vehicle
- Displaying the values in a grid of text works, but giving more importance to certain values (making them bigger, using addition graphics) is crucial

### Backend

The state of your application, including sensor data, will be managed in the backend, using C++. To communicate with QML in the UI use the appropriate [property system](https://doc.qt.io/qt-5/qtqml-cppintegration-topic.html), as described by the wiki.

There are no particular restriction on how to lay out the backend, make sure to use good software engineering practices to clearly organize your code in order to make it readable and easily updatable (example: adding a new sensor).

The data that you will organize in you application state will come from the class `Data`, which is declared in the `data.hpp` file, and exposes a signal named `dataReceived` that you will listen to using a [`slot`](https://doc.qt.io/qt-5/signalsandslots.html).

## Getting started

### Prerequisites

- `git` and a [GitHub](https://github.com) account
- C/C++ toolchain

For Debian / Ubuntu you can use:

```bash
sudo apt install build-essential
```

- [Qt installed via the Qt Online Installer](https://www.qt.io/download-qt-installer)
- Qt Creator (optional, but recommended. Can be installed with the Qt installed)

### Setup

- Download the project files [here](https://download-directory.github.io/?url=https%3A%2F%2Fgithub.com%2Feagletrt%2Frecruiting-sw%2Ftree%2Fmaster%2Fsteering_wheel)
- Create a new GitHub repository and upload the project files via git
- Start working on the task, creating git commits as you make progress
- When it's time to deliver, please send your recruiter a link to your github repository

### Building

#### Using Qt Creator

Simply press the ▶️ button.

#### Using Qt command line tools

The first time building the project:

```bash
mkdir -p build
cd build
qmake ..
make -j$(nproc)
```

This will build the executable that will be named `./steering_wheel`.

After that you can simply:

```bash
cd build
make -j$(nproc)
```