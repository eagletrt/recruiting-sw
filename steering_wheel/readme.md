# Recruiting steering wheel

> ⚠️ This document is fairly technical to maintain brevity, if you have **any** questions ask your recruiter.

## Abstract

Create a racing view for a Formula 1 steering wheel ([some examples](https://duckduckgo.com/?q=steering+wheel+formula+1+screen&t=h_&iar=images&iax=images&ia=images)), displaying sensor data, speed, RPM, … generated from a virtual CAN bus interface.

## Tools required

- Linux Computer / VM
- `git` and a [GitHub](https://github.com) account
- C/C++ toolchain
- Open source Qt installation + QtQuick (QML) + QSerialBus
- `libsocketcan` and `can-utils` installed using the package manager (apt, pacman, …)
- Qt Creator (optional, but raccomended)

## Starter

