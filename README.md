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
FastAPI </br>
mobilenet-ssd model </br>

The **mobilenet-ssd model** is a Single-Shot multibox Detection (SSD) network intended to perform object detection. This model is implemented using the Caffe* framework.

![image](https://github.com/ravi0dubey/ShredderMachine/assets/38419795/824776e4-5506-4fbd-b363-72bca9a53204)

## Accuracy
![image](https://github.com/ravi0dubey/ShredderMachine/assets/38419795/69253758-a67e-46e6-b45e-9655616cc193)


## How to run  
1. conda create -n shredmachineenv python=3.6 -y  </br>
2. conda activate shredmachineenv </br>
3. pip install -r requirements.txt </br>
4. python hand_detection.py </br>

