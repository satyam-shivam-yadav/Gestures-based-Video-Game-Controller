import cv2
import mediapipe as mp
import pyautogui
import math
import time
from collections import deque
import tkinter as tk
from tkinter import Frame, Label
from PIL import Image, ImageTk
import subprocess

subprocess.Popen(["python", r"C:\AI\Hand controller for games\but.py"])
pyautogui.leftClick(2390,24)
pyautogui.moveTo(1000,700)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

screen_width, screen_height = pyautogui.size()

def calculate_distance(point1, point2):
    return math.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)

def calculate_palm_center(landmarks):
    sum_x = landmarks[mp_hands.HandLandmark.WRIST].x
    sum_y = landmarks[mp_hands.HandLandmark.WRIST].y
    
    for mcp in [
        mp_hands.HandLandmark.INDEX_FINGER_MCP,
        mp_hands.HandLandmark.MIDDLE_FINGER_MCP,
        mp_hands.HandLandmark.RING_FINGER_MCP,
        mp_hands.HandLandmark.PINKY_MCP
    ]:
        sum_x += landmarks[mcp].x
        sum_y += landmarks[mcp].y
    
    palm_center_x = sum_x / 5
    palm_center_y = sum_y / 5
    return palm_center_x, palm_center_y

def get_direction(palm_center, thumb_tip):
    x_palm, y_palm = palm_center
    x_thumb, y_thumb = thumb_tip
    dx = x_thumb - x_palm
    dy = y_thumb - y_palm

    # Calculate angle
    angle = math.atan2(dy, dx)

    # Map angle to one of 4 directions: Up, Down, Left, Right
    if -math.pi / 4 <= angle < math.pi / 4:
        return (1, 0)  # Right
    elif math.pi / 4 <= angle < 3 * math.pi / 4:
        return (0, 1)  # Up
    elif -3 * math.pi / 4 <= angle < -math.pi / 4:
        return (0, -1)  # Down
    else:
        return (-1, 0)  # Left

def calculate_angle(point1, point2, point3):
    a = calculate_distance(point2, point3)
    b = calculate_distance(point1, point3)
    c = calculate_distance(point1, point2)
    angle = math.acos((b**2 + c**2 - a**2) / (2 * b * c))
    return math.degrees(angle)

def is_thumb_raised(landmarks, tip, mcp, wrist):
    # Calculate the angle between line (2, 5) and line (2, 4)
    angle = calculate_angle(landmarks[mcp], landmarks[5], landmarks[tip])
    
    # Calculate the distances for the new logic
    distance_4_17 = calculate_distance(landmarks[4], landmarks[17])
    distance_3_17 = calculate_distance(landmarks[3], landmarks[17])
    
    # Thumb is raised if both conditions are satisfied
    return angle > 40 and distance_4_17 / distance_3_17 >= 1.1

def is_finger_raised(landmarks, tip, mcp, wrist):
    distance_tip_wrist = calculate_distance(landmarks[tip], landmarks[wrist])
    distance_mcp_wrist = calculate_distance(landmarks[mcp], landmarks[wrist])
    return distance_tip_wrist / distance_mcp_wrist > 1.4

def is_hand_closed(landmarks):
    fingers = [(8, 5), (12, 9), (16, 13), (20, 17)]
    toreturn =  all(not is_finger_raised(landmarks, tip, mcp, 0) for tip, mcp in fingers)
    return (not is_thumb_raised(landmarks,4,2,0)) and toreturn

def video_mode(previous_mode, current_mode):
    global video_window, lbl_video_2, cap2

    # Only proceed if the mode has changed
    if previous_mode != current_mode:
        # Close the previous video window if it exists
        if 'video_window' in globals() and video_window:
            video_window.destroy()

        # Create a new window for the current mode
        video_window = tk.Toplevel(root)
        video_window.title(f"{current_mode.capitalize()} Mode Tutorial")
        video_window.geometry("600x400+1850+650")  # Set window size and position

        lbl_video_2 = tk.Label(video_window)
        lbl_video_2.pack()

        # Load the appropriate video based on the mode
        if current_mode == "mouse":
            video_path = r"C:\Users\asus\Downloads\mouse mode tutorial video - Made with Clipchamp.mp4"  # Replace with your mouse mode video path
        elif current_mode == "game":
            video_path = r"C:\Users\asus\Downloads\Game mode tutorial - Made with Clipchamp.mp4"  # Replace with your game mode video path

        cap2 = cv2.VideoCapture(video_path)

        def update_video():
            ret, frame_2 = cap2.read()
            if ret:
                frame_2 = cv2.resize(frame_2, (600, 400))  # Resize to fit the window
                frame_2 = cv2.cvtColor(frame_2, cv2.COLOR_BGR2RGB)
                img_2 = ImageTk.PhotoImage(Image.fromarray(frame_2))
                lbl_video_2.config(image=img_2)
                lbl_video_2.image = img_2
            else:
                cap2.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Restart the video if it ends
            lbl_video_2.after(10, update_video)

        update_video()

