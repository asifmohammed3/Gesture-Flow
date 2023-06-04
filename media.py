

import cv2
import pyautogui

from handModel import count_fingers


def mediaControl(image, results, mp_hands, mp_drawing):
    if results.multi_hand_landmarks and len(results.multi_hand_landmarks) > 0:
        for hand_landmarks in results.multi_hand_landmarks:
            if hand_landmarks is not None:
                cnt = count_fingers(hand_landmarks)

                if cnt == 1:
                    pyautogui.press("right")
                elif cnt == 2:
                    pyautogui.press("left")
                elif cnt == 3:
                    pyautogui.press("volumedown")
                elif cnt == 4:
                    pyautogui.press("volumeup")
                elif cnt == 5:
                    pyautogui.press("playpause")

            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    cv2.imshow("Hand Gesture Control", image)
