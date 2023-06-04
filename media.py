# import cv2
# import mediapipe as mp
# import pyautogui
# import time

# from handModel import count_fingers



# def mediaControl(image,res,hands,drawing):
#     print("1")
#     with hands.Hands(max_num_hands=1) as hand:

#         start_init = False
        
#         prev = -1
        

#         while True:
#             end_time = time.time()
#             # _, frm = cap.read()
#             frm=image
#             # frm = cv2.flip(frm, 1)
#             print("2")
#             # res = hands.process(cv2.cvtColor(frm, cv2.COLOR_BGR2RGB))
            
#             if res.multi_hand_landmarks:

#                 hand_keyPoints = res.multi_hand_landmarks[0]

#                 cnt = count_fingers(hand_keyPoints)

#                 if not (prev == cnt):
#                     if not start_init:
#                         start_time = time.time()
#                         start_init = True

#                     elif (end_time - start_time) > 0.2:
#                         if cnt == 1:
#                             pyautogui.press("right")
                            

#                         elif cnt == 2:
#                             pyautogui.press("left")

#                         elif cnt == 3:
#                             pyautogui.press("up")

#                         elif cnt == 4:
#                             pyautogui.press("down")
#                             print("volume down")

#                         elif cnt == 5:
#                             pyautogui.press("space")
#                             print("PAUSE/PLAY")

#                         prev = cnt
#                         start_init = False

#                 drawing.draw_landmarks(frm, hand_keyPoints)

#             # cv2.imshow("window", frm)

#             if cv2.waitKey(1) == 27:
#                 cv2.destroyAllWindows()
#                 # cap.release()
#                 break



import cv2
import pyautogui

def count_fingers(lst):
    cnt = 0

    thresh = (lst.landmark[0].y * 100 - lst.landmark[9].y * 100) / 2

    if (lst.landmark[5].y * 100 - lst.landmark[8].y * 100) > thresh:
        cnt += 1

    if (lst.landmark[9].y * 100 - lst.landmark[12].y * 100) > thresh:
        cnt += 1

    if (lst.landmark[13].y * 100 - lst.landmark[16].y * 100) > thresh:
        cnt += 1

    if (lst.landmark[17].y * 100 - lst.landmark[20].y * 100) > thresh:
        cnt += 1

    if (lst.landmark[5].x * 100 - lst.landmark[4].x * 100) > 6:
        cnt += 1

    return cnt

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
