# SmartHomeOS - 智慧家庭桌面系统

<p align="center">
  <img src="https://img.shields.io/badge/version-1.0.0-blue.svg" alt="Version">
  <img src="https://img.shields.io/badge/license-GPLv3-green.svg" alt="License">
  <img src="https://img.shields.io/badge/python-3.8+-yellow.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/platform-Linux%20%7C%20WSL-lightgrey.svg" alt="Platform">
</p>

## 项目简介

SmartHomeOS 是一个基于开源Linux构建的轻量级智慧家庭桌面系统，专为家庭场景设计，深度集成AI能力，提供一站式智慧家庭解决方案。

### 核心特性

- 🤖 **多Agent AI系统**：类似OpenClaw的多Agent协作框架
- 📚 **AI教育学习**：智能作业辅导、个性化学习计划、语言学习助手
- 🎬 **AI影视娱乐**：智能内容推荐、AI字幕生成、家庭影院模式
- 💼 **AI个人办公**：智能文档处理、会议助手、邮件管理、日程规划
- 🛒 **AI生活购物**：智能购物清单、价格比较、优惠券助手
- 🏠 **智能家居集成**：深度集成Home Assistant，统一管理智能设备
- 🔒 **隐私优先**：本地优先计算，保护用户数据安全
- 🚀 **轻量高效**：基于Debian+LXQt，最低512MB RAM即可运行

## 快速开始

### 系统要求

| 组件 | 最低配置 | 推荐配置 |
|------|----------|----------|
| CPU | 1GHz双核 | 2GHz四核 |
| 内存 | 512MB RAM | 2GB+ RAM |
| 存储 | 8GB | 32GB+ SSD |
| 网络 | 100Mbps | 千兆网卡 + WiFi6 |

### 安装方法

#### 方法一：快速体验（WSL/Linux）

```bash
# 克隆项目
git clone https://github.com/smarthomeos/smarthomeos.git
cd smarthomeos

# 安装依赖
pip install -r requirements.txt

# 快速开始（推荐）
python quickstart.py

# 或者直接运行主服务
python core/services/smarthomeos_service.py
```

#### 方法二：从ISO镜像安装

详见 [安装指南](./INSTALL_GUIDE.md)

## 项目结构

```
smarthomeos/
├── core/                           # 核心系统
│   ├── services/                   # 核心服务
│   │   ├── smarthomeos_service.py # 主服务协调器
│   │   └── task_scheduler.py      # 多Agent任务调度器
│   └── system/                     # 系统基础
│       └── config.py               # 配置管理
│
├── modules/                        # 功能模块
│   ├── education/                  # AI教育学习模块
│   │   └── education_module.py     # 作业辅导、学习计划、语言学习
│   ├── entertainment/              # AI影视娱乐模块 ✨
│   │   └── entertainment_module.py # 智能推荐、字幕生成、媒体中心
│   ├── office/                     # AI个人办公模块 ✨
│   │   └── office_module.py        # 文档处理、会议助手、邮件管理
│   └── shopping/                   # AI生活购物模块 ✨
│       └── shopping_module.py      # 购物清单、价格比较、配送助手
│
├── integrations/                   # 第三方集成
│   └── homeassistant/              # 智能家居集成
│       └── home_assistant.py       # Home Assistant 集成
│
├── build/                          # 构建系统
│   └── live-build/                 # Live系统构建
│
├── scripts/                        # 脚本工具
│   └── smarthomeos.service         # Systemd 服务配置
│
├── install.sh                      # 安装脚本
├── requirements.txt                # Python依赖
├── quickstart.py                   # 快速开始脚本 ✨
├── test_all_modules.py             # 综合测试脚本 ✨
├── INSTALL_GUIDE.md                # 安装指南 ✨
├── CODE_ANALYSIS.md                # 代码分析报告
└── README.md                       # 本文件
```

## 功能模块详解

### 1. AI教育学习模块

| 功能 | 描述 |
|------|------|
| 📝 智能作业辅导 | 自动识别题目，生成解答步骤 |
| 📚 个性化学习计划 | 根据年龄、科目制定学习计划 |
| 🌍 语言学习助手 | 语音识别、口语训练、翻译 |

### 2. AI影视娱乐模块

| 功能 | 描述 |
|------|------|
| 🎬 智能内容推荐 | 根据心情和偏好推荐内容 |
| 📺 AI字幕生成 | 自动生成多语言字幕 |
| 🎵 家庭影院模式 | 智能设备联动，营造影院氛围 |

### 3. AI个人办公模块

| 功能 | 描述 |
|------|------|
| 📄 智能文档处理 | 文档摘要、翻译、自动生成 |
| 🎤 会议助手 | 语音转文字、智能纪要生成 |
| 📧 邮件管理 | 智能分类、自动回复 |
| 📅 日程管理 | 冲突检测、智能安排 |

### 4. AI生活购物模块

| 功能 | 描述 |
|------|------|
| 🛒 智能购物清单 | 根据消费模式生成清单 |
| 💰 价格比较 | 多平台实时比价 |
| 🎫 优惠券助手 | 自动查找和应用优惠券 |
| 🚚 配送追踪 | 实时追踪配送状态 |

### 5. 智能家居控制

| 功能 | 描述 |
|------|------|
| 🔌 设备发现 | 自动发现智能设备 |
| 🎭 场景模式 | 离家、回家、睡眠、影院等预设场景 |
| 🔗 多设备联动 | 自动化规则和场景联动 |

