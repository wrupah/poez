import cv2
import mediapipe as mp
import time
import pyautogui as pygui
import math
import numpy as np
import HandTrackingModule as htm

def euclideanDistance(p1, p2):
    res = math.sqrt((p1[0]-p2[0])*(p1[0]-p2[0]) + (p1[1]-p2[1])*(p1[1]-p2[1]))
    return res

