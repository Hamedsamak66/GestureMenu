import cv2
import mediapipe as mp
import time

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Function to count fingers and get the position of the index finger
def count_fingers_and_get_index_pos(hand_landmarks):
    if hand_landmarks:
        landmarks = hand_landmarks[0].landmark
        fingers = []

        # Thumb
        if landmarks[mp_hands.HandLandmark.THUMB_TIP].x < landmarks[mp_hands.HandLandmark.THUMB_MCP].x:
            fingers.append(1)
        else:
            fingers.append(0)

        # 4 fingers (Index, Middle, Ring, and Pinky)
        for id in [mp_hands.HandLandmark.INDEX_FINGER_TIP,
                   mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
                   mp_hands.HandLandmark.RING_FINGER_TIP,
                   mp_hands.HandLandmark.PINKY_TIP]:
            tip = landmarks[id].y
            dip = landmarks[id - 2].y
            if tip < dip:
                fingers.append(1)
            else:
                fingers.append(0)

        index_pos = (int(landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * 640),
                     int(landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * 480))

        return sum(fingers), index_pos
    return 0, (0, 0)

# Open webcam
cap = cv2.VideoCapture(0)

# Menu state
menu_open = False
menu_colors = [(255, 255, 255), (255, 255, 255), (255, 255, 255)]  # Default white color for options
hover_start_time = [None, None, None]  # Start time for hovering over each option

# Infinite loop to process video frames
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame
    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            num_fingers, index_pos = count_fingers_and_get_index_pos(result.multi_hand_landmarks)

            # Open menu when 5 fingers are detected
            if num_fingers == 5:
                menu_open = True
            # Close menu when 0 fingers are detected (fist)
            elif num_fingers == 0:
                menu_open = False

            # Draw menu if open
            if menu_open:
                current_time = time.time()

                # Check if index finger is over any menu option
                for i, (x1, y1, x2, y2) in enumerate([(390, 100, 590, 150), (390, 160, 590, 210), (390, 220, 590, 270)]):
                    if x1 <= index_pos[0] <= x2 and y1 <= index_pos[1] <= y2:
                        if hover_start_time[i] is None:
                            hover_start_time[i] = current_time
                            menu_colors[i] = (0, 0, 255)  # Red when hovering
                        elif current_time - hover_start_time[i] >= 1:  # 3 seconds hover
                            menu_colors[i] = (0, 255, 0)  # Option becomes Green after 3 seconds
                    else:
                        hover_start_time[i] = None
                        menu_colors[i] = (255, 255, 255)  # Reset to white

                # Draw each menu option
                cv2.rectangle(frame, (390, 100), (590, 150), menu_colors[0], cv2.FILLED)
                cv2.putText(frame, "Option 1", (410, 130), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
                
                cv2.rectangle(frame, (390, 160), (590, 210), menu_colors[1], cv2.FILLED)
                cv2.putText(frame, "Option 2", (410, 190), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

                cv2.rectangle(frame, (390, 220), (590, 270), menu_colors[2], cv2.FILLED)
                cv2.putText(frame, "Option 3", (410, 250), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

    # Display the frame
    cv2.imshow("Gesture-Controlled Menu", frame)

    # Break loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close windows
cap.release()
cv2.destroyAllWindows()
