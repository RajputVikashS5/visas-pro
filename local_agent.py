import socketio
import pyttsx3
import threading
from core.voice_handler import VoiceHandler
from dotenv import load_dotenv

load_dotenv()
sio = socketio.Client()
voice = VoiceHandler()
CLOUD_URL = 'https://visas-pro.onrender.com'  # Replace with your Render URL
try:
    import requests
    if requests.get(CLOUD_URL, timeout=3).status_code != 200:
        CLOUD_URL = "http://localhost:5000"
        print("🌐 Using local server instead of Render.")
except:
    CLOUD_URL = "http://localhost:5000"
    print("🌐 Using local server (Render offline).")

@sio.event
def connect():
    print(f"✅ Connected to Visas Cloud: {CLOUD_URL}")

@sio.on('response')
def on_response(data):
    print(f"Visas: {data['text']}")
    voice.speak(data['text'])

@sio.on('notification')
def on_notification(data):
    print(f"🔔 {data['message']}")

# Start voice forwarding to cloud
def forward_voice():
    voice.start_continuous_listening_to_cloud(sio)  # Implement forwarding

if __name__ == '__main__':
    threading.Thread(target=forward_voice, daemon=True).start()
    sio.connect(CLOUD_URL)
    sio.wait()