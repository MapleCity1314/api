## SpoonOS ReAct Server Quick Start

# Installation

## Prerequisites

- Python 3.12～3.14
- Git
- Virtual environment (recommended)

## Quick Installation

## 中文快速运行（已验证）

以下步骤在 2026-01-29 使用 Python 3.12.12 验证可启动服务。

### 1. 创建虚拟环境（Python 3.12+）

```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

### 2. 安装依赖

```bash
python -m pip install -U pip
python -m pip install -e .
```

### 3. 配置 API Key

在项目根目录创建 `.env` 并写入：

```
OPENROUTER_API_KEY=sk-xxxx
```

可选：通过 `SPOON_LLM_PROVIDER` 与 `SPOON_LLM_MODEL` 指定模型与供应商。

### 4. 启动服务

```bash
uvicorn spoonos_server.server.app:app --host 0.0.0.0 --port 8000
```

### 5. 调用接口（需要可用的 API Key）

```bash
curl -N -X POST http://localhost:8000/v1/agent/stream \
  -H "Content-Type: application/json" \
  -d '{"message":"用三点说明SpoonOS是什么","stream_mode":"sse"}'
```

### 6. 常见提示

- 如果未配置有效 API Key，请求会返回鉴权或模型相关错误。
- 如果启动时看到 `fatal: bad revision 'HEAD'`，通常是运行环境缺少 git 历史导致，可忽略。

### 1. Create Virtual Environment

#### Option A: Using uv (recommended)

```bash
# macOS/Linux
uv venv .venv
source .venv/bin/activate

# Windows (PowerShell)
uv venv .venv
.\.venv\Scripts\Activate.ps1

```
#### Option B: Using built-in venv
```bash
# macOS/Linux
python -m venv .venv
source .venv/bin/activate

# Windows (PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

```
### 2. Install Dependencies

```bash
#uv （recommend）
uv pip install -e .

#venv
pip install -e .
```
If you want to enable Mem0 support
```bash
uv pip install ".[memory]"
# or
pip install ".[memory]"
```
---

### 3.Configure an OpenRouter or other API key（include gemini，anthropic，deepseek，openai）\*\*

Put the key into `.env`:

```
OPENROUTER_API_KEY=sk-xxxx
```

You can adjust the LLM provider and model via environment variables (`SPOON_LLM_PROVIDER`, `SPOON_LLM_MODEL`).

---

### 4. Run the Demo

```bash
uvicorn spoonos_server.server.app:app --reload
```

Then call the streaming endpoint:

```bash
curl -N -X POST http://localhost:8000/v1/agent/stream \
  -H "Content-Type: application/json" \
  -d '{"message":"用三点说明SpoonOS是什么","stream_mode":"sse"}'
```

---

### 5. Tips

- **`Cleanup failed for ...`** – means a provider isn’t configured; safe to ignore.
- **`websockets.legacy` DeprecationWarning** – upstream warning, safe to ignore.
