import time
import cv2
#from networktables import NetworkTable, NetworkTables as NT, NetworkTablesInstance as NTI
import numpy as np

window = 'colorfinder'

sink = cv2.VideoCapture(1)
input_img = 0

# [hue, saturation, value]
blueMin = np.asarray([5, 160, 50])
blueMax = np.asarray([15, 200, 300])

redMin = np.asarray([115, 180, 50])
redMax = np.asarray([120, 200, 300])

isred = False

time.sleep(2)
while True:
   
   times, input_img = sink.read()
   output_img = np.copy(input_img)
  

   #Takes input and converts its to a binary image
   HSV_img = cv2.cvtColor(input_img, cv2.COLOR_RGB2HSV)
   if isred == True:
      binary_img = cv2.inRange(HSV_img, redMin, redMax)
   else:
      binary_img = cv2.inRange(HSV_img, blueMin, blueMax)

   #creating a custom ellipse kernel 
   ksize = (3, 3)
   M = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, ksize)
   
   #Eroding followed by using Canny algorithm to find edges
   cv2.erode(binary_img, M, iterations=100)
   edges = cv2.Canny(binary_img, 128, 256)

   contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
   cv2.drawContours(output_img, contours, -1, (0,255,0), 3)

   cv2.waitKey(10)
   cv2.imshow(window, output_img)