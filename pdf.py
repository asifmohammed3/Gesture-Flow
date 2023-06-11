
import cv2
import pyautogui
import mediapipe as mp
from handModel import count_fingers
from const import flag

def pdfControl():
    print(flag)
    if flag==True:
    
        mp_drawing = mp.solutions.drawing_utils
        mp_hands = mp.solutions.hands




        # Video capture setup
        cap = cv2.VideoCapture(0)
        cap.set(3, 640)
        cap.set(4, 480)
        with mp_hands.Hands(static_image_mode=False,
                        max_num_hands=2,
                        min_detection_confidence=0.7,
                        min_tracking_confidence=0.5) as hands:

            while cap.isOpened():
                success, image = cap.read()
                
                if not success:
                    break

                image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
                temp=image
                image.flags.writeable = False

                results = hands.process(image)

                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)    
            



                if results.multi_hand_landmarks and len(results.multi_hand_landmarks) > 0:
                    for hand_landmarks in results.multi_hand_landmarks:
                        if hand_landmarks is not None:
                            cnt = count_fingers(hand_landmarks)

                            if cnt == 1:
                                pyautogui.press("up")
                            elif cnt == 2:
                                pyautogui.press("down")
                            elif cnt == 3:
                                pyautogui.press("pgup")
                            elif cnt == 4:
                                pyautogui.press("pgdn")
                            

                        mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # cv2.imshow("Hand Gesture Control", image)

                
                        
                cv2.imshow("Hand Gesture Control", image)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            cv2.destroyAllWindows()
    
    else:
        cv2.destroyAllWindows()



