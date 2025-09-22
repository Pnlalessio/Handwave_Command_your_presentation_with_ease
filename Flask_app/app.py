# Import necessary libraries.
from flask import Flask, jsonify, render_template, request, Response
from my_hand_detector import HandDetector # This is a custom hand detection module placed in an other class file.
import cv2
import pyautogui
from pynput.mouse import Controller, Button
import platform
import time
import requests

# Initialize Flask app.
app = Flask(__name__)

global global_outWidth
global global_outHeight
global global_inHeight
global global_inWidth
global global_screenHeight
global global_screenWidth
global tutorial_activated
global pen_activated
global back_from_full_screen
global_outWidth = 0
global_outHeight = 0
global_inHeight = 0
global_inWidth = 0
global_screenHeight = 0
global_screenWidth = 0
pen_activated = True
tutorial_activated = True
back_from_full_screen = False

global tutorial_activated_wio
global pen_activated_wio
pen_activated_wio = True
tutorial_activated_wio = True

# Function to get full screen.
def get_full_screen():
    global global_outWidth
    global global_outHeight
    global global_inWidth
    global global_inHeight

    # Get screen dimensions
    w = int(pyautogui.size()[0])
    h = int(pyautogui.size()[1])
    time.sleep(0.4)
    os_name = platform.system() # Detect operating system.

    # Toggle fullscreen based on the operating system.
    if os_name == "Windows":
        pyautogui.hotkey('F11')
    elif os_name == "Darwin":
        # Check if the screen dimensions have changed.
        if (global_outWidth != w or global_outHeight != h):
            time.sleep(0.4)
            pyautogui.keyDown('Command')
            pyautogui.keyDown('Ctrl') 
            pyautogui.press('f')
            pyautogui.keyUp('Command')
            pyautogui.keyUp('Ctrl')

# This function is called when we enter the hands-only control mode of a presentation.
def main():
    # Declare global variables.
    global global_outHeight
    global global_inHeight
    global tutorial_activated
    global pen_activated

    # Initialize variables.
    cursorStart = False
    os_name = platform.system()
    width, height = pyautogui.size()
    gesture_threshold = 500
    detector_hand = HandDetector(detection_confidence=0.8, max_num_hands=1)
    button_pressed = False
    delay = 20
    counter = 0
    pyautogui.FAILSAFE = False # Disable failsafe to prevent interruptions.

    # Initialize mouse controller.
    mouse = Controller()
    mouse.position = (900, 600)

    time.sleep(1) # Wait for 1 second.
    get_full_screen() # Enable fullscreen.
    time.sleep(2) # Wait for 2 seconds.

    # Simulate a left mouse click and pressing 'p' key twice.
    mouse.click(Button.left) 
    pyautogui.hotkey('p')
    pyautogui.hotkey('p')

    cap = cv2.VideoCapture(0) # Capture video from the default camera (0).

    # Continue processing frames while the video capture is open.
    while cap.isOpened():
        # Read a frame from the video capture, flip and resize this frame.
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (width, height))
        hands, frame = detector_hand.find_hands(frame) # Detect hands in the frame.
        cv2.line(frame, (0, gesture_threshold), (width, gesture_threshold), (0, 255, 0), 10) # Draw a green line at the gesture threshold.

        # Check if hands are detected and button is false.
        if hands and button_pressed is False:
            hand = hands[0]
            hand_type = hand["type"]
            cx, cy = hand["center"]
            lm_list = hand["landmarks_list"]
            fingers = detector_hand.count_fingers_up(hand)
            x_val = int(lm_list[8][0] * 1.2)
            y_val = int(lm_list[8][1] * 1.2)

            # Check gesture conditions based on finger positions.
            if cy <= gesture_threshold: # Condition to check that the gesture is performed above the green line used as a threshold.
                if fingers == [1, 0, 0, 0, 0]: # Gesture used to scroll the slide backward.
                    # Release left mouse button and simulate 'p' or 'n' key press based on the hand chosen by the user.
                    mouse.release(Button.left)
                    if hand_type =="Left":
                        pyautogui.hotkey('p')
                    else:
                        pyautogui.hotkey('n')
                    button_pressed = True
                elif fingers == [0, 0, 0, 0, 1]: # Gesture used to scroll the slide forward.
                    # Release left mouse button and simulate 'p' or 'n' key press based on the hand chosen by the user.
                    mouse.release(Button.left)
                    if hand_type =="Left":
                        pyautogui.hotkey('n')
                    else:
                        pyautogui.hotkey('p')
                    button_pressed = True
                elif fingers == [0, 1, 1, 1, 0]: # Gesture used to activate the pen.
                    # Release left mouse button and simulate 'shift' and 'L' key press.
                    mouse.release(Button.left)
                    pyautogui.hotkey('shift', 'L')
                    button_pressed = True
                    if cursorStart is True:
                        cursorStart = False
                        delay = 15
                    else:
                        cursorStart = True
                    if pen_activated is True:
                        pen_activated = False
                        delay = 15
                    else:
                        pen_activated = True
                elif fingers == [0, 0, 0, 0, 0]: # Gesture used to delete annotations.
                    # Release left mouse button and simulate 'A' key press.
                    mouse.release(Button.left)
                    pyautogui.hotkey('A')
                    button_pressed = True
                elif fingers == [1, 1, 1, 1, 1]: # Gesture used to exit the presentation and return to the homepage.
                    # Simulates pressing various shortcuts depending on the operating system.
                    if os_name == "Windows":
                        pyautogui.keyDown('alt')
                        pyautogui.press('left')
                        pyautogui.keyUp('alt')
                        get_full_screen()
                    elif os_name == "Darwin":
                        time.sleep(0.4)
                        pyautogui.hotkey('Command', 'left')
                        time.sleep(1)
                elif fingers == [0, 1, 1, 1, 1]: # Gesture used to open and close the tutorial.
                    button_pressed = True
                    if tutorial_activated is True:
                        tutorial_activated = False
                        delay = 15
                    else:
                        tutorial_activated = True

            if fingers == [0, 1, 1, 0, 0] and cursorStart is True: # Gesture used to move the pointer.
                mouse.release(Button.left)
                mouse.position = (x_val, y_val)
            if fingers == [0, 1, 0, 0, 0] and cursorStart is True: # Gesture used for drawing/annotating.
                if (int(mouse.position[1]) > (global_outHeight - global_inHeight + 10)) and (int(mouse.position[0]) > (global_outWidth - global_inWidth + 10)):
                    mouse.press(Button.left)
                    mouse.position = (x_val, y_val)
        # If button_pressed is true, handle the delay before next action.  
        if button_pressed:
            counter += 1
            if counter > delay:
                counter = 0
                button_pressed = False

        if not ret: # If video capture ends, exit the loop.
            break
        # Encode and yield the frame for streaming.
        _, buffer = cv2.imencode('.jpg', frame)
        frame_encoded = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_encoded + b'\r\n')

