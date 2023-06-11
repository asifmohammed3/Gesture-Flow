import cv2
import numpy as np
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import screen_brightness_control as sbc
import threading
import mediapipe as mp

# Hand detector class
class handDetector():
    def __init__(self, mode=False, maxHands=1, detectionCon=0.7, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands,
                                        self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,
                                               self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, draw=True):
        rlmlist = []

        if self.results.multi_hand_landmarks:
            if len(self.results.multi_hand_landmarks) == 2:
                rlmlist.append('both')
            elif len(self.results.multi_hand_landmarks) == 1:
                rlmlist.append(self.results.multi_handedness[0].classification[0].label)

            for n in self.results.multi_hand_landmarks:
                lmList = []
                myHand = n
                for id, lm in enumerate(myHand.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lmList.append([id, cx, cy])
                    if draw:
                        cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
                rlmlist.append(lmList)

        return rlmlist


    
def volBright():
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)


  
    handDetObj = handDetector(detectionCon=0.7)

   

    # Initialize audio volume control
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volRange = volume.GetVolumeRange()
    minVolume = volRange[0]
    maxVolume = volRange[1]

    # Initialize brightness control
    minBrightness = 0
    maxBrightness = 100

    # Function to set the audio volume based on hand distance
    def setVolume(dist):
        vol = np.interp(int(dist), [35, 215], [minVolume, maxVolume])
        volume.SetMasterVolumeLevel(vol, None)

    # Function to set the screen brightness based on hand distance
    def setBrightness(dist):
        brightness = np.interp(int(dist), [35, 230], [minBrightness, maxBrightness])
        sbc.set_brightness(int(brightness))



    # if results.multi_hand_landmarks and len(results.multi_hand_landmarks) > 0:
    #     for hand_landmarks in results.multi_hand_landmarks:
    #         print(hand_landmarks)
    while True:
        _,frame = cap.read()
        frame = cv2.flip(frame,1)
        frame = handDetObj.findHands(frame)
        lndmrks = handDetObj.findPosition(frame,draw=False)
        if lndmrks:
            # print(lndmrks[4],lndmrks[8])

            xr1,yr1 = lndmrks[1][4][1],lndmrks[1][4][2]
            xr2,yr2 = lndmrks[1][8][1],lndmrks[1][8][2]
            dist = math.hypot(xr2-xr1,yr2-yr1)

            if lndmrks[0] == 'Left':
                setBrightness(dist)
            elif lndmrks[0] == 'Right':
                setVolume(dist)
            elif lndmrks[0] == 'both':
                xl1, yl1 = lndmrks[1][4][1], lndmrks[1][4][2]
                xl2, yl2 = lndmrks[1][8][1], lndmrks[1][8][2]
                distl = math.hypot(xl2 - xl1, yl2 - yl1)
                
                t1 = threading.Thread(target=setVolume, args=(dist,))
                t2 = threading.Thread(target=setBrightness, args=(distl,))
                
                t1.start()
                t2.start()

        

        cv2.imshow("Hand Gesture Control",frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()
