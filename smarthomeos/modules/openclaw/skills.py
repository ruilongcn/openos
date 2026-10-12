#!/usr/bin/env python3
"""
SmartHomeOS OpenClaw - Skills（技能）系统
内置技能和技能管理
"""

import os
import sys
import logging
import time
import math
import random
from typing import Dict, List, Optional, Any
from pathlib import Path

# 添加项目根目录到Python路径
current_file = os.path.abspath(__file__)
core_dir = os.path.dirname(current_file)
root_dir = os.path.dirname(core_dir)
sys.path.insert(0, root_dir)

from .core import BaseSkill, logger


class CalculatorSkill(BaseSkill):
    """计算器技能"""
    name: str = "calculator"
    description: str = "Perform basic arithmetic calculations"

    def execute(self, input_data: Dict) -> Dict:
        """执行计算"""
        try:
            expression = input_data.get('expression', '')
            if not expression:
                return {
                    'status': 'error',
                    'message': 'No expression provided'
                }

            # 安全计算（简化版）
            allowed_chars = set('0123456789+-*/().^ ')
            if not all(c in allowed_chars for c in expression):
                return {
                    'status': 'error',
                    'message': 'Invalid characters in expression'
                }

            # 安全评估
            result = eval(expression, {'__builtins__': {}})

            return {
                'status': 'success',
                'expression': expression,
                'result': result
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Calculation error: {e}'
            }


class WebSearchSkill(BaseSkill):
    """网页搜索技能（模拟）"""
    name: str = "web_search"
    description: str = "Search the web for information"

    def execute(self, input_data: Dict) -> Dict:
        """执行搜索"""
        try:
            query = input_data.get('query', '')
            if not query:
                return {
                    'status': 'error',
                    'message': 'No query provided'
                }

            # 模拟搜索结果
            results = [
                {
                    'title': f"Search result 1 for: {query}",
                    'url': "https://example.com/result1",
                    'snippet': "This is a simulated search result for demonstration purposes."
                },
                {
                    'title': f"Search result 2 for: {query}",
                    'url': "https://example.com/result2",
                    'snippet': "Another simulated result showing how search skills work."
                },
                {
                    'title': f"Search result 3 for: {query}",
                    'url': "https://example.com/result3",
                    'snippet': "Additional search result with relevant information."
                }
            ]

            return {
                'status': 'success',
                'query': query,
                'results': results,
                'total_results': len(results)
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Search error: {e}'
            }


class FileSystemSkill(BaseSkill):
    """文件系统操作技能"""
    name: str = "file_system"
    description: str = "Read, write, and manage files"

    def execute(self, input_data: Dict) -> Dict:
        """执行文件操作"""
        try:
            action = input_data.get('action', 'read')
            file_path = input_data.get('file_path', '')
            content = input_data.get('content', '')

            if action == 'read':
                if not os.path.exists(file_path):
                    return {
                        'status': 'error',
                        'message': f'File not found: {file_path}'
                    }
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                return {
                    'status': 'success',
                    'action': 'read',
                    'file_path': file_path,
                    'content': content
                }

            elif action == 'write':
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                return {
                    'status': 'success',
                    'action': 'write',
                    'file_path': file_path,
                    'bytes_written': len(content)
                }

            elif action == 'list':
                if not os.path.exists(file_path):
                    return {
                        'status': 'error',
                        'message': f'Directory not found: {file_path}'
                    }
                files = os.listdir(file_path)
                return {
                    'status': 'success',
                    'action': 'list',
                    'directory': file_path,
                    'files': files
                }

            else:
                return {
                    'status': 'error',
                    'message': f'Unknown action: {action}'
                }

        except Exception as e:
            return {
                'status': 'error',
                'message': f'File system error: {e}'
            }


