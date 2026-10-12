#!/usr/bin/env python3
"""
SmartHomeOS Windows测试脚本
无需WSL，直接在Windows环境下测试核心功能
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
        logging.FileHandler('smarthomeos_test.log')
    ]
)

logger = logging.getLogger(__name__)

def check_python():
    """检查Python环境"""
    logger.info("检查Python环境...")
    try:
        import sys
        logger.info(f"Python版本: {sys.version}")
        return True
    except Exception as e:
        logger.error(f"Python环境检查失败: {e}")
        return False

def install_dependencies():
    """安装依赖"""
    logger.info("安装依赖包...")
    try:
        import pip
        # 安装必要的依赖
        packages = [
            'langchain',
            'transformers',
            'requests',
            'pymongo',
            'redis',
            'psutil',
            'pyyaml'
        ]
        
        for package in packages:
            try:
                __import__(package)
                logger.info(f"{package} 已安装")
            except ImportError:
                logger.info(f"安装 {package}...")
                pip.main(['install', package])
        
        return True
    except Exception as e:
        logger.error(f"依赖安装失败: {e}")
        return False

def test_task_scheduler():
    """测试任务调度器"""
    logger.info("测试任务调度器...")
    try:
        sys.path.append('smarthomeos')
        from core.services.task_scheduler import TaskScheduler, ExampleAgent
        
        # 创建调度器
        scheduler = TaskScheduler()
        
        # 注册Agent
        scheduler.register_agent('example_agent', ExampleAgent('example_agent'), ['general', 'example'])
        
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
        
        # 等待任务完成
        time.sleep(5)
        
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
        sys.path.append('smarthomeos')
        from modules.education.education_module import EducationModule
        
        # 创建教育模块
        education_module = EducationModule()
        
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
        sys.path.append('smarthomeos')
        from integrations.homeassistant.home_assistant import SmartHomeControlPanel
        
        # 创建智能家居控制面板
        control_panel = SmartHomeControlPanel()
        
        # 发现设备
        devices = control_panel.ha.discover_devices()
        logger.info(f"发现设备: {devices}")
        
        # 初始化默认场景
        control_panel.init_default_scenes()
        
        # 测试设备控制
        result = control_panel.ha.control_device('light.living_room', 'turn_on')
        logger.info(f"设备控制测试结果: {result}")
        
        # 测试场景激活
        result = control_panel.ha.activate_scene('home')
        logger.info(f"场景激活测试结果: {result}")
        
        # 获取设备摘要
        device_summary = control_panel.get_device_summary()
        logger.info(f"设备摘要: {device_summary}")
        
        # 获取场景摘要
        scene_summary = control_panel.get_scene_summary()
        logger.info(f"场景摘要: {scene_summary}")
        
        logger.info("智能家居集成测试成功")
        return True
    except Exception as e:
        logger.error(f"智能家居集成测试失败: {e}")
        return False

def test_main_service():
    """测试主服务"""
    logger.info("测试主服务...")
    try:
        sys.path.append('smarthomeos')
        from core.services.smarthomeos_service import SmartHomeOSService
        
        # 创建主服务
        service = SmartHomeOSService()
        
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
        time.sleep(10)
        
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
    logger.info("SmartHomeOS Windows测试开始")
    logger.info("================================")
    
    # 检查Python环境
    if not check_python():
        logger.error("Python环境检查失败，退出测试")
        return
    
    # 安装依赖
    if not install_dependencies():
        logger.error("依赖安装失败，退出测试")
        return
    
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