## 使用示例

### 快速开始

```bash
# 进入项目目录
cd smarthomeos

# 运行快速开始脚本（交互式菜单）
python quickstart.py
```

### 测试所有模块

```bash
# 运行综合测试
python test_all_modules.py
```

### 使用API方式调用

```python
from core.services.smarthomeos_service import SmartHomeOSService

# 创建服务实例
service = SmartHomeOSService()

# 启动服务
service.start()

# 使用教育模块
education = service.get_service('education')
plan = education.process_request('learning_plan', {
    'user_id': 'user001',
    'age': 15,
    'subjects': ['math', 'english']
})

# 使用娱乐模块
entertainment = service.get_service('entertainment')
recommend = entertainment.process_request('recommendation', {
    'user_id': 'user001',
    'mood': 'relaxed'
})

# 停止服务
service.stop()
```

## 技术架构

### 技术栈

| 层级 | 技术 |
|------|------|
| **系统基础** | Debian 12 (Bookworm) + Linux Kernel 6.1 |
| **桌面环境** | LXQt 1.4 (轻量高效) |
| **AI框架** | LangChain + 本地LLM (可选) |
| **智能家居** | Home Assistant 2025.12 |
| **数据存储** | SQLite + JSON配置 |
| **消息系统** | ThreadPoolExecutor + PriorityQueue |

### 设计模式

- **单例模式**：ConfigManager配置管理
- **工厂模式**：模块创建和管理
- **策略模式**：任务分配和评分
- **观察者模式**：服务状态监控

## 开发指南

### 环境搭建

```bash
# 克隆项目
git clone https://github.com/smarthomeos/smarthomeos.git
cd smarthomeos

# 安装依赖
pip install -r requirements.txt

# 运行测试
python test_all_modules.py
```

### 添加新模块

1. 在 `modules/` 下创建新模块目录
2. 继承基础助手类实现功能
3. 在主服务中注册模块
4. 添加测试用例

示例：
```python
# modules/newmodule/new_module.py
from abc import ABC, abstractmethod

class BaseNewAssistant(ABC):
    @abstractmethod
    def process(self, data):
        pass

class NewModule:
    def __init__(self):
        self.assistants = {
            'feature': MyAssistant()
        }

    def process_request(self, req_type, data):
        return self.assistants[req_type].process(data)
```

## 测试

### 运行所有测试

```bash
python test_all_modules.py
```

### 预期输出

```
============================================================
SmartHomeOS 综合测试开始
============================================================

============================================================
测试 AI 教育学习模块
============================================================
✓ 作业辅导: success
✓ 学习计划: success
✓ 语言学习: success

...

============================================================
测试结果汇总
============================================================
✓ 教育模块: 通过
✓ 娱乐模块: 通过
✓ 办公模块: 通过
✓ 购物模块: 通过
✓ 主服务: 通过

============================================================
测试完成: 5/5 通过
============================================================
🎉 所有测试通过！SmartHomeOS 系统运行正常
```

## 文档

- 📖 [安装指南](./INSTALL_GUIDE.md) - 详细的裸机安装说明
- 🔍 [代码分析](./CODE_ANALYSIS.md) - 完整的代码结构分析
- 📚 [智慧家庭设计方案](./../家庭智慧桌面系统技术基座方案.md) - 技术方案文档
- 📖 [开源操作系统研究](./../开源操作系统项目深度研究报告.md) - 项目研究报告

## 相关项目

- [操作系统用户检测系统](./../os-user-detection/) - 开源OS用户信息收集系统
- [Home Assistant](https://www.home-assistant.io/) - 开源智能家居平台
- [OpenClaw](https://github.com/) - 多Agent协作框架（参考）

## 贡献指南

我们欢迎社区贡献！请参考以下步骤：

1. Fork本仓库
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建Pull Request

## 许可证

本项目采用 GPLv3 许可证 - 详见 [LICENSE](LICENSE) 文件

## 致谢

- 感谢 [Debian](https://www.debian.org/) 提供的稳定基础系统
- 感谢 [Home Assistant](https://www.home-assistant.io/) 智能家居平台
- 感谢 [LXQt](https://lxqt-project.org/) 轻量桌面环境
- 感谢所有贡献者和支持者！

## 联系方式

- 🏠 项目主页：https://github.com/smarthomeos/smarthomeos
- 📧 邮箱：info@smarthomeos.org
- 🌐 社区论坛：https://forum.smarthomeos.org

---

<p align="center">
  <b>Made with ❤️ for Smart Home</b>
</p>

---

## Star History

如果这个项目对您有帮助，请给我们一个⭐ Star！

---

## 更新日志

### v1.0.0 (2026-04-19)

- ✨ 新增 AI影视娱乐模块
- ✨ 新增 AI个人办公模块
- ✨ 新增 AI生活购物模块
- ✨ 新增 快速开始交互式脚本
- ✨ 新增 综合测试脚本
- ✨ 新增 详细安装指南
- ✨ 新增 代码分析报告
- 🔧 优化 主服务模块加载逻辑
- 🔧 优化 任务调度器
- 📝 完善 项目文档

### v0.9.0 (2026-04-18)

- 🎉 初始版本发布
- 🤖 多Agent任务调度系统
- 📚 AI教育学习模块
- 🏠 智能家居集成
- 📝 基础文档和安装脚本
