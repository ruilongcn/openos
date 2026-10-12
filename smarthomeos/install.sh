#!/bin/bash
"""
SmartHomeOS 安装脚本
"""

set -e

echo "================================"
echo "SmartHomeOS 安装脚本"
echo "================================"

# 检查是否以root权限运行
if [ "$(id -u)" != "0" ]; then
    echo "错误: 请以root权限运行此脚本"
    exit 1
fi

# 检查磁盘空间
echo "检查磁盘空间..."
if [ "$(df -m / | tail -n 1 | awk '{print $4}')" -lt 10240 ]; then
    echo "错误: 至少需要10GB可用空间"
    exit 1
fi

# 安装依赖
echo "安装系统依赖..."
apt update && apt install -y \
    python3 python3-pip python3-venv \
    git build-essential \
    lxqt-core sddm openbox \
    network-manager network-manager-gnome \
    firewalld fail2ban \
    vlc ffmpeg gstreamer1.0 \
    firmware-linux firmware-linux-nonfree

# 创建smarthome用户
echo "创建smarthome用户..."
if ! id -u smarthome >/dev/null 2>&1; then
    useradd -m -s /bin/bash smarthome
    echo "smarthome:smarthome" | chpasswd
    usermod -aG sudo smarthome
fi

# 创建安装目录
echo "创建安装目录..."
mkdir -p /opt/smarthomeos
chown -R smarthome:smarthome /opt/smarthomeos

# 复制文件
echo "复制SmartHomeOS文件..."
cp -r ./* /opt/smarthomeos/
chown -R smarthome:smarthome /opt/smarthomeos

# 安装Python依赖
echo "安装Python依赖..."
cd /opt/smarthomeos
pip3 install -r requirements.txt

# 配置服务
echo "配置系统服务..."
cp scripts/smarthomeos.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable smarthomeos.service
systemctl start smarthomeos.service

# 配置防火墙
echo "配置防火墙..."
systemctl enable firewalld
systemctl start firewalld
firewall-cmd --permanent --add-service=ssh
firewall-cmd --permanent --add-service=http
firewall-cmd --permanent --add-service=https
firewall-cmd --reload

# 配置自动登录
echo "配置自动登录..."
mkdir -p /etc/sddm.conf.d
echo "[Autologin]\nUser=smarthome\nSession=LXQt" > /etc/sddm.conf.d/autologin.conf

# 配置网络
echo "配置网络..."
systemctl enable NetworkManager
systemctl start NetworkManager

# 清理
echo "清理安装文件..."
apt clean

# 完成
echo "================================"
echo "SmartHomeOS 安装完成!"
echo "================================"
echo "系统将在30秒后重启..."
sleep 30
reboot
