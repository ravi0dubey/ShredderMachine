# Hand Detection in ShredderMachine



## Problem Statement

Shredder machine is a useful but dangerous tool which should be handled with care. Most warehouse/workshop uses shredder machine to shred different kind of waste product, ranging from paper, bottles to heavy equipment </br>
Warehouses/workshop often has the risk of machine handler unknowlingly putting their hand closer to Machine which results in grave injuries.

![img1](https://github.com/ravi0dubey/ShredderMachine/assets/38419795/8e3cbcbe-3a52-4ff2-8e2e-d6b3a4563c8b)


## Solution Proposed

Deep Learning is used to warn the machine handler if their hand/fingers are closer to shred machine. A camera is placed over the machine which is monitoring the hand of machine handler. There are 2 lines on machine, first line act as a warning and  </br>
second line if crossed, machine will stop automatically inorder to prevent the injuries.

The model is trained on SSD mobile net, the data was collected from a recording of 24 hours of workers working with the shredder. The data was then augmented and validated using Data augmentation techniques. The data was then annotated and trained using faster RCNN and Mobilenet SSD model, as Mobile net gave better results it was chosen for productionizing.The code is available in master branch of the repository.


## Tech Stack Used
Python </br>
mobilenet-ssd model </br>

The **mobilenet-ssd model** is a Single-Shot multibox Detection (SSD) network intended to perform object detection. This model is implemented using the Caffe* framework. I am using custom trained model.

MobileNet is a CNN architecture model for Image Classification and Mobile Vision. It has very little computation power to run or apply transfer learning which makes it a perfect fit for Mobile devices, embedded systems, and computers without GPU or low computational efficiency without compromising significantly with the accuracy of the results. If we combine both the MobileNet architecture and the Single Shot Detector (SSD) framework, we arrive at a fast, efficient deep learning-based method to object detection. 
The MobileNet SSD was first trained on the COCO dataset (Common Objects in Context).

Hence Mobilenet-SSD model was used in this project for faster object detection.



![image](https://github.com/ravi0dubey/ShredderMachine/assets/38419795/824776e4-5506-4fbd-b363-72bca9a53204)

## Accuracy
![image](https://github.com/ravi0dubey/ShredderMachine/assets/38419795/69253758-a67e-46e6-b45e-9655616cc193)


## How to run  
1. conda create -n shredmachineenv python=3.6 -y  </br>
2. conda activate shredmachineenv </br>
3. pip install -r requirements.txt </br>
4. python hand_detection.py </br>

## Demo video of the project
https://youtu.be/RktGCTXaF-g

# Output 
1. Number of time webcam was able the hand as well as the number of times hand crossed the warning line gets stored in result.xls

## How project was designed and build
1. **hand_detection.py**  -> Main python file which gets called. It is created to detect maximum of **2** hands.**Safety line is set to 30%** from the orientation and **Danger line at 15%** from the orientation side </br>.
   Hand Detection threshold set to **0.8** </br>
   It calls orien_lines.py to get position of the safety and dange line on the live video. </br>
   It calls detector_utils.py to load the mobilenet_ssd model and then load the livestream video <.br?
2. **orien_lines.py** ->function to check the orientation lines in the video frame. Two lines gets created on the video stream. Red line which is the alert line and the second line which is the danger line. </br>
  Camera can be positioned in any direction and at any orientation we need to have capability to draw 2 lines at the top or at the bottom, also starting from left orgit  the right . </br>
  Hence based on different orientation of the camera we get the position of the 2 lines to be draw. </br>
4. **detector_utils.py** -> Load the ssd model, load the live feed of video and check the distance of hand from the safey lines
5. **alertcheck.py** -> draw the 2 lines and if hand touches the safety lines then sound the alarm
