import importlib
import os

def load_plugins():
    plugins = {}
    plugin_dir = os.path.dirname(__file__)

    for filename in os.listdir(plugin_dir):
        if filename.endswith("_plugin.py"):
            module_name = f"plugins.{filename[:-3]}"
            module = importlib.import_module(module_name)

            # ✅ Instantiate Plugin() if class exists
            if hasattr(module, "Plugin"):
                plugins[module_name] = module.Plugin()
            else:
                plugins[module_name] = module

    return plugins
