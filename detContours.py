from cscore import CameraServer
from networktables import NetworkTables as nt
import time
import cscore
import cv2
import numpy as np
import json


def main():
    #cm is never used but wpilibpi complains if you don't use their stuff
    cm = CameraServer()

    cm.enableLogging()

    vision_nt = nt.getTable('Vision')

    with open('/boot/frc.json') as pain:
        config = json.load(pain)
    camera = config['cameras'][0]

    width = camera['width']
    height = camera['height']

    cm.startAutomaticCapture()

    sink = cv2.VideoCapture(0)
    input_img = 0

    input_stream = cm.getVideo()
    output = cm.putVideo("E", width, height)

    # [hue, saturation, value]
    blueMin = np.asarray([5, 160, 100])
    blueMax = np.asarray([15, 200, 300])

    redMin = np.asarray([115, 180, 100])
    redMax = np.asarray([120, 200, 300])

    isred = True

    time.sleep(.05)

    while True:
        times, input_img = sink.read()
        output_img = np.copy(input_img)

        if times == 0:
            output.notifyError(input_stream.getError())
            continue


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
        cv2.drawContours(output_img, contours, -1, (0,255,0), 3) #This part isn't necassary but incase we get video to work on wpilibpi it helps visualize the contours

        count = 1
        for element in contours:
            vision_nt.putNumberArray('contoursunwrapped' + str(count), element)
            count += 1

        print(binary_img)
main()