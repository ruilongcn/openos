#!/usr/bin/env python3
"""
SmartHomeOS OpenClaw - 多Agent协作系统
SubAgent, Agent Teams, AgentToAgent
"""

import os
import sys
import logging
import time
import random
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum, auto
from abc import ABC, abstractmethod

# 添加项目根目录到Python路径
current_file = os.path.abspath(__file__)
core_dir = os.path.dirname(current_file)
root_dir = os.path.dirname(core_dir)
sys.path.insert(0, root_dir)

from .core import OpenClawCore, AgentConfig, AgentContext, AgentState, AgentRole
from .skills import SkillRegistry

logger = logging.getLogger(__name__)


class CollaborationMode(Enum):
    """协作模式"""
    SUBAGENT = auto()       # 子Agent模式 - 父Agent委派任务
    TEAM = auto()           # 团队协作模式 - 平等协作
    AGENT_TO_AGENT = auto() # Agent间通信模式


class TaskStatus(Enum):
    """任务状态"""
    PENDING = auto()
    ASSIGNED = auto()
    IN_PROGRESS = auto()
    COMPLETED = auto()
    FAILED = auto()


@dataclass
class Task:
    """子任务"""
    task_id: str
    description: str
    requirements: List[str]
    priority: int = 3
    status: TaskStatus = TaskStatus.PENDING
    assigned_to: Optional[str] = None
    result: Optional[Any] = None
    created_at: float = field(default_factory=time.time)
    completed_at: Optional[float] = None


@dataclass
class AgentTeam:
    """Agent团队"""
    team_id: str
    name: str
    members: List[str] = field(default_factory=list)
    leader: Optional[str] = None
    shared_context: Dict[str, Any] = field(default_factory=dict)


class SubAgentCoordinator:
    """子Agent协调器 - 父Agent委派任务给子Agent"""

    def __init__(self, core: OpenClawCore):
        self.core = core
        self.parent_agents: Dict[str, List[str]] = {}  # parent -> [children]
        self.pending_tasks: Dict[str, List[Task]] = {}  # parent -> [tasks]

    def create_subagent(self, parent_id: str, config: AgentConfig) -> Optional[AgentContext]:
        """创建子Agent"""
        if parent_id not in self.core.agents:
            logger.error(f"Parent agent {parent_id} not found")
            return None

        config.agent_id = f"{parent_id}_sub_{len(self.parent_agents.get(parent_id, [])) + 1}"
        agent = self.core.create_agent(config)

        if agent:
            if parent_id not in self.parent_agents:
                self.parent_agents[parent_id] = []
            self.parent_agents[parent_id].append(config.agent_id)
            logger.info(f"Created subagent {config.agent_id} for parent {parent_id}")

        return agent

    def delegate_task(self, parent_id: str, task: Task,
                     child_id: Optional[str] = None) -> bool:
        """委派任务给子Agent"""
        if parent_id not in self.core.agents:
            logger.error(f"Parent agent {parent_id} not found")
            return False

        if parent_id not in self.parent_agents:
            logger.error(f"No subagents for parent {parent_id}")
            return False

        # 选择子Agent
        if not child_id:
            child_id = self._select_best_child(parent_id, task)

        if child_id not in self.parent_agents.get(parent_id, []):
            logger.error(f"Child {child_id} not a subagent of {parent_id}")
            return False

        # 委派任务
        task.assigned_to = child_id
        task.status = TaskStatus.ASSIGNED

        if parent_id not in self.pending_tasks:
            self.pending_tasks[parent_id] = []
        self.pending_tasks[parent_id].append(task)

        logger.info(f"Task {task.task_id} delegated to {child_id}")

        # 模拟执行
        self._execute_subagent_task(parent_id, child_id, task)
        return True

    def _select_best_child(self, parent_id: str, task: Task) -> str:
        """选择最佳子Agent"""
        children = self.parent_agents.get(parent_id, [])
        if not children:
            raise ValueError("No subagents available")

        # 简单策略：选择第一个可用的
        return children[0]

    def _execute_subagent_task(self, parent_id: str, child_id: str, task: Task):
        """执行子Agent任务"""
        child = self.core.get_agent(child_id)
        if not child or child.state != AgentState.RUNNING:
            logger.error(f"Child agent {child_id} not available")
            task.status = TaskStatus.FAILED
            return

        task.status = TaskStatus.IN_PROGRESS

        # 模拟任务执行
        try:
            time.sleep(0.5)
            task.result = f"Task completed by {child_id}: {task.description}"
            task.status = TaskStatus.COMPLETED
            task.completed_at = time.time()
            logger.info(f"Subagent {child_id} completed task {task.task_id}")
        except Exception as e:
            task.status = TaskStatus.FAILED
            logger.error(f"Subagent task failed: {e}")

    def get_agent_tasks(self, agent_id: str) -> List[Task]:
        """获取Agent的任务"""
        tasks = []
        for parent, parent_tasks in self.pending_tasks.items():
            if agent_id == parent:
                tasks.extend(parent_tasks)
            for task in parent_tasks:
                if task.assigned_to == agent_id:
                    tasks.append(task)
        return tasks


