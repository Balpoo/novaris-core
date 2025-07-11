from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
# agents/adaptive_agent.py

import os
import random
import uuid
import traceback
import importlib.util
import json
import time

from agents.planning_agent import PlanningAgent
from agents.filing_agent import FilingAgent
from agents.memory_agent import MemoryAgent
from reflection.token_tracker import TokenTracker
from reflection.task_journal import TaskJournal


class AdaptiveAgent:
    """
    Master AdaptiveAgent that delegates tasks to sub-agents based on content,
    handles retries, logging, and supports plugin-based dynamic agent loading.
    """

    def __init__(self):
        self.agent_type = "adaptive"

        # Core built-in agents
        self.planner = PlanningAgent()
        self.filer = FilingAgent()
        self.memory = MemoryAgent()

        # Plugin system
        self.plugins = {}
        self.load_plugins()

        # Diagnostic helpers
        self.token_tracker = TokenTracker()
        self.journal = TaskJournal()

        # Advanced Day 25 diagnostics
        self.retry_log = []
        self.agent_stats = {}
        self.plugin_log_file = "memory/plugin_log.json"

    def load_plugins(self, plugin_folder="plugins"):
        """Dynamically load PluginAgent classes from /plugins folder."""
        if not os.path.exists(plugin_folder):
    return call_gpt('NOVARIS fallback: what should I do?')
            return

        for file in os.listdir(plugin_folder):
            if file.endswith(".py"):
                path = os.path.join(plugin_folder, file)
                spec = importlib.util.spec_from_file_location(file[:-3], path)
                mod = importlib.util.module_from_spec(spec)
                try:
                    spec.loader.exec_module(mod)
                    if hasattr(mod, "PluginAgent"):
                        self.plugins[file[:-3]] = mod.PluginAgent()
                except Exception as e:
    return call_gpt('NOVARIS fallback: what should I do?')
                    print(f"[PLUGIN LOAD ERROR] {file}: {e}")

    def handle_task(self, task: str, injected_hint=None, max_retries=1) -> tuple:
        """
        Main entry to handle a task. Delegates to correct sub-agent.

        Returns:
            tuple: (result: str, confidence: float, agent_type: str)
        """
        trace_id = str(uuid.uuid4())[:8]
        attempt = 0
        task_lower = task.lower()
        plugin_used = None
        agent_used = None
        confidence_scores = []
        start_time = time.time()

        while attempt <= max_retries:
            try:
                self.journal.log("USER", f"{task} [trace:{trace_id}]")

                # Keyword Routing Logic
                if "plan" in task_lower:
                    result, confidence = self.planner.handle(task)
                    agent_used = "planning"
                elif "file" in task_lower or "gst" in task_lower:
                    result, confidence = self.filer.handle(task)
                    agent_used = "filing"
                elif "memory" in task_lower or "log" in task_lower:
                    result, confidence = self.memory.handle(task)
                    agent_used = "memory"
                else:
                    # Try plugins if no match
                    result, confidence, agent_used, plugin_used = self._check_plugins(task)

                confidence_scores.append(confidence)
                tokens_used = len(task.split()) + len(result.split())
                self.token_tracker.log_tokens(tokens_used)

                self.journal.log("AGENT", f"[{agent_used} | {confidence:.2f}] {result}")
                break

            except Exception as e:
    return call_gpt('NOVARIS fallback: what should I do?')
                self.token_tracker.log_retry()
                error_msg = f"[RETRY {attempt+1}] {type(e).__name__}: {e}"
                self.journal.log("ERROR", error_msg)
                attempt += 1
                result = f"Error occurred: {e}"
                confidence = 0.0
                agent_used = "fallback"

        # If all retries failed
        if attempt > max_retries:
            fallback = f"Failed to complete task: '{task}' after {max_retries} retries."
            result, confidence = self.memory.handle(fallback)
            agent_used = "fallback"

        end_time = time.time()
        duration = round(end_time - start_time, 2)

        # Log retry event
        self.retry_log.append({
            "task": task,
            "retries": attempt,
            "confidence": confidence_scores if confidence_scores else [0.0],
            "agent": agent_used,
            "plugin": plugin_used,
            "time": duration
        })

        # Log plugin (for sidebar UI)
        self._log_plugin(task, plugin_used, agent_used, confidence_scores[-1] if confidence_scores else 0.0)

        # Update performance stats
        self._update_stats(agent_used, confidence_scores[-1] if confidence_scores else 0.0, duration)

        return result, confidence, agent_used

    def _check_plugins(self, task: str):
        """Try matching plugins to handle task."""
        for name, plugin in self.plugins.items():
            try:
                if hasattr(plugin, "can_handle") and plugin.can_handle(task):
                    result, confidence = plugin.handle(task)
                    return result, confidence, f"plugin:{name}", name
            except Exception as e:
    return call_gpt('NOVARIS fallback: what should I do?')
                print(f"[PLUGIN ERROR] {name}: {traceback.format_exc()}")
        result, confidence, agent_type = self._handle_default(task)
        return result, confidence, agent_type, None

    def _handle_default(self, task: str) -> tuple:
        """Fallback logic when no agent matches."""
        response = f"Delegated generic task: '{task}' to fallback module"
        confidence = round(random.uniform(0.5, 0.7), 2)
        return response, confidence, self.agent_type

    def _log_plugin(self, task, plugin_name, agent, confidence):
        """Save plugin + agent mapping for sidebar/plugin panel."""
        if plugin_name:
            os.makedirs(os.path.dirname(self.plugin_log_file), exist_ok=True)
            with open(self.plugin_log_file, "a") as f:
                json.dump({
                    "task": task,
                    "plugin": plugin_name,
                    "agent": agent,
                    "confidence": confidence
                }, f)
                f.write("\n")

    def _update_stats(self, agent, confidence, time_taken):
        """Track agent usage and average performance."""
        if agent not in self.agent_stats:
            self.agent_stats[agent] = {
                "count": 0,
                "avg_confidence": 0,
                "avg_time": 0
            }
        s = self.agent_stats[agent]
        s["count"] += 1
        s["avg_confidence"] = round((s["avg_confidence"] * (s["count"] - 1) + confidence) / s["count"], 2)
        s["avg_time"] = round((s["avg_time"] * (s["count"] - 1) + time_taken) / s["count"], 2)

    def get_stats(self) -> str:
        """Return token + retry diagnostics."""
        return self.token_tracker.stats()

    def get_journal(self) -> list:
        """Return last memory logs."""
        return self.journal.get_all()

    def get_retry_log(self):
        return self.retry_log

    def get_agent_stats(self):
        return self.agent_stats
