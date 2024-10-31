# E-Agle Formula Student Driverless Perception Task

## **Objective**  
The goal of this task is to implement a **perception module** for a **Formula Student Driverless vehicle**. The candidate will work with **C++, OpenCV, and CMake** (or alternatively **PCL for LiDAR data**) to process and extract meaningful information from sensor inputs, simulating a **perception pipeline for an autonomous racing car**.  

## **Overview**  
Candidates will progressively complete tasks of increasing complexity, earning **points** for each successfully implemented feature.  
The challenge consists of **five levels** plus bonus tasks.  

| **Level** | **Task** | 
|-----------|---------|
| **1** | Load and display an image or LiDAR dataset | 
| **2** | Apply edge detection to extract track boundaries | 
| **3** | Detect the racing line and track edges | 
| **4** | Identify and classify cones on the track | 
| **5** | Generate an optimal trajectory using perception data | 
| **Bonus** | Process 3D point clouds to detect cones (PCL) | 
| **Bonus** | Visualize the perception pipeline in an interactive GUI | 

---

## **📜 Task Breakdown**

### **Level 1: Load and Display an Image or LiDAR Data (10 Points)**
#### **Goal:**  
- Load a **track image** (for the OpenCV version) or a **LiDAR point cloud** (for the PCL version).  
- Display the loaded data for visualization.  

#### **Requirements:**  
- C++ program that reads an input **image (PNG/JPG)** or **LiDAR dataset (PCD/CSV)**.  
- Use **OpenCV (`cv::imshow`)** to display images, or **PCL (`pcl::visualization::PCLVisualizer`)** for point clouds.  

#### **Bonus:**  
- Print **metadata** such as image dimensions, channels, or LiDAR point count.  

---

### **Level 2: Detect Track Boundaries (15 Points)**
#### **Goal:**  
- Apply **edge detection** to extract the track's boundaries.  

#### **Requirements:**  
- Convert image to **grayscale** and apply **Canny or Sobel edge detection**.  
- Display detected edges overlaid on the original image.  
- For LiDAR: Filter and visualize only the **ground points** (e.g., use a height threshold).  

#### **Bonus:**  
- Use **adaptive thresholding** to improve edge detection robustness.  

---

### **Level 3: Extract Racing Line and Track Edges (20 Points)**
#### **Goal:**  
- Identify the **racing line** and **track edges** using contours or line detection.  

#### **Requirements:**  
- Apply **Hough Line Transform** (`cv::HoughLinesP`) or **contour detection** (`cv::findContours`).  
- Highlight detected track edges and approximate the **racing line**.  
- For LiDAR: Cluster ground points and fit **a track boundary model**.  

#### **Bonus:**  
- Export track edges as a **CSV file** for further processing.  

---

### **Level 4: Cone Detection (20 Points)**
#### **Goal:**  
- Detect and classify **blue and yellow cones** from the track image.  

#### **Requirements:**  
- Convert the image to **HSV color space**.  
- Use **`cv::inRange`** to segment blue and yellow objects.  
- Draw bounding boxes around detected cones.  
- For LiDAR: Apply **DBSCAN clustering** to separate objects in the point cloud.  

#### **Bonus:**  
- Output cone **positions (x, y coordinates)** to a file.  

---

### **Level 5: Generate an Optimal Trajectory (25 Points)**
#### **Goal:**  
- Compute an **optimal path** based on detected cones and track boundaries.  

#### **Requirements:**  
- Use detected **cones or edges** to compute the vehicle’s **midline trajectory**.  
- Fit a **smooth curve** (e.g., polynomial or spline).  
- Output the computed **trajectory coordinates**.  

#### **Bonus:**  
- Implement **dynamic path smoothing** using interpolation.  

---

## **🎯 Bonus Challenges**
🏆 **Process 3D LiDAR Data (10 Points)**  
- Instead of images, use **PCL (Point Cloud Library)** to:  
  - Load a `.pcd` file or `.csv` containing LiDAR points.  
  - Filter out **ground points**.  
  - Cluster and **detect cones using DBSCAN or k-means**.  

🏆 **Build an Interactive GUI for Debugging (10 Points)**  
- Create an **OpenCV interface** where:  
  - The user can adjust thresholds dynamically.  
  - Processed outputs update in real-time.  

---

## **📅 Submission Guidelines**
📆 **Time Limit: 2 Weeks**  

### **✅ What to Submit?**  
1. **Code repository (GitHub or zip)**  
2. **CMakeLists.txt for easy compilation**  
3. **Short report (PDF or Markdown) covering:**  
   - Approach used  
   - Challenges faced  
   - Possible improvements  
4. **Screenshots or GIFs** showcasing results  

---

## **🏆 Evaluation Criteria**
✅ **Completion:** Have all levels been completed?  
✅ **Code Quality:** Is the code **well-structured, modular, and documented**?  
✅ **Accuracy:** How well does the system detect cones and track edges?  
✅ **Efficiency:** Is the pipeline optimized for real-time performance?  
✅ **Creativity:** Did the candidate explore **new approaches or enhancements**?  

🎯 **Exceptional candidates may be invited for an interview and potential recruitment into the team!**  

---

## **💡 Final Notes**
This challenge simulates **real-world perception tasks** for an autonomous Formula Student car. Candidates should **experiment with different techniques, optimize performance, and deliver a structured, well-documented solution**.  

Good luck, future Driverless Engineers! 🚗💨  

