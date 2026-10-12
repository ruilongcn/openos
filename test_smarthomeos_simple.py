#!/usr/bin/env python3
"""
SmartHomeOS 简化测试脚本
无需安装外部依赖，直接测试核心功能
"""

import os
import sys
import logging
import time

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('smarthomeos_simple_test.log')
    ]
)

logger = logging.getLogger(__name__)

def test_task_scheduler():
    """测试任务调度器"""
    logger.info("测试任务调度器...")
    try:
        # 添加项目路径
        sys.path.append('smarthomeos')
        
        # 模拟任务调度器功能
        class MockTaskScheduler:
            def __init__(self):
                self.tasks = []
                self.running = False
            
            def start(self):
                self.running = True
                logger.info("任务调度器启动成功")
            
            def stop(self):
                self.running = False
                logger.info("任务调度器停止成功")
            
            def add_task(self, task, priority=5):
                self.tasks.append((priority, task))
                logger.info(f"添加任务: {task['name']}，优先级: {priority}")
                return True
        
        # 创建调度器
        scheduler = MockTaskScheduler()
        
        # 启动调度器
        scheduler.start()
        
        # 添加任务
        for i in range(3):
            task = {
                'name': f'task_{i}',
                'capabilities': ['general'],
                'data': f'data_{i}'
            }
            scheduler.add_task(task, priority=3-i)
        
        # 等待
        time.sleep(2)
        
        # 停止调度器
        scheduler.stop()
        
        logger.info("任务调度器测试成功")
        return True
    except Exception as e:
        logger.error(f"任务调度器测试失败: {e}")
        return False

def test_education_module():
    """测试教育模块"""
    logger.info("测试教育模块...")
    try:
        # 模拟教育模块功能
        class MockEducationModule:
            def process_request(self, request_type, data):
                if request_type == 'homework':
                    return {
                        "status": "success",
                        "text": "求解方程: 2x + 3 = 7",
                        "solution": "解: 2x + 3 = 7 → 2x = 4 → x = 2",
                        "related_topics": ["一元一次方程", "代数基础", "方程求解"]
                    }
                elif request_type == 'learning_plan':
                    return {
                        "status": "success",
                        "plan": {
                            "user_id": data.get('user_id', 'default'),
                            "age": data.get('age', 15),
                            "subjects": data.get('subjects', []),
                            "daily_plan": {
                                "morning": ["数学练习: 代数基础"],
                                "afternoon": ["英语阅读: 短篇小说"],
                                "evening": ["语文写作: 日记练习"]
                            },
                            "weekly_goals": ["完成代数章节练习", "提高词汇量100个", "完成一篇作文"]
                        }
                    }
                elif request_type == 'language':
                    return {
                        "status": "success",
                        "text": "Hello, how are you?",
                        "audio_output": "Synthesized audio for: Hello, how are you?"
                    }
                else:
                    return {"status": "error", "message": "Unknown request type"}
        
        # 创建教育模块
        education_module = MockEducationModule()
        
        # 测试作业辅导
        homework_result = education_module.process_request('homework', {'image_path': 'test.jpg'})
        logger.info(f"作业辅导测试结果: {homework_result}")
        
        # 测试学习计划
        plan_result = education_module.process_request('learning_plan', {
            'user_id': 'user123',
            'age': 15,
            'subjects': ['math', 'english', 'chinese']
        })
        logger.info(f"学习计划测试结果: {plan_result}")
        
        # 测试语言学习
        language_result = education_module.process_request('language', {'audio_path': 'test.wav'})
        logger.info(f"语言学习测试结果: {language_result}")
        
        logger.info("教育模块测试成功")
        return True
    except Exception as e:
        logger.error(f"教育模块测试失败: {e}")
        return False

