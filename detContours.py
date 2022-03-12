from cscore import CameraServer
import cscore
import cv2
import numpy as np

cm = CameraServer()
csc = cscore.CvSource("bob", PixelFormat(4))

cm.enableLogging()

camera = cm.startAutomaticCapture()
camera.setResolution(1600, 900)

#cv2.VideoCapture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc("M", "J", "P", "G"))

sink = cv2.VideoCapture(0)
input_img = 0

# [hue, saturation, value]
blueMin = [0, 0, 0]
blueMax = [360, 360, 360]

redMin = [0, 0, 0]
redMax = [360, 360, 360]

while True:
    time, input_img = sink.read()

    HSV_img = cv2.cvtColor(input_img, cv2.COLOR_RGB2HSV)
    csc.putFrame(HSV_img)
    #binary_img = cv2.inRange(hsv_img, blueMin, blueMax)