from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods

# tasks/task_tree_node.py


class TaskTreeNode:
    def __init__(self, task_id, task_description, parent=None):
        self.task_id = task_id
        self.task_description = task_description
        self.parent = parent
        self.children = []
        self.agent_assigned = None
        self.status = "pending"
        self.retry_count = 0
        self.result = None

    def add_child(self, child_node):
        self.children.append(child_node)

    def is_leaf(self):
        return not self.children

    def to_dict(self):
        return {
            "task_id": self.task_id,
            "description": self.task_description,
            "status": self.status,
            "agent": self.agent_assigned,
            "retry_count": self.retry_count,
            "result": self.result,
            "children": [child.to_dict() for child in self.children],
        }
