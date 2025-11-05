# plugins/clipboard_plugin.py
import pyperclip

class Plugin:
    def get_tools(self):
        return [{
            "type": "function",
            "function": {
                "name": "smart_clipboard",
                "description": "AI-summarize, format, or translate clipboard content",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {"type": "string", "enum": ["summarize", "format", "translate"], "default": "summarize"}
                    },
                    "required": []
                }
            }
        }]

    def execute(self, function_name, **args):
        if function_name == "smart_clipboard":
            text = pyperclip.paste()
            if not text.strip():
                return "Clipboard is empty."
            action = args.get("action", "summarize")
            prompt = {
                "summarize": f"Summarize this in 1 sentence: {text[:1000]}",
                "format": f"Format this text professionally: {text[:1000]}",
                "translate": f"Translate this to Spanish: {text[:1000]}"
            }.get(action, f"Summarize: {text[:1000]}")
            return f"Clipboard AI → {action.capitalize()}: Send this to Grok → `{prompt}`"
        return "Invalid action"