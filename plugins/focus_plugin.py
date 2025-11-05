# plugins/focus_plugin.py
from core.focus_mode import FocusMode

focus_mode = FocusMode()

class Plugin:
    def get_tools(self):
        return [{
            "type": "function",
            "function": {
                "name": "start_focus_mode",
                "description": "Start distraction-free focus mode for N minutes",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "minutes": {"type": "integer", "description": "Duration in minutes", "default": 25}
                    },
                    "required": []
                }
            }
        }]

    def execute(self, function_name, **args):
        if function_name == "start_focus_mode":
            mins = args.get("minutes", 25)
            result = focus_mode.start(mins)
            return result
        return "Focus mode failed"