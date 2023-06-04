import cv2
import mediapipe as mp
import time
import media
from pdf import pdfControl
import volumeBrightness 

# MediaPipe setup
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Define the list of modes
modes = ["media", "volume_brightness", "pdf"]
current_mode = "volume_brightness"
last_mode_change_time = time.time()

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
                if hand_landmarks is not None:  # Check if hand landmarks are available

                    # Get hand landmarks
                    # Use landmarks to determine hand gestures

                    # Example: Determine if thumbs up gesture
                    thumb_up = False
                    thumb_landmark = hand_landmarks.landmark[4]
                    index_finger_landmark = hand_landmarks.landmark[20]
                    if thumb_landmark.y > index_finger_landmark.y:
                        thumb_up = True

                    if thumb_up and time.time() - last_mode_change_time > 2:  # Check if 2 seconds have passed
                        # Set the mode to the next mode in the list
                        current_mode_index = (modes.index(current_mode) + 1) % len(modes)
                        current_mode = modes[current_mode_index]
                        last_mode_change_time = time.time()

        # Handle different modes
        if current_mode == "media":
            if time.time() - last_mode_change_time < 1:  # Display mode activation for 0.5 seconds
                print("Media control mode activated")
            media.mediaControl(image, results, mp_hands, mp_drawing)
            # Add your media control logic here

        elif current_mode == "volume_brightness":
            if time.time() - last_mode_change_time < 1:  # Display mode activation for 0.5 seconds
                print("Volume control mode activated")
                volumeBrightness.volBright(cap)
                cap.release()
            # Add your volume control logic here

        elif current_mode == "pdf":
            if time.time() - last_mode_change_time < 1:  # Display mode activation for 0.5 seconds
                print("PDF control mode activated")
                pdfControl(image, results, mp_hands, mp_drawing)
            # Add your PDF control logic here

        if results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        cv2.imshow("Hand Gesture Control", image)
        if cv2.waitKey(5) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()
