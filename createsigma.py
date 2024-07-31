import subprocess
import sys

def install_packages():
    """Install required packages."""
    requirements = [
        'pyautogui',
        'opencv-python',
        'numpy'
    ]
    for package in requirements:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

def main():
    try:
        import pyautogui
        import cv2
        import numpy as np
    except ImportError:
        print("Required packages are not installed. Installing...")
        install_packages()
        import pyautogui
        import cv2
        import numpy as np

    # Define the screen size
    screen_size = pyautogui.size()
    width, height = screen_size.width, screen_size.height

    # Define the codec and create a VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('screen_record.avi', fourcc, 20.0, (width, height))

    print("Recording... Press Ctrl+C to stop.")

    try:
        while True:
            # Take a screenshot
            img = pyautogui.screenshot()

            # Convert the image to a format suitable for OpenCV
            frame = np.array(img)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Write the frame to the video file
            out.write(frame)
    except KeyboardInterrupt:
        print("Recording stopped.")

    # Release everything when the recording is done
    out.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
