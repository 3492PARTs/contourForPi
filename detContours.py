from cscore import CameraServer
from networktables import NetworkTables as nt
import time
import cscore
import cv2
import numpy as np
import json


def main():
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
    blueMin = np.asarray([0, 160, 0])
    blueMax = np.asarray([15, 200, 300])

    redMin = np.asarray([110, 180, 0])
    redMax = np.asarray([120, 200, 300])

    isred = True

    time.sleep(.05)

    while True:
        times, input_img = sink.read()
        output_img = np.copy(input_img)

        if times == 0:
            output.notifyError(input_stream.getError())
            continue


        #Takes input and converts its to a binary image (to do: make not bad (did))
        HSV_img = cv2.cvtColor(input_img, cv2.COLOR_RGB2HSV)
        if isred == True:
            binary_img = cv2.inRange(HSV_img, redMin, redMax)
        else:
            binary_img = cv2.inRange(HSV_img, blueMin, blueMax)


        #removing most of the noise
        kernel = np.ones((3, 3), np.uint8)
        binary_img = cv2.morphologyEx(binary_img, cv2.MORPH_OPEN, kernel)

        #contour is a pain that I hope no one else has to endure
        _, contour_list, _ = cv2.findContours(binary_img, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)

        for contour in contour_list:
            if cv2.contourArea(contour) < 15:
                continue

            cv2.drawContours(output_img, contour, -1, color = (255, 255, 255), thickness = -1)

            outline = cv2.minAreaRect(contour)
            center, size, angle = outline
            center = tuple([int(dim) for dim in center])

            cv2.drawContours(output_img, [cv2.boxPoints(outline).astype(int)], -1, color = (0, 0, 255), thickness = 2)
            cv2.circle(output_img, center = center, radius = 3, color = (0, 0, 255), thickness = -1)

        count = 1
        for element in binary_img:
            vision_nt.putNumberArray('binaryImgUnwrapped' + str(count), element)
            count += 1

        print(binary_img)
main()