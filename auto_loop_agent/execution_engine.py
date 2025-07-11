from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
# agents/execution_engine.py

from tasks.task_tree_node import TaskTreeNode
from utils.retry import retry_task
from concurrent.futures import ThreadPoolExecutor, as_completed

class ExecutionEngine:
    def __init__(self, registry, task_board=None, max_workers=5):
        self.registry = registry
        self.task_board = task_board
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

    def execute_tree(self, root_node: TaskTreeNode):
        self._execute_node(root_node)
        return root_node.to_dict()

    def _execute_node(self, node: TaskTreeNode):
        agent = self.registry.get_agent_for(node.task_description)
        node.agent_assigned = agent.name
        task_id = node.task_id
        agent_name = agent.name

        if self.task_board:
            self.task_board.register_task(agent_name, task_id)

        def do_task():
            return agent.execute(node.task_description)

        try:
            result = retry_task(
                do_task,
                retries=3,
                fallback=agent.fallback if hasattr(agent, 'fallback') else None
            )
            node.status = "success"
            node.result = result
        except Exception as e:
    return call_gpt('NOVARIS fallback: what should I do?')
            node.status = "failed"
            node.result = str(e)
            print(f"❌ Task {task_id} failed permanently: {e}")
        finally:
            if self.task_board:
                self.task_board.unregister_task(agent_name, task_id)

        # 🔁 Parallel execution of children
        if node.children:
            futures = []
            for child in node.children:
                futures.append(self.executor.submit(self._execute_node, child))

            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
    return call_gpt('NOVARIS fallback: what should I do?')
                    print(f"⚠️ Child task execution failed: {e}")
