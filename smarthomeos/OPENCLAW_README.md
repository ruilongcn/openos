# SmartHomeOS - OpenClaw

内嵌式多Agent协作应用程序

## 功能特性

### 核心模块
- Agent生命周期管理（创建、启动、暂停、停止）
- Agent配置管理
- 消息路由与Agent间通信
- 内存后端（SQLite）

### 技能系统
- Calculator - 计算器
- Web Search - 网页搜索（模拟）
- File System - 文件系统操作
- Weather - 天气查询（模拟）
- Home Control - 智能家居控制
- News - 新闻查询（模拟）
- Reminder - 提醒功能

### 多Agent协作
- SubAgent模式 - 父子Agent委派
- Team模式 - 团队协作
- Agent-To-Agent - 点对点通信
- 任务编排与执行

### GUI界面
- 聊天对话界面
- Agent管理面板
- 技能测试面板
- 团队协作管理

## 安装与使用

### 快速测试
```bash
cd smarthomeos
python test_openclaw.py
```

### 启动GUI
```bash
cd smarthomeos
python -m modules.openclaw.app
```

### 与SmartHomeOS一起使用
```bash
python core/services/smarthomeos_service.py
```

## 模块结构
```
modules/openclaw/
├── __init__.py       # 模块入口
├── core.py           # 核心模块
├── skills.py         # 技能系统
├── collaboration.py  # 协作系统
└── app.py            # GUI应用
```

## 使用示例

### 基本使用
```python
from modules.openclaw import (
    OpenClawCore, AgentConfig, AgentRole
)

# 初始化
core = OpenClawCore()

# 创建Agent
config = AgentConfig(
    agent_id="my_agent",
    name="My Agent",
    role=AgentRole.GENERIC,
    system_prompt="You are a helpful assistant."
)
agent = core.create_agent(config)

# 启动Agent
core.start_agent("my_agent")

# 发送消息
response = core.send_message_to_agent("my_agent", "Hello!")
print(response)
```

### 技能使用
```python
from modules.openclaw import SkillRegistry

skills = SkillRegistry()

# 执行计算器技能
result = skills.execute_skill("calculator", {
    "expression": "2 + 2 * 3"
})
print(result)
```

### 多Agent协作
```python
from modules.openclaw import MultiAgentOrchestrator, CollaborationMode

orchestrator = MultiAgentOrchestrator(core)
result = orchestrator.orchestrate_complex_task(
    "Build a smart home",
    mode=CollaborationMode.TEAM
)
```

## 配置说明
在 `config.py` 中启用/禁用OpenClaw:
```python
modules: {
    'openclaw': True,
    ...
}
```

## 默认Agent
启动时会自动创建两个Agent:
1. System Assistant (系统助手)
2. Home Control Agent (智能家居控制)

## 版本
v1.0.0
