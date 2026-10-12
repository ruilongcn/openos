# SmartHomeOS 裸机安装使用指南

## 目录

1. [系统要求](#系统要求)
2. [准备工作](#准备工作)
3. [安装方法](#安装方法)
    - [方法一：从ISO镜像安装](#方法一从iso镜像安装)
    - [方法二：在现有Linux系统上安装](#方法二在现有linux系统上安装)
    - [方法三：使用WSL（Windows用户）](#方法三使用wslwindows用户)
4. [首次配置](#首次配置)
5. [功能使用](#功能使用)
6. [常见问题](#常见问题)

---

## 系统要求

### 最低配置

| 组件 | 规格 | 说明 |
|------|------|------|
| CPU | 1GHz双核处理器 | 支持x86_64架构 |
| 内存 | 512MB RAM | 建议1GB以获得更好体验 |
| 存储 | 8GB可用空间 | 建议16GB+ |
| 网络 | 100Mbps网卡 | 用于智能家居设备连接 |

### 推荐配置

| 组件 | 规格 | 说明 |
|------|------|------|
| CPU | 2GHz四核处理器 | 支持AI模型本地推理 |
| 内存 | 2GB RAM | 4GB+最佳 |
| 存储 | 32GB SSD | 提升系统响应速度 |
| 网络 | 千兆网卡 + WiFi6 | 流畅的智能设备连接 |

### 支持的硬件架构

- x86_64 (Intel/AMD 64位)
- ARM64 (树莓派4/5、OrangePi等)
- 虚拟机 (VirtualBox、VMware、QEMU)

---

## 准备工作

### 1. 下载SmartHomeOS

#### 获取最新版本

```bash
# 方式一：从GitHub下载
git clone https://github.com/smarthomeos/smarthomeos.git
cd smarthomeos

# 方式二：下载预构建ISO镜像
# 访问 https://github.com/smarthomeos/smarthomeos/releases
```

### 2. 准备安装介质

#### 使用Rufus（Windows）

1. 下载Rufus：https://rufus.ie/
2. 插入USB闪存盘（建议8GB+）
3. 打开Rufus
4. 选择下载的ISO镜像
5. 点击"开始"创建启动盘

#### 使用Etcher（跨平台）

1. 下载Etcher：https://etcher.io/
2. 选择ISO镜像
3. 选择USB设备
4. 点击"Flash"

#### 使用dd命令（Linux）

```bash
# 查找USB设备（注意确认设备号，避免误删数据！）
sudo fdisk -l

# 写入USB（假设设备是/dev/sdb）
sudo dd if=smarthomeos-1.0.0.iso of=/dev/sdb bs=4M status=progress

# 同步数据
sudo sync
```

### 3. 备份重要数据

⚠️ **重要警告**：安装前请备份所有重要数据！

---

## 安装方法

### 方法一：从ISO镜像安装

#### 步骤1：从USB启动

1. 将制作好的启动盘插入电脑
2. 开机并按F2/Del/F12等按键进入BIOS/UEFI
3. 调整启动顺序，将USB设为第一启动项
4. 保存重启

#### 步骤2：启动安装程序

1. 选择"Install SmartHomeOS"
2. 选择语言：简体中文
3. 选择时区：Asia/Shanghai

#### 步骤3：磁盘分区

**方式一：自动分区（推荐新手）**
- 选择"使用整个磁盘"
- 选择目标磁盘
- 点击"安装"

**方式二：手动分区**
- 创建 `/` 分区：至少8GB，ext4格式
- 创建 `/home` 分区：建议10GB+，ext4格式
- 创建交换分区（swap）：等于内存大小
- 点击"继续"

#### 步骤4：用户设置

1. 设置主机名：`smarthomeos`
2. 创建用户：
   - 用户名：`smarthome`
   - 密码：您的密码
3. 点击"继续"

#### 步骤5：完成安装

1. 等待安装完成（通常10-30分钟）
2. 点击"现在重启"
3. 拔出USB启动盘

---

### 方法二：在现有Linux系统上安装

#### 前提条件

- 已安装Debian 12 (Bookworm) 或 Ubuntu 22.04+
- 有sudo权限
- 网络连接正常

#### 步骤1：安装依赖

```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装基础软件
sudo apt install -y python3 python3-pip git

# 安装LXQt桌面环境
sudo apt install -y lxqt-core openbox

# 安装其他依赖
sudo apt install -y network-manager firewalld
```

#### 步骤2：获取SmartHomeOS

```bash
# 克隆仓库
cd ~
git clone https://github.com/smarthomeos/smarthomeos.git
cd smarthomeos
```

#### 步骤3：运行安装脚本

```bash
# 给安装脚本执行权限
chmod +x install.sh

# 运行安装脚本
sudo bash install.sh
```

#### 步骤4：启用服务

```bash
# 启用SmartHomeOS服务
sudo systemctl enable smarthomeos
sudo systemctl start smarthomeos

# 查看服务状态
sudo systemctl status smarthomeos
```

---

### 方法三：使用WSL（Windows用户）

#### 步骤1：启用WSL

1. 以管理员身份打开PowerShell
2. 运行：
```powershell
wsl --install
```
3. 重启电脑

#### 步骤2：安装Ubuntu 22.04

```powershell
# 安装Ubuntu 22.04
wsl --install Ubuntu-22.04

# 启动Ubuntu
wsl
```

#### 步骤3：在WSL中安装SmartHomeOS

```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 克隆仓库
cd ~
git clone https://github.com/smarthomeos/smarthomeos.git
cd smarthomeos

# 安装Python依赖
pip3 install -r requirements.txt

# 运行主服务
python3 core/services/smarthomeos_service.py
```

---

## 首次配置

### 1. 系统初始化向导

首次启动后会显示初始化向导：

```
============================================================
          欢迎使用 SmartHomeOS 智慧家庭系统
============================================================

1. 配置网络连接
2. 连接智能家居设备
3. 设置用户偏好
4. 完成初始化

正在启动服务...
```

### 2. 网络配置

#### 配置WiFi

```bash
# 使用NetworkManager配置WiFi
nmcli device wifi list
nmcli device wifi connect "您的WiFi名称" password "您的密码"

# 查看网络状态
ip addr
ping -c 3 8.8.8.8
```

#### 配置静态IP（可选）

```bash
# 编辑网络配置
sudo nmtui

# 或者手动编辑
sudo nano /etc/network/interfaces
```

### 3. 智能家居设备发现

#### 启动发现服务

```bash
# 设备发现（模拟）
python3 -c "
from integrations.homeassistant.home_assistant import SmartHomeControlPanel
ctrl = SmartHomeControlPanel()
devices = ctrl.ha.discover_devices()
print(f'发现 {len(devices)} 个设备')
"
```

#### 添加设备

1. 在桌面打开"智能家居控制中心"
2. 点击"发现设备"
3. 选择要添加的设备
4. 点击"添加"

### 4. 创建自动化场景

#### 预设场景

- **离家模式**：关闭所有灯光，关闭空调，锁定门锁
- **回家模式**：开启客厅灯，开启空调
- **睡眠模式**：关闭客厅灯，开启空调
- **影院模式**：关闭客厅灯

---

## 功能使用

### 1. AI教育学习模块

#### 作业辅导

1. 点击"教育学习"应用
2. 选择"作业辅导"
3. 上传作业照片（或使用摄像头拍照）
4. 等待AI生成解答

#### 学习计划

```bash
# 生成学习计划
python3 -c "
from modules.education.education_module import EducationModule
edu = EducationModule()
plan = edu.process_request('learning_plan', {
    'user_id': 'user001',
    'age': 15,
    'subjects': ['math', 'english', 'chinese']
})
print(plan)
"
```

### 2. AI影视娱乐模块

#### 智能推荐

1. 打开"影视娱乐"应用
2. 选择"心情推荐"
3. 选择当前心情：兴奋/放松/开心/难过
4. 查看推荐内容

#### 家庭影院

1. 选择要播放的视频
2. 点击"影院模式"
3. 智能设备会自动调整到影院模式

### 3. AI个人办公模块

#### 文档处理

```bash
# 文档摘要
python3 -c "
from modules.office.office_module import OfficeModule
office = OfficeModule()
result = office.process_request('document', {
    'action': 'summarize',
    'document_path': '/path/to/document.pdf'
})
print(result['summary'])
"
```

#### 会议助手

1. 点击"会议助手"
2. 选择"安排会议"
3. 填写会议信息
4. 系统自动发送会议邀请

### 4. AI生活购物模块

#### 智能清单

1. 打开"生活购物"应用
2. 点击"生成购物清单"
3. 输入家庭人数
4. 系统智能生成清单

#### 价格比较

```bash
# 比价示例
python3 -c "
from modules.shopping.shopping_module import ShoppingModule
shop = ShoppingModule()
result = shop.process_request('compare', {'product_name': '牛奶'})
print(f'最便宜: {result['cheapest']['store']} - ¥{result['cheapest']['price']}')
"
```

### 5. 智能家居控制

#### 设备控制界面

```
┌─────────────────────────────────────────────────────────────┐
│  🏠 智能家庭设备                             [场景] [设置]  │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │ 客厅灯   │  │主卧空调 │  │ 前门锁   │  │ 摄像头   │   │
│  │    🟢    │  │    🟢    │  │    🔴    │  │    🟢    │   │
│  │ [开]/[关]│  │ [开]/[关]│  │[锁]/[开] │  │ [开]/[关]│   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
├─────────────────────────────────────────────────────────────┤
│  [离家模式] [回家模式] [睡眠模式] [影院模式] [自定义场景]  │
└─────────────────────────────────────────────────────────────┘
```

---

## 日常使用

### 1. 系统更新

#### 检查更新

```bash
# 检查系统更新
sudo apt update

# 查看可更新的包
apt list --upgradable

# 应用更新
sudo apt upgrade -y
```

#### 更新SmartHomeOS

```bash
cd ~/smarthomeos

# 拉取最新代码
git pull origin main

# 安装新的依赖（如果有）
pip3 install -r requirements.txt --upgrade

# 重启服务
sudo systemctl restart smarthomeos
```

### 2. 备份与恢复

#### 备份配置

```bash
# 备份配置目录
sudo cp -r /etc/smarthomeos /var/backups/smarthomeos-config-$(date +%Y%m%d)

# 备份用户数据
cp -r ~/.smarthomeos /var/backups/smarthomeos-data-$(date +%Y%m%d)
```

#### 恢复配置

```bash
# 恢复配置
sudo cp -r /var/backups/smarthomeos-config-20260419 /etc/smarthomeos

# 恢复用户数据
cp -r /var/backups/smarthomeos-data-20260419 ~/.smarthomeos

# 重启服务
sudo systemctl restart smarthomeos
```

### 3. 日志查看

#### 系统日志

```bash
# 查看SmartHomeOS服务日志
sudo journalctl -u smarthomeos -f

# 查看系统日志
sudo journalctl -f
```

#### 应用日志

```bash
# 查看应用日志目录
ls -la ~/.smarthomeos/logs/

# 查看特定日志
tail -f ~/.smarthomeos/logs/smarthomeos-$(date +%Y%m%d).log
```

---

## 常见问题

### 1. 启动问题

#### 问题：服务无法启动

```bash
# 查看服务状态
sudo systemctl status smarthomeos

# 查看服务日志
sudo journalctl -u smarthomeos -n 50

# 重启服务
sudo systemctl restart smarthomeos
```

#### 问题：模块加载失败

```bash
# 检查Python依赖
pip3 list | grep -E 'langchain|transformers'

# 重新安装依赖
cd ~/smarthomeos
pip3 install -r requirements.txt
```

### 2. 网络问题

#### 问题：无法连接网络

```bash
# 检查网络连接
ip addr
ping -c 3 8.8.8.8

# 重启NetworkManager
sudo systemctl restart NetworkManager
```

#### 问题：智能家居设备离线

```bash
# 检查设备连接
ping -c 3 设备IP地址

# 重新发现设备
python3 -c "
from integrations.homeassistant.home_assistant import SmartHomeControlPanel
ctrl = SmartHomeControlPanel()
ctrl.ha.discover_devices()
"
```

### 3. 性能问题

#### 问题：系统响应缓慢

```bash
# 查看资源使用
htop

# 查看磁盘使用
df -h

# 清理缓存
sudo apt clean
```

#### 问题：内存不足

```bash
# 查看内存使用
free -h

# 如果内存不足，增加swap
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

### 4. AI模型问题

#### 问题：模型加载失败

```bash
# 检查模型目录
ls -la ~/.smarthomeos/models/

# 重新下载模型（如果有）
# 参考模型提供商文档
```

---

## 进阶配置

### 1. 启用远程访问

#### 配置SSH

```bash
# 启用SSH（默认已启用）
sudo systemctl enable ssh
sudo systemctl start ssh

# 查看IP地址
ip addr

# 从其他电脑连接
ssh smarthome@您的IP地址
```

#### 配置防火墙

```bash
# 允许SSH
sudo firewall-cmd --permanent --add-service=ssh

# 允许8123端口（Home Assistant）
sudo firewall-cmd --permanent --add-port=8123/tcp

# 重启防火墙
sudo firewall-cmd --reload
```

### 2. 配置安全更新

```bash
# 启用自动安全更新
sudo dpkg-reconfigure unattended-upgrades

# 配置自动更新
sudo nano /etc/apt/apt.conf.d/50unattended-upgrades
```

### 3. 数据备份

#### 配置自动备份

```bash
# 编辑crontab
sudo crontab -e

# 添加每日备份任务
0 2 * * * /opt/smarthomeos/scripts/backup.sh
```

---

## 获取帮助

### 1. 文档资源

- 项目主页：https://github.com/smarthomeos/smarthomeos
- 用户手册：https://smarthomeos.github.io/docs/
- 常见问题：https://smarthomeos.github.io/faq/

### 2. 社区支持

- GitHub Issues：https://github.com/smarthomeos/smarthomeos/issues
- 社区论坛：https://forum.smarthomeos.org/
- Discord频道：https://discord.gg/smarthomeos

### 3. 联系我们

- 邮箱：support@smarthomeos.org
- 网站：https://www.smarthomeos.org

---

## 附录

### A. 快捷命令参考

```bash
# 系统服务
sudo systemctl status smarthomeos
sudo systemctl start smarthomeos
sudo systemctl stop smarthomeos
sudo systemctl restart smarthomeos

# 日志查看
sudo journalctl -u smarthomeos -f

# 网络管理
nmcli device status
ping 8.8.8.8

# 系统信息
uname -a
cat /etc/debian_version
df -h
free -h
```

### B. 端口说明

| 端口 | 协议 | 用途 |
|------|------|------|
| 22 | TCP | SSH远程访问 |
| 80 | TCP | HTTP（如果启用Web界面） |
| 443 | TCP | HTTPS（如果启用Web界面） |
| 8123 | TCP | Home Assistant |
| 8000-9000 | TCP/UDP | 智能设备通信 |

### C. 目录结构

```
/opt/smarthomeos/              # 程序目录
├── core/                      # 核心系统
├── modules/                   # 功能模块
├── integrations/              # 第三方集成
└── scripts/                   # 脚本工具

/etc/smarthomeos/              # 配置目录
├── config.json                # 主配置文件
└── modules/                   # 模块配置

~/.smarthomeos/                # 用户目录
├── logs/                      # 日志目录
├── data/                      # 用户数据
└── cache/                     # 缓存目录

/var/log/smarthomeos/          # 系统日志目录
```

---

**版本**：1.0.0  
**最后更新**：2026-04-19  
**适用系统**：SmartHomeOS 1.x
