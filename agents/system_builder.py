# -*- coding: utf-8 -*-
"""系统构建与裁剪 Agent：构建配置、组件裁剪、最小系统/定制镜像。

能力：
- 生成系统构建配置（内核配置/组件列表/根文件系统）；
- 按场景裁剪组件（桌面/服务器/移动/嵌入式）；
- 输出 data/build/build_*.json 契约。
"""
from __future__ import annotations

import time
from typing import Any, Dict

from .base_agent import BaseAgent

PROFILES = {
    "desktop": {"components": ["图形栈(DRM/Wayland)", "桌面环境", "办公/浏览器", "多媒体"], "size_note": "完整桌面体验"},
    "server": {"components": ["内核+网络栈", "容器运行时", "数据库/中间件", "运维工具"], "size_note": "无图形，精简稳定"},
    "mobile": {"components": ["内核(移动电源管理)", "图形栈", "应用框架", "调制解调器驱动"], "size_note": "低功耗、触控"},
    "embedded": {"components": ["裁剪内核", "最小 init", "单应用运行时"], "size_note": "最小可启动镜像"},
}


class SystemBuilderAgent(BaseAgent):
    name = "system_builder"
    description = "系统构建与裁剪：内核配置、组件裁剪、按场景生成最小/定制系统方案"

    def run(self, task: Dict[str, Any]) -> Dict[str, Any]:
        action = task.get("action", "profile")
        if action == "kernelconfig":
            return self._kernelconfig(task)
        return self._profile(task)

    def _profile(self, task: Dict[str, Any]) -> Dict[str, Any]:
        profile = task.get("profile", "desktop")
        cfg = PROFILES.get(profile, PROFILES["desktop"])
        payload = {
            "profile": profile,
            "components": cfg["components"],
            "notes": cfg["size_note"],
            "build_pipeline": [
                "获取内核源码（自主分支）",
                "按 profile 生成 .config",
                "交叉编译内核 + 模块",
                "构建根文件系统（busybox/systemd 自主版）",
                "打包镜像（initramfs/disk image）",
                "签名与校验（配合 openbios Secure Boot）",
            ],
            "trimming_strategy": ["关闭未用子系统", "模块化加载", "移除调试符号", "按需固件/驱动"],
            "generated_at": int(time.time()),
        }
        path = self._write_contract("build", f"profile_{int(time.time())}.json", payload)
        payload["contract_path"] = str(path)
        return {"status": "ok", **payload}

    def _kernelconfig(self, task: Dict[str, Any]) -> Dict[str, Any]:
        payload = {
            "kernel_config_sections": {
                "arch": "riscv64 / loongarch64 / arm64 / x86_64 可选",
                "scheduler": "CFS + RT 组调度",
                "memory": "大页、cgroup、zram",
                "fs": "自主 FS + ext4 兼容 + FUSE",
                "net": "TCP/IP 栈、wireguard 类加密隧道可选",
                "security": "LSM、SELinux 类强制访问、模块签名",
                "ai": "AI 子系统钩子（NPU 驱动接口）",
            },
            "auto_tune": "按 profile 推荐开关组合，用户可逐项覆盖",
            "generated_at": int(time.time()),
        }
        path = self._write_contract("build", f"kconfig_{int(time.time())}.json", payload)
        payload["contract_path"] = str(path)
        return {"status": "ok", **payload}
