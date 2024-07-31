import os
import subprocess
import sys
import requests

WEBHOOK_URL = 'YOUR_DISCORD_WEBHOOK_URL'  # Replace with your Discord webhook URL

def install_requirements():
    """Install required packages."""
    try:
        import requests
    except ImportError:
        print("Installing required packages...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])

def get_ip():
    """Fetch the public IP address."""
    try:
        response = requests.get('https://api.ipify.org?format=json')
        response.raise_for_status()  # Check if the request was successful
        ip_data = response.json()
        return ip_data['ip']
    except requests.RequestException as e:
        print(f"Error fetching IP address: {e}")
        return None

def send_ip_to_discord(ip):
    """Send the IP address to a Discord webhook."""
    if ip:
        payload = {
            "content": f"Your IP address is: {ip}"
        }
        try:
            response = requests.post(WEBHOOK_URL, json=payload)
            response.raise_for_status()  # Check if the request was successful
            print("IP address sent to Discord successfully.")
        except requests.RequestException as e:
            print(f"Error sending IP address to Discord: {e}")

if __name__ == "__main__":
    install_requirements()
    ip = get_ip()
    send_ip_to_discord(ip)
