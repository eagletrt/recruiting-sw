## **E-Agle Formula Student Driverless Perception Task**

### **Objective**  
The goal of this task is to implement a **perception module** for a **Formula Student Driverless vehicle**. You will work with **C++, CMake, OpenCV**, and/or **PCL** to process sensor inputs, extracting meaningful information to simulate a **perception pipeline for an autonomous racing car**. You should also use **git** effectively to keep track of the changes that occur through the different stages of your work.

The challenge consists of **five levels** plus an additional bonus tasks. You are required to choose between **either Image or LiDAR processing tasks**, and complete all levels focusing on the choice made prior. For the Image path, levels 1 - 4 need to be completed relying on **frame_1.png**, whereas level 5 requires the usage of **both frame_1 and frame_2**. As for the LiDAR path, levels 1 - 4 should be completed using **cones.pcd**, while level 5 should be tackled using **first.pcd and second.pcd** .


| **Level** | **Task** |
|-----------|----------|
| **1** | Load, display, and preprocess image or LiDAR data |
| **2** |  Detect cones  |
| **3** | Classify objects (cones or obstacles) in the scene  |
| **4** | Extract track edges or racing line |
| **5** | Perform odometry using image or LiDAR data |
| **Bonus** | Implement interactive visualization for debugging |

---

## **📜 Task Breakdown**

### **Level 1: Load and Display Captured Data**
#### **Goal:**
- **Image Version:** Load and display an image of the racetrack.
- **LiDAR Version:** Load and display a 3D point cloud dataset from a LiDAR sensor.

**Steps:**
- **For image:** Use **OpenCV** (for image) or **PCL** (for point cloud) to load the data.
- **For LiDAR:** Display the raw data using **OpenCV** or visualize the point cloud using **PCL visualizer**.

---

### **Level 2: Cone Detection**
#### **Goal:**  
- **Image Version:** Detect cones from the image. and classify them according to color.
- **LiDAR Version:** Extract points corresponding to objects in the scan. and classify them as either cones or obstacles on the track.

**Steps:**
- **For image:** Apply geometry and color thresholding or machine learning-based classifiers (e.g., **SVM** or **CNN**) to detect cones.
- **For LiDAR:** Use clustering and classification algorithms (e.g., **K-Means**, **DBSCAN**) to detect from the point cloud.

---

### **Level 3: Object Classification**
#### **Goal:**  
- **Image Version:** Classify the cones obtained from the previous step based on their color.
- **LiDAR Version:** Classify the objects obtained previously as either cones or general obstacles.

**Steps:**
- **For image:** Use color segmentation techniques or machine learning-based classifiers as the previous point to infer the class of the cone.
- **For LiDAR:** Use point cloud geometry fitting such as **RANSAC** to determine the shape, or perform **ICP** using an ideal cone model to infer its shape.

---

### **Level 4: Extract Track Edges**
#### **Goal:**  
- **Image Version:** Identify the track edges or lines that define the path of the track based on the cones.
- **LiDAR Version:** Identify the **racing line** based on cone positions.

**Steps:**
- **For image:** Rely on cone classification to determine the track.
- **For LiDAR:** Use clustering algorithms (e.g., **RANSAC**) to fit lines to detected cone clusters or boundaries, helping to define the racing line.

---

### **Level 5: Odometry**
#### **Goal:**  
- **Image Version:** Given two images, perform a pose estimation using feature extraction algorithms.
- **LiDAR Version:** Given two point clouds, perform a pose estimation relying on registration algorithms.

**Steps:**
- **For image:** Extract key features from the two images using feature detection algorithms such as **ORB** and match them with descriptor matchers like **Brute Force**. Make sure to use as the intrinsics matrix for this task

```
K = [387.3502807617188, 0,                 317.7719116210938,
     0,                 387.3502807617188, 242.4875946044922,
     0,                 0,                 1                ]
```

- **For LiDAR:** Use a point cloud registration algorithm like **ICP (Iterative Closest Point)** to align the two point clouds, and extract the relative transformation between the two. 

---

## **🎯 Bonus Challenges**
🏆 **Interactive Visualization for Debugging**  
- **Task:** Build an interactive interface to visualize the pipeline described above.  
- Create a GUI where the user can adjust parameters dynamically (e.g., thresholds for cone detection, edge detection). The processed results should update in real-time as the parameters change.

---

## **📅 Submission Guidelines**
📆 **Time Limit: 2 Weeks**

### **✅ What to Submit?**
1. **Code repository (GitHub)**
2. **CMakeLists.txt for easy compilation**
3. **Short report (PDF or Markdown) covering:**
   - Approach used for each task.
   - Challenges faced and how they were overcome.
   - Any possible improvements or optimizations.
4. **Screenshots or GIFs showcasing results** (especially for interactive GUI)

---