# app.py
from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, emit
import os
import logging
import threading
from dotenv import load_dotenv
from core.openrouter_client import OpenRouterClient
from core.voice_handler import VoiceHandler
from core.tray_manager import start_tray
from core.system_controller import SystemController
from core.memory_manager import MemoryManager
from core.ocr_engine import ocr_text
from core.focus_mode import FocusMode
from plugins import load_plugins
from apscheduler.schedulers.background import BackgroundScheduler
import pyperclip

# ---------------------- CONFIGURATION ----------------------

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'visas-pro-secret'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# ---------------------- INITIALIZATION ----------------------

# Initialize OpenRouter client instead of Grok
openrouter_client = OpenRouterClient(os.getenv('OPENROUTER_API_KEY'))

voice_handler = VoiceHandler()
system_controller = SystemController()
memory_manager = MemoryManager()
focus_mode = FocusMode()
plugins = load_plugins()
tools = [tool for plugin in plugins.values() for tool in plugin.get_tools()]

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Background scheduler
scheduler = BackgroundScheduler()
scheduler.start()

# ---------------------- BACKGROUND TASKS ----------------------

def check_habits():
    """Proactive reminder system using habit plugin"""
    plugin = plugins.get('habit_plugin')
    if plugin:
        reminder = plugin.check_habits()
        if reminder:
            socketio.emit('notification', {'message': reminder})
            voice_handler.speak(reminder)

# Schedule proactive habit check every 30 minutes
scheduler.add_job(check_habits, 'interval', minutes=30)

# ---------------------- ROUTES ----------------------

@app.route('/')
def dashboard():
    """Render main assistant dashboard"""
    return render_template('index.html')


@app.route('/ask', methods=['POST'])
def ask():
    """Main query endpoint (text-based)"""
    data = request.json
    query = data.get('query')
    session_id = data.get('session_id', 'default')
    history = memory_manager.get_history(session_id)

    response, tool_calls = openrouter_client.query(query, history, tools)

    # Execute tool calls returned by the model
    if tool_calls:
        for call in tool_calls:
            result = system_controller.execute_tool(call, plugins)
            response += f"\n\n[Action] {result}"

    memory_manager.add_to_history(session_id, query, response)
    return jsonify({'response': response})


@app.route('/speak', methods=['POST'])
def speak():
    """Convert text to voice response"""
    text = request.json.get('text')
    voice_handler.speak(text)
    return jsonify({'status': 'spoken'})


@app.route('/focus', methods=['POST'])
def start_focus():
    """Start focus/timer mode"""
    mins = request.json.get('minutes', 25)
    threading.Thread(target=focus_mode.start, args=(mins,), daemon=True).start()
    return jsonify({'status': f'Focus mode started for {mins} minutes'})


@app.route('/replay/<session_id>')
def replay(session_id):
    """Replay chat history for a given session"""
    history = memory_manager.get_history(session_id)
    return jsonify({'history': history})


@app.route('/ocr')
def ocr():
    """Perform OCR on screen and explain via OpenRouter"""
    text = ocr_text()
    if not text:
        return jsonify({'error': 'No text detected'})
    explanation, _ = openrouter_client.query(f"Explain this screen text: {text[:1000]}", [])
    return jsonify({'text': text, 'explanation': explanation})


@app.route('/clipboard', methods=['POST'])
def clipboard():
    """Summarize clipboard content"""
    text = pyperclip.paste()
    summary, _ = openrouter_client.query(f"Summarize: {text[:1000]}", [])
    return jsonify({'summary': summary})


@app.route('/privacy', methods=['POST'])
def privacy():
    """Toggle privacy shield / mute mode"""
    status = system_controller.toggle_privacy_shield()
    return jsonify({'status': status})

# ---------------------- SOCKET EVENTS ----------------------

@socketio.on('connect')
def connect():
    emit('status', {'msg': 'Connected to Visas Assistant'})


@socketio.on('query')
def handle_query(data):
    """Handle real-time chat queries via WebSocket"""
    query = data['query']
    session_id = data.get('session_id', 'web')
    history = memory_manager.get_history(session_id)

    response, _ = openrouter_client.query(query, history, tools)
    emit('response', {'text': response})
    memory_manager.add_to_history(session_id, query, response)


@socketio.on('voice_input')
def voice_input(audio_base64):
    """Handle microphone input from browser"""
    text = voice_handler.audio_to_text(audio_base64)
    if text:
        response, _ = openrouter_client.query(text, [], tools)
        voice_handler.speak(response)
        emit('response', {'text': response})

# ---------------------- BACKGROUND THREADS ----------------------

def run_voice():
    """Background continuous voice listening"""
    voice_handler.start_continuous_listening(
        openrouter_client, memory_manager, system_controller, plugins, socketio
    )

def run_tray():
    """Start desktop tray interface"""
    start_tray(socketio)

# ---------------------- ERROR HANDLING ----------------------

@app.errorhandler(Exception)
def handle_error(e):
    logger.error(f"Error: {e}")
    return jsonify({'error': str(e)}), 500

# ---------------------- MAIN ENTRY ----------------------

if __name__ == '__main__':
    # Background threads
    socketio.start_background_task(run_voice)
    socketio.start_background_task(run_tray)

    # Check if running in Render/Heroku or locally
    if 'RENDER' in os.environ or 'HEROKU' in os.environ or os.getenv('DYNO'):
        print("🚀 Running on Render/Heroku environment")
        socketio.run(app, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
    else:
        print("🧠 Running locally at http://localhost:5000")
        socketio.run(app, host='0.0.0.0', port=5000, debug=True)