#This function is called when we enter the control mode of a presentation using Wio Terminal      
def main_wio():
    # Declare global variables..
    global global_outHeight
    global global_inHeight
    global tutorial_activated_wio
    os_name = platform.system() # Get the operating system name.

    # Initialize local variables
    button_pressed_wio = False
    delay_wio = 15
    counter_wio = 0
    pyautogui.FAILSAFE = False # Disable PyAutoGUI failsafe to prevent accidental termination.

    # Initialize mouse controller and set initial position.
    mouse = Controller()
    mouse.position = (900, 600)

    time.sleep(1) # Wait for 1 second before starting.
    get_full_screen() # Trigger the function to get the full screen.
    time.sleep(2) # Wait for an additional 2 seconds.

    # Simulate a left mouse click and press 'p' twice.
    mouse.click(Button.left) 
    pyautogui.hotkey('p')
    pyautogui.hotkey('p')

    # Start an infinite loop for continuous Wio Terminal control.
    while True:
        value = blynk_request() # Make a request to the Blynk server to retrieve the value of the label associated with the gesture made with the Wio Terminal and sent in real-time to the server.

        if value is not None and button_pressed_wio is False: # Check if a valid value is received and button_pressed_wio is false.
            if value == "idle": # If the received value is idle, it does nothing.
                print("idle")
            elif value == "left": # If the received value is left, switch to the previous slide.
                pyautogui.hotkey('p')
                button_pressed_wio = True
            elif value == "right": # If the received value is right, switch to the next slide.
                pyautogui.hotkey('n')
                button_pressed_wio = True
            elif value == "flip": # If the received value is flip, it exits the presentation and returns to the homepage.
                if os_name == "Windows": 
                    button_pressed_wio = True
                    pyautogui.keyDown('alt')
                    pyautogui.press('left')
                    pyautogui.keyUp('alt')
                    get_full_screen()
                    break
                elif os_name == "Darwin":
                    button_pressed_wio = True
                    time.sleep(0.4)
                    pyautogui.hotkey('Command', 'left')
                    time.sleep(1)
                    break
            elif value == "down": # If the received value is down, it opens or closes the tutorial.
                button_pressed_wio = True
                if tutorial_activated_wio is True:
                    tutorial_activated_wio = False
                    delay_wio = 25
                else:
                    tutorial_activated_wio = True
            else:
                print("Unknown value:", value) # Print an unknown value

        if button_pressed_wio: # If button_pressed_wio is true, handle the delay before next action.
            counter_wio += 1
            if counter_wio > delay_wio:
                counter_wio = 0
                button_pressed_wio = False
    
