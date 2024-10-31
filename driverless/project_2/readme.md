# Eagle Driverless Control Task

## **Objective**
The goal of this challenge is to implement a **feedback controller** for a **Formula Student Driverless vehicle**. The candidate will work with **C++ and CMake** to develop a controller that allows the vehicle to follow a trajectory while maintaining stability and minimizing tracking errors.

The task is divided into **five levels** of increasing complexity, with bonus challenges available for advanced candidates.

## **Overview**
Each level introduces new challenges in vehicle control, ranging from basic kinematic modeling to advanced feedback control techniques. Candidates will earn **points** for each completed level.

| **Level** | **Task** |
|-----------|---------|
| **1** | Implement a kinematic bicycle model | 
| **2** | Make the vehicle follow a straight path | 
| **3** | Implement a Proportional Controller (P) for steering | 
| **4** | Upgrade to a PID controller for better tracking | 
| **5** | Implement Stanley or Pure Pursuit Control | 
| **Bonus** | Extend to a dynamic bicycle model with slip | 
| **Bonus** | Implement Model Predictive Control (MPC) | 

---

## **📜 Task Breakdown**

### **Level 1: Implement a Kinematic Bicycle Model**
#### **Goal:**
- Implement a **kinematic bicycle model** to simulate vehicle motion.

#### **Requirements:**
- Implement the following equations of motion:
  \[
  x_{t+1} = x_t + v \cos(\theta) dt
  \]
  \[
  y_{t+1} = y_t + v \sin(\theta) dt
  \]
  \[
  \theta_{t+1} = \theta_t + \frac{v}{L} \tan(\delta) dt
  \]
  - Where:
    - \( v \) is velocity.
    - \( \delta \) is steering angle.
    - \( L \) is wheelbase.
    - \( \theta \) is heading.

- Simulate and plot the vehicle’s movement.
- Implement a visaluzation of the vehicle trajectory in **2D** usinf **raylib or imgui**.

#### **Bonus:**
- Add **acceleration and deceleration** to the model.

---

### **Level 2: Make the Vehicle Follow a Straight Path**
#### **Goal:**
- Implement a **simple heading correction** to keep the vehicle on a straight trajectory.

#### **Requirements:**
- Introduce **small disturbances** (e.g., noise in heading axis).
- Implement a **proportional control law**:
  \[
  \delta = K_p \cdot e
  \]
  - Where \( e \) is the heading error.
- Visualize how well the controller keeps the vehicle aligned.

#### **Bonus:**
- Introduce lateral drift and correct for it.

---

### **Level 3: Implement a Proportional Controller (P) for Steering**
#### **Goal:**
- Implement a **Proportional Controller** for trajectory tracking.

#### **Requirements:**
- Generate a **smooth path** for the vehicle to follow (e.g., a straight line, a sine wave and a more complex path).
- Given a **set of waypoints** from the generated path, use a **P controller** to adjust the steering angle:
  \[
  \delta = K_p \cdot e
  \]
  - Where \( e \) is the **cross-track error** (distance from the desired path).
- Visualize the vehicle’s trajectory and the **tracking error**.
- Tune the **\( K_p \)** value for optimal performance.

#### **Bonus:**
- Implement a **path planner** to generate more complex paths (e.g., a circle or a figure-eight).

---

### **Level 4: Upgrade to a PID Controller for Better Tracking**
#### **Goal:**
- Improve path tracking accuracy using a **PID controller**.

#### **Requirements:**
- Extend the **P-controller** to a **PID controller**:
  \[
  \delta = K_p e + K_d \frac{de}{dt} + K_i \int e dt
  \]
- Implement:
  - **Derivative (D) term** to reduce oscillations.
  - **Integral (I) term** to correct steady-state errors.
- Tune the **PID gains** to **minimize tracking error**.

#### **Bonus:**
- Test the PID controller on a **sharper track layout** (e.g., a chicane).

---

### **Level 5: Implement an Advanced Controller (25 Points)**
#### **Goal:**
- Implement **Stanley Control or Pure Pursuit Control**.

#### **Option 1: Stanley Controller**  
- Control law:
  \[
  \delta = \theta_e + \tan^{-1} \left( \frac{K e}{v} \right)
  \]
  - Where:
    - \( e \) is the cross-track error.
    - \( \theta_e \) is the heading error.

#### **Option 2: Pure Pursuit Controller**
- Control law:
  \[
  \delta = \tan^{-1} \left(\frac{2 L y}{L_d^2} \right)
  \]
  - Where:
    - \( y \) is the lookahead point.
    - \( L_d \) is the lookahead distance.

#### **Bonus:**
- Test different controller parameters and plot the **tracking performance** over time.

---

## **🎯 Bonus Challenges**
🏆 **Extend to a Dynamic Bicycle Model**  
- Implement a **dynamic bicycle model** with:
  - Tire slip angles.
  - Lateral forces.
  - Understeer/oversteer behavior.

🏆 **Implement Model Predictive Control (MPC)**  
- Formulate the control problem as an **optimization problem**.
- Use an **MPC solver (e.g., CasADi)** to predict the vehicle’s future states.

---

## **📅 Submission Guidelines**
📆 **Time Limit: 2 Weeks**

### **✅ What to Submit?**
1. **Code repository (GitHub or zip)**
2. **CMakeLists.txt for easy compilation**
3. **Short report (PDF or Markdown) covering:**
   - Approach used
   - Controller tuning strategy
   - Challenges faced
4. **Simulation results** (plots or animations of the vehicle path).

---

## **🏆 Evaluation Criteria**
✅ **Completion:** Are all levels completed?  
✅ **Code Quality:** Is the code **structured, readable, and documented**?  
✅ **Controller Performance:** Does the vehicle follow the path accurately?  
✅ **Efficiency:** Is the controller computationally efficient?  
✅ **Creativity:** Did the candidate experiment with **different approaches or optimizations**?  

---

## **💡 Final Notes**
This task simulates **real-world autonomous vehicle control problems**. Candidates should **experiment with different techniques, optimize controller performance, and deliver a structured, well-documented solution**.

Good luck, future Driverless Engineers! 🚗💨

