GestureMenu
GestureMenu is a simple gesture-controlled menu system that allows users to interact with a visual menu using hand gestures detected by a webcam. This project utilizes MediaPipe for hand landmark detection and OpenCV for visual processing.

Features
Hand Tracking: Uses MediaPipe to detect and track hand landmarks and gestures.
Dynamic Right-Side Menu: Displays a three-option menu on the right side of the screen.
Gesture-Based Hover Selection: Hovering over a menu option changes its color to red, and holding the hover for 3 seconds turns it green, indicating a selection.
Prerequisites
Ensure the following are installed on your machine:

Python 3.x
OpenCV
MediaPipe
Install the required packages with:

bash
pip install opencv-python mediapipe
How to Run
Clone the Repository:

bash
git clone https://github.com/Hamedsamak66/GestureMenu.git
cd GestureMenu
Run the Script:

Execute the script by using:

bash
python gesture_menu.py
Usage Instructions:

The script will open your webcam. Ensure your hand is visible within the frame.
Extend all five fingers to open the menu.
Hover over any menu option to highlight it in red.
Continue holding your hand over an option for 3 seconds to select (turns green).
Exit:

To exit the program, press the ‘q’ key on your keyboard.
Project Structure
gesture_menu.py: Main script containing logic for hand tracking and gesture-based menu interaction.
Customization
Adjust menu locations, sizes, and colors by editing the rectangle positions and colors in the code to customize the UI layout as needed.
Troubleshooting
Ensure your webcam is functional and that Python has access to it.
If the hand landmarks do not appear reliably, adjust the lighting and ensure your hand is fully visible to the webcam.
License
This project is licensed under the MIT License.

Contributions
Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

Credits
Thanks to the MediaPipe team for providing efficient and effective hand tracking solutions.
