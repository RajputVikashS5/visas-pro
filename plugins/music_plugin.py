# plugins/music_plugin.py
import subprocess
import platform

class Plugin:
    def get_tools(self):
        return [{
            "type": "function",
            "function": {
                "name": "play_music",
                "description": "Play music by genre or mood",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "genre": {"type": "string", "enum": ["lofi", "focus", "chill", "motivation"]}
                    },
                    "required": ["genre"]
                }
            }
        }]

    def execute(self, function_name, **args):
        if function_name == "play_music":
            playlists = {
                "lofi": "https://www.youtube.com/watch?v=jfKfPfyJRdk",
                "focus": "spotify:playlist:37i9dQZF1DX8NTLI2TtZa6",
                "chill": "https://www.youtube.com/watch?v=5qap5aO4i9A",
                "motivation": "https://www.youtube.com/watch?v=1-xGerv5a_4"
            }
            url = playlists.get(args['genre'], playlists['lofi'])
            if platform.system() == "Darwin":
                subprocess.run(["open", url])
            elif platform.system() == "Windows":
                subprocess.run(["start", url], shell=True)
            else:
                subprocess.run(["xdg-open", url])
            return f"Playing {args['genre']} music..."
        return "Invalid genre"