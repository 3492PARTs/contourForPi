from cscore import CameraServer
from networktables import NetworkTables
import time
import cscore
import cv2
import numpy as np
import json

cm = CameraServer()

cm.enableLogging()

with open('/boot/frc.json') as pain:
      config = json.load(pain)
camera = config['cameras'][0]

width = camera['width']
height = camera['height']

cm.startAutomaticCapture()

sink = cv2.VideoCapture(0)
input_img = 0

output = cm.putVideo("E", width, height)

# [hue, saturation, value]
blueMin = np.asarray([50, 50, 50])
blueMax = np.asarray([360, 360, 360])

redMin = np.asarray([0, 0, 0])
redMax = np.asarray([25, 360, 360])

time.sleep(.05)

while True:
    time, input_img = sink.read()
    output_img = np.copy(input_img)

    #Takes input and converts its to a binary image (to do: make not bad)
    HSV_img = cv2.cvtColor(input_img, cv2.COLOR_RGB2HSV)
    binary_img = cv2.inRange(HSV_img, redMin, redMax)


    #removing most of the noise
    kernel = np.ones((3, 3), np.uint8)
    binary_img = cv2.morphologyEx(binary_img, cv2.MORPH_OPEN, kernel)

    #contour is a pain that I hope no one else has to endure
    _, contour_list, _ = cv2.findContours(binary_img, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)
    x_list = []
    y_list = []

    for contour in contour_list:
        if cv2.contourArea(contour) < 15:
            continue

        cv2.drawContours(output_img, contour, -1, color = (255, 255, 255), thickness = -1)

        outline = cv2.minAreaRect(contour)
        center, size, angle = outline
        center = tuple([int(dim) for dim in center])

        cv2.drawContours(output_img, [cv2.boxPoints(outline).astype(int)], -1, color = (0, 0, 255), thickness = 2)
        cv2.circle(output_img, center = center, radius = 3, color = (0, 0, 255), thickness = -1)

        x_list.append((center[0] - width / 2) / (width / 2))
        x_list.append((center[1] - width / 2) / (width / 2))


    print(binary_img)
    output.putFrame(output_img) 