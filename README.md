# Sleep-quality-monitoring-system

This undergraduate senior project is from the Department of Communication Engineering, Feng Chia University(Taichung, Taiwan)  
Made by 林郁全、陳妤萱、黃聿莛、梁芷瑄、王佩瑄  

# Abstract  
Modern work stress has led people to increasingly prioritize sleep issues. According to a 2019 survey by the Taiwan Sleep Medicine Association, 60% of respondents reported snoring problems. Snoring is closely associated with sleep apnea and other cardiovascular diseases. Many individuals are unaware of their sleep problems, prompting us to develop a solution that allows people to monitor their sleep at home. Through our product, users can track their sleeping posture, blood oxygen levels, respiratory rate, and snoring detection, providing preliminary insights into their sleep issues. Additionally, it can be used as a reference for diagnostic assistance.

Our project utilizes an infrared camera to capture the subject's sleeping posture at night, aided by OpenPose to recognize whether they are sleeping on their back, side, or stomach. We also incorporate a snoring sound filter to record instances of snoring. Objective measurements such as blood oxygen levels and heart rate are recorded, and discussions with nursing students help identify potential occurrences of sleep apnea. Combining objective data with subjective questionnaire responses, we create a software interface that allows users to clearly understand their condition and receive recommendations to better monitor their health.  
# Equipment required  
  MAX30102(A arduino module for measure spo2 and heartbeat)  
  computer  
# Environment Setup  
  This project is based on openpose, so you need to install openpose.  
  When openpose is installed, please follow this step.  
  1. use anaconda prompt or cmd to activate openpose enviroment
  2. pip install -r requirements.txt

# Run test  
  This project has some problems and bugs, this is how we run this project.  
  1. open 2 anaconda prompt or cmd to activate openpose environment
  2. 1 command window type `python final.py`(run openpose)
  3. When openpose starts running, another command window type `python tkfinal.py`(run GUI)

# FILE
  |- openpose -> final.py  
  |- GUI -> tkfinal.py and best.keras(this file is detect snoring)  
  
# Reference  
  1. Some nursing issue or experience from Department of Nursing, Chang Gung University Of Science and Technology(Taoyuan, Taiwan)  
  2. openpose  [Link](https://github.com/CMU-Perceptual-Computing-Lab/openpose)
