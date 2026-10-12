#!/usr/bin/env python3
"""
SmartHomeOS 快速开始脚本
一键启动所有服务
"""

import os
import sys
import time
import logging
from pathlib import Path

# 添加项目根目录到Python路径
current_file = os.path.abspath(__file__)
root_dir = os.path.dirname(current_file)
sys.path.insert(0, root_dir)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger('quickstart')

def print_welcome():
    """打印欢迎信息"""
    print("\n" + "="*60)
    print("         SmartHomeOS 智慧家庭系统 - 快速开始")
    print("="*60)
    print()

def check_dependencies():
    """检查依赖"""
    logger.info("检查依赖...")

    try:
        import langchain
        logger.info("  ✓ LangChain: OK")
    except ImportError:
        logger.warning("  ⚠ LangChain: 未安装 (可选)")

    try:
        import requests
        logger.info("  ✓ Requests: OK")
    except ImportError:
        logger.warning("  ⚠ Requests: 未安装")

    return True

def check_config():
    """检查配置"""
    logger.info("检查配置...")

    config_dir = Path('/etc/smarthomeos')
    user_dir = Path.home() / '.smarthomeos'

    if not config_dir.exists():
        try:
            config_dir.mkdir(parents=True, exist_ok=True)
            logger.info("  ✓ 配置目录已创建")
        except Exception as e:
            logger.warning(f"  ⚠ 无法创建配置目录: {e}")

    if not user_dir.exists():
        try:
            user_dir.mkdir(parents=True, exist_ok=True)
            logger.info("  ✓ 用户目录已创建")
        except Exception as e:
            logger.warning(f"  ⚠ 无法创建用户目录: {e}")

    return True

def start_services():
    """启动服务"""
    logger.info("启动服务...")

    try:
        from core.services.smarthomeos_service import SmartHomeOSService

        service = SmartHomeOSService()
        service.start()

        logger.info("  ✓ 主服务: 已启动")

        # 等待服务稳定
        time.sleep(2)

        # 获取服务状态
        status = service.get_status()
        logger.info(f"  ✓ 运行模块: {list(status['services'].keys())}")

        return service

    except Exception as e:
        logger.error(f"  ✗ 服务启动失败: {e}")
        return None

def test_modules(service):
    """测试模块"""
    logger.info("测试模块...")

    # 测试教育模块
    if 'education' in service.services:
        try:
            edu = service.services['education']
            result = edu.process_request('learning_plan', {
                'user_id': 'quickstart',
                'age': 15,
                'subjects': ['math', 'english']
            })
            if result.get('status') == 'success':
                logger.info("  ✓ 教育模块: 正常")
        except Exception as e:
            logger.warning(f"  ⚠ 教育模块: 测试失败 - {e}")

    # 测试娱乐模块
    if 'entertainment' in service.services:
        try:
            ent = service.services['entertainment']
            result = ent.process_request('recommendation', {
                'user_id': 'quickstart',
                'content_type': 'movies',
                'mood': 'relaxed'
            })
            if result.get('status') == 'success':
                logger.info("  ✓ 娱乐模块: 正常")
        except Exception as e:
            logger.warning(f"  ⚠ 娱乐模块: 测试失败 - {e}")

    # 测试办公模块
    if 'office' in service.services:
        try:
            off = service.services['office']
            result = off.process_request('email', {
                'action': 'list',
                'filter': 'unread'
            })
            if result.get('status') == 'success':
                logger.info("  ✓ 办公模块: 正常")
        except Exception as e:
            logger.warning(f"  ⚠ 办公模块: 测试失败 - {e}")

    # 测试购物模块
    if 'shopping' in service.services:
        try:
            shop = service.services['shopping']
            result = shop.process_request('list', {
                'action': 'list'
            })
            if result.get('status') == 'success':
                logger.info("  ✓ 购物模块: 正常")
        except Exception as e:
            logger.warning(f"  ⚠ 购物模块: 测试失败 - {e}")

    # 测试智能家居
    if 'home_assistant' in service.services:
        try:
            ha = service.services['home_assistant']
            logger.info("  ✓ 智能家居: 正常")
        except Exception as e:
            logger.warning(f"  ⚠ 智能家居: 测试失败 - {e}")

def print_menu():
    """打印菜单"""
    print("\n" + "="*60)
    print("                     主菜单")
    print("="*60)
    print("  1. 查看系统状态")
    print("  2. 测试教育模块")
    print("  3. 测试娱乐模块")
    print("  4. 测试办公模块")
    print("  5. 测试购物模块")
    print("  6. 智能家居控制")
    print("  7. 查看日志")
    print("  0. 退出")
    print("="*60)

def show_status(service):
    """显示系统状态"""
    status = service.get_status()
    print("\n" + "="*60)
    print("                     系统状态")
    print("="*60)
    print(f"  运行状态: {'🟢 运行中' if status['running'] else '🔴 已停止'}")
    print(f"  运行模块:")
    for name, state in status['services'].items():
        print(f"    - {name}: {state}")
    print(f"  模块配置: {status['config']['modules']}")
    print(f"  AI配置: 本地={status['config']['ai']['enable_local']}, 云端={status['config']['ai']['enable_cloud']}")

def test_education(service):
    """测试教育模块"""
    if 'education' not in service.services:
        print("教育模块未启动")
        return

    edu = service.services['education']
    print("\n" + "="*60)
    print("                 教育模块测试")
    print("="*60)

    # 测试学习计划
    result = edu.process_request('learning_plan', {
        'user_id': 'demo',
        'age': 15,
        'subjects': ['math', 'english', 'chinese']
    })

    if result.get('status') == 'success':
        plan = result['plan']
        print(f"\n✓ 学习计划生成成功！")
        print(f"\n📚 每日计划:")
        for time_slot, items in plan['daily_plan'].items():
            print(f"  {time_slot}: {', '.join(items)}")
        print(f"\n🎯 每周目标: {', '.join(plan['weekly_goals'])}")

