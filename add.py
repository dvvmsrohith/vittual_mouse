import cv2
import mediapipe as mp
import pyautogui
import math
import time


# ============================================================
# SCREEN
# ============================================================

screen_width, screen_height = pyautogui.size()


# ============================================================
# CAMERA
# ============================================================

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Camera open avvaledu!")
    exit()


# ============================================================
# MEDIAPIPE HANDS
# ============================================================

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)


# ============================================================
# MOUSE SETTINGS
# ============================================================

smoothening = 7

prev_x = screen_width // 2
prev_y = screen_height // 2

mouse_initialized = False


# ============================================================
# CLICK CONTROL
# ============================================================

left_clicking = False
right_clicking = False


# ============================================================
# FIST / EXIT CONTROL
# ============================================================

fist_frames = 0

# Number of frames required to close
FIST_HOLD_FRAMES = 25

exit_program = False


# ============================================================
# CAMERA CONTROL AREA
# ============================================================

frame_margin_x = 0.15
frame_margin_y = 0.15


# ============================================================
# HELPER FUNCTION
# ============================================================

def distance(point1, point2):
    """
    Calculate distance between two MediaPipe landmarks.
    """
    return math.hypot(
        point1.x - point2.x,
        point1.y - point2.y
    )


# ============================================================
# MAIN LOOP
# ============================================================

