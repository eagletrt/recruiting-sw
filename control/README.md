# E-Agle TRT AS Controls Software Task

This task is a small version of what the controls software group does every day: take data from other parts of the car, decide what the car should do, and talk to the vehicle over CAN. You will drive a simulated Formula Student car down an acceleration track and stop it in the right place.

You have **2 weeks**. The code must be **C++** on **ROS 2 Humble**.

---

## 1. The scenario

The car starts at the beginning of a straight track.

- The track is 75 m long and 4 m wide.
- Blue cones are on the left, yellow cones on the right, one pair every 5 m.
- At the end there are 4 big orange cones that form a box, 10 m long. That is the stop zone.

Your job: get from the start to the stop zone as fast as you can, come to a full stop **inside** the box, and tell the car the mission is finished.

```
   blue    o     o     o     o   ...   o     O----------O
                                             |   STOP   |
   car  [=>]  - - - - - - - - - - - - - - -  |   ZONE   |
                                             |          |
   yellow  o     o     o     o   ...   o     O----------O

   x = 0                                    75 m       85 m
```

---

## 2. What we give you

| Path | What it is |
|---|---|
| `docker/Dockerfile` | The environment. ROS 2 Humble, RViz, CAN tools, everything you need. (May be extended in case extra dependencies are required, your call) |
| `can/eagle_task.dbc` | The CAN database. It describes the messages between you and the car. |
| `src/eagle_msgs` | Message definitions (`Cone`, `ConeArray`). |
| `src/eagle_sim` | The simulator: track, fake perception, vehicle, lateral controller, CAN gateway. |

Please do not modify `eagle_msgs` or `eagle_sim`. If you think something in there is broken, tell us.

---

## 3. Setting up

### The container

We give you a Dockerfile and nothing else on purpose. How you run it is up to you: plain `docker run`, docker compose, a VS Code devcontainer, whatever you like. Whatever you choose, put it in your repo so we can run it too, detailing the steps to reproduce what you've done.

Things your container will need:

- This repository mounted as the workspace. The image expects it at `/home/eagle/ws`.
- A way to show GUI windows, because you will use RViz.
- Host networking, so the container can see the CAN interface (see below).
- The `NET_ADMIN` capability if you want to create the CAN interface from inside the container.

The image is around 4 GB, so start the build early.
You need Linux or Windows with WSL2. macOS does not work for this task because Docker there cannot give you a virtual CAN interface. If a Mac is all you have, tell us **right away** and we will adjust the task for you.

### The virtual CAN bus

The car talks CAN, and since there is no real car, we use a virtual CAN interface called `vcan0`. It behaves like a real CAN bus but lives entirely in the Linux kernel.

Create it on your host (or inside the container if it has `NET_ADMIN`):

```bash
sudo modprobe vcan
sudo ip link add dev vcan0 type vcan
sudo ip link set up vcan0
```

Check that it is there:

```bash
ip link show vcan0
```

This does **not** survive a reboot. If you restart your machine (or WSL) and suddenly get `No such device` errors, this is why. Just run the three commands again.

---

## 4. The simulator

The simulator is a set of ROS nodes in the `eagle_sim` package. We include one launch file, `dev.launch.py`, that starts the simulator and RViz so you can have a first look around. It does not start any of your code. Writing your own launch file that runs everything together is part of your task (see section 7).

| Executable | What it does |
|---|---|
| `track_publisher` | Publishes the track so RViz can draw it. |
| `fake_perception` | Pretends to be the perception stack. Publishes the cones the car can currently see. |
| `vehicle_sim` | The car itself. Simulates the physics and publishes where the car is. |
| `lateral_controller` | Steers the car along the centerline **you** publish. |
| `can_gateway` | The car's side of the CAN bus. Receives your commands, sends you the speed. |

All of them should be started with the parameter file `config/track.yaml` from the `eagle_sim` package.

There is also an RViz config at `rviz/base.rviz` in the same package. It shows the track and the car and nothing else.

### What you can read

**`/perception/cones`** (`eagle_msgs/msg/ConeArray`, 10 Hz)

The cones the car sees right now.

- Positions are in the **car's frame** (`base_link`), not in the world. x is forward, y is left.
- The cones are sorted from nearest to farthest.
- Each cone has a colour: `BLUE`, `YELLOW`, `ORANGE_SMALL`, `ORANGE_BIG` (constants are in `Cone.msg`).
- The car sees up to 50 m ahead, in a 120 degree cone in front of it. Cones next to the car or behind it are not visible.

**TF: `map` -> `base_link`**

The pose of the car in the world. `base_link` is at the centre of the rear axle. The car starts at the origin of `map`, facing +x.

**CAN: `VEH_SPEED`**

The speed of the car. See section 5.

### What you must publish

**`/planning/centerline`** (`nav_msgs/msg/Path`)

The line the car should follow. Our lateral controller steers along it.

- Use any frame you like, as long as there is a TF from it to `base_link`. Set `header.frame_id` correctly.
- Keep publishing it. If the last one is older than 0.5 s the lateral controller gives up and holds the wheels straight.
- It needs points in front of the car.

### What you must not use

Everything under `/sim/...` is internal to the simulator. Some of those topics contain the answer (the true speed of the car, for example). **Do not subscribe to them in your solution.** We will check. Looking at them while debugging is fine.