class AgentTeamCoordinator:
    """Agent团队协调器 - 团队协作模式"""

    def __init__(self, core: OpenClawCore):
        self.core = core
        self.teams: Dict[str, AgentTeam] = {}

    def create_team(self, team_id: str, name: str) -> AgentTeam:
        """创建团队"""
        team = AgentTeam(team_id=team_id, name=name)
        self.teams[team_id] = team
        logger.info(f"Created team: {team_id} - {name}")
        return team

    def add_member(self, team_id: str, agent_id: str) -> bool:
        """添加成员"""
        if team_id not in self.teams:
            logger.error(f"Team {team_id} not found")
            return False
        if agent_id not in self.core.agents:
            logger.error(f"Agent {agent_id} not found")
            return False

        if agent_id not in self.teams[team_id].members:
            self.teams[team_id].members.append(agent_id)
            logger.info(f"Added {agent_id} to team {team_id}")
        return True

    def set_leader(self, team_id: str, agent_id: str) -> bool:
        """设置团队领导"""
        if team_id not in self.teams:
            logger.error(f"Team {team_id} not found")
            return False
        if agent_id not in self.teams[team_id].members:
            logger.error(f"Agent {agent_id} not in team {team_id}")
            return False

        self.teams[team_id].leader = agent_id
        logger.info(f"Set {agent_id} as leader of team {team_id}")
        return True

    def broadcast_to_team(self, team_id: str, message: str) -> bool:
        """向团队广播消息"""
        if team_id not in self.teams:
            logger.error(f"Team {team_id} not found")
            return False

        team = self.teams[team_id]
        logger.info(f"Broadcasting to team {team_id}: {message}")

        for member in team.members:
            agent = self.core.get_agent(member)
            if agent and agent.state == AgentState.RUNNING:
                logger.info(f"   -> Delivered to {member}")

        return True

    def delegate_team_task(self, team_id: str, task: Task) -> bool:
        """团队任务委派"""
        if team_id not in self.teams:
            logger.error(f"Team {team_id} not found")
            return False

        team = self.teams[team_id]
        if not team.members:
            logger.error(f"Team {team_id} has no members")
            return False

        # 选择成员执行任务
        executor = self._select_team_executor(team, task)
        task.assigned_to = executor
        task.status = TaskStatus.ASSIGNED

        logger.info(f"Team {team_id} delegated task {task.task_id} to {executor}")

        # 执行
        self._execute_team_task(team_id, executor, task)
        return True

    def _select_team_executor(self, team: AgentTeam, task: Task) -> str:
        """选择任务执行者"""
        # 优先选择领导
        if team.leader and team.leader in team.members:
            return team.leader
        # 随机选择
        return random.choice(team.members)

    def _execute_team_task(self, team_id: str, executor_id: str, task: Task):
        """执行团队任务"""
        task.status = TaskStatus.IN_PROGRESS

        # 模拟团队协作
        try:
            time.sleep(0.3)
            task.result = f"Team {team_id} completed task {task.task_id} via {executor_id}"
            task.status = TaskStatus.COMPLETED
            task.completed_at = time.time()
        except Exception as e:
            task.status = TaskStatus.FAILED
            logger.error(f"Team task failed: {e}")

    def update_shared_context(self, team_id: str, key: str, value: Any):
        """更新团队共享上下文"""
        if team_id not in self.teams:
            logger.error(f"Team {team_id} not found")
            return

        self.teams[team_id].shared_context[key] = value
        logger.info(f"Updated shared context for team {team_id}: {key} = {value}")


