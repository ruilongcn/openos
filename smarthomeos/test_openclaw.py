#!/usr/bin/env python3
"""
SmartHomeOS OpenClaw 测试脚本
"""

import os
import sys
import logging

# 添加项目根目录到Python路径
current_file = os.path.abspath(__file__)
root_dir = os.path.dirname(current_file)
sys.path.insert(0, root_dir)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

print("=" * 60)
print("SmartHomeOS - OpenClaw 测试")
print("=" * 60)

try:
    # 导入OpenClaw
    print("\n[1/6] 导入OpenClaw模块...")
    from modules.openclaw import (
        OpenClawCore, AgentConfig, AgentState, AgentRole,
        SkillRegistry, MultiAgentOrchestrator, CollaborationMode, Task
    )
    print("✓ OpenClaw导入成功")

    # 测试核心
    print("\n[2/6] 初始化OpenClaw核心...")
    core = OpenClawCore()
    print("✓ 核心初始化成功")

    # 测试技能
    print("\n[3/6] 初始化技能系统...")
    skills = SkillRegistry()
    print(f"✓ 已加载 {len(skills.skills)} 个技能")
    for skill_name in skills.skills.keys():
        print(f"  - {skill_name}")

    # 测试创建Agent
    print("\n[4/6] 创建Agent...")
    config = AgentConfig(
        agent_id="test_agent",
        name="Test Agent",
        role=AgentRole.GENERIC,
        system_prompt="You are a test agent.",
        skills=list(skills.skills.keys())
    )

    # 注册技能
    for name, skill in skills.skills.items():
        core.register_skill(skill)

    agent = core.create_agent(config)
    print(f"✓ Agent创建成功: {agent.config.name}")

    # 测试启动Agent
    print("\n[5/6] 启动Agent...")
    if core.start_agent("test_agent"):
        print("✓ Agent启动成功")
        agent_info = core.get_agent("test_agent")
        print(f"  - 当前状态: {agent_info.state.name}")

    # 测试消息发送
    print("\n[6/6] 测试发送消息...")
    response = core.send_message_to_agent("test_agent", "Hello World!")
    print(f"✓ 消息发送成功")
    print(f"  - Agent响应: {response[:50]}...")

    # 测试多Agent编排
    print("\n[额外] 测试多Agent编排...")
    orchestrator = MultiAgentOrchestrator(core)
    result = orchestrator.orchestrate_complex_task(
        "Test task for SmartHomeOS",
        mode=CollaborationMode.TEAM
    )
    print(f"✓ 编排完成: {result['status']}")

    print("\n" + "=" * 60)
    print("✓ 所有测试通过！")
    print("=" * 60)
    print("\n现在可以运行: python -m modules.openclaw.app 启动GUI")

except Exception as e:
    print(f"\n✗ 测试失败: {e}")
    import traceback
    print("\n错误详情:")
    traceback.print_exc()
    sys.exit(1)
