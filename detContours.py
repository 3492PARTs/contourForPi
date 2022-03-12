from cscore import CameraServer
import cscore
import cv2
import numpy as np

cm = CameraServer()

cm.enableLogging()

camera = cm.startAutomaticCapture()
camera.setResolution(1280, 720)

sink = cv2.VideoCapture(0)
input_img = 0

output = cm.putVideo("Camera rPi", 1280, 720)

# [hue, saturation, value]
blueMin = np.asarray([50, 50, 50])
blueMax = np.asarray([360, 360, 360])

redMin = np.asarray([0, 0, 0])
redMax = np.asarray([360, 360, 360])

while True:
    time, input_img = sink.read()

    HSV_img = cv2.cvtColor(input_img, cv2.COLOR_RGB2HSV)
    binary_img = cv2.inRange(HSV_img, blueMax, blueMin)
   
    output.putFrame(binary_img) 