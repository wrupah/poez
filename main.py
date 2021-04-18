import cv2
import mediapipe as mp
import time
import HandTrackingModule as htm
import utils as util
import commands as command
import numpy as np

import keyboard

# Use MIT license (see more into this)
from ctypes import cast, POINTER
#from comtypes import CLSCTX_ALL
#from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


#### distances
screenshot_distance = 20
ss_cnt = 0
frm_counter = 0

## for volume
# used for volume control and other shenanigans
#devices = AudioUtilities.GetSpeakers()
#interface = devices.Activate(
#    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
#volume = cast(interface, POINTER(IAudioEndpointVolume))

pTime = 0
cTime = 0
cam = 4
cap = cv2.VideoCapture(cam)
detector = htm.handDetector(False, 2, 0.7, 0.5)

frame_cnt = 0

toggle_hands = False

while True:
    frame_cnt+=1

    success, img = cap.read()
    if cam == 4:
        img = cv2.flip(img, -1)

    cx,cy,cc = np.shape(img)
    blk = np.zeros([cx, cy, 3], dtype=np.uint8)
    blk.fill(0)  # or img[:] = 255

    img = detector.findHands(img, True, False)
    detector.find3DPosition(img, False)

    #detector.commandTakePhoto(img, 40)
    #detector.commandVolume(img, volume)

    #detector.highlightHands(img)

    if frame_cnt == 10:
        #detector.commandPlayPause(img)
        #detector.commandToggleDraw()
        #detector.addPoints()
        frame_cnt = 0

    #detector.commandTakePhoto(img)

    cv2.imshow("Image", img)
    cv2.waitKey(1)