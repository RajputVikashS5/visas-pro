# plugins/habit_plugin.py
from core.memory_manager import MemoryManager
import re
from datetime import datetime, timedelta

class Plugin:
    def __init__(self):
        self.memory = MemoryManager()

    def get_tools(self):
        return []

    def check_habits(self):
        history = self.memory.get_history('voice', limit=50)
        recent = " ".join([msg['content'].lower() for msg in history[-20:]])
        
        patterns = {
            "lunch": ["lunch", "eat", "food", "hungry"],
            "break": ["break", "rest", "tired"],
            "water": ["water", "drink", "thirsty"]
        }
        
        missing = []
        for habit, keywords in patterns.items():
            if not any(k in recent for k in keywords):
                missing.append(habit)
        
        if missing:
            return f"You haven't mentioned {', '.join(missing)} recently. Need a reminder?"
        return None