import requests
import json
import os

class OpenRouterClient:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        self.base_url = 'https://openrouter.ai/api/v1/chat/completions'

    def query(self, query, history=None, tools=None):
        """
        Sends a chat completion request to OpenRouter.
        Compatible with your existing GrokClient code.
        """
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'HTTP-Referer': 'https://yourapp.example.com',  # optional but recommended
            'X-Title': 'Visas AI Assistant',
            'Content-Type': 'application/json'
        }

        # Ensure history is a list
        if not history:
            history = []

        messages = history + [{'role': 'user', 'content': query}]
        payload = {
            'model': 'deepseek/deepseek-r1:free',  # ✅ You can change to any OpenRouter model
            'messages': messages,
            'temperature': 0.7,
            'max_tokens': 1000
        }

        if tools:
            payload['tools'] = tools

        try:
            response = requests.post(self.base_url, json=payload, headers=headers, timeout=30)
            response.raise_for_status()  # Catch HTTP errors
            data = response.json()

            # Handle malformed responses
            if "choices" not in data or not data["choices"]:
                return "[Error] No valid response from OpenRouter.", []

            message = data["choices"][0]["message"]
            content = message.get("content", "")
            tool_calls = message.get("tool_calls", [])

            return content, tool_calls

        except requests.exceptions.RequestException as e:
            return f"[Network Error] {str(e)}", []
        except (KeyError, json.JSONDecodeError) as e:
            return f"[Parse Error] {str(e)}", []
