import cv2
import mediapipe as mp
import time
import pyautogui as pygui
import utils as util
import webbrowser
import numpy as np
import math
from pynput.keyboard import Key, Controller
from playsound import playsound


class handDetector():
    def __init__(self,mode=False, maxHands = 2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.lmList = []

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands,
                                        self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

        #draw points in space
        self.drawing = False
        self.drawingpts = []

    def findHands(self, img, draw=True, debug=False):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)

                    if debug:
                        for id, lm in enumerate(handLms.landmark):
                            h,w,c = img.shape
                            cx, cy = int(lm.x*w), int(lm.y*h)
                            print(id, cx, cy)
                            cv2.putText(img, str(int(id)), (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1)

        return img

    def findPosition(self, img, debug=False):
        self.lmList = []

        if self.results.multi_hand_landmarks:
            for handno in range(0, len(self.results.multi_hand_landmarks)):
                tmp_list = []
                myHand = self.results.multi_hand_landmarks[handno]
                for id, lm in enumerate(myHand.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    tmp_list.append([id, cx, cy])
                    if (debug):
                        cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
                self.lmList.append(list(tmp_list))

    def find3DPosition(self, img, debug=False):
        self.lmList = []

        if self.results.multi_hand_landmarks:
            for handno in range(0, len(self.results.multi_hand_landmarks)):
                tmp_list = []
                myHand = self.results.multi_hand_landmarks[handno]
                for id, lm in enumerate(myHand.landmark):
                    h, w, c = img.shape
                    cx, cy, cz = int(lm.x * w), int(lm.y * h), int(lm.z*1000)
                    tmp_list.append([id, cx, cy, cz])
                    if (debug):
                        cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
                self.lmList.append(list(tmp_list))

    def drawPoints(self, img):

        for i in range(0, len(self.lmList)):
            hand = self.lmList[i]
            for j in range(0, len(hand)):
                id, cx, cy, z = hand[j][0], hand[j][1], hand[j][2], hand[j][3]
                print(z)
                if(int(z) > 500):
                    z = 500
                if(int(z) < -500):
                    z = -500

                gsColor = np.interp(int(z), [-500, 500], [0, 255])
                cv2.circle(img, (cx, cy), 15, (gsColor, gsColor, gsColor), cv2.FILLED)
                cv2.putText(img, str(int(id)), (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1)

        lista = self.lmList
        print(lista)

    def animateHands(self, img):
        for i in range(0, len(self.lmList)):
            hand = self.lmList[i]

            p00 = hand[0]
            p01 = hand[1]
            p02 = hand[2]
            p03 = hand[3]
            p04 = hand[4]
            p05 = hand[5]
            p06 = hand[6]
            p07 = hand[7]
            p08 = hand[8]
            p09 = hand[9]
            p10 = hand[10]
            p11 = hand[11]
            p12 = hand[12]
            p13 = hand[13]
            p14 = hand[14]
            p15 = hand[15]
            p16 = hand[16]
            p17 = hand[17]
            p18 = hand[18]
            p19 = hand[19]
            p20 = hand[20]

            palm_size = 40
            thumb_size = 40
            index_size = 35
            middle_size = 35
            ring_size = 30
            pinky_size = 22

            # palm - red
            cv2.line(img, (p00[1], p00[2]), (p01[1], p01[2]), (0, 0, 255), palm_size)
            cv2.line(img, (p00[1], p00[2]), (p05[1], p05[2]), (0, 0, 255), palm_size)
            cv2.line(img, (p00[1], p00[2]), (p17[1], p17[2]), (0, 0, 255), palm_size)
            cv2.line(img, (p05[1], p05[2]), (p09[1], p09[2]), (0, 0, 255), palm_size)
            cv2.line(img, (p09[1], p09[2]), (p13[1], p13[2]), (0, 0, 255), palm_size)
            cv2.line(img, (p01[1], p01[2]), (p05[1], p05[2]), (0, 0, 255), int(palm_size*0.6))
            cv2.line(img, (p17[1], p17[2]), (p13[1], p13[2]), (0, 0, 255), palm_size)

            # thumb - green
            cv2.line(img, (p02[1], p02[2]), (p01[1], p01[2]), (0, 255, 0), thumb_size)
            cv2.line(img, (p02[1], p02[2]), (p03[1], p03[2]), (0, 255, 0), int(thumb_size*0.8))
            cv2.line(img, (p04[1], p04[2]), (p03[1], p03[2]), (0, 255, 0), int(thumb_size*0.8))

            # index - blue
            cv2.line(img, (p06[1], p06[2]), (p05[1], p05[2]), (255, 0, 0), index_size)
            cv2.line(img, (p06[1], p06[2]), (p07[1], p07[2]), (255, 0, 0), int(index_size*0.8))
            cv2.line(img, (p08[1], p08[2]), (p07[1], p07[2]), (255, 0, 0), int(index_size*0.8))

            # middle - yellow
            cv2.line(img, (p09[1], p09[2]), (p10[1], p10[2]), (0, 255, 255), middle_size)
            cv2.line(img, (p11[1], p11[2]), (p10[1], p10[2]), (0, 255, 255), int(middle_size*0.9))
            cv2.line(img, (p11[1], p11[2]), (p12[1], p12[2]), (0, 255, 255), int(middle_size*0.9))

            # ring - magenta
            cv2.line(img, (p14[1], p14[2]), (p13[1], p13[2]), (255, 0, 255), ring_size)
            cv2.line(img, (p14[1], p14[2]), (p15[1], p15[2]), (255, 0, 255), int(ring_size*0.9))
            cv2.line(img, (p16[1], p16[2]), (p15[1], p15[2]), (255, 0, 255), int(ring_size*0.9))

            # pinky - cyan
            cv2.line(img, (p17[1], p17[2]), (p18[1], p18[2]), (255, 255, 0), pinky_size)
            cv2.line(img, (p19[1], p19[2]), (p18[1], p18[2]), (255, 255, 0), int(pinky_size*0.9))
            cv2.line(img, (p19[1], p19[2]), (p20[1], p20[2]), (255, 255, 0), int(pinky_size*0.9))

    def highlightHands(self, img):
        if len(self.lmList) != 0:
            palm = (self.lmList[0][0][1], self.lmList[0][0][2])
            index = (self.lmList[0][8][1], self.lmList[0][8][2])
            thumb = (self.lmList[0][4][1], self.lmList[0][4][2])
            pinky = (self.lmList[0][20][1], self.lmList[0][20][2])


            cv2.circle(img, palm, 10, (0,255,0), cv2.FILLED)
            cv2.circle(img, index, 10, (0, 255, 0), cv2.FILLED)
            cv2.circle(img, thumb, 10, (0, 255, 0), cv2.FILLED)

            centroid = ( (palm[0]+index[0]+thumb[0]+pinky[0])//4 , (palm[1]+index[1]+thumb[1]+pinky[1])//4 )
            cv2.circle(img, centroid, 10, (255, 255, 0), cv2.FILLED)

            radius = np.sqrt( (centroid[0]-thumb[0])**2 + (centroid[1]-thumb[1])**2 )

            cv2.circle(img, centroid, int(1.5*radius), (255, 255, 0), 20)

    # one hand command
    def commandOneHand(self, img, min_dist = 20):
        if len(self.lmList) != 0:
            thumb = (self.lmList[0][4][1], self.lmList[0][4][2])
            index = (self.lmList[0][8][1], self.lmList[0][8][2])
            middle = (self.lmList[0][12][1], self.lmList[0][12][2])
            if (bool(thumb) and bool(index) and bool(middle)):
                # highlight thumb and index
                cv2.circle(img, thumb, 15, (0, 0, 255), cv2.FILLED)
                cv2.circle(img, index, 15, (0, 0, 255), cv2.FILLED)
                cv2.circle(img, middle, 15, (0, 0, 255), cv2.FILLED)

                dist_thumb_index = util.euclideanDistance(thumb, index)
                dist_thumb_middle = util.euclideanDistance(thumb, middle)
                if(dist_thumb_index < min_dist):
                    cv2.circle(img, thumb, 15, (0, 255, 0), cv2.FILLED)
                    cv2.circle(img, index, 15, (0, 255, 0), cv2.FILLED)
                    time.sleep(1)
                    keyboard = Controller()
                    keyboard.press(Key.left)
                    playsound("wavs/next.wav")
                    keyboard.release(Key.left)
                    print("_________ NEXT ____________")

                if(dist_thumb_middle < min_dist):
                    cv2.circle(img, thumb, 15, (0, 255, 0), cv2.FILLED)
                    cv2.circle(img, middle, 15, (0, 255, 0), cv2.FILLED)
                    keyboard = Controller()
                    keyboard.press(Key.right)
                    playsound("wavs/previous.wav")
                    keyboard.release(Key.right)
                    print("_________ PREVIOUS ____________")

        return img

    # two hand command
    # NOT WORKING PROPERLY ( not detected)
    def commandTwoHands(self, img, debug=False, screenshot_distance=20):
        if len(self.lmList) == 2:
            thumb1 = (self.lmList[0][4][1], self.lmList[0][4][2])
            thumb2 = (self.lmList[1][4][1], self.lmList[1][4][2])
            index1 = (self.lmList[0][8][1], self.lmList[0][8][2])
            index2 = (self.lmList[1][8][1], self.lmList[1][8][2])
            if (bool(thumb1) and bool(thumb2) and bool(index1) and bool(index2)):
                dist1 = util.euclideanDistance(thumb1, thumb2)
                dist2 = util.euclideanDistance(index2, index1)
                print("dist 1 = " + str(dist1) + "       dist 2 =  " + str(dist2))
                if dist1 < screenshot_distance and dist2 < screenshot_distance:
                    print("_________ media play/pause ____________")
                    time.sleep(0.5)
                    keyboard = Controller()
                    keyboard.press(Key.media_play_pause)
                    playsound("wavs/playpause.wav")
                    keyboard.release(Key.media_play_pause)

    # DEFINITE COMMANDS
    # Play/pause - triângulo --> DONE
    def commandPlayPause(self, img, min_dist = 20):
        if len(self.lmList) == 2:
            thumb1 = (self.lmList[0][4][1], self.lmList[0][4][2])
            thumb2 = (self.lmList[1][4][1], self.lmList[1][4][2])
            index1 = (self.lmList[0][8][1], self.lmList[0][8][2])
            index2 = (self.lmList[1][8][1], self.lmList[1][8][2])
            if (bool(thumb1) and bool(thumb2) and bool(index1) and bool(index2)):
                dist1 = util.euclideanDistance(thumb1, thumb2)
                dist2 = util.euclideanDistance(index2, index1)
                if dist1 < min_dist and dist2 < min_dist:
                    print("___ PLAY / PAUSE ___")
                    playsound("wavs/playpause.wav")

    # Aumentar volume - arrastar dedos --> DONE
    def commandVolume(self, img, volume, debug=False):
        if len(self.lmList) != 0:
            thumb = (self.lmList[0][4][1], self.lmList[0][4][2])
            index = (self.lmList[0][8][1], self.lmList[0][8][2])
            if (bool(thumb) and bool(index)):
                # highlight thumb and index
                cv2.circle(img, thumb, 15, (0, 0, 255), cv2.FILLED)
                cv2.circle(img, index, 15, (0, 0, 255), cv2.FILLED)

                # center of line
                cx, cy = (thumb[0] + index[0]) // 2, (thumb[1] + index[1]) // 2
                cv2.circle(img, (cx, cy), 15, (0, 255, 255), cv2.FILLED)

                cv2.line(img, thumb, index, (255, 0, 0), 3)

                # hypot is the same as euclidean distance
                length = math.hypot(thumb[0] - index[0], thumb[1] - index[1])

                volRange = volume.GetVolumeRange()
                vol = np.interp(length, [50, 250], [volRange[0], volRange[1]])
                vol0_100 = np.interp(vol, [volRange[0], volRange[1]], [0, 100])

                cv2.putText(img, str(int(vol0_100)), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 255), 3)
                volume.SetMasterVolumeLevel(vol, None)
                if length < 50:
                    cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)

        return img

    # mudar de música - arrastar 2 dedos (indicador pirete)


    # Scroll - arrastar dedo para cima ou para baixo



    # Zoom - abrir e fechar dedos



    # Tirar fotos - movimento do clique do botão de uma máquina fotográfica --> DONE
    def commandTakePhoto(self, img, min_dist = 20):
        if len(self.lmList) != 0:
            thumb = (self.lmList[0][4][1], self.lmList[0][4][2])
            index = (self.lmList[0][8][1], self.lmList[0][8][2])
            middle = (self.lmList[0][12][1], self.lmList[0][12][2])
            ring = (self.lmList[0][16][1], self.lmList[0][16][2])
            pinky = (self.lmList[0][20][1], self.lmList[0][20][2])

            if (bool(thumb) and bool(index) and bool(middle) and bool(ring) and bool(pinky)):
                dist_middle_ring = util.euclideanDistance(middle, ring)
                dist_ring_pinky = util.euclideanDistance(pinky, ring)
                if(dist_middle_ring < min_dist and dist_ring_pinky < min_dist):
                    cv2.circle(img, thumb, 15, (0, 255, 255), cv2.FILLED)
                    cv2.circle(img, index, 15, (0, 255, 255), cv2.FILLED)
                    mid_falangeta = (self.lmList[0][10][1], self.lmList[0][10][2])
                    cv2.circle(img, mid_falangeta, 15, (0, 0, 255), cv2.FILLED)

                    dist_mid_index = util.euclideanDistance(mid_falangeta, index)
                    if dist_mid_index < 2*min_dist:
                        playsound("wavs/shutter.wav")
                        print("_________ PHOTO ____________")

    # Filmar - dedos fechados em círculo

    # DRAW
    def commandToggleDraw(self, minT = 20):
        if len(self.lmList) == 2:
            index1 = (self.lmList[0][8][1], self.lmList[0][8][2])
            index2 = (self.lmList[1][8][1], self.lmList[1][8][2])
            dist = util.euclideanDistance(index1, index2)
            if(dist < minT):
                self.drawing = not self.drawing
                playsound("wavs/playpause.wav")
                print("drawing = " + str(self.drawing))

    def addPoints(self):
        if len(self.lmList) == 2 and self.drawing:
            index1 = (self.lmList[0][8][1], self.lmList[0][8][2])
            index2 = (self.lmList[1][8][1], self.lmList[1][8][2])

            self.drawingpts.append(index1)
            self.drawingpts.append(index2)

            print("len = " + str(len(self.drawingpts)))

    def commandDraw(self, img):
        n_pts = len(self.drawingpts)
        for i in range(0, n_pts):
            cv2.circle(img, self.drawingpts[i], 10, (255,255,0), cv2.FILLED)
            if i < n_pts-1:
                cv2.line(img, self.drawingpts[i], self.drawingpts[i+1], (255,0,255), 10)