# Function to check specific gestures for mouse actions
def detect_mouse_gestures(left_hand_landmarks):
    if is_hand_closed(left_hand_landmarks):
        return "closed"

    index_raised = is_finger_raised(left_hand_landmarks, 8, 5, 0)
    middle_raised = is_finger_raised(left_hand_landmarks, 12, 9, 0)
    thumb_raised = is_thumb_raised(left_hand_landmarks, 4, 2, 0)

    if index_raised and not middle_raised and not thumb_raised:
        return "left_click"
    elif thumb_raised and not index_raised and not middle_raised:
        return "right_click"
    elif index_raised and middle_raised and not thumb_raised:
        return "mouse_down"

    return None

# Initialize tkinter window
root = tk.Tk()
root.title("Camera Feed")

root.geometry("665x500+1850+100") 

#Camera feed
frame_camera = Frame(root, width=640, height=480, bg="black")
frame_camera.grid(row=0, column=0, padx=10, pady=10)

lbl_video = Label(frame_camera)
lbl_video.pack()

# Handle window close event
def on_closing():
    cap.release()  # Release the camera
    root.destroy()  # Destroy the tkinter window

# Initialize variables
cap = cv2.VideoCapture(0)
root.protocol("WM_DELETE_WINDOW", on_closing)

game_mode_active = False
# Variables to track current and previous mode
current_mode = "mouse"  # Initial mode is mouse
previous_mode = None

gesture_triggered = {"left_click": False, "right_click": False}
prev_x, prev_y = pyautogui.position()
move_distance=100
smoothing_factor = 0.9
mouse_down_active = False

# Constants for landmarks intially for scrolling
INDEX_FINGER_TIP = 8
INDEX_FINGER_MCP = 5
MIDDLE_FINGER_TIP = 12
MIDDLE_FINGER_MCP = 9
WRIST = 0

# Initialize variables for cursor
prev_index_x, prev_index_y = None, None
middle_y_buffer = deque(maxlen=5)  # Buffer for smoothing middle finger Y-coordinate
scroll_time = time.time()

# Sensitivity settings for cursor
SCROLL_THRESHOLD = 0.03  # Minimum movement threshold (normalized)
SMOOTHING_FACTOR = 5 

