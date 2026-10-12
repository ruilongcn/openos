#!/usr/bin/env python3
"""
SmartHomeOS 任务调度器
负责智能分配任务给最合适的Agent
"""

import time
import logging
import threading
from concurrent.futures import ThreadPoolExecutor
from queue import PriorityQueue

class TaskScheduler:
    def __init__(self):
        self.task_queue = PriorityQueue()
        self.executor = ThreadPoolExecutor(max_workers=10)
        self.agents = {}
        self.running = False
        self.logger = logging.getLogger(__name__)
        
    def register_agent(self, agent_name, agent_instance, capabilities):
        """注册Agent"""
        self.agents[agent_name] = {
            'instance': agent_instance,
            'capabilities': capabilities,
            'status': 'idle'
        }
        self.logger.info(f"Agent {agent_name} registered with capabilities: {capabilities}")
    
    def add_task(self, task, priority=5):
        """添加任务到队列"""
        self.task_queue.put((priority, time.time(), task))
        self.logger.info(f"Task added: {task['name']} with priority {priority}")
    
    def find_best_agent(self, task):
        """找到最适合执行任务的Agent"""
        best_agent = None
        best_score = 0
        
        for agent_name, agent_info in self.agents.items():
            if agent_info['status'] == 'idle':
                score = self._calculate_score(agent_info, task)
                if score > best_score:
                    best_score = score
                    best_agent = agent_name
        
        return best_agent
    
    def _calculate_score(self, agent_info, task):
        """计算Agent执行任务的得分"""
        score = 0
        required_capabilities = task.get('capabilities', [])
        
        for capability in required_capabilities:
            if capability in agent_info['capabilities']:
                score += 1
        
        return score
    
    def execute_task(self, task):
        """执行任务"""
        agent_name = self.find_best_agent(task)
        
        if agent_name:
            self.logger.info(f"Assigning task {task['name']} to agent {agent_name}")
            self.agents[agent_name]['status'] = 'busy'
            
            def task_wrapper():
                try:
                    result = self.agents[agent_name]['instance'].execute(task)
                    self.logger.info(f"Task {task['name']} completed successfully")
                    return result
                finally:
                    self.agents[agent_name]['status'] = 'idle'
            
            return self.executor.submit(task_wrapper)
        else:
            self.logger.warning(f"No available agent for task {task['name']}")
            return None
    
    def start(self):
        """启动调度器"""
        self.running = True
        threading.Thread(target=self._process_queue, daemon=True).start()
        self.logger.info("Task scheduler started")
    
    def _process_queue(self):
        """处理任务队列"""
        while self.running:
            if not self.task_queue.empty():
                priority, timestamp, task = self.task_queue.get()
                self.execute_task(task)
                self.task_queue.task_done()
            else:
                time.sleep(0.1)
    
    def stop(self):
        """停止调度器"""
        self.running = False
        self.executor.shutdown(wait=True)
        self.logger.info("Task scheduler stopped")

class BaseAgent:
    """Agent基类"""
    def __init__(self, name):
        self.name = name
        self.capabilities = []
        self.logger = logging.getLogger(f"agent.{name}")
    
    def execute(self, task):
        """执行任务"""
        raise NotImplementedError("Subclasses must implement execute method")

class ExampleAgent(BaseAgent):
    """示例Agent"""
    def __init__(self, name):
        super().__init__(name)
        self.capabilities = ['general', 'example']
    
    def execute(self, task):
        """执行任务"""
        self.logger.info(f"Executing task: {task['name']}")
        # 模拟任务执行
        time.sleep(1)
        return f"Task {task['name']} executed by {self.name}"

if __name__ == "__main__":
    # 配置日志
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # 创建调度器
    scheduler = TaskScheduler()
    
    # 注册Agent
    scheduler.register_agent('example_agent', ExampleAgent('example_agent'), ['general', 'example'])
    
    # 启动调度器
    scheduler.start()
    
    # 添加任务
    for i in range(5):
        task = {
            'name': f'task_{i}',
            'capabilities': ['general'],
            'data': f'data_{i}'
        }
        scheduler.add_task(task, priority=5-i)
    
    # 等待任务完成
    time.sleep(10)
    
    # 停止调度器
    scheduler.stop()
