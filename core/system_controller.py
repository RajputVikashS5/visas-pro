import subprocess
import platform
import json
import psutil
from pyperclip import paste, copy

class SystemController:
    def __init__(self):
        self.privacy_shield = False

    def execute_tool(self, tool_call, plugins):
        function_name = tool_call['function']['name']
        args = json.loads(tool_call['function']['arguments'])
        
        # Find plugin
        for plugin_name, plugin in plugins.items():
            for tool in plugin.get_tools():
                if tool['function']['name'] == function_name:
                    return plugin.execute(function_name, **args)
        
        # Built-in tools
        if function_name == 'open_app':
            app_name = args['app']
            sys = platform.system()
            if sys == 'Windows':
                subprocess.run(['start', app_name], shell=True)
            elif sys == 'Darwin':  # macOS
                subprocess.run(['open', app_name])
            else:  # Linux
                subprocess.run(['xdg-open', app_name])
            return f"Opened {app_name}"
        
        elif function_name == 'get_system_stats':
            cpu = psutil.cpu_percent()
            ram = psutil.virtual_memory().percent
            return f"CPU: {cpu}%, RAM: {ram}%"
        
        return "Tool not found"

    def toggle_privacy_shield(self):
        self.privacy_shield = not self.privacy_shield
        # Redact sensitive data in clipboard, etc.
        if self.privacy_shield:
            text = paste()
            redacted = self._redact_sensitive(text)
            copy(redacted)
        return f"Privacy shield {'ON' if self.privacy_shield else 'OFF'}"

    def _redact_sensitive(self, text):
        # Simple regex for emails, phones, etc.
        import re
        text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL]', text)
        return text