import cv2
import mediapipe as mp
import time
import pyautogui as pygui
import math
import utils as util

ss_cnt = 0
def ScreenShot(handLmList, img,
               debug=False, screenshot_distance=20):

    thumb1 = (handLmList[0][4][1], handLmList[0][4][2])
    thumb2 = (handLmList[1][4][1], handLmList[1][4][2])
    index1 = (handLmList[0][8][1], handLmList[0][8][2])
    index2 = (handLmList[1][8][1], handLmList[1][8][2])
    if (bool(thumb1) and bool(thumb2) and bool(index1) and bool(index2)):
        print(thumb1)
        print(thumb2)
        print(index1)
        print(index2)
        dist1 = util.euclideanDistance(thumb1, index2)
        dist2 = util.euclideanDistance(thumb2, index1)
        print("dist1 = " + str(dist1) + "          dist2 = " + str(dist2))
        if dist1 < screenshot_distance and dist2 < screenshot_distance:
            print("---------------------------------- SCRENSHOT TAKEN ---------------------------------- ")
            if debug:
                cv2.circle()
            cv2.imwrite('C:/Users/Jorge Monteiro/PycharmProjects/HandTracker/screenshot_' + str(ss_cnt) + '.png', img)
            ss_cnt += 1

    # print("---------------------------------- SCRENSHOT TAKEN ---------------------------------- ")
    # cv2.imwrite('C:/Users/Jorge Monteiro/PycharmProjects/HandTracker/screenshot.png', img)
    # myss = pygui.screenshot()
    # myss.save('C:/Users/Jorge Monteiro/PycharmProjects/HandTracker/screenshot.png')
