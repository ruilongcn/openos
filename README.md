---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: d32db8dd5a6f99a1df3565db906abe3a_ca2381d9c07211f18019525400248c00
    ReservedCode1: kQhviDxLN8dUsFg0BNC0+jl1PYx+PqKiiiazz4Mubi6iwZeo4+qyoZSHasm/Zd6Moa0roH5u/TzwgUSR6QJEyNYyC8zcq4jaWiglKWHYGcAJ25p9eoMbWIzTa2sB5Nt6kPPlNEHQSCUgC/oqNEteBDcUencjIvQ11kmnCu2QdlDPUsWl0ZuPo4oo3Z4=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: d32db8dd5a6f99a1df3565db906abe3a_ca2381d9c07211f18019525400248c00
    ReservedCode2: kQhviDxLN8dUsFg0BNC0+jl1PYx+PqKiiiazz4Mubi6iwZeo4+qyoZSHasm/Zd6Moa0roH5u/TzwgUSR6QJEyNYyC8zcq4jaWiglKWHYGcAJ25p9eoMbWIzTa2sB5Nt6kPPlNEHQSCUgC/oqNEteBDcUencjIvQ11kmnCu2QdlDPUsWl0ZuPo4oo3Z4=
---

# 操作系统与 AI 操作系统智能体团队（OpenOS Agent Team）

面向自主可控操作系统与 AI 操作系统研发的网页版专业智能体团队软件。覆盖内核/驱动/文件系统/调度/内存管理、系统构建与裁剪、AI 操作系统（系统级智能体、AI 原生交互、智能资源调度）、反捆绑与用户自主选择。

## 技术栈

- **后端**：FastAPI + Uvicorn（Python 3.11+）
- **多智能体流水线**：Orchestrator 意图解析 → 路由 Agent → JSON 契约落盘（data/）
- **前端**：原生 HTML + CSS + JavaScript（零构建、零依赖）
- **LLM 网关**：云端优先，失败自动降级本地 Ollama（纯规则引擎不依赖 LLM 也可运行）

## 智能体团队

| Agent | 职责 |
|---|---|
| kernel_engineer | 内核工程师：内核架构、调度、内存管理、文件系统、驱动框架设计 |
| system_builder | 系统构建与裁剪：按场景生成最小/定制系统方案、内核配置建议 |
| ai_os | AI 操作系统：系统级智能体框架、AI 原生交互、智能资源调度 |
| freedom | 反捆绑与用户自主选择：去中心化应用商店、零预装治理、软硬件自由组合 |

## 快速启动

### 方式一：双击脚本（Windows）

```bat
scripts\start.bat
```

### 方式二：命令行

```powershell
cd F:\openos
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python scripts\start_backend.py
```

启动后浏览器访问：<http://127.0.0.1:8003>

## 目录结构

```
F:\openos\
├── agents\            # 多智能体（kernel_engineer / system_builder / ai_os / freedom）
├── services\          # llm_gateway
├── web\               # FastAPI 入口 + static 前端
├── scripts\           # 启动脚本
├── config\            # models.json + .env.example
├── data\              # Agent 产出契约（kernel/build/aios/freedom）
├── requirements.txt
├── README.md
└── 技术方案.md
```

## API 一览

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | / | 前端页面 |
| GET | /api/health | 健康检查 + LLM 状态 |
| GET | /api/agents | Agent 列表 |
| POST | /api/tasks | 提交目标，Orchestrator 规划并执行 |
| GET | /api/tasks/{id} | 查询任务报告 |
| GET | /api/contracts/{sub_dir} | 浏览 data/ 下契约产物 |

详细设计见 [技术方案.md](技术方案.md)。
*（内容由AI生成，仅供参考）*
