from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods

# utils/pretty_tree.py


def print_task_tree(tree_dict, indent="", is_last=True):
    """
    Recursively prints a tree structure from a task dict
    """
    branch = "└── " if is_last else "├── "
    prefix = indent + branch

    title = tree_dict.get("task_description", "Unnamed Task")
    agent = tree_dict.get("agent_assigned", "Unassigned")
    status = tree_dict.get("status", "unknown")
    result = tree_dict.get("result", "")

    print(
        f"{prefix}{title}  [{agent}]  ✅"
        if status == "success"
        else f"{prefix}{title}  [{agent}]  ❌"
    )

    if result:
        lines = result.splitlines()
        for line in lines[:2]:  # Only show first 2 lines of result for brevity
            print(indent + ("    " if is_last else "│   ") + f"↪ {line.strip()}")

        if len(lines) > 2:
            print(
                indent + ("    " if is_last else "│   ") + f"↪ ... ({len(lines)} lines)"
            )

    children = tree_dict.get("children", [])
    for i, child in enumerate(children):
        is_child_last = i == len(children) - 1
        print_task_tree(child, indent + ("    " if is_last else "│   "), is_child_last)