class WeatherSkill(BaseSkill):
    """天气查询技能（模拟）"""
    name: str = "weather"
    description: str = "Get weather information for a location"

    def execute(self, input_data: Dict) -> Dict:
        """查询天气"""
        try:
            location = input_data.get('location', 'Beijing')

            # 模拟天气数据
            conditions = ['Sunny', 'Cloudy', 'Rainy', 'Partly Cloudy', 'Clear']
            condition = random.choice(conditions)
            temp = random.randint(15, 30)
            humidity = random.randint(40, 80)
            wind_speed = random.randint(5, 25)

            return {
                'status': 'success',
                'location': location,
                'weather': {
                    'condition': condition,
                    'temperature': temp,
                    'temperature_unit': 'C',
                    'humidity': humidity,
                    'humidity_unit': '%',
                    'wind_speed': wind_speed,
                    'wind_speed_unit': 'km/h'
                },
                'last_updated': time.strftime('%Y-%m-%d %H:%M:%S')
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Weather error: {e}'
            }


class HomeControlSkill(BaseSkill):
    """家庭控制技能"""
    name: str = "home_control"
    description: str = "Control smart home devices"

    def __init__(self):
        super().__init__()
        self.device_states = {
            'light_living_room': 'off',
            'light_bedroom': 'off',
            'ac_living_room': 'off',
            'lock_front_door': 'locked',
            'tv_living_room': 'off'
        }

    def execute(self, input_data: Dict) -> Dict:
        """执行家庭控制"""
        try:
            action = input_data.get('action', '')
            device = input_data.get('device', '')

            if action == 'list_devices':
                return {
                    'status': 'success',
                    'devices': list(self.device_states.keys())
                }

            elif action == 'get_state':
                if device not in self.device_states:
                    return {
                        'status': 'error',
                        'message': f'Device not found: {device}'
                    }
                return {
                    'status': 'success',
                    'device': device,
                    'state': self.device_states[device]
                }

            elif action == 'set_state':
                if device not in self.device_states:
                    return {
                        'status': 'error',
                        'message': f'Device not found: {device}'
                    }
                state = input_data.get('state', 'off')
                self.device_states[device] = state
                return {
                    'status': 'success',
                    'device': device,
                    'state': state,
                    'message': f'{device} set to {state}'
                }

            elif action == 'turn_on':
                if device not in self.device_states:
                    return {
                        'status': 'error',
                        'message': f'Device not found: {device}'
                    }
                self.device_states[device] = 'on'
                return {
                    'status': 'success',
                    'device': device,
                    'state': 'on',
                    'message': f'{device} turned on'
                }

            elif action == 'turn_off':
                if device not in self.device_states:
                    return {
                        'status': 'error',
                        'message': f'Device not found: {device}'
                    }
                self.device_states[device] = 'off'
                return {
                    'status': 'success',
                    'device': device,
                    'state': 'off',
                    'message': f'{device} turned off'
                }

            elif action == 'activate_scene':
                scene = input_data.get('scene', '')
                result = self._activate_scene(scene)
                return {
                    'status': 'success',
                    'scene': scene,
                    'result': result
                }

            else:
                return {
                    'status': 'error',
                    'message': f'Unknown action: {action}'
                }

        except Exception as e:
            return {
                'status': 'error',
                'message': f'Home control error: {e}'
            }

    def _activate_scene(self, scene: str) -> Dict:
        """激活场景"""
        scene_actions = {
            'home': {
                'light_living_room': 'on',
                'ac_living_room': 'on'
            },
            'away': {
                'light_living_room': 'off',
                'light_bedroom': 'off',
                'ac_living_room': 'off',
                'tv_living_room': 'off',
                'lock_front_door': 'locked'
            },
            'sleep': {
                'light_living_room': 'off',
                'light_bedroom': 'on',
                'ac_living_room': 'on'
            },
            'movie': {
                'light_living_room': 'dim',
                'tv_living_room': 'on'
            }
        }

        if scene not in scene_actions:
            return {'message': f'Unknown scene: {scene}'}

        actions = scene_actions[scene]
        for device, state in actions.items():
            if device in self.device_states:
                self.device_states[device] = state

        return {
            'message': f'Scene {scene} activated',
            'devices_affected': list(actions.keys())
        }