class AgentToAgentProtocol:
    """AgentToAgent协议 - 跨Agent通信"""

    def __init__(self, core: OpenClawCore):
        self.core = core
        self.message_queue: List[Dict] = []
        self.subscribers: Dict[str, List[str]] = {}  # topic -> [agents]

    def send_message(self, from_agent: str, to_agent: str,
                    message: str, topic: str = "general") -> bool:
        """发送消息给另一个Agent"""
        if from_agent not in self.core.agents or to_agent not in self.core.agents:
            logger.error(f"Agent not found for message: {from_agent} -> {to_agent}")
            return False

        msg = {
            'from': from_agent,
            'to': to_agent,
            'message': message,
            'topic': topic,
            'timestamp': time.time()
        }

        self.message_queue.append(msg)
        logger.info(f"Message sent: {from_agent} -> {to_agent}: {message[:30]}...")
        return True

    def broadcast_message(self, from_agent: str, message: str,
                       topic: str = "general") -> int:
        """向所有订阅主题的Agent广播消息"""
        if from_agent not in self.core.agents:
            logger.error(f"From agent {from_agent} not found")
            return 0

        recipients = self.subscribers.get(topic, list(self.core.agents.keys()))
        if from_agent in recipients:
            recipients = [r for r in recipients if r != from_agent]

        count = 0
        for to_agent in recipients:
            if self.send_message(from_agent, to_agent, message, topic):
                count += 1

        logger.info(f"Broadcast to {count} agents on topic {topic}")
        return count

    def subscribe(self, agent_id: str, topic: str = "general") -> bool:
        """Agent订阅主题"""
        if agent_id not in self.core.agents:
            logger.error(f"Agent {agent_id} not found")
            return False

        if topic not in self.subscribers:
            self.subscribers[topic] = []
        if agent_id not in self.subscribers[topic]:
            self.subscribers[topic].append(agent_id)
        logger.info(f"Agent {agent_id} subscribed to {topic}")
        return True

    def get_messages(self, agent_id: str, since: float = 0) -> List[Dict]:
        """获取Agent的消息"""
        return [
            msg for msg in self.message_queue
            if msg['to'] == agent_id and msg['timestamp'] >= since
        ]


