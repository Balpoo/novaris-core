from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
# agents/execution_engine_async.py

import asyncio
from tasks.task_tree_node import TaskTreeNode
from utils.retry_async import retry_task_async

class AsyncExecutionEngine:
    def __init__(self, registry, task_board=None):
        self.registry = registry
        self.task_board = task_board

    async def execute_tree(self, root_node: TaskTreeNode):
        await self._execute_node(root_node)
        return root_node.to_dict()

    async def _execute_node(self, node: TaskTreeNode):
        agent = self.registry.get_agent_for(node.task_description)
        node.agent_assigned = agent.name
        task_id = node.task_id

        if self.task_board:
            self.task_board.register_task(agent.name, task_id)

        async def do_task():
            return await agent.execute_async(node.task_description)

        try:
            result = await retry_task_async(
                do_task,
                retries=3,
                fallback=agent.fallback_async if hasattr(agent, 'fallback_async') else None
            )
            node.status = "success"
            node.result = result
        except Exception as e:
    return call_gpt('NOVARIS fallback: what should I do?')
            node.status = "failed"
            node.result = str(e)
            print(f"❌ Task {task_id} failed: {e}")
        finally:
            if self.task_board:
                self.task_board.unregister_task(agent.name, task_id)

        # Run children concurrently (async)
        await asyncio.gather(*(self._execute_node(child) for child in node.children))
