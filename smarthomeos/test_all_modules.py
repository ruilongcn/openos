#!/usr/bin/env python3
"""
SmartHomeOS 综合测试脚本
测试所有模块功能
"""

import os
import sys

# 添加项目根目录到Python路径
current_file = os.path.abspath(__file__)
root_dir = os.path.dirname(current_file)
sys.path.insert(0, root_dir)

import logging
import time

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def test_education_module():
    """测试教育模块"""
    logger.info("\n" + "="*60)
    logger.info("测试 AI 教育学习模块")
    logger.info("="*60)

    try:
        from modules.education.education_module import EducationModule

        education = EducationModule()

        # 测试作业辅导
        result = education.process_request('homework', {'image_path': 'test.jpg'})
        logger.info(f"✓ 作业辅导: {result['status']}")

        # 测试学习计划
        result = education.process_request('learning_plan', {
            'user_id': 'user123',
            'age': 15,
            'subjects': ['math', 'english', 'chinese']
        })
        logger.info(f"✓ 学习计划: {result['status']}")

        # 测试语言学习
        result = education.process_request('language', {'audio_path': 'test.wav'})
        logger.info(f"✓ 语言学习: {result['status']}")

        return True
    except Exception as e:
        logger.error(f"✗ 教育模块测试失败: {e}")
        return False

def test_entertainment_module():
    """测试娱乐模块"""
    logger.info("\n" + "="*60)
    logger.info("测试 AI 影视娱乐模块")
    logger.info("="*60)

    try:
        from modules.entertainment.entertainment_module import EntertainmentModule

        entertainment = EntertainmentModule()

        # 测试智能推荐
        result = entertainment.process_request('recommendation', {
            'user_id': 'user123',
            'content_type': 'movies',
            'mood': 'relaxed'
        })
        logger.info(f"✓ 智能推荐: {result['status']}")

        # 测试字幕生成
        result = entertainment.process_request('subtitle', {
            'video_path': '/movies/test.mp4',
            'language': 'zh-CN'
        })
        logger.info(f"✓ 字幕生成: {result['status']}")

        # 测试媒体中心
        result = entertainment.process_request('media_center', {
            'action': 'play',
            'media_path': '/movies/test.mp4',
            'media_type': 'video'
        })
        logger.info(f"✓ 媒体中心: {result['status']}")

        return True
    except Exception as e:
        logger.error(f"✗ 娱乐模块测试失败: {e}")
        return False

def test_office_module():
    """测试办公模块"""
    logger.info("\n" + "="*60)
    logger.info("测试 AI 个人办公模块")
    logger.info("="*60)

    try:
        from modules.office.office_module import OfficeModule

        office = OfficeModule()

        # 测试文档处理
        result = office.process_request('document', {
            'action': 'summarize',
            'document_path': '/docs/report.pdf'
        })
        logger.info(f"✓ 文档摘要: {result['status']}")

        # 测试会议助手
        result = office.process_request('meeting', {
            'action': 'schedule',
            'title': '项目评审会',
            'participants': ['张三', '李四']
        })
        logger.info(f"✓ 会议安排: {result['status']}")

        # 测试邮件管理
        result = office.process_request('email', {
            'action': 'list',
            'filter': 'unread'
        })
        logger.info(f"✓ 邮件管理: {result['status']}")

        # 测试日程管理
        result = office.process_request('schedule', {
            'action': 'suggest',
            'tasks': ['完成报告', '团队会议', '代码审查']
        })
        logger.info(f"✓ 日程管理: {result['status']}")

        return True
    except Exception as e:
        logger.error(f"✗ 办公模块测试失败: {e}")
        return False

def test_shopping_module():
    """测试购物模块"""
    logger.info("\n" + "="*60)
    logger.info("测试 AI 生活购物模块")
    logger.info("="*60)

    try:
        from modules.shopping.shopping_module import ShoppingModule

        shopping = ShoppingModule()

        # 测试购物清单
        result = shopping.process_request('list', {
            'action': 'list'
        })
        logger.info(f"✓ 购物清单: {result['status']}")

        # 测试清单生成
        result = shopping.process_request('list', {
            'action': 'generate',
            'family_size': 4,
            'pattern': 'normal'
        })
        logger.info(f"✓ 智能生成清单: {result['status']}")

        # 测试价格比较
        result = shopping.process_request('compare', {
            'product_name': '牛奶'
        })
        logger.info(f"✓ 价格比较: {result['status']}")

        # 测试购物助手
        result = shopping.process_request('assistant', {
            'action': 'recommend',
            'category': '食品',
            'budget': 500
        })
        logger.info(f"✓ 商品推荐: {result['status']}")

        # 测试配送追踪
        result = shopping.process_request('delivery', {
            'action': 'track',
            'order_id': 'ORD123456'
        })
        logger.info(f"✓ 配送追踪: {result['status']}")

        return True
    except Exception as e:
        logger.error(f"✗ 购物模块测试失败: {e}")
        return False

def test_main_service():
    """测试主服务"""
    logger.info("\n" + "="*60)
    logger.info("测试 SmartHomeOS 主服务")
    logger.info("="*60)

    try:
        from core.services.smarthomeos_service import SmartHomeOSService

        # 创建主服务
        service = SmartHomeOSService()

        # 启动服务
        service.start()
        logger.info("✓ 服务启动成功")

        # 测试服务状态
        status = service.get_status()
        logger.info(f"✓ 服务状态: running={status['running']}")
        logger.info(f"  运行服务: {list(status['services'].keys())}")

        # 测试任务执行
        test_task = {
            'name': 'test_task',
            'capabilities': ['general'],
            'data': 'test data'
        }
        service.execute_task(test_task)
        logger.info("✓ 任务执行成功")

        # 停止服务
        service.stop()
        logger.info("✓ 服务停止成功")

        return True
    except Exception as e:
        logger.error(f"✗ 主服务测试失败: {e}")
        return False

def main():
    """主函数"""
    logger.info("="*60)
    logger.info("SmartHomeOS 综合测试开始")
    logger.info("="*60)

    # 测试各模块
    tests = [
        ("教育模块", test_education_module),
        ("娱乐模块", test_entertainment_module),
        ("办公模块", test_office_module),
        ("购物模块", test_shopping_module),
        ("主服务", test_main_service)
    ]

    results = []
    for test_name, test_func in tests:
        try:
            if test_func():
                results.append((test_name, "通过"))
            else:
                results.append((test_name, "失败"))
        except Exception as e:
            logger.error(f"测试 {test_name} 时发生异常: {e}")
            results.append((test_name, "异常"))

    # 打印测试结果
    logger.info("\n" + "="*60)
    logger.info("测试结果汇总")
    logger.info("="*60)

    for test_name, result in results:
        status_symbol = "✓" if result == "通过" else "✗"
        logger.info(f"{status_symbol} {test_name}: {result}")

    # 统计
    passed = sum(1 for _, r in results if r == "通过")
    total = len(results)

    logger.info("\n" + "="*60)
    logger.info(f"测试完成: {passed}/{total} 通过")
    logger.info("="*60)

    if passed == total:
        logger.info("🎉 所有测试通过！SmartHomeOS 系统运行正常")
    else:
        logger.warning("⚠ 部分测试失败，请检查日志")

if __name__ == "__main__":
    main()
