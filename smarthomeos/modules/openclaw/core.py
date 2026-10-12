#!/usr/bin/env python3
"""
SmartHomeOS OpenClaw - 内嵌式多Agent协作框架
核心架构模块
"""

import os
import sys
import json
import time
import logging
from enum import Enum, auto
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from abc import ABC, abstractmethod

# 添加项目根目录到Python路径
current_file = os.path.abspath(__file__)
core_dir = os.path.dirname(os.path.dirname(current_file))
root_dir = os.path.dirname(core_dir)
sys.path.insert(0, root_dir)

logger = logging.getLogger(__name__)


class AgentState(Enum):
    """Agent状态枚举"""
    CREATED = auto()      # 已创建但未运行
    INITIALIZING = auto() # 正在初始化
    RUNNING = auto()      # 运行中
    PAUSED = auto()       # 已暂停
    STOPPED = auto()      # 已停止
    ERROR = auto()        # 错误状态


class AgentRole(Enum):
    """Agent角色类型"""
    GENERIC = auto()        # 通用助手
    EDUCATION = auto()      # 教育助手
    ENTERTAINMENT = auto()  # 娱乐助手
    OFFICE = auto()         # 办公助手
    SHOPPING = auto()       # 购物助手
    HOME_CONTROL = auto()   # 家庭控制助手
    CUSTOM = auto()         # 自定义角色


@dataclass
class AgentConfig:
    """Agent配置"""
    agent_id: str
    name: str
    role: AgentRole
    system_prompt: str
    model: str = "ollama/llama3:8b"
    temperature: float = 0.7
    max_turns: int = 50
    channels: List[str] = field(default_factory=lambda: ["terminal"])
    memory_backend: str = "sqlite"
    skills: List[str] = field(default_factory=list)
    workspace: Optional[str] = None
    created_at: float = field(default_factory=time.time)

    @classmethod
    def from_dict(cls, data: Dict) -> 'AgentConfig':
        """从字典创建配置"""
        role = AgentRole[data.get('role', 'GENERIC')]
        return cls(
            agent_id=data.get('agent_id', 'default'),
            name=data.get('name', 'Unnamed Agent'),
            role=role,
            system_prompt=data.get('system_prompt', 'You are a helpful assistant.'),
            model=data.get('model', 'ollama/llama3:8b'),
            temperature=data.get('temperature', 0.7),
            max_turns=data.get('max_turns', 50),
            channels=data.get('channels', ['terminal']),
            memory_backend=data.get('memory_backend', 'sqlite'),
            skills=data.get('skills', []),
            workspace=data.get('workspace')
        )

    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            'agent_id': self.agent_id,
            'name': self.name,
            'role': self.role.name,
            'system_prompt': self.system_prompt,
            'model': self.model,
            'temperature': self.temperature,
            'max_turns': self.max_turns,
            'channels': self.channels,
            'memory_backend': self.memory_backend,
            'skills': self.skills,
            'workspace': self.workspace,
            'created_at': self.created_at
        }


@dataclass
class AgentContext:
    """Agent运行时上下文"""
    config: AgentConfig
    state: AgentState = AgentState.CREATED
    session_history: List[Dict] = field(default_factory=list)
    current_conversation: List[Dict] = field(default_factory=list)
    memory: Optional[Any] = None
    tools: Dict[str, Any] = field(default_factory=dict)
    start_time: Optional[float] = None
    last_activity: Optional[float] = None
    total_messages: int = 0

    def get_session_file(self, base_dir: Path) -> Path:
        """获取会话存储文件"""
        return base_dir / f"{self.config.agent_id}_session.jsonl"


class BaseSkill(ABC):
    """技能基类"""
    name: str
    description: str
    version: str = "1.0.0"

    @abstractmethod
    def execute(self, input_data: Dict) -> Dict:
        """执行技能"""
        pass

    def get_metadata(self) -> Dict:
        """获取技能元数据"""
        return {
            'name': self.name,
            'description': self.description,
            'version': self.version
        }


class BaseMemoryBackend(ABC):
    """记忆存储后端基类"""
    @abstractmethod
    def store(self, key: str, value: Any) -> bool:
        """存储数据"""
        pass

    @abstractmethod
    def retrieve(self, key: str) -> Optional[Any]:
        """检索数据"""
        pass

    @abstractmethod
    def search(self, query: str, limit: int = 10) -> List[Any]:
        """搜索记忆"""
        pass