class NewsSkill(BaseSkill):
    """新闻查询技能（模拟）"""
    name: str = "news"
    description: str = "Get latest news on various topics"

    def execute(self, input_data: Dict) -> Dict:
        """查询新闻"""
        try:
            topic = input_data.get('topic', 'general')
            limit = input_data.get('limit', 5)

            # 模拟新闻
            news = [
                {
                    'title': f"Top {topic} news 1",
                    'source': "NewsSource",
                    'published_at': time.strftime('%Y-%m-%d %H:%M:%S'),
                    'snippet': "Breaking news about this topic that you might find interesting."
                },
                {
                    'title': f"Top {topic} news 2",
                    'source': "DailyNews",
                    'published_at': time.strftime('%Y-%m-%d %H:%M:%S'),
                    'snippet': "Another important development in this area."
                },
                {
                    'title': f"Top {topic} news 3",
                    'source': "TechToday",
                    'published_at': time.strftime('%Y-%m-%d %H:%M:%S'),
                    'snippet': "Interesting trends and analysis in this field."
                }
            ]

            return {
                'status': 'success',
                'topic': topic,
                'news': news[:limit],
                'total_articles': len(news)
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'News error: {e}'
            }


class ReminderSkill(BaseSkill):
    """提醒功能技能"""
    name: str = "reminder"
    description: str = "Set and manage reminders"

    def __init__(self):
        super().__init__()
        self.reminders = []

    def execute(self, input_data: Dict) -> Dict:
        """执行提醒操作"""
        try:
            action = input_data.get('action', '')

            if action == 'set':
                reminder = {
                    'id': len(self.reminders) + 1,
                    'message': input_data.get('message', ''),
                    'time': input_data.get('time', time.time()),
                    'created_at': time.time()
                }
                self.reminders.append(reminder)
                return {
                    'status': 'success',
                    'action': 'set',
                    'reminder': reminder
                }

            elif action == 'list':
                return {
                    'status': 'success',
                    'action': 'list',
                    'reminders': self.reminders
                }

            elif action == 'delete':
                reminder_id = input_data.get('id', 0)
                self.reminders = [r for r in self.reminders if r['id'] != reminder_id]
                return {
                    'status': 'success',
                    'action': 'delete',
                    'deleted_id': reminder_id
                }

            else:
                return {
                    'status': 'error',
                    'message': f'Unknown action: {action}'
                }

        except Exception as e:
            return {
                'status': 'error',
                'message': f'Reminder error: {e}'
            }


class SkillRegistry:
    """技能注册表"""

    def __init__(self):
        self.skills: Dict[str, BaseSkill] = {}
        self._register_default_skills()

    def _register_default_skills(self):
        """注册默认技能"""
        default_skills = [
            CalculatorSkill(),
            WebSearchSkill(),
            FileSystemSkill(),
            WeatherSkill(),
            HomeControlSkill(),
            NewsSkill(),
            ReminderSkill()
        ]

        for skill in default_skills:
            self.register_skill(skill)
        logger.info(f"Registered {len(default_skills)} default skills")

    def register_skill(self, skill: BaseSkill):
        """注册技能"""
        self.skills[skill.name] = skill
        logger.info(f"Registered skill: {skill.name}")

    def get_skill(self, name: str) -> Optional[BaseSkill]:
        """获取技能"""
        return self.skills.get(name)

    def list_skills(self) -> List[Dict]:
        """列出所有技能"""
        return [skill.get_metadata() for skill in self.skills.values()]

    def execute_skill(self, name: str, input_data: Dict) -> Dict:
        """执行技能"""
        if name not in self.skills:
            return {
                'status': 'error',
                'message': f'Skill not found: {name}'
            }

        skill = self.skills[name]
        logger.info(f"Executing skill: {name}")
        return skill.execute(input_data)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    print("=== OpenClaw Skills Test ===")

    registry = SkillRegistry()

    print(f"\nAvailable skills: {[s['name'] for s in registry.list_skills()]}")

    # 测试计算器
    print("\n--- Testing Calculator ---")
    calc_result = registry.execute_skill("calculator", {'expression': "2 + 2 * 3"})
    print(calc_result)

    # 测试天气
    print("\n--- Testing Weather ---")
    weather_result = registry.execute_skill("weather", {'location': "Beijing"})
    print(weather_result)

    # 测试家庭控制
    print("\n--- Testing Home Control ---")
    list_result = registry.execute_skill("home_control", {'action': 'list_devices'})
    print(list_result)

    scene_result = registry.execute_skill("home_control", {'action': 'activate_scene', 'scene': 'home'})
    print(scene_result)

    print("\n=== Test Complete ===")
