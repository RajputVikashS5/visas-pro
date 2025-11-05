# plugins/code_plugin.py
class Plugin:
    def get_tools(self):
        return [{
            "type": "function",
            "function": {
                "name": "write_code",
                "description": "Generate, explain, or debug code in any language",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "language": {"type": "string"},
                        "task": {"type": "string"},
                        "code": {"type": "string", "description": "Optional existing code"}
                    },
                    "required": ["task"]
                }
            }
        }]

    def execute(self, function_name, **args):
        if function_name == "write_code":
            lang = args.get("language", "Python")
            task = args["task"]
            code = args.get("code", "")
            prompt = f"Write {lang} code for: {task}"
            if code:
                prompt += f"\nExisting code:\n``` {code} ```\nImprove or debug it."
            return f"Code AI → Send to Grok: `{prompt}`"
        return "Invalid code request"