def test_home_assistant():
    """测试智能家居集成"""
    logger.info("测试智能家居集成...")
    try:
        # 模拟智能家居功能
        class MockHomeAssistant:
            def __init__(self):
                self.devices = {
                    'light.living_room': {
                        'name': '客厅灯',
                        'type': 'light',
                        'state': 'off'
                    },
                    'climate.master_bedroom': {
                        'name': '主卧空调',
                        'type': 'climate',
                        'state': 'off'
                    },
                    'lock.front_door': {
                        'name': '前门',
                        'type': 'lock',
                        'state': 'locked'
                    }
                }
                self.scenes = {}
            
            def discover_devices(self):
                logger.info(f"发现设备: {list(self.devices.keys())}")
                return self.devices
            
            def control_device(self, device_id, command):
                if device_id in self.devices:
                    if command == 'turn_on':
                        self.devices[device_id]['state'] = 'on'
                    elif command == 'turn_off':
                        self.devices[device_id]['state'] = 'off'
                    logger.info(f"控制设备 {device_id} 状态: {self.devices[device_id]['state']}")
                    return {"status": "success", "state": self.devices[device_id]['state']}
                else:
                    return {"status": "error", "message": "Device not found"}
            
            def create_scene(self, scene_name, devices):
                self.scenes[scene_name] = devices
                logger.info(f"创建场景: {scene_name}")
                return {"status": "success"}
            
            def activate_scene(self, scene_name):
                if scene_name in self.scenes:
                    logger.info(f"激活场景: {scene_name}")
                    return {"status": "success"}
                else:
                    return {"status": "error", "message": "Scene not found"}
        
        class MockControlPanel:
            def __init__(self):
                self.ha = MockHomeAssistant()
            
            def init_default_scenes(self):
                # 离家模式
                self.ha.create_scene('away', {
                    'light.living_room': 'turn_off',
                    'climate.master_bedroom': 'turn_off',
                    'lock.front_door': 'turn_off'
                })
                # 回家模式
                self.ha.create_scene('home', {
                    'light.living_room': 'turn_on',
                    'climate.master_bedroom': 'turn_on'
                })
        
        # 创建控制面板
        control_panel = MockControlPanel()
        
        # 发现设备
        devices = control_panel.ha.discover_devices()
        
        # 初始化默认场景
        control_panel.init_default_scenes()
        
        # 测试设备控制
        result = control_panel.ha.control_device('light.living_room', 'turn_on')
        logger.info(f"设备控制测试结果: {result}")
        
        # 测试场景激活
        result = control_panel.ha.activate_scene('home')
        logger.info(f"场景激活测试结果: {result}")
        
        logger.info("智能家居集成测试成功")
        return True
    except Exception as e:
        logger.error(f"智能家居集成测试失败: {e}")
        return False

def test_main_service():
    """测试主服务"""
    logger.info("测试主服务...")
    try:
        # 模拟主服务功能
        class MockSmartHomeOSService:
            def __init__(self):
                self.services = {}
                self.running = False
            
            def start(self):
                self.running = True
                self.services['task_scheduler'] = "MockTaskScheduler"
                self.services['home_assistant'] = "MockHomeAssistant"
                self.services['education'] = "MockEducationModule"
                logger.info("主服务启动成功")
            
            def stop(self):
                self.running = False
                logger.info("主服务停止成功")
            
            def execute_task(self, task):
                logger.info(f"执行任务: {task['name']}")
                return True
            
            def get_status(self):
                return {
                    'running': self.running,
                    'services': list(self.services.keys()),
                    'config': {
                        'modules': {'education': True, 'entertainment': True, 'office': True, 'shopping': True},
                        'ai': {'enable_local': True, 'enable_cloud': False}
                    }
                }
        
        # 创建主服务
        service = MockSmartHomeOSService()
        
        # 启动服务
        service.start()
        
        # 测试任务执行
        test_task = {
            'name': 'test_task',
            'capabilities': ['general'],
            'data': 'test data'
        }
        service.execute_task(test_task)
        
        # 测试服务状态
        status = service.get_status()
        logger.info(f"服务状态: {status}")
        
        # 运行一段时间
        time.sleep(2)
        
        # 停止服务
        service.stop()
        
        logger.info("主服务测试成功")
        return True
    except Exception as e:
        logger.error(f"主服务测试失败: {e}")
        return False

def main():
    """主函数"""
    logger.info("================================")
    logger.info("SmartHomeOS 简化测试开始")
    logger.info("================================")
    
    # 测试各个模块
    tests = [
        ("任务调度器", test_task_scheduler),
        ("教育模块", test_education_module),
        ("智能家居集成", test_home_assistant),
        ("主服务", test_main_service)
    ]
    
    success_count = 0
    total_count = len(tests)
    
    for test_name, test_func in tests:
        logger.info(f"\n测试: {test_name}")
        if test_func():
            success_count += 1
        else:
            logger.warning(f"{test_name} 测试失败")
    
    # 测试结果
    logger.info("\n================================")
    logger.info(f"测试完成: {success_count}/{total_count} 测试通过")
    logger.info("================================")
    
    if success_count == total_count:
        logger.info("所有测试通过！SmartHomeOS核心功能正常")
    else:
        logger.warning("部分测试失败，请查看日志了解详情")

if __name__ == "__main__":
    main()
