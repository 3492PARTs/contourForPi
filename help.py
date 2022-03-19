from pickle import TRUE
import time
import cv2
#from networktables import NetworkTable, NetworkTables as NT, NetworkTablesInstance as NTI
import numpy as np

window = 'colorfinder'

sink = cv2.VideoCapture(1)
input_img = 0

# [hue, saturation, value]
blueMin = np.asarray([0, 160, 0])
blueMax = np.asarray([15, 200, 300])

redMin = np.asarray([110, 160, 0])
redMax = np.asarray([120, 200, 300])

isred = False

time.sleep(2)
while True:
   
   times, input_img = sink.read()
   output_img = np.copy(input_img)
  

   #Takes input and converts its to a binary image (to do: make not bad)
   HSV_img = cv2.cvtColor(input_img, cv2.COLOR_RGB2HSV)
   if isred == True:
      binary_img = cv2.inRange(HSV_img, redMin, redMax)
   else:
      binary_img = cv2.inRange(HSV_img, blueMin, blueMax)

   kernel = np.ones((3, 3), np.uint8)
   binary_img = cv2.morphologyEx(binary_img, cv2.MORPH_OPEN, kernel)

   edges = cv2.Canny(binary_img, 1400, 1500)

   cv2.waitKey(10)
   cv2.imshow(window, edges)