# -*- coding: utf-8 -*-
"""Agent 基类：所有操作系统智能体的公共抽象。"""
from __future__ import annotations

import json
import logging
import time
import uuid
from pathlib import Path
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


class BaseAgent:
    name: str = "base"
    description: str = ""

    def __init__(self, config: Optional[Dict[str, Any]] = None, data_dir: Optional[Path] = None):
        self.agent_id = f"{self.name}_{uuid.uuid4().hex[:8]}"
        self.config = config or {}
        self.data_dir = Path(data_dir) if data_dir else Path("data")
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def _write_contract(self, sub_dir: str, filename: str, payload: Dict[str, Any]) -> Path:
        target_dir = self.data_dir / sub_dir
        target_dir.mkdir(parents=True, exist_ok=True)
        path = target_dir / filename
        payload.setdefault("_meta", {})
        payload["_meta"].update({"agent": self.name, "agent_id": self.agent_id, "ts": int(time.time())})
        with open(path, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        logger.info("[%s] 契约已写入: %s", self.name, path)
        return path

    def run(self, task: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError

    def llm(self, gateway, prompt: str, **kwargs) -> str:
        return gateway.chat(prompt, **kwargs)
