from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
import os
import datetime


def get_modules_with_metadata(folder_path="planner"):
    modules = []
    for filename in os.listdir(folder_path):
        filepath = os.path.join(folder_path, filename)
        if os.path.isfile(filepath):
            size_kb = os.path.getsize(filepath) // 1024
            mod_time = datetime.datetime.fromtimestamp(os.path.getmtime(filepath))
            mod_str = mod_time.strftime("%d %b %Y, %I:%M %p")
            modules.append(
                {"name": filename, "label": f"{filename} ({size_kb} KB, {mod_str})"}
            )
    return modules
