from threading import Thread
import pygame as pg
import cv2
import mediapipe as mp

'''
Star Wars Theme
C G F E D C G
F E D C G
F E F D
x2
G A A F E D
C C D E DA B
G G A
A F E D C G D D
x2
'''


def gen_piano(x, y, s, h):
    key_points = []
    for j in range(x, h, s):
        key_points.append((j, y))
    return key_points


def hit_box(rect, pt):
    logic = rect[0] < pt[0] < rect[2] and rect[1] < pt[1] < rect[3]
    return logic


def play_notes(notePath, duration):
    pg.mixer.Sound(notePath).play(maxtime=duration)


# audio files
path = 'notes/'
notes = ['g3', 'a3', 'b3', 'c4', 'd4', 'e4', 'f4', 'g4', 'a4', 'b4', 'c5']

# audio player
pg.mixer.init()
pg.init()
pg.mixer.set_num_channels(len(notes))
last_note = -1
counter = 0

# camera setup
device = 6
cap = cv2.VideoCapture(device)
cap.set(3, 1280)
cap.set(4, 720)

# hand tracker
mpHands = mp.solutions.hands
hands = mpHands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)
mpDraw = mp.solutions.drawing_utils

# aruco markers
dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_1000)
parameters = cv2.aruco.DetectorParameters_create()
marker = (0, 0)
marker2 = (800, 0)

# draw debug features
draw = False

while True:
    # command keys
    k = cv2.waitKey(1) & 0xff
    if k == 27: break
    elif k == ord('q'): break
    elif k == ord('a'): draw = not draw

    # open camera and read frame
    success, frame = cap.read()
    if not success: continue

    # detect markers
    markerCorners, markerIds, rejectedCandidates = cv2.aruco.detectMarkers(frame, dictionary, parameters=parameters)
    if draw: frame = cv2.aruco.drawDetectedMarkers(frame, markerCorners, markerIds, (0, 255, 0))
    if markerIds is not None:
        for i in range(0, markerIds.size):
            if int(markerIds[i]) == 15:
                marker = int(markerCorners[i][0][0][0]), int(markerCorners[i][0][0][1])
            if int(markerIds[i] == 12):
                marker2 = int(markerCorners[i][0][0][0]), int(markerCorners[i][0][0][1])

    # generate piano keys based on markers
    key_ww = int((marker2[0]-marker[0])/2.4)
    key_hh = int((marker2[0]-marker[0])/11)-3
    piano_keys = gen_piano(marker[0], marker[1]+10, int((marker2[0]-marker[0])/11)+1, marker2[0])

    # detect hands
    frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frameRGB)
    cx1, cy1, cx2, cy2 = 0, 0, 0, 0
    if results.multi_hand_landmarks:
        for i, handsLms in enumerate(results.multi_hand_landmarks):
            if draw:
                mpDraw.draw_landmarks(frame, handsLms, mpHands.HAND_CONNECTIONS)
            for id, lm in enumerate(handsLms.landmark):
                h, w, c = frame.shape
                if i == 0 and id == 8:
                    cx1, cy1, = int(lm.x * w), int(lm.y * h)
                if i == 1 and id == 8:
                    cx2, cy2, = int(lm.x * w), int(lm.y * h)

    # detected selected key
    note = -1
    for cnt, (center_x, center_y) in enumerate(piano_keys):
        if draw:
            cv2.rectangle(frame, (center_x, center_y), (center_x + key_hh, center_y + key_ww), (255, 255, 255), 2, -1)
        key_area = (center_x, center_y, center_x + key_hh, center_y + key_ww)
        if hit_box(key_area, (cx1, cy1)) or hit_box(key_area, (cx2, cy2)):
            note = cnt
            (pt1, pt2) = piano_keys[note]
            cv2.rectangle(frame, (center_x, center_y), (center_x + key_hh, center_y + key_ww), (255, 0, 0), 4, -1)

    # play selected note
    if note != -1 and note < len(notes) and counter > 6:
        last_note = note
        counter = 0
        t = Thread(target=play_notes, args=(path + '{}.wav'.format(notes[note]), 2000))
        t.start()
    counter += 1

    # display image
    cv2.imshow("POEZ - Piano Player", frame)

cv2.destroyAllWindows()