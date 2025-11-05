import sqlite3
from cryptography.fernet import Fernet
import os
import json
from datetime import datetime

class MemoryManager:
    def __init__(self):
        self.db_path = 'visas_memory.db'
        self.key_file = 'memory.key'
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self._init_db()
        self.cipher = self._get_cipher()

    def _init_db(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS history 
                               (session_id TEXT, timestamp TEXT, query BLOB, response BLOB)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS reminders 
                               (id INTEGER PRIMARY KEY, reminder TEXT, due TEXT, completed INTEGER)''')
        self.conn.commit()

    def _get_cipher(self):
        if not os.path.exists(self.key_file):
            key = Fernet.generate_key()
            with open(self.key_file, 'wb') as f:
                f.write(key)
        else:
            with open(self.key_file, 'rb') as f:
                key = f.read()
        return Fernet(key)

    def add_to_history(self, session_id, query, response):
        timestamp = datetime.now().isoformat()
        enc_query = self.cipher.encrypt(query.encode())
        enc_response = self.cipher.encrypt(response.encode())
        self.cursor.execute('INSERT INTO history VALUES (?, ?, ?, ?)', 
                           (session_id, timestamp, enc_query, enc_response))
        self.conn.commit()

    def get_history(self, session_id, limit=10):
        self.cursor.execute('SELECT timestamp, query, response FROM history WHERE session_id = ? ORDER BY timestamp DESC LIMIT ?', 
                           (session_id, limit))
        rows = self.cursor.fetchall()
        messages = []
        for ts, q, r in reversed(rows):  # Chronological order
            messages.append({'role': 'user', 'content': self.cipher.decrypt(q).decode()})
            messages.append({'role': 'assistant', 'content': self.cipher.decrypt(r).decode()})
        return messages

    def add_reminder(self, reminder, due):
        enc_reminder = self.cipher.encrypt(reminder.encode())
        self.cursor.execute('INSERT INTO reminders (reminder, due, completed) VALUES (?, ?, 0)', 
                           (enc_reminder, due))
        self.conn.commit()

    def get_reminders(self):
        self.cursor.execute('SELECT reminder, due FROM reminders WHERE completed = 0')
        return [(self.cipher.decrypt(r).decode(), d) for r, d in self.cursor.fetchall()]