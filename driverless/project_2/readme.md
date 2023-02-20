# Project 2

> ⚠️ This document is fairly technical to maintain brevity, if you have **any** questions ask your recruiter or come visit us at floor -2 of Povo 2.

## Abstract

You are tasked with estimate the rough pixel-coordinates motion between subsequent frames of a [video](https://drive.google.com/file/d/1JKEB5-I1O6TLbAkb223dl69tdJloUgxu/view?usp=sharing).

For this task you are required to extract feature points in subsequent frames, and to match corresponding keypoints between them, the requirement that you have is precision and the real time-ness of the process (loose requirement depending on the capabilities of your machine, 10 fps can be considered good, 0.5 fps cannot).

Keep in mind that we are interested in the motion of the platform, not of the static objects in the scene.

In order to continue with the processing chain you are required to produce, at compute time, a CSV file containing some statistics about the matching process, in particular, the computed homography between subsequent frames based on the filtered and matched keypoints, average and std of both distance (in pixel) and angle (in radiants) of matched keypoints (vector connecting the keypoint with the corresponding matchin pixel coordinates), you are also required to briefly describe each step of your processing and the reasoning behind it.

The process can be briefly summarized as
- Extract keypoints
- Match keypoints
- Filter keypoints
- Produce statistics
    
## To provide

The code you implemented 
The CSV file described before
You are furthermore required to be able to explain your implementation choices if asked to. 

## Useful material

[Resource 1](https://ieeexplore.ieee.org/document/4362878)
[resource 2](https://ieeexplore.ieee.org/document/8346440)
		
## Note

While surely it's not discouraged, you are not required to implement each step from scratch, we're not here to re-invent the wheel, choose a commonly available library to perform the various steps and, most importantly, be able to justify your choices if asked to.