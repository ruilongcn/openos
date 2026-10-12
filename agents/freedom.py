# -*- coding: utf-8 -*-
"""反捆绑与用户自主选择 Agent：去中心化应用商店、无强制预装、软硬件自由组合。

能力：
- 去中心化应用商店设计（多源镜像/签名验证/无抽成中心）；
- 反强制预装治理（预装清单审查、一键卸载、黑名单）；
- 软硬件自由组合方案（OS ↔ 硬件 ↔ 指令集 ↔ 固件）；
- 输出 data/freedom/freedom_*.json 契约。
"""
from __future__ import annotations

import time
from typing import Any, Dict

from .base_agent import BaseAgent


class FreedomAgent(BaseAgent):
    name = "freedom"
    description = "反捆绑与用户自主选择：去中心化应用商店、无强制预装、软硬件自由组合"

    def run(self, task: Dict[str, Any]) -> Dict[str, Any]:
        action = task.get("action", "store")
        if action == "preinstall":
            return self._preinstall(task)
        if action == "combo":
            return self._combo(task)
        return self._store(task)

    def _store(self, task: Dict[str, Any]) -> Dict[str, Any]:
        payload = {
            "decentralized_store": {
                "model": "多源应用仓库（官方源 + 社区源 + 私有源），无单一中心抽成",
                "signing": "应用包签名校验（开发者公钥），支持用户自定义信任源",
                "permission": "安装前展示权限/来源/签名，用户显式确认",
                "no_lockin": "应用包格式开放（.cnap 自主格式 + 兼容 .deb/.apk 类格式）",
                "anti_monopoly": "仓库间自由迁移，应用数据可导出",
            },
            "anti_cutting": ["无竞价排名", "无预装返利", "无强制更新", "无全家桶捆绑安装"],
            "generated_at": int(time.time()),
        }
        path = self._write_contract("freedom", f"store_{int(time.time())}.json", payload)
        payload["contract_path"] = str(path)
        return {"status": "ok", **payload}

    def _preinstall(self, task: Dict[str, Any]) -> Dict[str, Any]:
        payload = {
            "preinstall_policy": {
                "default": "出厂零预装（或仅系统必需组件）",
                "audit": "预装清单必须公开可审计，逐项可卸载",
                "one_key_clean": "一键卸载全部预装非系统应用",
                "blacklist": "黑名单应用禁止静默安装",
            },
            "user_rights": ["选择默认浏览器/输入法/商店", "选择是否启用云服务", "自由更换桌面环境"],
            "generated_at": int(time.time()),
        }
        path = self._write_contract("freedom", f"preinstall_{int(time.time())}.json", payload)
        payload["contract_path"] = str(path)
        return {"status": "ok", **payload}

    def _combo(self, task: Dict[str, Any]) -> Dict[str, Any]:
        os_name = task.get("os_name", "CNOS")
        combo = {
            "os": os_name,
            "combo_options": [
                {"hardware": "自主指令集芯片（配合 chip design robot）", "firmware": "自主 BIOS/UEFI（配合 openbios）", "note": "全自主链路"},
                {"hardware": "RISC-V 开放硬件", "firmware": "coreboot/OpenFirmware 自主构建", "note": "开放生态链路"},
                {"hardware": "既有 x86/ARM 硬件", "firmware": "兼容引导（Secure Boot 用户密钥）", "note": "兼容迁移链路"},
            ],
            "principle": "用户自由组合操作系统与硬件，不被任何厂商锁定",
            "generated_at": int(time.time()),
        }
        path = self._write_contract("freedom", f"combo_{int(time.time())}.json", payload)
        combo["contract_path"] = str(path)
        return {"status": "ok", **combo}
