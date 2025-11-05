import psutil
import subprocess
import time
import threading
from plyer import notification

class FocusMode:
    def __init__(self):
        self.active = False
        self.blocked_apps = ['discord.exe', 'slack.exe', 'chrome.exe']  # Customize
        self.start_time = None

    def start(self, minutes=25):
        if self.active:
            return "Focus mode already active"
        
        self.active = True
        self.start_time = time.time()
        notification.notify(title="🧠 Focus Mode", message=f"Started for {minutes} minutes")
        
        # Dim screen (platform-specific)
        if subprocess.call(['nircmd.exe', 'settransparency', '50'], shell=True) != 0:  # Windows fallback
            pass  # Add macOS/Linux equivalents
        
        # Block distracting apps
        self._block_distractions()
        
        # Play focus music (placeholder)
        subprocess.Popen(['open', 'spotify:playlist:lofi'], shell=True)
        
        # Timer
        def timer():
            time.sleep(minutes * 60)
            self.end()
        
        threading.Thread(target=timer, daemon=True).start()
        return f"Focus mode activated for {minutes} minutes"

    def _block_distractions(self):
        for proc in psutil.process_iter(['pid', 'name']):
            if any(app in proc.info['name'].lower() for app in self.blocked_apps):
                try:
                    proc.terminate()
                except:
                    pass

    def end(self):
        self.active = False
        notification.notify(title="🧠 Focus Complete", message="Great job! Take a break.")