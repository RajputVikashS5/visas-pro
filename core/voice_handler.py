from datetime import time
import traceback
import speech_recognition as sr
import sounddevice as sd
import pyttsx3
import numpy as np
import librosa
import io
import base64
import threading
import logging

class VoiceHandler:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.recognizer = sr.Recognizer()
        try:
            self.microphone = sr.Microphone()
        except Exception as e:
            print(f"[VoiceHandler] ⚠️ Microphone initialization failed: {e}")
            self.microphone = None
        self.whisper_mode = False
        self.listening = False
    def start_continuous_listening_to_cloud(self, sio, phrase_time_limit=5):
        """Capture mic audio and send base64 WAV chunks to server via 'voice_input' event."""
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)

        while True:
            try:
                with self.microphone as source:
                    audio = self.recognizer.listen(source, phrase_time_limit=phrase_time_limit)

                wav_bytes = audio.get_wav_data()                # 16-bit PCM WAV
                audio_b64 = base64.b64encode(wav_bytes).decode("ascii")
                sio.emit('voice_input', audio_b64)              # matches your server event
            except Exception:
                traceback.print_exc()
                time.sleep(0.5)
    def detect_emotion(self, audio_wav):
        y, sr = librosa.load(io.BytesIO(audio_wav), sr=16000)
        energy = np.mean(librosa.feature.rms(y=y))
        pitch = np.mean(librosa.yin(y, fmin=50, fmax=500))
        if energy > 0.12: return "stressed"
        if energy < 0.04: return "calm"
        return "neutral"

    def speak(self, text):
        rate = 80 if self.whisper_mode else 150
        volume = 0.3 if self.whisper_mode else 1.0
        self.engine.setProperty('rate', rate)
        self.engine.setProperty('volume', volume)
        self.engine.say(text)
        self.engine.runAndWait()

    def audio_to_text(self, audio_base64):
        audio_data = base64.b64decode(audio_base64)
        with sr.AudioFile(io.BytesIO(audio_data)) as source:
            audio = self.recognizer.record(source)
        try:
            return self.recognizer.recognize_google(audio)
        except:
            return None

    def toggle_whisper(self):
        self.whisper_mode = not self.whisper_mode
        return f"Whisper mode {'ON' if self.whisper_mode else 'OFF'}"

    def start_continuous_listening(self, openrouter_client, memory_manager, system_controller, plugins, socketio):
        self.listening = True
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
        while self.listening:
            try:
                audio = self.recognizer.listen(source, timeout=1)
                text = self.recognizer.recognize_google(audio)
                if "hey visas" in text.lower():
                    query = text.lower().replace("hey visas", "").strip()
                    emotion = self.detect_emotion(audio.get_wav_data())
                    if emotion == "stressed":
                        query = f"[Stressed user] {query}"
                    session_id = 'voice'
                    history = memory_manager.get_history(session_id)
                    response, tool_calls = openrouter_client.query(query, history, [t for p in plugins.values() for t in p.get_tools()])
                    if tool_calls:
                        for call in tool_calls:
                            result = system_controller.execute_tool(call, plugins)
                            response += f"\nExecuted: {result}"
                    memory_manager.add_to_history(session_id, query, response)
                    self.speak(response)
                    socketio.emit('response', {'text': response, 'emotion': emotion})
            except sr.WaitTimeoutError:
                pass
            except Exception as e:
                logging.error(f"Voice error: {e}")