# Function to make a request to the Blynk server      
def blynk_request():
    blynk_server = "https://fra1.blynk.cloud/external/api/getAll?token=NmEFh0ohBnnS-Xwmykao8XBWPLOkoHoN" # Blynk server URL with the provided token
    response = requests.get(blynk_server) # Send a GET request to the Blynk server
    if response.status_code == 200: # Check if the response status code is 200 (OK)
        return response.json()["v0"] # Return the value received from the Blynk server
    else:
        print("Error code: " + str(response.status_code)) # Print an error message if the response status code is not 200

# Define a Flask route for the home page, accessible via POST and GET methods
# This function was used to retrieve the values of the web page dimensions, both for the outer and inner dimensions. This function is designed to 
# periodically check the current status of the web page. Depending on whether it is in fullscreen or not, certain operations are performed.
@app.route('/', methods=['POST', 'GET'])
def home(): 
    global back_from_full_screen
    os_name = platform.system()
    value_to_pass = request.args.get('value_to_pass', '')
    if value_to_pass == "true":
        back_from_full_screen = True
    if request.method == 'POST':
        data_full_screen = request.get_json()
        isVisible = data_full_screen.get('isVisible', 'Unknown isVisible')
        if back_from_full_screen == True and isVisible == "true":
            if os_name == "Windows":
                time.sleep(2)
                get_full_screen()
            back_from_full_screen = False

    if request.method == 'POST':
        data = request.get_json()
        global global_outWidth
        global global_outHeight
        global global_inHeight
        global global_inWidth
        global global_screenHeight
        global global_screenWidth

        # Get values from the JSON data or set default values if they are not present.
        outWidth = data.get('w', "Unknown w")
        outHeight = data.get('h', "Unknown h")
        inWidth = data.get('width', "Unknown width")
        inHeight = data.get('height', "Unknown height")

        # Update global variables based on received data.
        if outWidth != "Unknown w":
            global_outWidth = outWidth
        if outHeight != "Unknown h":
            global_outHeight = outHeight
        if inWidth != "Unknown width":
            global_inWidth = inWidth
        if inHeight != "Unknown height":
            global_inHeight = inHeight
        return jsonify({'success': True}) # Return a JSON response indicating success.
    else:
        return render_template('index.html', value_to_pass=value_to_pass) # Return a rendered template with 'value_to_pass' passed as context.

# Flask route for the hand control page.
@app.route('/hand_control_page', methods=['POST', 'GET'])
def hand_control_page():
    # Check if the request method is POST.
    if request.method == 'POST':
        global tutorial_activated
        global pen_activated
        if tutorial_activated is False: # Check and update the state of tutorial activation.
            tutorial_activated = True
        if pen_activated is False: # Check and update the state of pen activation.
            pen_activated = True            
        presentation_url = request.form.get('presentation_url', '') # Get the presentation URL from the form data.
        return render_template('hand_control_page.html', presentation_url=presentation_url, tutorial_activated=tutorial_activated, pen_activated=pen_activated) # Render the 'hand_control_page.html' template with updated variables.
    else:
        return Response(main(), mimetype='multipart/x-mixed-replace; boundary=frame') # If the request method is not POST, return the response from the 'main' function.

# Flask route for the Wio Terminal control page with support for both POST and GET requests.
@app.route('/wio_control_page', methods=['POST', 'GET'])
def wio_control_page():
    if request.method == 'POST': # Check if the request method is POST.
        global tutorial_activated_wio
        global pen_activated_wio
        if tutorial_activated_wio is False: # Check and update the tutorial activation status for Wio Terminal control.
            tutorial_activated_wio = True
        if pen_activated_wio is False: # Check and update the pen activation status for Wio Terminal control.
            pen_activated_wio = True            
        presentation_url = request.form.get('presentation_url', '') # Get the 'presentation_url' value from the form data.
        return render_template('wio_control_page.html', presentation_url=presentation_url, tutorial_activated_wio=tutorial_activated_wio, pen_activated_wio=pen_activated_wio) # Render the 'wio_control_page.html' template with relevant data.
    else:
        return Response(main_wio(), mimetype='multipart/x-mixed-replace; boundary=frame') # If the request method is not POST, return the response from the 'main_wio()' function.

# Flask route for getting the hand control tutorial status.
@app.route('/get_tutorial_status')
def get_tutorial_status():
    global tutorial_activated
    return {'tutorial_activated': tutorial_activated}

# Flask route for getting the hand control pen status.
@app.route('/get_pen_status')
def get_pen_status():
    global pen_activated
    return {'pen_activated': pen_activated}

# Flask route for getting the Wio Terminal tutorial status.
@app.route('/get_tutorial_status_wio')
def get_tutorial_status_wio():
    global tutorial_activated_wio
    return {'tutorial_activated_wio': tutorial_activated_wio}

if __name__ == '__main__':
    app.run(debug=True)