# Variables for game mode:
a_pressed = False
d_pressed = False
w_pressed = False
space_pressed = False
s_pressed = False

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        continue

    # Flip frame horizontally for a mirrored view
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        hand_landmarks_list = results.multi_hand_landmarks
        handedness_list = results.multi_handedness

        left_hand = None
        right_hand = None

        for hand_landmarks, handedness in zip(hand_landmarks_list, handedness_list):
            label = handedness.classification[0].label
            if label == "Left":
                left_hand = hand_landmarks
            elif label == "Right":
                right_hand = hand_landmarks

        # Check if we need to activate game mode
        if not game_mode_active and left_hand and right_hand:
            left_index_raised = is_finger_raised(left_hand.landmark, 8, 5, 0)
            left_pinky_raised = is_finger_raised(left_hand.landmark, 20, 17, 0)
            right_index_raised = is_finger_raised(right_hand.landmark, 8, 5, 0)
            right_pinky_raised = is_finger_raised(right_hand.landmark, 20, 17, 0)

            if left_index_raised and left_pinky_raised and right_index_raised and right_pinky_raised:
                game_mode_active = True
                pyautogui.press('space')
                time.sleep(1)

        # Deactivate game mode if all fingers of the left hand are raised
        if game_mode_active and left_hand:
            all_fingers_raised = all(
                is_finger_raised(left_hand.landmark, tip, mcp, 0)
                for tip, mcp in [(8, 5), (12, 9), (16, 13), (20, 17)]
            )
            thumb_up = is_thumb_raised(left_hand.landmark, 4, 2, 0)

            # print("Index:", is_finger_raised(left_hand.landmark, 8, 5, 0))
            # print("Middle:", is_finger_raised(left_hand.landmark, 12, 9, 0))
            # print("Ring:", is_finger_raised(left_hand.landmark, 16, 13, 0))
            # print("Pinky:", is_finger_raised(left_hand.landmark, 20, 17, 0))
            # print("Thumb:", thumb_up)

            if all_fingers_raised and thumb_up:
                print("All fingers raised: Deactivating game mode.")
                game_mode_active = False
                pyautogui.press('esc')
                time.sleep(1)

        # Handle game mode
        if game_mode_active:
            mode_text = "Game Mode"
            current_mode = "game"
            # Add logic for game mode (if any)
            LEFT_THUMB_RAISED = False
            LEFT_INDEX_RAISED = False
            LEFT_MIDDLE_RAISED = False
            RIGHT_THUMB_RAISED = False
            RIGHT_INDEX_RAISED = False
            RIGHT_MIDDLE_RAISED = False

            if left_hand :
                if is_thumb_raised(left_hand.landmark,4,2,0):
                    LEFT_THUMB_RAISED = True
                if is_finger_raised(left_hand.landmark,8,5,0):
                    LEFT_INDEX_RAISED = True
                if is_finger_raised(left_hand.landmark,12,9,0):
                    LEFT_MIDDLE_RAISED = True

            if right_hand:
                if is_thumb_raised(right_hand.landmark,4,2,0):
                    RIGHT_THUMB_RAISED = True
                if is_finger_raised(right_hand.landmark,8,5,0):
                    RIGHT_INDEX_RAISED = True
                if is_finger_raised(right_hand.landmark,12,9,0):
                    RIGHT_MIDDLE_RAISED = True
            
            if LEFT_THUMB_RAISED:          #For pressing a
                if not a_pressed:
                    pyautogui.keyDown('a')
                    print("pressed a")
                    a_pressed = True
            elif a_pressed:
                pyautogui.keyUp('a')
                print("released a")
                a_pressed = False
            
            if RIGHT_THUMB_RAISED:         # For pressing d
                if not d_pressed:
                    pyautogui.keyDown('d')
                    print("pressed d")
                    d_pressed = True
            elif d_pressed:
                pyautogui.keyUp('d')
                print("released d")
                d_pressed = False

            if LEFT_INDEX_RAISED and LEFT_MIDDLE_RAISED and RIGHT_INDEX_RAISED and RIGHT_MIDDLE_RAISED :
                if not space_pressed:
                    pyautogui.keyDown('space')
                    print("pressed space")
                    space_pressed = True
            elif space_pressed:
                pyautogui.keyUp('space')
                print("released space")
                space_pressed = False
            
            if LEFT_INDEX_RAISED and not LEFT_MIDDLE_RAISED:
                if not s_pressed:
                    pyautogui.keyDown('s')
                    print("pressed s")
                    s_pressed = True
            elif s_pressed:
                pyautogui.keyUp('s')
                print("released s")
                s_pressed = False
            
            if RIGHT_INDEX_RAISED and not RIGHT_MIDDLE_RAISED:
                if not w_pressed:
                    pyautogui.keyDown('w')
                    print("pressed w")
                    w_pressed = True
            elif w_pressed:
                pyautogui.keyUp('w')
                print("released w")
                w_pressed = False

        # Handle mouse mode
        else:
            mode_text = "Mouse Mode"
            current_mode = "mouse"
            if left_hand:
                gesture = detect_mouse_gestures(left_hand.landmark)
                
                # Left click gesture
                if gesture == "left_click":
                    if not gesture_triggered["left_click"]:  # Only trigger once
                        pyautogui.click()
                        print("Left click")
                        gesture_triggered["left_click"] = True
                elif gesture_triggered["left_click"]:  # Reset if no left click gesture
                    gesture_triggered["left_click"] = False

                
                # Right click gesture
                if gesture == "right_click":
                    if not gesture_triggered["right_click"]:  # Only trigger once
                        pyautogui.click(button='right')
                        print("Right click")
                        gesture_triggered["right_click"] = True
                elif gesture_triggered["right_click"]:  # Reset if no right click gesture
                    gesture_triggered["right_click"] = False

                if gesture == "mouse_down":
                    if not mouse_down_active:
                        pyautogui.mouseDown()
                        mouse_down_active = True
                elif gesture == "closed" and mouse_down_active:
                    pyautogui.mouseUp()
                    print("mouseUp")
                    mouse_down_active = False

            if right_hand:
                if is_thumb_raised(right_hand.landmark, 4, 2, 0) and not is_finger_raised(right_hand.landmark,8,5,0):
                    thumb_tip = right_hand.landmark[mp_hands.HandLandmark.THUMB_TIP]

                    # Highlight the thumb
                    h, w, _ = frame.shape
                    thumb_tip_x = int(thumb_tip.x * w)
                    thumb_tip_y = int(thumb_tip.y * h)
                    cv2.circle(frame, (thumb_tip_x, thumb_tip_y), 10, (0, 0, 255), -1)

                    # Calculate palm center using MCPs
                    palm_center_x, palm_center_y = calculate_palm_center(right_hand.landmark)

                    # Convert normalized coordinates to pixel coordinates
                    palm_center_x_pixels = int(palm_center_x * w)
                    palm_center_y_pixels = int(palm_center_y * h)

                    # Draw palm center for visualization
                    cv2.circle(frame, (palm_center_x_pixels, palm_center_y_pixels), 5, (0, 255, 0), -1)

                    # Calculate direction and move cursor
                    direction = get_direction((palm_center_x_pixels, palm_center_y_pixels), (thumb_tip_x, thumb_tip_y))

                    # Move cursor by a larger distance
                    move_x = move_distance * direction[0]
                    move_y = move_distance * direction[1]

                    # Get current position of the cursor
                    current_pos = pyautogui.position()

                    # Calculate new cursor position with smoothing
                    target_x = min(max(current_pos[0] + move_x, 0), screen_width - 1)
                    target_y = min(max(current_pos[1] + move_y, 0), screen_height - 1)

                    # Apply smoothing
                    new_x = int(prev_x + smoothing_factor * (target_x - prev_x))
                    new_y = int(prev_y + smoothing_factor * (target_y - prev_y))

                    # Move cursor
                    pyautogui.moveTo(new_x, new_y, 0.01)

                    # Update previous cursor position
                    prev_x, prev_y = new_x, new_y
                
                elif is_finger_raised(right_hand.landmark,8,5,0) and not is_finger_raised(right_hand.landmark,12,9,0):
                    landmarks = right_hand.landmark
                    index_tip = landmarks[8]
                    index_mcp = landmarks[5]
                    wrist = landmarks[0]

                    # Cursor Control: Move based on index finger
                    curr_index_x, curr_index_y = int(index_tip.x * screen_width), int(index_tip.y * screen_height)
                    if prev_index_x is not None and prev_index_y is not None:
                        # Calculate the direction of movement
                        delta_x = curr_index_x - prev_index_x
                        delta_y = curr_index_y - prev_index_y

                        # Update the cursor position
                        pyautogui.move(delta_x, delta_y)

                    # Update the previous position
                    prev_index_x, prev_index_y = curr_index_x, curr_index_y

                elif is_finger_raised(right_hand.landmark,8,5,0) and is_finger_raised(right_hand.landmark,12,9,0):
                    # Scroll Control: Use the middle finger
                    middle_y_buffer.append(right_hand.landmark[MIDDLE_FINGER_TIP].y)  # Add current Y to the buffer

                    if len(middle_y_buffer) == SMOOTHING_FACTOR:
                        # Calculate the smoothed Y-coordinate
                        smoothed_middle_y = sum(middle_y_buffer) / SMOOTHING_FACTOR
                        curr_time = time.time()

                        if (abs(smoothed_middle_y - middle_y_buffer[0]) > SCROLL_THRESHOLD and curr_time - scroll_time >= 0.1):
                            # Calculate the scroll direction
                            delta_y = smoothed_middle_y - middle_y_buffer[0]
                            scroll_amount = int(delta_y * 4000)  # Scaling factor for smoother scrolling
                            pyautogui.scroll(scroll_amount)  # Negative for correct direction

                            # Update the scroll time
                            scroll_time = curr_time
                else:
                    # Fingers not raised, reset previous positions
                    prev_index_x, prev_index_y = None, None
                    middle_y_buffer.clear()

        # Draw landmarks and mode text
        for hand_landmarks in hand_landmarks_list:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    else:
        mode_text = "Mouse Mode"

    # Display the mode name
    cv2.putText(frame, mode_text, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    video_mode(previous_mode, current_mode)
    previous_mode = current_mode

    # Convert the frame to PIL format and update the tkinter Label
    img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    imgtk = ImageTk.PhotoImage(image=img)
    lbl_video.imgtk = imgtk
    lbl_video.configure(image=imgtk)

    # Update the tkinter GUI
    root.update_idletasks()
    root.update()

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()