class MultiAgentOrchestrator:
    """多Agent编排器 - 统一管理所有协作模式"""

    def __init__(self, core: OpenClawCore):
        self.core = core
        self.subagent_coordinator = SubAgentCoordinator(core)
        self.team_coordinator = AgentTeamCoordinator(core)
        self.agent_to_agent = AgentToAgentProtocol(core)
        self.skill_registry = SkillRegistry()

        logger.info("MultiAgentOrchestrator initialized")

    def orchestrate_complex_task(self, task_description: str,
                                mode: CollaborationMode = CollaborationMode.TEAM) -> Dict:
        """编排复杂任务 - 核心功能"""
        logger.info(f"Orchestrating complex task: {task_description}, mode: {mode}")

        # 1. 任务分解
        subtasks = self._decompose_task(task_description)

        # 2. 根据模式选择执行策略
        if mode == CollaborationMode.SUBAGENT:
            result = self._orchestrate_subagent_mode(subtasks)
        elif mode == CollaborationMode.TEAM:
            result = self._orchestrate_team_mode(subtasks)
        elif mode == CollaborationMode.AGENT_TO_AGENT:
            result = self._orchestrate_a2a_mode(subtasks)
        else:
            result = {'status': 'error', 'message': f'Unknown mode: {mode}'}

        return {
            'status': 'success',
            'mode': mode.name,
            'task_description': task_description,
            'subtasks': [t.__dict__ for t in subtasks],
            'result': result,
            'completed_at': time.time()
        }

    def _decompose_task(self, task_description: str) -> List[Task]:
        """任务分解 - 将复杂任务分解为子任务"""
        task_types = [
            'research',
            'analysis',
            'planning',
            'execution',
            'summary'
        ]

        subtasks = []
        for i, task_type in enumerate(task_types):
            task = Task(
                task_id=f"sub_{i+1}",
                description=f"{task_type.capitalize()}: {task_description[:50]}",
                requirements=[task_type],
                priority=i + 1
            )
            subtasks.append(task)

        logger.info(f"Decomposed task into {len(subtasks)} subtasks")
        return subtasks

    def _orchestrate_subagent_mode(self, subtasks: List[Task]) -> Dict:
        """子Agent模式编排"""
        # 创建一个主Agent和多个子Agent
        main_agent = next(iter(self.core.agents.values()), None)
        if not main_agent:
            return {'status': 'error', 'message': 'No agents available'}

        results = []
        for i, task in enumerate(subtasks):
            # 为每个任务创建子Agent（或使用现有）
            results.append({
                'task_id': task.task_id,
                'result': f"Subagent executed {task.description}"
            })

        return {
            'mode': 'subagent',
            'results': results
        }

    def _orchestrate_team_mode(self, subtasks: List[Task]) -> Dict:
        """团队模式编排"""
        results = []

        # 使用现有Agent团队协作
        agents = list(self.core.agents.values())
        if not agents:
            return {'status': 'error', 'message': 'No agents available'}

        for i, task in enumerate(subtasks):
            executor = agents[i % len(agents)]
            results.append({
                'task_id': task.task_id,
                'executor': executor.config.agent_id,
                'result': f"Team collaboration completed {task.description}"
            })

        return {
            'mode': 'team',
            'results': results
        }

    def _orchestrate_a2a_mode(self, subtasks: List[Task]) -> Dict:
        """AgentToAgent模式编排"""
        results = []
        agents = list(self.core.agents.keys())

        if len(agents) < 2:
            return {'status': 'error', 'message': 'Need at least 2 agents for A2A'}

        # 模拟Agent间通信传递任务
        for i, task in enumerate(subtasks):
            from_agent = agents[i % len(agents)]
            to_agent = agents[(i + 1) % len(agents)]
            self.agent_to_agent.send_message(from_agent, to_agent, f"Please handle: {task.description}")
            results.append({
                'task_id': task.task_id,
                'message': f"Agent-to-Agent relay: {from_agent} -> {to_agent}"
            })

        return {
            'mode': 'agent_to_agent',
            'results': results
        }


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    print("=== OpenClaw MultiAgent Test ===")

    # 创建核心
    core = OpenClawCore()

    # 创建一些测试Agent
    config1 = AgentConfig(
        agent_id="agent_alice",
        name="Alice",
        role=AgentRole.GENERIC,
        system_prompt="You are Alice, a helpful assistant."
    )

    config2 = AgentConfig(
        agent_id="agent_bob",
        name="Bob",
        role=AgentRole.GENERIC,
        system_prompt="You are Bob, a supportive team member."
    )

    core.create_agent(config1)
    core.create_agent(config2)
    core.start_agent("agent_alice")
    core.start_agent("agent_bob")

    # 测试编排器
    orchestrator = MultiAgentOrchestrator(core)

    print("\n--- Testing Team Collaboration ---")
    team = orchestrator.team_coordinator.create_team("dev_team", "Development Team")
    orchestrator.team_coordinator.add_member("dev_team", "agent_alice")
    orchestrator.team_coordinator.add_member("dev_team", "agent_bob")
    orchestrator.team_coordinator.set_leader("dev_team", "agent_alice")
    orchestrator.team_coordinator.broadcast_to_team("dev_team", "Welcome to the team!")

    print("\n--- Testing Orchestration ---")
    task = Task(
        task_id="main_task",
        description="Build a smart home system",
        requirements=["planning", "coding", "testing"]
    )

    result = orchestrator.orchestrate_complex_task(
        "Build a comprehensive smart home automation system",
        mode=CollaborationMode.TEAM
    )

    print(f"\nOrchestration Result: {result}")

    print("\n=== Test Complete ===")
