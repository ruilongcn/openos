#!/usr/bin/env python3
"""
SmartHomeOS - OpenClaw Module
内嵌式多Agent协作应用程序
"""

from .core import (
    OpenClawCore,
    AgentConfig,
    AgentContext,
    AgentState,
    AgentRole,
    BaseSkill,
    BaseMemoryBackend,
    SQLiteMemoryBackend
)

from .skills import (
    SkillRegistry,
    CalculatorSkill,
    WebSearchSkill,
    FileSystemSkill,
    WeatherSkill,
    HomeControlSkill,
    NewsSkill,
    ReminderSkill
)

from .collaboration import (
    MultiAgentOrchestrator,
    CollaborationMode,
    SubAgentCoordinator,
    AgentTeamCoordinator,
    AgentToAgentProtocol,
    AgentTeam,
    Task,
    TaskStatus
)

from .app import OpenClawGUI, main as run_openclaw_gui

__version__ = "1.0.0"
__all__ = [
    "OpenClawCore", "AgentConfig", "AgentContext",
    "AgentState", "AgentRole", "BaseSkill",
    "BaseMemoryBackend", "SQLiteMemoryBackend",
    "SkillRegistry", "CalculatorSkill",
    "WebSearchSkill", "FileSystemSkill",
    "WeatherSkill", "HomeControlSkill",
    "NewsSkill", "ReminderSkill",
    "MultiAgentOrchestrator", "CollaborationMode",
    "SubAgentCoordinator", "AgentTeamCoordinator",
    "AgentToAgentProtocol", "AgentTeam",
    "Task", "TaskStatus",
    "OpenClawGUI", "run_openclaw_gui"
]
