# E-Agle TRT AS Perception Software Task

This task is a small version of what the perception software group does every day: take raw sensor data from the car and turn it into something the rest of the autonomous system can use. You will work with a LiDAR recording of a vehicle driving a lap, and build a ROS 2 node that makes sense of it.

You have **2 weeks**. The code must be **C++** on **ROS 2 Humble**.

---

## 1. The scenario

A driverless car drives one lap of a small track marked with cones. A LiDAR on the car records everything it sees. You get that recording as a ROS 2 bag.

You pick **one** of two paths. Both use the same recording.

| | Path A: Cone detection | Path B: Odometry |
|---|---|---|
| Goal | Find the cones in every scan and say where they are | Work out how the car moved over the whole lap |
| Typical steps | Remove the ground, group the remaining points, decide what is a cone, estimate its position | Remove the ground, downsample, align each scan with the previous ones, chain the motion together |
| Output | Cone positions in the vehicle frame | The pose of the car over time |

Pick the one that interests you more. Neither is the "easy" one.

---

## 2. What we give you

| Path | What it is |
|---|---|
| `docker/Dockerfile` | The environment. ROS 2 Humble, RViz, PCL, Eigen and the usual build tools. (May be extended in case extra dependencies are required, your call) |
| The bag | The LiDAR recording. Too big for git, download it here (zip, 185 MB) and unzip it: [link](https://drive.google.com/file/d/1HqndNg_hM8jUir8dcPa35IBpF1yGo5Ck/view?usp=sharing)|

That is all. There is no package skeleton. Creating the workspace and the packages is part of the task.

---

## 3. Setting up

We give you a Dockerfile and nothing else on purpose. How you run it is up to you: plain `docker run`, docker compose, a VS Code devcontainer, whatever you like. Whatever you choose, put it in your repo so we can run it too, detailing the steps to reproduce what you've done.

Things your container will need:

- Your workspace mounted. The image expects it at `/home/eagle/ws`.
- The bag somewhere it can read it.
- A way to show GUI windows if you want to use RViz, and you probably do.

The image is around 4 GB, so start the build early.

---

## 4. The data

The bag holds about 34 seconds of driving: one lap, starting from standstill and ending just past the start line.

### `/lidar/points` (`sensor_msgs/msg/PointCloud2`, 10 Hz)

One message per LiDAR scan, around 35 000 points each.

- The sensor is a spinning LiDAR with 48 beams that sees all around the car.
- Every point has `x`, `y`, `z` in metres, an `intensity` (how strongly the surface reflected the laser, 0 to 255) and a `ring` (which of the 48 beams it came from, 0 is the lowest).
- The points are in the **sensor's frame** (`lidar`), not the vehicle's.
- All points of a scan belong to the timestamp in its header. You do not need to correct for the car moving during a scan.

### `/tf_static`

The transform from the vehicle frame (`base_link`) to the sensor frame (`lidar`). The sensor is not mounted at the vehicle origin and it is not perfectly level, so you will need this.

`base_link` is at the centre of the rear axle, on the ground. x is forward, y is left, z is up.

### What is not in the bag

- Where the car is. That is the whole point of path B.
- Where the cones are. That is the whole point of path A.
- Any other ground truth. 

### Things worth knowing

- The cones are standard Formula Student cones. Small ones are 228 mm wide at the base and 325 mm tall. Big orange ones are 285 mm wide and 505 mm tall.
- Blue cones are on the left of the track, yellow cones on the right. Big orange cones mark the start line.
- Blue cones have a white stripe, yellow cones have a black stripe, orange cones have white stripes. Stripes reflect the laser differently from the rest of the cone.
- The track is not in an empty field. There are buildings, barriers, people and other things around it.
- The ground is flat and nothing in the scene moves except the car.
- The messages are big. Subscribe with the default (reliable) QoS. With a best effort subscription you will silently lose most of the scans.

---

## 5. Your task

Create a ROS 2 workspace with **at least two packages**, and solve one of the two paths in it.

### For both paths

1. **Interface package.** A package (`ament_cmake` + `rosidl`) that defines your own messages. What goes in it depends on your path, see below.
2. **Node package.** A C++ (`rclcpp`) package with a node that subscribes to `/lidar/points` and publishes its results.
3. **Frames and time.** Use `/tf_static` to get from the sensor to the vehicle. Stamp everything you publish with the time of the scan it came from, not the time you finished computing.
4. **Parameters.** Every threshold and tunable number is a ROS parameter loaded from a YAML file. Nothing hardcoded.
5. **Launch file.** One launch file that starts your node with its parameters.
6. **Visualization.** Publish your results as `visualization_msgs/msg/MarkerArray` as well, so they can be seen in RViz on top of the point cloud.
7. **Processing time.** Measure how long you take per scan and publish it for every scan in a message of your own, defined in your interface package. Report the numbers. The car produces a scan every 100 ms, so that is the budget in real life.
8. **README.** How to set up and run your solution, step by step. We will follow it literally on a clean machine.
9. **Report.** A short document (Markdown or LaTeX) about your implementation: your approach, the problems you ran into and how you solved them, what could be improved, and screenshots or GIFs of the results. This is separate from the README. The README tells us how to run it, the report tells us how you think.
10. **Git.** Work in git from the first day and commit as you go. Small commits that each do one thing, with messages that say what changed and why. We read the history, not just the final state, and one giant commit at the end tells us nothing about how you work. Keep generated files out of the repo (`build/`, `install/`, `log/`): a `.gitignore` is expected.
11. **Code quality.** Write the code for the person who has to read it next. Clear names, small functions, a structure that makes sense, no dead code or commented-out experiments left behind, and a build without warnings.

### Path A: Cone detection

Detect the cones in each scan and publish where they are.

- Topic: `/perception/cones`
- Message: your own cone array message. It must have a `header` and a list called `cones`, where each cone has a `position` of type `geometry_msgs/Point`. Anything else you add is up to you.
- Positions are in the **vehicle frame** (`base_link`). A cone's position is the centre of the cone on the ground, not the middle of the points you happened to see.
- Not everything that sticks out of the ground is a cone.

### Path B: Odometry

Estimate how the car moves through the whole recording by aligning the scans with each other.

- Topic: `/odometry` (`nav_msgs/msg/Odometry`), from frame `odom` to `base_link`. Also broadcast the same thing on TF.
- The car starts at the origin of `odom`, facing +x.
- One message per scan.
- The car drives a full lap and passes the start line again at the end. A good estimate ends up where the track says it should.

### Nice to have

Everything above is required. These are not, but they are welcome:

- **Path A:** tell blue cones from yellow ones using the intensity of the points.
- **Path B:** build one point cloud map of the whole track from all the scans and your estimated poses.
- **Either path:** make your parameters changeable while the node is running, so you can tune without restarting.

---

## 6. Handing it in

Send us a link to a git repository that contains:

- your workspace with your packages,
- whatever you used to run the container,
- your README,
- your report.

Do not commit the bag. 

We will clone it, follow your README, and run it.

If you get stuck on the setup or think something is wrong with the data, write to us as usual.

## AI Usage

Include an honest table describing how you used AI tools (e.g., Claude, ChatGPT, Gemini, Copilot) during the project: which tool, and what for (explaining a concept, writing or debugging code, drafting text, etc.).

| Tool | What it was used for |
|------|----------------------|
| e.g. Claude | Explained how X works |
| e.g. Gemini | Generated the parsing function in `utils.cpp` |

Please be transparent: AI use is allowed, but undisclosed use will be noticed.