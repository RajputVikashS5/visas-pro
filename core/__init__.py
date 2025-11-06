# core/__init__.py
"""
Core package initializer for Visas Pro AI Assistant.
Uses OpenRouter as the primary LLM backend.
"""

from .openrouter_client import OpenRouterClient
from .voice_handler import VoiceHandler
from .tray_manager import start_tray
from .system_controller import SystemController
from .memory_manager import MemoryManager
from .ocr_engine import ocr_text
from .focus_mode import FocusMode

__all__ = [
    'OpenRouterClient',
    'VoiceHandler',
    'start_tray',
    'SystemController',
    'MemoryManager',
    'ocr_text',
    'FocusMode'
]

# Singleton factory for OpenRouter client
_instances = {}

def get_openrouter_client(api_key: str = None) -> OpenRouterClient:
    """
    Returns a singleton instance of OpenRouterClient.
    Uses API key from environment if not provided.
    """
    import os
    key = api_key or os.getenv('OPENROUTER_API_KEY')
    if not key:
        raise ValueError("OPENROUTER_API_KEY not found in environment or argument")
    
    if key not in _instances:
        _instances[key] = OpenRouterClient(api_key=key)
    return _instances[key]