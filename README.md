🖱️ Virtual Mouse Using Hand Gestures

A Python-based Virtual Mouse that allows users to control their computer mouse using hand gestures through a webcam.

The project uses OpenCV for video processing, MediaPipe for hand tracking, and PyAutoGUI for controlling the system mouse.

🚀 Features

- 🖱️ Move the cursor using the index finger
- 👆 Thumb + Index Finger → Left Click
- 🤏 Thumb + Middle Finger → Right Click
- ✊ Hold a fist → Close the program
- 🎯 Smooth cursor movement
- ✋ Real-time hand landmark detection
- ⌨️ Press "ESC" to exit
- 📊 Fist-hold progress indicator

🛠️ Technologies Used

- Python
- OpenCV
- MediaPipe
- PyAutoGUI
- Math

📂 Project Structure

virtual-mouse/
│
├── virtual_mouse.py
├── requirements.txt
└── README.md

⚙️ How It Works

The webcam captures the user's hand and MediaPipe detects the hand landmarks.

The detected landmarks are then used to identify different gestures. Based on the detected gesture, PyAutoGUI performs the corresponding mouse action.

Webcam
   ↓
OpenCV
   ↓
MediaPipe Hand Detection
   ↓
Gesture Recognition
   ↓
PyAutoGUI
   ↓
Mouse Action

✋ Gesture Controls

Gesture| Action
☝️ Index finger open| Move cursor
👆 Thumb + Index finger| Left click
🤏 Thumb + Middle finger| Right click
✊ Closed fist| Close program
"ESC"| Exit

🖱️ Cursor Movement

When the index finger is open, its position is detected using MediaPipe.

The camera coordinates are converted into screen coordinates, allowing the index finger to control the mouse cursor.

The project also uses cursor smoothing to reduce unwanted shaking.

smoothening = 7

👆 Left Click

When the thumb and index finger come close together, the program detects the gesture as a left click.

thumb_index_distance < 0.055

🤏 Right Click

When the thumb and middle finger come close together while the index finger is open, the program performs a right click.

thumb_middle_distance < 0.055

✊ Exit Using Fist

When all four fingers are closed, the program detects a fist.

The fist must be held for a specific number of frames before the program closes.

FIST_HOLD_FRAMES = 25

This prevents the program from closing accidentally when a fist is detected for only a short time.

📦 Installation

1. Clone the Repository

git clone https://github.com/YOUR_USERNAME/virtual-mouse.git

2. Open the Project

cd virtual-mouse

3. Install Dependencies

pip install -r requirements.txt

Or install them directly:

pip install opencv-python mediapipe pyautogui

📄 requirements.txt

opencv-python
mediapipe
pyautogui

▶️ Run the Project

Make sure your webcam is connected and run:

python virtual_mouse.py

A window named Virtual Mouse will open and start detecting your hand.

⚠️ Troubleshooting

Camera Not Opening

If you see:

Camera open avvaledu!

make sure your webcam is connected and available.

You can also try changing:

cap = cv2.VideoCapture(0)

to:

cap = cv2.VideoCapture(1)

MediaPipe Error

If you get:

AttributeError: module 'mediapipe' has no attribute 'solutions'

check your MediaPipe installation and make sure there is no file or folder named "mediapipe.py" inside your project.

You can check the installed version with:

pip show mediapipe

🔮 Future Improvements

Some possible improvements are:

- Double-click gesture
- Mouse drag gesture
- Scroll using hand gestures
- Two-hand support
- Adjustable gesture sensitivity
- Voice commands
- Improved gesture accuracy
- GUI for changing mouse settings

👨‍💻 Author

Rohith Dupaguntla

CSE – Artificial Intelligence

⭐ Support

If you find this project useful, consider giving the repository a ⭐ on GitHub.

📜 License

This project is created for educational and personal use.
