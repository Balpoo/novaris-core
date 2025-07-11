from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods

# dashboard/widgets/plugin_loader.py

import importlib.util
import os


class PluginLoader:
    def __init__(self, plugin_folder="plugins"):
        self.plugin_folder = plugin_folder
        self.plugins = {}

    def load_plugins(self):
        for file in os.listdir(self.plugin_folder):
            if file.endswith(".py"):
                path = os.path.join(self.plugin_folder, file)
                spec = importlib.util.spec_from_file_location(file[:-3], path)
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                if hasattr(mod, "PluginAgent"):
                    self.plugins[file[:-3]] = mod.PluginAgent()
