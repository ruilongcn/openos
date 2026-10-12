#!/usr/bin/env python3
"""
SmartHomeOS 主服务
"""

import logging
import threading
import time
import os
import sys
from datetime import datetime

# 添加项目根目录到Python路径
import os
import sys

# 获取当前文件路径
current_file = os.path.abspath(__file__)
# 获取core目录路径
core_dir = os.path.dirname(os.path.dirname(current_file))
# 获取项目根目录
root_dir = os.path.dirname(core_dir)
# 添加根目录到Python路径
sys.path.insert(0, root_dir)

print(f"Current file: {current_file}")
print(f"Core directory: {core_dir}")
print(f"Root directory: {root_dir}")
print(f"Python path: {sys.path}")

from core.services.task_scheduler import TaskScheduler
from modules.education.education_module import EducationModule
from integrations.homeassistant.home_assistant import SmartHomeControlPanel
from core.system.config import ConfigManager
from modules.openclaw import OpenClawCore, SkillRegistry, MultiAgentOrchestrator

class SmartHomeOSService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.config_manager = ConfigManager()
        self.config = self.config_manager.get_config()
        self.services = {}
        self.running = False
        
        # 初始化OpenClaw
        self.openclaw_core = None
        self.openclaw_skills = None
        self.openclaw_orchestrator = None
        
        self.logger.info("SmartHomeOS service initialized")

    def start(self):
        """启动服务"""
        self.running = True

        # 启动核心服务
        self._start_core_services()

        # 启动功能模块
        self._start_modules()

        # 启动监控线程
        self.monitor_thread = threading.Thread(target=self._monitor_services, daemon=True)
        self.monitor_thread.start()

        self.logger.info("SmartHomeOS service started")

    def _start_core_services(self):
        """启动核心服务"""
        # 启动任务调度器
        self.services['task_scheduler'] = TaskScheduler()
        self.services['task_scheduler'].start()
        self.logger.info("Task scheduler started")

        # 启动智能家居控制
        self.services['home_assistant'] = SmartHomeControlPanel()
        self.services['home_assistant'].ha.discover_devices()
        self.services['home_assistant'].init_default_scenes()
        self.logger.info("Home Assistant integration started")

    def _start_modules(self):
        """启动功能模块"""
        # 启动教育模块
        if self.config.modules.get('education', True):
            self.services['education'] = EducationModule()
            self.logger.info("Education module started")

        # 启动娱乐模块
        if self.config.modules.get('entertainment', True):
            from modules.entertainment.entertainment_module import EntertainmentModule
            self.services['entertainment'] = EntertainmentModule()
            self.logger.info("Entertainment module started")

        # 启动办公模块
        if self.config.modules.get('office', True):
            from modules.office.office_module import OfficeModule
            self.services['office'] = OfficeModule()
            self.logger.info("Office module started")

        # 启动购物模块
        if self.config.modules.get('shopping', True):
            from modules.shopping.shopping_module import ShoppingModule
            self.services['shopping'] = ShoppingModule()
            self.logger.info("Shopping module started")
            
        # 启动OpenClaw多Agent协作模块
        if self.config.modules.get('openclaw', True):
            self._start_openclaw()
            self.logger.info("OpenClaw module started")
            
    def _start_openclaw(self):
        """启动OpenClaw"""
        # 初始化核心
        self.openclaw_core = OpenClawCore()
        self.openclaw_skills = SkillRegistry()
        self.openclaw_orchestrator = MultiAgentOrchestrator(self.openclaw_core)
        
        # 注册技能
        for name, skill in self.openclaw_skills.skills.items():
            self.openclaw_core.register_skill(skill)
        
        # 创建默认Agent
        from modules.openclaw import AgentConfig, AgentRole
        
        # 创建系统助手Agent
        sys_config = AgentConfig(
            agent_id="openclaw_system",
            name="System Assistant",
            role=AgentRole.GENERIC,
            system_prompt="You are the SmartHomeOS system assistant. Help manage the smart home and coordinate other agents.",
            skills=list(self.openclaw_skills.skills.keys())
        )
        self.openclaw_core.create_agent(sys_config)
        self.openclaw_core.start_agent("openclaw_system")
        
        # 创建智能家居控制Agent
        home_config = AgentConfig(
            agent_id="openclaw_home",
            name="Home Control Agent",
            role=AgentRole.GENERIC,
            system_prompt="You are the home control agent. Manage smart home devices, scenes, and automation.",
            skills=["home_control", "weather", "reminder"]
        )
        self.openclaw_core.create_agent(home_config)
        self.openclaw_core.start_agent("openclaw_home")
        
        self.services['openclaw'] = {
            'core': self.openclaw_core,
            'skills': self.openclaw_skills,
            'orchestrator': self.openclaw_orchestrator
        }
        self.logger.info("OpenClaw initialized with 2 agents")

    def _monitor_services(self):
        """监控服务状态"""
        while self.running:
            try:
                # 检查服务状态
                for service_name, service in self.services.items():
                    # 这里可以添加服务健康检查
                    pass

                # 记录服务状态
                if datetime.now().second == 0:  # 每分钟记录一次
                    self.logger.info(f"Services running: {list(self.services.keys())}")

                time.sleep(1)
            except Exception as e:
                self.logger.error(f"Error monitoring services: {e}")
                time.sleep(5)

    def stop(self):
        """停止服务"""
        self.running = False

        # 停止核心服务
        if 'task_scheduler' in self.services:
            self.services['task_scheduler'].stop()

        # 等待监控线程结束
        if hasattr(self, 'monitor_thread'):
            self.monitor_thread.join(timeout=5)

        self.logger.info("SmartHomeOS service stopped")

    def get_service(self, service_name):
        """获取服务"""
        return self.services.get(service_name)

    def execute_task(self, task):
        """执行任务"""
        if 'task_scheduler' in self.services:
            return self.services['task_scheduler'].add_task(task)
        else:
            self.logger.error("Task scheduler not available")
            return None

    def get_status(self):
        """获取服务状态"""
        status = {
            'running': self.running,
            'services': {},
            'config': {
                'modules': self.config.modules,
                'ai': {
                    'enable_local': self.config.ai.enable_local,
                    'enable_cloud': self.config.ai.enable_cloud
                }
            }
        }

        for service_name, service in self.services.items():
            status['services'][service_name] = 'running'

        return status

if __name__ == "__main__":
    # 配置日志
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # 创建并启动服务
    service = SmartHomeOSService()
    service.start()

    # 测试任务执行
    test_task = {
        'name': 'test_task',
        'capabilities': ['general'],
        'data': 'test data'
    }
    service.execute_task(test_task)

    # 测试服务状态
    print("Service status:", service.get_status())

    # 运行一段时间后停止
    try:
        time.sleep(60)
    finally:
        service.stop()
