# **E-Agle Formula Student Driverless Simulation Task**
### **Version 1 – C++ with raylib (2D Simulation + ZeroMQ Sensor Stream)**

## **Objective**
The goal of this challenge is to design and implement a **2D driverless vehicle simulation** using **C++ and raylib**, integrating **sensor simulation** and real-time **data publishing over ZeroMQ topics**. This setup simulates a realistic autonomy pipeline where sensor data is streamed to perception and control modules.

Those steps are a general guideline for the candidate to develop its own project in the field of autonomous vehicle simulation, the specific implementation details and decisions are up to the candidate.

---

## **Overview**
Each level introduces new challenges in simulation, ranging from basic vehicle modeling to advanced sensor simulations. Candidates will earn **points** for each completed level.

| **Level** | **Task** |
|-----------|---------|
| **1**   | Set up a raylib simulation window with a basic track | 
| **2**   | Implement a kinematic bicycle model | 
| **3**   | Render the vehicle, track, and waypoints |
| **4**   | Simulate a virtual sensor and publish data on ZeroMQ | 
| **5**   | Implement a path-following controller | 
| **Bonus**     | Add obstacles and collision detection |
| **Bonus**     | Replace with a physics-based bicycle model |

## **📈 Challenge Structure**

| **Level** | **Task** | **Points** |
|-----------|----------|------------|

---

## **Task Breakdown**

### **Level 1: Simulation Setup and Track Rendering**

#### Goal:
- Create a simulation window using raylib.
- Draw a simple 2D race track and visualization elements.

#### Requirements:
- Initialize a raylib window (`InitWindow`).
- Draw the track boundaries using `DrawLine()` or `DrawRectangle()`.
- Draw static waypoints as small circles on the track.

#### Bonus:
- Load the track from a **CSV or JSON file** for flexible layouts.

---

### **Level 2: Implement a Kinematic Bicycle Model**

#### Goal:
- Model the vehicle’s motion using basic kinematic equations.

#### Requirements:
- Implement the kinematic bicycle model:
  \[
  x_{t+1} = x_t + v \cos(\theta) \cdot dt
  \]
  \[
  y_{t+1} = y_t + v \sin(\theta) \cdot dt
  \]
  \[
  \theta_{t+1} = \theta_t + \frac{v}{L} \tan(\delta) \cdot dt
  \]
- Allow basic manual inputs (arrow keys) to test motion.

#### Bonus:
- Display velocity, heading, and steering angle as an on-screen HUD.

---

### **Level 3: Visualize Vehicle and Path**

#### Goal:
- Render the vehicle and trajectory on-screen.

#### Requirements:
- Draw the vehicle as a triangle or rectangle.
- Update orientation based on heading.
- Display the current path and previously visited points.

#### Bonus:
- Add camera movement (panning or zooming) to follow the car.

---

### **Level 4: Simulate Virtual Sensor and Publish via ZeroMQ**

#### Goal:
- Simulate a basic virtual sensor and publish its output to a **ZeroMQ PUB socket**.

#### Requirements:
- Choose one of the following sensors:
  - **LiDAR**: Cast multiple rays from the vehicle and compute intersections with track edges.
  - **Camera**: Simulate a viewport around the car (e.g., cropped image or data array).
- Package sensor data into a **JSON or Protobuf structure**.
- Publish data over a **ZeroMQ PUB socket** on a named topic (e.g., `"sensor.lidar"` or `"sensor.camera"`).
- Implement a test **ZeroMQ SUB client** to receive and print the sensor data.

#### Bonus:
- Add **noise**, configurable **update rate**, and **sensor range** limits.

---

### **Level 5: Implement a Path-Following Controller**

#### Goal:
- Make the vehicle follow a predefined trajectory autonomously.

#### Requirements:
- Implement a **Pure Pursuit** or **Stanley** controller.
- Use the waypoints to compute the desired steering angle.
- Visualize the actual vs. desired trajectory.

#### Bonus:
- Plot tracking error in real-time as a debug graph.

---

## **Bonus Challenges**

### Add Obstacles and Collision Detection
- Introduce obstacles (static or dynamic) on the track.
- Detect collisions and update vehicle behavior accordingly.

---

### Replace with a Physics-Based Bicycle Model
- Extend the model to simulate:
  - Lateral tire slip
  - Steering dynamics
  - Realistic velocity/acceleration behavior

---

## **📅 Submission Guidelines**
📆 **Time Limit: 2 Weeks**

### **✅ What to Submit?**
1. **Code repository (GitHub or zip)**
2. **CMakeLists.txt for easy compilation**
3. **Short report (PDF or Markdown) covering:**
   - Approach used
   - Functionality and sensors implemented
   - Challenges faced
4. **Simulation results** (screenshots or recordings of the working simulator).

---

## **🏆 Evaluation Criteria**
The goal of this task is to evaluate the ability of the candidate of solving problems and investigating new areas of study, it is not mandatory to complete all the points.
The criteria above are general guidelines for a good delivery, the **main criteria** on which the candidate will be evaluated is the **effort** put in the development of the project (even if it is not fully working).

✅ **Completion:** Are all levels completed?  
✅ **Code Quality:** Is the code **structured, readable, and documented**?  
✅ **Simulator Usability:** Can the simulator used to test different perception or control algorithms?
✅ **Creativity:** Did the candidate experiment with **different sensors and approaches**?  

---

## **📌 Final Notes**
This simulation will serve as the **foundation** for later modules in the driverless stack: perception, planning, and control. The integration of **ZeroMQ messaging** reflects how real-world robotic systems are built with modular, distributed components.

Good luck, Simulation Engineer! 🚗📡💨