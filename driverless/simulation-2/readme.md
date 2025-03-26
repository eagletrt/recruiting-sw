# **E-Agle Formula Student Driverless Simulation Task**
### **Version 2 – Unreal Engine (3D Simulation)**

## **Objective**
The goal of this challenge is to build a **realistic 3D driverless vehicle simulation** using **Unreal Engine**. The simulation will feature a Formula Student-style autonomous car navigating a track using **simulated physics, sensors, and control logic**.

The task is divided into **four levels** of increasing complexity, with bonus challenges available for advanced candidates.

Those steps are a general guideline for the candidate to develop its own project in the field of autonomous vehicle control, the specific implementation details and decisions are up to the candidate.

---

## **Overview**
Each level introduces new challenges in vehicle control, ranging from basic kinematic modeling to advanced feedback control techniques. Candidates will earn **points** for each completed level.

| **Level** | **Task** |
|-----------|----------|
| **1**   | Set up a 3D track and vehicle in Unreal Engine |
| **2**   | Implement a physics-based vehicle model | 
| **3**   | Simulate camera and LiDAR sensors |
| **4**   | Make the vehicle follow an autonomous path |
| **Bonus**     | Add dynamic obstacles and traffic | 
| **Bonus**     | Export telemetry data for analysis |

---

## **Task Breakdown**

### **Level 1: 3D Track and Vehicle Setup**

#### Goal:
- Create a 3D simulation scene with a vehicle and a racetrack.

#### Requirements:
- Import or build a **Formula Student-style vehicle mesh**.
- Create a **basic track** using spline meshes or imported geometry.
- Add **track markers** or **cones** to visually define the path.

#### Bonus:
- Load the track layout from an external **CSV or JSON** file.

---

### **Level 2: Physics-Based Vehicle Model**

#### Goal:
- Implement a vehicle model with **realistic dynamics**.

#### Requirements:
- Use Unreal's **Wheeled Vehicle** or **Chaos Vehicle** system.
- Configure:
  - Mass, suspension, torque curve
  - Tire friction and slip
  - Steering response

#### Bonus:
- Implement **aerodynamic effects** (drag, downforce).

---

### **Level 3: Simulate Perception Sensors**

#### Goal:
- Simulate **camera** and **LiDAR** sensors on the vehicle.

#### Requirements:
- Attach a **virtual camera** to simulate a front-facing RGB feed.
- Simulate a **2D/3D LiDAR** using raycasting (line traces).
- Visualize sensor data in real time (e.g., point clouds, overlays).

#### Bonus:
- Export sensor data (e.g., images, point cloud arrays) to disk or via **ZeroMQ**.

---

### **Level 4: Autonomous Path Following**

#### Goal:
- Implement a control algorithm to follow a path autonomously.

#### Requirements:
- Implement one of the following:
  - **Pure Pursuit**
  - **Stanley Controller**
  - **Model Predictive Control (MPC)**
- Use the simulated sensor data or known map to follow the track.
- Visualize the planned and executed path.

#### Bonus:
- Plot **cross-track error** and export lap time metrics.

---

## **Bonus Challenges**

### Add Dynamic Obstacles and Traffic 
- Introduce moving vehicles or objects on the track.
- Implement **basic interaction logic** (e.g., collision handling, evasion).

---

### Export Telemetry Data 
- Log vehicle telemetry data (e.g., position, speed, steering angle) in real time.
- Export to **CSV**, **JSON**, or **stream using ZeroMQ**.

---

## **📅 Sumbission Guidelines**
📆 **Time Limit: 2 Weeks**


### **✅ What to Submit?**

1. Unreal project folder or a link to a GitHub repository.
2. Brief **README** with build and run instructions.
3. Short **report** (Markdown or PDF) including:
    - Implemented features
    - Control approach
    - Bonus tasks
4. Optional: screen recording or in-simulation footage.


---

## **📊 Evaluation Criteria**

The goal of this task is to evaluate the ability of the candidate of solving problems and investigating new areas of study, it is not mandatory to complete all the points.
The criteria above are general guidelines for a good delivery, the **main criteria** on which the candidate will be evaluated is the **effort** put in the development of the project (even if it is not fully working).

✅ **Completion:** Are all levels completed?  
✅ **Code Quality:** Is the code **structured, readable, and documented**?  
✅ **Simulator Usability:** Can the simulator used to test different perception or control algorithms?
✅ **Creativity:** Did the candidate experiment with **different sensors and approaches**?  

---

## **📌 Final Notes**
This challenge replicates the conditions of a **Formula Student Driverless simulation stack**, helping candidates demonstrate their ability to **develop and integrate vehicle models, sensors, and control logic in a 3D environment**.

Advanced candidates may integrate the simulation with **UnrealCV**, or **ZeroMQ** to simulate real autonomy pipelines.

Good luck, Simulation Engineer! 🧠🕹️🚗💨