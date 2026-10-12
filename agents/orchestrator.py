# -*- coding: utf-8 -*-
"""Orchestrator：操作系统与 AI 操作系统多智能体流水线编排器。"""
from __future__ import annotations

import logging
import uuid
from typing import Any, Dict, List

from . import kernel_engineer, system_builder, ai_os, freedom

logger = logging.getLogger(__name__)

AGENT_REGISTRY = {
    "kernel_engineer": (kernel_engineer.KernelEngineerAgent, "内核工程师（架构/调度/内存/文件系统/驱动）"),
    "system_builder": (system_builder.SystemBuilderAgent, "系统构建与裁剪"),
    "ai_os": (ai_os.AIOSAgent, "AI 操作系统（系统级智能体/AI 交互/智能调度）"),
    "freedom": (freedom.FreedomAgent, "反捆绑与用户自主选择"),
}


class Orchestrator:
    def __init__(self, llm_gateway=None, data_dir=None):
        self.llm_gateway = llm_gateway
        self.data_dir = data_dir
        self._tasks: Dict[str, Dict[str, Any]] = {}

    def plan(self, goal: str) -> List[Dict[str, Any]]:
        g = goal.lower()
        plan: List[Dict[str, Any]] = []
        if any(k in g for k in ["内核", "驱动", "文件系统", "调度", "内存", "kernel", "driver", "fs", "sched"]):
            plan.append({"agent": "kernel_engineer", "action": "arch", "params": {}})
        if any(k in g for k in ["构建", "裁剪", "镜像", "最小系统", "build", "trim"]):
            plan.append({"agent": "system_builder", "action": "profile", "params": {}})
        if any(k in g for k in ["ai", "智能", "系统级智能体", "aios", "agent framework"]):
            plan.append({"agent": "ai_os", "action": "agent_framework", "params": {}})
        if any(k in g for k in ["反捆绑", "预装", "商店", "自主选择", "去中心", "捆绑", "store", "preinstall"]):
            plan.append({"agent": "freedom", "action": "store", "params": {}})
        if not plan:
            plan = [{"agent": "kernel_engineer", "action": "arch", "params": {}},
                    {"agent": "system_builder", "action": "profile", "params": {}},
                    {"agent": "ai_os", "action": "agent_framework", "params": {}},
                    {"agent": "freedom", "action": "store", "params": {}}]
        return plan

    def execute(self, goal: str, plan: List[Dict[str, Any]], params: Dict[str, Any]) -> Dict[str, Any]:
        results = []
        for step in plan:
            agent_name = step["agent"]
            agent_cls, _ = AGENT_REGISTRY[agent_name]
            agent = agent_cls(config={}, data_dir=self.data_dir)
            task = dict(step.get("params", {}))
            task.update(params)
            task["action"] = step.get("action", "default")
            try:
                res = agent.run(task)
                results.append({"agent": agent_name, "ok": True, "result": res})
            except Exception as exc:  # noqa: BLE001
                logger.exception("Agent %s 失败", agent_name)
                results.append({"agent": agent_name, "ok": False, "error": str(exc)})
        task_id = f"task_{uuid.uuid4().hex[:8]}"
        report = {"task_id": task_id, "goal": goal, "plan": plan, "results": results,
                  "status": "done", "created_at": __import__("time").time()}
        self._tasks[task_id] = report
        return report

    def run(self, goal: str, params: Dict[str, Any] | None = None) -> Dict[str, Any]:
        params = params or {}
        plan = self.plan(goal)
        return self.execute(goal, plan, params)

    def get_task(self, task_id: str) -> Dict[str, Any] | None:
        return self._tasks.get(task_id)

    def list_agents(self) -> List[Dict[str, Any]]:
        return [{"name": name, "description": desc, "action_hint": self._hint(name)}
                for name, (cls, desc) in AGENT_REGISTRY.items()]

    def _hint(self, name: str) -> str:
        hints = {"kernel_engineer": "arch / scheduler / memory / fs / driver",
                 "system_builder": "profile / kernelconfig",
                 "ai_os": "agent_framework / interaction / scheduler",
                 "freedom": "store / preinstall / combo"}
        return hints.get(name, "")