class SQLiteMemoryBackend(BaseMemoryBackend):
    """SQLite记忆存储后端"""
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.db = None
        self._init_db()

    def _init_db(self):
        """初始化数据库"""
        import sqlite3
        self.db = sqlite3.connect(self.db_path)
        cursor = self.db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memory
            (key TEXT PRIMARY KEY, value TEXT, timestamp REAL)
        ''')
        self.db.commit()

    def store(self, key: str, value: Any) -> bool:
        """存储数据"""
        try:
            import sqlite3
            cursor = self.db.cursor()
            cursor.execute(
                'INSERT OR REPLACE INTO memory VALUES (?, ?, ?)',
                (key, json.dumps(value), time.time())
            )
            self.db.commit()
            return True
        except Exception as e:
            logger.error(f"Failed to store memory: {e}")
            return False

    def retrieve(self, key: str) -> Optional[Any]:
        """检索数据"""
        try:
            cursor = self.db.cursor()
            cursor.execute('SELECT value FROM memory WHERE key = ?', (key,))
            row = cursor.fetchone()
            if row:
                return json.loads(row[0])
            return None
        except Exception as e:
            logger.error(f"Failed to retrieve memory: {e}")
            return None

    def search(self, query: str, limit: int = 10) -> List[Any]:
        """搜索记忆"""
        try:
            cursor = self.db.cursor()
            cursor.execute(
                'SELECT value FROM memory WHERE value LIKE ? ORDER BY timestamp DESC LIMIT ?',
                (f'%{query}%', limit)
            )
            return [json.loads(row[0]) for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"Failed to search memory: {e}")
            return []


class BaseChannel(ABC):
    """通信渠道基类"""
    name: str

    @abstractmethod
    def send(self, message: str, recipient: Optional[str] = None) -> bool:
        """发送消息"""
        pass

    @abstractmethod
    def receive(self) -> Optional[str]:
        """接收消息"""
        pass


class TerminalChannel(BaseChannel):
    """终端渠道"""
    name: str = "terminal"

    def send(self, message: str, recipient: Optional[str] = None) -> bool:
        """发送消息到终端"""
        print(f"\n{'>' * 50}")
        print(message)
        print(f"{'<' * 50}\n")
        return True

    def receive(self) -> Optional[str]:
        """从终端接收消息"""
        try:
            user_input = input(">> ")
            return user_input.strip() if user_input else None
        except (KeyboardInterrupt, EOFError):
            return None


class OpenClawCore:
    """OpenClaw核心引擎"""

    def __init__(self, base_dir: Optional[str] = None):
        self.base_dir = Path(base_dir or Path.home() / ".smarthomeos" / "openclaw")
        self.workspace_dir = self.base_dir / "workspace"
        self.agents_dir = self.base_dir / "agents"
        self.skills_dir = self.base_dir / "skills"
        self.config_file = self.base_dir / "openclaw.json"

        self._setup_directories()

        self.agents: Dict[str, AgentContext] = {}
        self.skills: Dict[str, BaseSkill] = {}
        self.channels: Dict[str, BaseChannel] = {}
        self.config: Dict[str, Any] = self._load_config()

        self._load_default_channels()
        logger.info("OpenClawCore initialized")

    def _setup_directories(self):
        """设置目录结构"""
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.workspace_dir.mkdir(exist_ok=True)
        self.agents_dir.mkdir(exist_ok=True)
        self.skills_dir.mkdir(exist_ok=True)

    def _load_config(self) -> Dict[str, Any]:
        """加载配置"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Failed to load config: {e}")
                return self._get_default_config()
        return self._get_default_config()

    def _get_default_config(self) -> Dict[str, Any]:
        """获取默认配置"""
        return {
            'version': '1.0.0',
            'default_model': 'ollama/llama3:8b',
            'default_memory_backend': 'sqlite',
            'default_temperature': 0.7,
            'agents': {},
            'skills': [],
            'channels': ['terminal']
        }

    def _save_config(self):
        """保存配置"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            logger.error(f"Failed to save config: {e}")
            return False

    def _load_default_channels(self):
        """加载默认渠道"""
        self.channels['terminal'] = TerminalChannel()
        logger.info("Default channels loaded: terminal")

    def create_agent(self, config: AgentConfig) -> Optional[AgentContext]:
        """创建新Agent"""
        if config.agent_id in self.agents:
            logger.error(f"Agent {config.agent_id} already exists")
            return None

        # 创建Agent工作空间
        if not config.workspace:
            config.workspace = str(self.workspace_dir / config.agent_id)
        (Path(config.workspace)).mkdir(parents=True, exist_ok=True)

        # 创建Agent目录
        agent_dir = self.agents_dir / config.agent_id
        agent_dir.mkdir(exist_ok=True)

        # 创建默认配置文件
        self._create_agent_files(agent_dir, config)

        # 初始化记忆存储
        memory_backend = self._create_memory_backend(config)

        # 创建Agent上下文
        context = AgentContext(
            config=config,
            memory=memory_backend
        )

        self.agents[config.agent_id] = context
        self.config['agents'][config.agent_id] = config.to_dict()
        self._save_config()

        logger.info(f"Created agent: {config.agent_id}")
        return context

    def _create_agent_files(self, agent_dir: Path, config: AgentConfig):
        """创建Agent相关文件"""
        # SOUL.md - Agent个性定义
        with open(agent_dir / "SOUL.md", 'w', encoding='utf-8') as f:
            f.write(f"# {config.name} - SOUL\n\n")
            f.write("## Personality Traits\n")
            f.write("- Helpful and friendly\n")
            f.write("- Knowledgeable in {config.role.name} domain\n\n")
            f.write("## Core Values\n")
            f.write("- Privacy first\n")
            f.write("- User-centric approach\n")

        # AGENTS.md - Agent指令
        with open(agent_dir / "AGENTS.md", 'w', encoding='utf-8') as f:
            f.write(f"# {config.name} - Instructions\n\n")
            f.write("## Role\n")
            f.write(f"You are {config.name}, an AI assistant for {config.role.name} tasks.\n\n")
            f.write("## System Prompt\n")
            f.write(config.system_prompt)

        # WORKING.md - 工作状态
        with open(agent_dir / "WORKING.md", 'w', encoding='utf-8') as f:
            f.write("# Working State\n\n")
            f.write("## Current Tasks\n")
            f.write("- No active tasks\n\n")

    def _create_memory_backend(self, config: AgentConfig) -> BaseMemoryBackend:
        """创建记忆存储后端"""
        if config.memory_backend == 'sqlite':
            db_path = str(self.agents_dir / config.agent_id / "memory.sqlite")
            return SQLiteMemoryBackend(db_path)
        else:
            db_path = str(self.agents_dir / config.agent_id / "memory.sqlite")
            return SQLiteMemoryBackend(db_path)

    def start_agent(self, agent_id: str) -> bool:
        """启动Agent"""
        if agent_id not in self.agents:
            logger.error(f"Agent {agent_id} not found")
            return False

        agent = self.agents[agent_id]

        if agent.state == AgentState.RUNNING:
            logger.warning(f"Agent {agent_id} is already running")
            return True

        agent.state = AgentState.INITIALIZING
        logger.info(f"Initializing agent: {agent_id}")

        # 加载Agent技能
        self._load_agent_skills(agent)

        # 启动Agent
        agent.state = AgentState.RUNNING
        agent.start_time = time.time()
        agent.last_activity = time.time()

        logger.info(f"Agent started: {agent_id}")
        return True

    def _load_agent_skills(self, agent: AgentContext):
        """加载Agent技能"""
        for skill_name in agent.config.skills:
            if skill_name in self.skills:
                agent.tools[skill_name] = self.skills[skill_name]
                logger.info(f"Loaded skill {skill_name} for agent {agent.config.agent_id}")

    def stop_agent(self, agent_id: str) -> bool:
        """停止Agent"""
        if agent_id not in self.agents:
            logger.error(f"Agent {agent_id} not found")
            return False

        agent = self.agents[agent_id]

        if agent.state == AgentState.STOPPED:
            logger.warning(f"Agent {agent_id} is already stopped")
            return True

        agent.state = AgentState.STOPPED
        logger.info(f"Agent stopped: {agent_id}")
        return True

    def pause_agent(self, agent_id: str) -> bool:
        """暂停Agent"""
        if agent_id not in self.agents:
            logger.error(f"Agent {agent_id} not found")
            return False

        agent = self.agents[agent_id]

        if agent.state == AgentState.RUNNING:
            agent.state = AgentState.PAUSED
            logger.info(f"Agent paused: {agent_id}")
            return True
        return False

    def resume_agent(self, agent_id: str) -> bool:
        """恢复Agent"""
        if agent_id not in self.agents:
            logger.error(f"Agent {agent_id} not found")
            return False

        agent = self.agents[agent_id]

        if agent.state == AgentState.PAUSED:
            agent.state = AgentState.RUNNING
            logger.info(f"Agent resumed: {agent_id}")
            return True
        return False

    def get_agent(self, agent_id: str) -> Optional[AgentContext]:
        """获取Agent"""
        return self.agents.get(agent_id)

    def list_agents(self) -> List[Dict]:
        """列出所有Agent"""
        return [
            {
                'agent_id': agent.config.agent_id,
                'name': agent.config.name,
                'role': agent.config.role.name,
                'state': agent.state.name,
                'start_time': agent.start_time,
                'total_messages': agent.total_messages
            }
            for agent in self.agents.values()
        ]

    def register_skill(self, skill: BaseSkill):
        """注册技能"""
        self.skills[skill.name] = skill
        self.config['skills'].append(skill.get_metadata())
        logger.info(f"Skill registered: {skill.name}")
        self._save_config()

    def send_message_to_agent(self, agent_id: str, message: str,
                             channel: str = 'terminal') -> Optional[str]:
        """向Agent发送消息"""
        if agent_id not in self.agents:
            logger.error(f"Agent {agent_id} not found")
            return None

        agent = self.agents[agent_id]

        if agent.state != AgentState.RUNNING:
            logger.error(f"Agent {agent_id} is not running")
            return None

        # 记录消息
        user_message = {
            'role': 'user',
            'content': message,
            'timestamp': time.time()
        }
        agent.current_conversation.append(user_message)
        agent.session_history.append(user_message)
        agent.total_messages += 1
        agent.last_activity = time.time()

        # 生成响应（模拟）
        response = self._generate_agent_response(agent, message)

        assistant_message = {
            'role': 'assistant',
            'content': response,
            'timestamp': time.time()
        }
        agent.current_conversation.append(assistant_message)
        agent.session_history.append(assistant_message)
        agent.total_messages += 1

        # 通过渠道发送响应
        if channel in self.channels:
            self.channels[channel].send(response)

        return response

    def _generate_agent_response(self, agent: AgentContext, message: str) -> str:
        """生成Agent响应（模拟）"""
        role = agent.config.role
        name = agent.config.name

        role_translation = {
            AgentRole.GENERIC: "通用",
            AgentRole.EDUCATION: "教育",
            AgentRole.ENTERTAINMENT: "娱乐",
            AgentRole.OFFICE: "办公",
            AgentRole.SHOPPING: "购物",
            AgentRole.HOME_CONTROL: "家居控制",
            AgentRole.MANAGER: "管理",
            AgentRole.WORKER: "执行",
            AgentRole.RESEARCHER: "研究",
            AgentRole.ANALYST: "分析",
            AgentRole.COORDINATOR: "协调"
        }
        
        role_cn = role_translation.get(role, "通用")
        base_response = f"你好！我是 {name}，你的{role_cn}助手。\n\n"

        if role == AgentRole.EDUCATION:
            return base_response + f"我来帮你学习：{message[:50]}..."
        elif role == AgentRole.ENTERTAINMENT:
            return base_response + f"让我们一起享受娱乐时光：{message[:50]}..."
        elif role == AgentRole.OFFICE:
            return base_response + f"我来协助你的工作：{message[:50]}..."
        elif role == AgentRole.SHOPPING:
            return base_response + f"我来帮你购物：{message[:50]}..."
        elif role == AgentRole.HOME_CONTROL:
            return base_response + f"正在控制你的智能家居：{message[:50]}..."
        else:
            return base_response + f"我能帮你做什么：{message[:50]}？"

    def shutdown(self):
        """关闭OpenClaw核心"""
        logger.info("Shutting down OpenClawCore")
        for agent_id in list(self.agents.keys()):
            self.stop_agent(agent_id)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # 测试OpenClaw核心
    core = OpenClawCore()

    # 创建测试Agent
    config = AgentConfig(
        agent_id="test_assistant",
        name="Test Assistant",
        role=AgentRole.GENERIC,
        system_prompt="You are a helpful test assistant.",
        skills=[]
    )

    agent = core.create_agent(config)

    if agent:
        core.start_agent("test_assistant")
        print("\n=== OpenClaw Test ===\n")
        print("Agent created and started!")
        print(f"\nAgents list: {core.list_agents()}")

        # 测试发送消息
        response = core.send_message_to_agent("test_assistant", "Hello!")
        print(f"\nAgent response: {response}")

        core.stop_agent("test_assistant")
