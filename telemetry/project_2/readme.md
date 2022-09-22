# Project 2

> ⚠️ This document is fairly technical to maintain brevity, if you have **any** questions ask your recruiter or come visit us at floor -2 of Povo 2.

## Abstract

Build the most basic and crucial part of a telemetry software: logging every information received.

The functions in **fake_receiver.h** will simulate an interface to CAN bus (protocol used in automotive to share data between ECUs). The data received must be parsed and then eventually logged.

You will implement a basic [Finite State Machine](#finite-state-machine) with Idle and Run states, both in Idle and Run you will receive data from "CAN" and [Parse](#parsing) them. Two specific messages will trigger a state transition. Only in Run state the telemetry will log the data. Then with the parsed messages compute some basic [statistics](#statistics).

So the requirements are:

- [Finite State Machine](#finite-state-machine)
- [Logging](#logged-file)
- [Parse](#parsing)
- [statistics](#statistics)

**_Message example_**

```CAN
0A0#6601
```

### Finite State Machine

Use a state machine architecture to separate the functionalities in Idle and Run state.

#### Idle

Receive messages and parse them, when you receive the start message transition to Run state. This defines that a new session is started.

#### Run

Receive and parse messages, save the raw messages in a file (each new session must have a different file). If you receive the stop message, then close the file and transition back to Idle.

#### Extra states

If you want you can add some extra states. Is not required.

### Logged file

The output file will have a line for each message received prepended with the timestamp at wich the message was received.

```CAN
// received message
0A0#6601

// logged message
(unix_timestamp) 0A0#6601
```

Each session must have a unique filename.

### Start and Stop messages

```CAN
// Start
0A0#6601
0A0#FF01

// Stop
0A0#66FF
```

The start messages will be two, if one of them is received then transition to Run. If you are already in run, then do nothing.

### Parsing

You need to parse the received messages. **Don't** simply match string by string.

Message description:

```CAN
0A0#6601
```

The message is composed by ID and payload.
The string received is formatted as **_\<ID>#\<PAYLOAD>_**.

#### ID

In the example is **_0A0_**, it is expressed in hexadecimal, so it represent 160 in decimal base. This field is at most 12 bits, use a uin16_t to represent it.

#### Payload

It is composed by at most 8 bytes, each composed by 2 chars in hexadecimal. So in the example there are only 2 bytes:

```CAN
// first example
6601

66 -> first byte  -> 102 in decimal
01 -> second byte -> 1 in decimal

// second example
90291
this is a nonvalid payload as the number of chars is not even.
```

### Statistics

For each message ID, compute the statistics of the elapsed time beween messages of the same ID.

Compute the mean time (in milliseconds) between each message. Note that message frequencies are different for each ID. Each time the FSM transitions to Stop, your script must save a [CSV](https://it.wikipedia.org/wiki/Comma-separated_values) containing the computed values (in number):

|ID|number_of_messages|mean_time|
|-:|-:|-:|
|0A0|1|100|
|181|100|0.01|

## Getting started

### Prerequisites

- `git` and a [GitHub](https://github.com) account
- C/C++ toolchain, with CMake

For Debian / Ubuntu you can use:

```bash
sudo apt install build-essential cmake
```

### Setup

- Download the project files [here](https://download-directory.github.io/?url=https%3A%2F%2Fgithub.com%2Feagletrt%2Frecruiting-sw%2Ftree%2Fmaster%2Ftelemetry%2Fproject_2)
- Create a new GitHub repository and upload the project files via git
- Start working on the task, creating git commits as you make progress
- When it's time to deliver, please send your recruiter a link to your github repository

### Building

The project contains a CMakeLists.txt with a basic setup to build the project.

The first time building the project:

```bash
mkdir -p build
cd build
cmake ..
make -j$(nproc)
```

This will build the executable that will be located in `./bin` directory.
