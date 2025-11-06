from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView
import sys
import requests
import os
import webbrowser


class AvatarWidget(QWebEngineView):
    def __init__(self):
        super().__init__()
        avatar_path = os.path.abspath('static/avatar.html')
        self.load(QUrl.fromLocalFile(avatar_path))
        self.setFixedSize(200, 200)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.show()  # Show immediately


def start_tray(socketio):
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)  # Keep tray alive when window closed

    # Avatar window
    avatar = AvatarWidget()

    # Tray icon
    tray = QSystemTrayIcon()
    icon_path = os.path.abspath("static/icon.png")
    tray.setIcon(QIcon(icon_path))
    tray.setToolTip('Visas Pro - AI Assistant')

    # Menu setup
    menu = QMenu()

    # Dashboard
    open_dashboard = QAction("🖥️ Open Dashboard")
    open_dashboard.triggered.connect(lambda: webbrowser.open('http://localhost:5000'))

    # Voice mode toggle
    toggle_voice = QAction("🎤 Toggle Voice Mode")
    toggle_voice.triggered.connect(
        lambda: requests.post('http://localhost:5000/tray', json={'action': 'toggle_voice'})
    )

    # Focus mode
    start_focus = QAction("🧠 Start Focus Mode (25min)")
    start_focus.triggered.connect(
        lambda: requests.post('http://localhost:5000/focus', json={'minutes': 25})
    )

    # Whisper mode
    whisper_mode = QAction("🤫 Toggle Whisper Mode")
    whisper_mode.triggered.connect(
        lambda: requests.post('http://localhost:5000/ask', json={'query': 'toggle whisper'})
    )

    # Privacy shield
    privacy_shield = QAction("🛡️ Toggle Privacy Shield")
    privacy_shield.triggered.connect(
        lambda: requests.post('http://localhost:5000/privacy')
    )