while True:

    success, img = cap.read()

    if not success:
        print("Camera frame read avvaledu!")
        break


    # --------------------------------------------------------
    # MIRROR CAMERA
    # --------------------------------------------------------

    img = cv2.flip(img, 1)


    # --------------------------------------------------------
    # CONVERT BGR -> RGB
    # --------------------------------------------------------

    rgb_img = cv2.cvtColor(
        img,
        cv2.COLOR_BGR2RGB
    )


    # --------------------------------------------------------
    # HAND DETECTION
    # --------------------------------------------------------

    result = hands.process(rgb_img)


    # ========================================================
    # IF HAND DETECTED
    # ========================================================

    if result.multi_hand_landmarks:

        hand_landmarks = result.multi_hand_landmarks[0]


        # ----------------------------------------------------
        # DRAW HAND LANDMARKS
        # ----------------------------------------------------

        mp_draw.draw_landmarks(
            img,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS
        )


        # ====================================================
        # LANDMARKS
        # ====================================================

        thumb = hand_landmarks.landmark[4]

        index_finger = hand_landmarks.landmark[8]
        middle_finger = hand_landmarks.landmark[12]
        ring_finger = hand_landmarks.landmark[16]
        pinky_finger = hand_landmarks.landmark[20]

        index_pip = hand_landmarks.landmark[6]
        middle_pip = hand_landmarks.landmark[10]
        ring_pip = hand_landmarks.landmark[14]
        pinky_pip = hand_landmarks.landmark[18]

        palm = hand_landmarks.landmark[9]


        # ====================================================
        # FINGER OPEN/CLOSED STATUS
        # ====================================================

        index_open = index_finger.y < index_pip.y
        middle_open = middle_finger.y < middle_pip.y
        ring_open = ring_finger.y < ring_pip.y
        pinky_open = pinky_finger.y < pinky_pip.y


        # ====================================================
        # FIST DETECTION
        # ====================================================

        fist = (
            not index_open
            and not middle_open
            and not ring_open
            and not pinky_open
        )


        # ====================================================
        # FIST -> CLOSE PROGRAM
        # ====================================================

        if fist:

            fist_frames += 1


            cv2.putText(
                img,
                "HOLD FIST TO CLOSE",
                (30, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (0, 0, 255),
                2
            )


            # Progress bar
            progress = min(
                fist_frames / FIST_HOLD_FRAMES,
                1.0
            )


            bar_width = 300

            cv2.rectangle(
                img,
                (30, 70),
                (30 + bar_width, 100),
                (255, 255, 255),
                2
            )


            cv2.rectangle(
                img,
                (30, 70),
                (
                    30 + int(bar_width * progress),
                    100
                ),
                (0, 0, 255),
                -1
            )


            # Close after holding fist
            if fist_frames >= FIST_HOLD_FRAMES:

                cv2.putText(
                    img,
                    "CLOSING...",
                    (30, 140),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 0, 255),
                    3
                )

                cv2.imshow(
                    "Virtual Mouse",
                    img
                )

                cv2.waitKey(500)

                exit_program = True
                break


        # ====================================================
        # NORMAL GESTURES
        # ====================================================

        else:

            # Reset fist counter
            fist_frames = 0


            # =================================================
            # DISTANCES
            # =================================================

            thumb_index_distance = distance(
                thumb,
                index_finger
            )

            thumb_middle_distance = distance(
                thumb,
                middle_finger
            )


            # =================================================
            # LEFT CLICK
            # Thumb + Index
            # =================================================

            if thumb_index_distance < 0.055:

                if not left_clicking:

                    pyautogui.click()

                    left_clicking = True


                cv2.putText(
                    img,
                    "LEFT CLICK",
                    (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.9,
                    (0, 255, 0),
                    2
                )


            else:

                left_clicking = False


            # =================================================
            # RIGHT CLICK
            # Thumb + Middle
            # =================================================

            if (
                thumb_middle_distance < 0.055
                and index_open
            ):

                if not right_clicking:

                    pyautogui.rightClick()

                    right_clicking = True


                cv2.putText(
                    img,
                    "RIGHT CLICK",
                    (30, 90),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.9,
                    (255, 0, 0),
                    2
                )


            else:

                right_clicking = False


            # =================================================
            # CURSOR MOVEMENT
            # =================================================

            if index_open:

                # ---------------------------------------------
                # Camera coordinates
                # ---------------------------------------------

                cam_x = int(
                    index_finger.x * img.shape[1]
                )

                cam_y = int(
                    index_finger.y * img.shape[0]
                )


                # ---------------------------------------------
                # Camera control area
                # ---------------------------------------------

                x = max(
                    frame_margin_x,
                    min(
                        index_finger.x,
                        1 - frame_margin_x
                    )
                )

                y = max(
                    frame_margin_y,
                    min(
                        index_finger.y,
                        1 - frame_margin_y
                    )
                )


                # ---------------------------------------------
                # Convert camera → screen
                # ---------------------------------------------

                mouse_x = int(
                    (
                        (x - frame_margin_x)
                        /
                        (1 - 2 * frame_margin_x)
                    )
                    * screen_width
                )


                mouse_y = int(
                    (
                        (y - frame_margin_y)
                        /
                        (1 - 2 * frame_margin_y)
                    )
                    * screen_height
                )


                # ---------------------------------------------
                # Keep cursor inside screen
                # ---------------------------------------------

                mouse_x = max(
                    0,
                    min(
                        screen_width - 1,
                        mouse_x
                    )
                )

                mouse_y = max(
                    0,
                    min(
                        screen_height - 1,
                        mouse_y
                    )
                )


                # ---------------------------------------------
                # Initialize mouse position
                # ---------------------------------------------

                if not mouse_initialized:

                    prev_x = mouse_x
                    prev_y = mouse_y

                    mouse_initialized = True


                # ---------------------------------------------
                # Smooth movement
                # ---------------------------------------------

                smooth_x = (
                    prev_x
                    +
                    (mouse_x - prev_x)
                    /
                    smoothening
                )


                smooth_y = (
                    prev_y
                    +
                    (mouse_y - prev_y)
                    /
                    smoothening
                )


                # ---------------------------------------------
                # Move mouse
                # ---------------------------------------------

                pyautogui.moveTo(
                    int(smooth_x),
                    int(smooth_y)
                )


                # Update previous position

                prev_x = smooth_x
                prev_y = smooth_y


                # ---------------------------------------------
                # Draw index finger position
                # ---------------------------------------------

                cv2.circle(
                    img,
                    (cam_x, cam_y),
                    10,
                    (0, 255, 0),
                    cv2.FILLED
                )


                # ---------------------------------------------
                # Show cursor status
                # ---------------------------------------------

                cv2.putText(
                    img,
                    "MOVING",
                    (30, 130),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 255, 0),
                    2
                )


    else:

        # ====================================================
        # NO HAND DETECTED
        # ====================================================

        fist_frames = 0

        left_clicking = False
        right_clicking = False

        cv2.putText(
            img,
            "NO HAND DETECTED",
            (30, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (0, 0, 255),
            2
        )


    # ========================================================
    # EXIT PROGRAM
    # ========================================================

    if exit_program:
        break


    # ========================================================
    # SHOW CAMERA
    # ========================================================

    cv2.imshow(
        "Virtual Mouse",
        img
    )


    # ========================================================
    # ESC -> EXIT
    # ========================================================

    key = cv2.waitKey(1) & 0xFF

    if key == 27:
        break


# ============================================================
# CLEANUP
# ============================================================

cap.release()

cv2.destroyAllWindows()

hands.close()

print("Virtual Mouse closed successfully.")