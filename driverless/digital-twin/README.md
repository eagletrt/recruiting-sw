# **E-Agle Formula Student Driverless Simulation Task**

## **Objective**
The goal of this challenge is to build a **realistic 3D vehicle simulation** using **Unreal Engine 4.26**. The simulation will feature a Formula Student-style autonomous car navigating a track using **simulated physics, and sensors logic**.

The task is divided into **three levels** of increasing complexity, with bonus challenges available for advanced candidates.

Those steps are a general guideline for the candidate to develop its own project in the field of autonomous vehicle control, the specific implementation details and decisions are up to the candidate.

---

## **Overview**
Each level introduces new challenges in vehicle control, ranging from basic kinematic modeling to advanced feedback control techniques. Candidates will earn **points** for each completed level.

| **Level** | **Task** |
|-----------|----------|
| **1**   | Set up a 3D track and vehicle in Unreal Engine |
| **2**   | Implement a physics-based vehicle model |
| **3**   | Simulate camera and LiDAR sensors |
| **Bonus** | Add dynamic obstacles and traffic | 

---

## **Task Breakdown**

### **Level 1: 3D Track and Vehicle Setup**

#### Goal:
- Create a 3D simulation scene with a vehicle and a racetrack.

#### Requirements:
- Import or build a **Formula Student-style vehicle mesh**.
- Create a **basic track** using spline meshes or imported geometry. It would be better if you could define manually the materials used, not all of them, because it would be time-exhausting, but at least a couple, just to show some understanding of how the blueprints and the material engines work.
- Add **track markers** or **cones** to visually define the path.

#### Bonus:
- Dinamically spawn the cones, using a controller.

---

### **Level 2: Physics-Based Vehicle Model**

#### Goal:
- Implement a vehicle model with **realistic dynamics**.
- Make it both controllable by the user and via code.

#### Requirements:
- Use Unreal's **Wheeled Vehicle** or **Chaos Vehicle** system.

---

### **Level 3: Simulate Perception Sensors**

#### Goal:
- Simulate **camera** and **LiDAR** sensors on the vehicle.

#### Requirements:
- Attach a **virtual camera** to simulate a front-facing RGB feed.
- Simulate a **2D/3D LiDAR** using raycasting (line traces).
- Visualize sensor data in real time (e.g., point clouds, overlays).

---

## **📅 Sumbission Guidelines**
📆 **Time Limit: 2 Weeks**


### **✅ What to Submit?**

1. Unreal project folder or a link to a GitHub repository.
2. Use Git LFS, assure that you follow the structure of Unreal Engine's projects and ensure that it can be run on other systems.
3. Brief **README** with build and run instructions.
4. Screen recording or in-simulation footage.


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
This challenge replicates the conditions of a **Formula Student simulation stack**, helping candidates demonstrate their ability to **develop and integrate vehicle models, sensors, and control logic in a 3D environment**.

Good luck, Candidate *Digital Twink*! 🧠🕹️🚗💨