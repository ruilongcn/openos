# SmartHomeOS 构建配置

## 系统配置

### 基础系统
- **发行版**：Debian 12 (Bookworm)
- **架构**：amd64, arm64
- **内核**：Linux 6.1 LTS

### 桌面环境
- **桌面**：LXQt 1.4
- **显示管理器**：SDDM
- **窗口管理器**：Openbox

### 核心组件
- **AI框架**：LangChain, Llama 3
- **智能家居**：Home Assistant 2025.12
- **数据存储**：MongoDB 7.0, Redis 7.2
- **消息系统**：RabbitMQ 3.13, Celery 5.3.4

## 构建步骤

### 1. 安装构建依赖

```bash
sudo apt update
sudo apt install -y live-build
sudo apt install -y debootstrap squashfs-tools xorriso
```

### 2. 配置构建环境

```bash
# 进入构建目录
cd build/live-build

# 基础配置
lb config \
  --distribution bookworm \
  --architectures amd64 \
  --archive-areas "main contrib non-free" \
  --linux-flavours amd64 \
  --debootstrap-options "--variant=minbase" \
  --binary-images iso-hybrid \
  --bootappend-live "boot=live components hostname=smarthomeos username=smarthome"
```

### 3. 添加自定义包

在 `config/package-lists/` 目录创建 `smarthomeos.list.chroot` 文件：

```
# 基础系统
linux-image-amd64
live-boot
systemd-sysv

# 桌面环境
lxqt
lxqt-core
openbox
sddm

# 网络工具
network-manager
network-manager-gnome
wpasupplicant
ppp

# 系统工具
firewalld
fail2ban
apticron
timesyncd

# 多媒体
vlc
ffmpeg
gstreamer1.0

# Home Assistant依赖
python3
python3-venv
libffi-dev
libssl-dev

# AI依赖
python3-pip
python3-tensorflow
python3-pytorch

# 开发工具
git
build-essential

# 硬件支持
firmware-linux
firmware-linux-nonfree
```

### 4. 添加自定义脚本

在 `config/hooks/` 目录创建 `01-smarthomeos.hook.chroot` 文件：

```bash
#!/bin/sh

# 创建smarthome用户
useradd -m -s /bin/bash smarthome
echo "smarthome:smarthome" | chpasswd
usermod -aG sudo smarthome

# 创建必要的目录
mkdir -p /opt/smarthome/{homeassistant,control-panel,media-center,app-store,settings}

# 配置自动登录
echo "[Autologin]"
 echo "User=smarthome"
 echo "Session=LXQt"
 > /etc/sddm.conf.d/autologin.conf

# 启用服务
systemctl enable NetworkManager
systemctl enable sddm
systemctl enable firewalld

# 配置防火墙
firewall-cmd --permanent --add-service=ssh
firewall-cmd --permanent --add-service=http
firewall-cmd --permanent --add-service=https
firewall-cmd --reload
```

### 5. 构建镜像

```bash
# 构建镜像
lb build

# 构建完成后，镜像位于
binary.iso
```

## 测试镜像

### 虚拟机测试

```bash
# 使用QEMU测试
qemu-system-x86_64 -m 2048 -boot d -cdrom binary.iso -enable-kvm
```

### 物理机测试

1. 使用Rufus或Etcher制作启动盘
2. 从启动盘启动计算机
3. 测试系统功能

## 发布镜像

### 签名镜像

```bash
# 生成GPG密钥
# gpg --gen-key

# 签名镜像
# gpg --sign --detach-sign binary.iso
```

### 上传镜像

```bash
# 上传到服务器
# scp binary.iso* user@server:/path/to/mirror/
```

## 故障排除

### 构建失败

- 检查网络连接
- 检查磁盘空间
- 查看构建日志 `live-build.log`

### 启动失败

- 检查硬件兼容性
- 检查启动顺序
- 查看启动日志

## 版本管理

| 版本 | 日期 | 描述 |
|------|------|------|
| 1.0.0 | 2026-04-18 | 初始版本 |
| 1.0.1 | 2026-05-18 | 修复bug |
| 1.1.0 | 2026-06-18 | 功能更新 |
