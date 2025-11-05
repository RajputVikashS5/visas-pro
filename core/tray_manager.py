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
        self.load(QUrl.fromLocalFile(os.path.abspath('static/avatar.html')))
        self.setFixedSize(200, 200)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

def start_tray(socketio):
    app = QApplication(sys.argv)
    
    # Avatar window
    avatar = AvatarWidget()
    avatar.show()
    
    # Tray icon
    tray = QSystemTrayIcon()
    tray.setIcon(QIcon('static/icon.png'))  # Add your icon
    tray.setToolTip('Visas Pro - AI Assistant')

    menu = QMenu()
    
    open_dashboard = QAction("🖥️ Open Dashboard")
    open_dashboard.triggered.connect(lambda: webbrowser.open('http://localhost:5000'))
    
    toggle_voice = QAction("🎤 Toggle Voice Mode")
    toggle_voice.triggered.connect(lambda: requests.post('http://localhost:5000/tray', json={'action': 'toggle_voice'}))
    
    start_focus = QAction("🧠 Start Focus Mode (25min)")
    start_focus.triggered.connect(lambda: requests.post('http://localhost:5000/focus', json={'minutes': 25}))
    
    whisper_mode = QAction("🤫 Toggle Whisper Mode")
    whisper_mode.triggered.connect(lambda: requests.post('http://localhost:5000/ask', json={'query': 'toggle whisper'}))
    
    privacy_shield = QAction("🛡️ Toggle Privacy Shield")
    privacy_shield.triggered.connect(lambda: requests.post('http://localhost:5000/privacy'))
    
    view_history = QAction("📜 View Conversation History")
    view_history.triggered.connect(lambda: QMessageBox.information(None, "History", "Last 5: Coming soon!"))
    
    exit_action = QAction("❌ Exit")
    exit_action.triggered.connect(app.quit)

    menu.addAction(open_dashboard)
    menu.addAction(toggle_voice)
    menu.addAction(start_focus)
    menu.addAction(whisper_mode)
    menu.addAction(privacy_shield)
    menu.addAction(view_history)
    menu.addSeparator()
    menu.addAction(exit_action)

    tray.setContextMenu(menu)
    tray.show()
    
    sys.exit(app.exec_())