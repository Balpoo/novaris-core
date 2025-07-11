from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
import os
import json


def map_project_folders(base_path="."):
    folder_map = {}
    for root, dirs, files in os.walk(base_path):
        for d in dirs:
            full_path = os.path.join(root, d)
            rel_path = os.path.relpath(full_path, base_path)
            folder_map[rel_path] = {
                "full_path": full_path,
                "contains": os.listdir(full_path),
            }
    return folder_map


def save_folder_map(folder_map, output_file="core/folder_map.json"):
    with open(output_file, "w") as f:
        json.dump(folder_map, f, indent=2)


if __name__ == "__main__":
    project_map = map_project_folders()
    save_folder_map(project_map)
    print("📁 Folder map generated and saved.")
