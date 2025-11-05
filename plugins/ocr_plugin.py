# plugins/ocr_plugin.py
from core.ocr_engine import ocr_text

class Plugin:
    def get_tools(self):
        return [{
            "type": "function",
            "function": {
                "name": "read_screen",
                "description": "Read and explain any text visible on the user's screen",
                "parameters": {"type": "object", "properties": {}, "required": []}
            }
        }]

    def execute(self, function_name, **args):
        if function_name == "read_screen":
            text = ocr_text()
            if not text.strip():
                return "No text detected on screen."
            return f"Screen text captured: {text[:500]}{'...' if len(text) > 500 else ''}"
        return "Unknown action"