---

## 5. Talking to the car: CAN

**There is no ROS topic for driving the car.** The car does not wait for a command on a topic. The only way to make it move is to send CAN frames on `vcan0`, and the only place to get its speed is from CAN frames on `vcan0`. Just like on the real car.

There are two messages. Both are defined in `can/eagle_task.dbc`.

| ID | Name | Direction | How often | Signals |
|---|---|---|---|---|
| `0x100` | `AS_CMD` | you -> car | every 10 ms | `ThrottleReq` (0 to 1), `BrakeReq` (0 to 1), `MissionFinished` (0 or 1) |
| `0x200` | `VEH_SPEED` | car -> you | every 10 ms | `VehicleSpeed` (m/s) |

How it behaves:

- `ThrottleReq` and `BrakeReq` go from 0 (nothing) to 1 (full).
- The car sits still until it receives `AS_CMD` frames with some throttle in them. There is no "go" signal. When you send throttle, it goes.
- You must keep sending `AS_CMD` every 10 ms, even if nothing changed. **If the car hears nothing for 200 ms, it slams the emergency brake**, and the brake stays on until the simulator is reset. A real car does the same thing: if the computer goes silent, stop.
- When the car is standing still inside the stop zone, send `MissionFinished = 1`. That is how you tell us you are done.

### Use the DBC, do not hand-write the bytes

A DBC file is the standard way to describe CAN messages: which bits mean what, and how to scale them. Nobody packs those bytes by hand on a real car. They generate code from the DBC.

We want you to do the same. `cantools` is installed in the image and can generate C code from the DBC.
This gives you `eagle_task.h` and `eagle_task.c`, with functions to pack, unpack, encode and decode both messages. Use that generated code in your C++ node. How you bring it into your package and your build is your decision.

Opening the socket and reading and writing frames on `vcan0` is still on you. Look up SocketCAN.

## 6. Resetting

To put the car back at the start and release the emergency brake without restarting everything:

```bash
ros2 service call /sim/reset std_srvs/srv/Trigger
ros2 service call /can_gateway/reset std_srvs/srv/Trigger
```

Your own nodes will probably need a restart too, unless you handle that yourself.

---

## 7. Your task

Create **your own ROS 2 package** (C++) in `src/`, next to ours. In it:

1. **Centerline.** Subscribe to `/perception/cones`, work out the middle of the track, and publish it on `/planning/centerline`. Remember the cones arrive in the car's frame.
2. **Speed from CAN.** Read `VEH_SPEED` from `vcan0`.
3. **Longitudinal control.** A PID controller that decides throttle and brake. Go fast, then stop inside the orange box.
4. **Commands to CAN.** Send `AS_CMD` every 10 ms, and set `MissionFinished` once you are stopped in the box.
5. **Parameters.** Gains, speeds, anything tunable goes in a YAML file, not hardcoded.
6. **Launch file.** Your own launch file, in your package. One command that starts everything: all five simulator nodes, your nodes, and RViz with your config.
7. **RViz.** Start from our `base.rviz` and make your own config that also shows what your software is doing. The centerline at least. Anything else that helps you (or us) understand what is going on is welcome.
8. **Robustness.** Handle the things that can go wrong. What does your software do if the speed stops arriving? If the cones stop arriving?
9. **Rosbag.** Record a bag of a successful run and include it.
10. **Plots.** Speed and commands over time for that run.
11. **README.** How to set up and run your solution, step by step. We will follow it literally on a clean machine.
12. **Report.** A short document (Markdown or LaTeX) about your implementation: the steps you took and the choices you made and why. This is separate from the README. The README tells us how to run it, the report tells us how you think.

How many nodes you write and how you split the work between them is your call. Tell us why you chose it.

### If you have never written a PID

A PID controller looks at the difference between what you want and what you have, and turns it into a command. Here, what you want is a target speed and what you have is the speed from CAN.

```
error  = target_speed - measured_speed

output = Kp * error
       + Ki * (sum of error over time)
       + Kd * (how fast the error is changing)
```

- **P (proportional)** reacts to the error right now. Far from the target, push hard. Close to it, push gently.
- **I (integral)** adds up the error over time. It removes the small error that P alone never quite gets rid of.
- **D (derivative)** reacts to how quickly the error changes. It calms things down when you approach the target too fast.

`Kp`, `Ki` and `Kd` are the three gains you tune. You run this at a fixed rate, and every cycle you turn `output` into a command: positive means throttle, negative means brake, both limited to the 0 to 1 range the car accepts.

That is all there is to it. Choosing the target speed, and knowing when to start slowing down for the stop zone, is the part you have to think about.

For tuning the three gains, this guide is a good place to start: [Practical PID tuning guide](https://tlk-energy.de/blog-en/practical-pid-tuning-guide).

### Nice to have

Everything above is required. These are not, but they are welcome:

- Unit tests.
- Your own lateral controller, replacing ours.

---

## 8. Handing it in

Send us a link to a git repository that contains:

- this workspace with your package added,
- your README,
- your report,
- the rosbag and the plots.

We will clone it, follow your README, and run it.

If you get stuck on the setup or think you found a bug in the simulator, write to us as usual.
