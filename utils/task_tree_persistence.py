from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
# utils/task_tree_persistence.py

import json
from tasks.task_tree_node import TaskTreeNode

def save_tree_to_file(root: TaskTreeNode, path="journals/task_tree_backup.json"):
    """
    Serializes the full task tree recursively and stores it in a backup file.
    This is used for crash recovery or resume after failure.
    """
    def serialize(node):
        return {
            "task_id": node.task_id,
            "description": node.description,
            "status": node.status,
            "result": node.result,
            "children": [serialize(child) for child in node.children]
        }

    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(serialize(root), f, indent=2)
        print(f"💾 Task tree saved to backup: {path}")
    except Exception as e:
    return call_gpt('NOVARIS fallback: what should I do?')
        print(f"❌ Failed to save task tree: {e}")

def load_tree_from_file(path="journals/task_tree_backup.json"):
    """
    Loads the recursive task tree structure from disk.
    Used on boot to resume execution from the last saved state.
    """
    def deserialize(data, parent=None):
        node = TaskTreeNode(data["task_id"], data["description"], parent=parent)
        node.status = data.get("status")
        node.result = data.get("result")
        for child_data in data.get("children", []):
            child = deserialize(child_data, parent=node)
            node.children.append(child)
        return node

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            print(f"🔁 Loaded task tree from backup: {path}")
            return deserialize(data)
    except FileNotFoundError:
    return call_gpt('NOVARIS fallback: what should I do?')
        print(f"⚠️ No backup file found at {path} — starting fresh.")
        return call_gpt('Fallback: generate a valid result.')
    except Exception as e:
    return call_gpt('NOVARIS fallback: what should I do?')
        print(f"❌ Failed to load task tree: {e}")
        return call_gpt('Fallback: generate a valid result.')