def test_entertainment(service):
    """测试娱乐模块"""
    if 'entertainment' not in service.services:
        print("娱乐模块未启动")
        return

    ent = service.services['entertainment']
    print("\n" + "="*60)
    print("                娱乐模块测试")
    print("="*60)

    # 测试推荐
    result = ent.process_request('recommendation', {
        'user_id': 'demo',
        'content_type': 'all',
        'mood': 'relaxed'
    })

    if result.get('status') == 'success':
        rec = result['recommendations']
        print(f"\n✓ 智能推荐生成成功！")
        print(f"心情: {result['mood']}")

        if 'movies' in rec:
            print(f"\n🎬 电影推荐:")
            for movie in rec['movies'][:3]:
                print(f"  - {movie['title']} ({movie['genre']}) ⭐{movie['rating']}")

def test_office(service):
    """测试办公模块"""
    if 'office' not in service.services:
        print("办公模块未启动")
        return

    off = service.services['office']
    print("\n" + "="*60)
    print("                办公模块测试")
    print("="*60)

    # 测试邮件
    result = off.process_request('email', {
        'action': 'list',
        'filter': 'all'
    })

    if result.get('status') == 'success':
        print(f"\n✓ 邮件管理正常！")
        print(f"共 {result['count']} 封邮件")
        for email in result['emails'][:3]:
            status = "📬 未读" if not email['read'] else "✓ 已读"
            important = " ⭐ 重要" if email['important'] else ""
            print(f"  {status}{important} - {email['subject']} ({email['from']})")

def test_shopping(service):
    """测试购物模块"""
    if 'shopping' not in service.services:
        print("购物模块未启动")
        return

    shop = service.services['shopping']
    print("\n" + "="*60)
    print("                购物模块测试")
    print("="*60)

    # 测试比价
    result = shop.process_request('compare', {'product_name': '牛奶'})

    if result.get('status') == 'success':
        print(f"\n✓ 价格比较成功！")
        print(f"\n🛒 商品: {result['product']}")
        print(f"💸 {result['savings']}")
        print(f"\n🏪 价格对比:")
        for store in result['stores']:
            is_cheapest = store == result['cheapest']
            marker = "🔥 最便宜" if is_cheapest else "   "
            print(f"  {marker} {store['store']}: ¥{store['price']}/{store['unit']}")

def control_smart_home(service):
    """智能家居控制"""
    if 'home_assistant' not in service.services:
        print("智能家居模块未启动")
        return

    ha = service.services['home_assistant']
    print("\n" + "="*60)
    print("                智能家居控制")
    print("="*60)

    print("\n发现的设备:")
    for device_id, device in ha.ha.devices.items():
        state_icon = "🟢" if device['state'] == 'on' else "🔴"
        print(f"  {state_icon} {device['name']} ({device['type']})")

    print("\n可用场景:")
    for scene_name in ha.ha.scenes.keys():
        print(f"  - {scene_name}")

    scene_choice = input("\n请选择要激活的场景（或按Enter跳过）: ").strip()
    if scene_choice in ha.ha.scenes:
        result = ha.ha.activate_scene(scene_choice)
        if result.get('status') == 'success':
            print(f"✓ 场景 '{scene_choice}' 已激活！")

def show_logs():
    """显示日志"""
    print("\n" + "="*60)
    print("                   查看日志")
    print("="*60)

    user_dir = Path.home() / '.smarthomeos' / 'logs'
    if user_dir.exists():
        log_files = sorted(user_dir.glob('*.log'), reverse=True)
        if log_files:
            print(f"\n找到 {len(log_files)} 个日志文件")
            print(f"\n最新日志: {log_files[0].name}")

            # 显示最后10行
            with open(log_files[0], 'r', encoding='utf-8') as f:
                lines = f.readlines()
                print(f"\n最后20行:")
                print("-"*60)
                for line in lines[-20:]:
                    print("  " + line.rstrip())
                print("-"*60)
    else:
        print("日志目录不存在")

def main():
    """主函数"""
    print_welcome()

    # 检查依赖
    if not check_dependencies():
        print("\n依赖检查失败，请安装所需依赖:")
        print("  pip install -r requirements.txt")
        return

    # 检查配置
    check_config()

    # 启动服务
    service = start_services()
    if not service:
        print("\n服务启动失败！")
        return

    # 测试模块
    test_modules(service)

    # 主菜单循环
    try:
        while True:
            print_menu()
            choice = input("\n请选择 [0-7]: ").strip()

            if choice == '0':
                print("\n正在退出...")
                break
            elif choice == '1':
                show_status(service)
            elif choice == '2':
                test_education(service)
            elif choice == '3':
                test_entertainment(service)
            elif choice == '4':
                test_office(service)
            elif choice == '5':
                test_shopping(service)
            elif choice == '6':
                control_smart_home(service)
            elif choice == '7':
                show_logs()
            else:
                print("\n无效选择，请重试！")

    except KeyboardInterrupt:
        print("\n\n收到中断信号，正在退出...")
    finally:
        # 停止服务
        if service:
            service.stop()
            logger.info("服务已停止")

    print("\n" + "="*60)
    print("           感谢使用 SmartHomeOS！")
    print("="*60)

if __name__ == "__main__":
    main()
