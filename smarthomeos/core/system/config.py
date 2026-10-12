#!/usr/bin/env python3
"""
SmartHomeOS 主配置文件
"""

import os
import json
from dataclasses import dataclass, field
from typing import Dict, List, Optional

@dataclass
class AIConfig:
    """AI配置"""
    models: Dict[str, str] = field(default_factory=lambda: {
        'llm': 'llama3:8b',
        'speech': 'whisper:v3',
        'vision': 'yolo:v8'
    })
    enable_local: bool = True
    enable_cloud: bool = False
    cloud_api_key: Optional[str] = None

@dataclass
class HomeAssistantConfig:
    """Home Assistant配置"""
    host: str = 'localhost'
    port: int = 8123
    token: Optional[str] = None
    ssl: bool = False
    enable: bool = True

@dataclass
class NetworkConfig:
    """网络配置"""
    hostname: str = 'smarthomeos'
    dhcp: bool = True
    static_ip: Optional[str] = None
    gateway: Optional[str] = None
    dns: List[str] = field(default_factory=lambda: ['8.8.8.8', '8.8.4.4'])

@dataclass
class SecurityConfig:
    """安全配置"""
    firewall: bool = True
    fail2ban: bool = True
    auto_update: bool = True
    enable_ssh: bool = True
    ssh_port: int = 22

@dataclass
class SmartHomeOSConfig:
    """SmartHomeOS配置"""
    ai: AIConfig = field(default_factory=AIConfig)
    home_assistant: HomeAssistantConfig = field(default_factory=HomeAssistantConfig)
    network: NetworkConfig = field(default_factory=NetworkConfig)
    security: SecurityConfig = field(default_factory=SecurityConfig)
    modules: Dict[str, bool] = field(default_factory=lambda: {
        'education': True,
        'entertainment': True,
        'office': True,
        'shopping': True,
        'agents': True,
        'openclaw': True
    })
    user: str = 'smarthome'
    timezone: str = 'Asia/Shanghai'
    language: str = 'zh_CN'

class ConfigManager:
    """配置管理器"""
    def __init__(self, config_dir: str = '/etc/smarthomeos'):
        self.config_dir = config_dir
        self.config_file = os.path.join(config_dir, 'config.json')
        self.config = self._load_config()
    
    def _load_config(self) -> SmartHomeOSConfig:
        """加载配置"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return SmartHomeOSConfig(**data)
            except Exception as e:
                print(f"Error loading config: {e}")
                return SmartHomeOSConfig()
        else:
            return SmartHomeOSConfig()
    
    def save_config(self) -> bool:
        """保存配置"""
        try:
            os.makedirs(self.config_dir, exist_ok=True)
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config.__dict__, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    def get_config(self) -> SmartHomeOSConfig:
        """获取配置"""
        return self.config
    
    def update_config(self, **kwargs) -> bool:
        """更新配置"""
        try:
            for key, value in kwargs.items():
                if hasattr(self.config, key):
                    setattr(self.config, key, value)
            return self.save_config()
        except Exception as e:
            print(f"Error updating config: {e}")
            return False

if __name__ == "__main__":
    # 测试配置管理器
    config_manager = ConfigManager()
    config = config_manager.get_config()
    
    print("Current config:")
    print(f"AI models: {config.ai.models}")
    print(f"Home Assistant: {config.home_assistant.host}:{config.home_assistant.port}")
    print(f"Network: {config.network.hostname}")
    print(f"Enabled modules: {[k for k, v in config.modules.items() if v]}")
    
    # 更新配置
    config_manager.update_config(
        user='homeuser',
        timezone='America/New_York'
    )
    
    print("\nUpdated config:")
    config = config_manager.get_config()
    print(f"User: {config.user}")
    print(f"Timezone: {config.timezone}")
