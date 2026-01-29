import json
import os
from pathlib import Path
from typing import Dict, List, Optional

from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()


class LLMConfig(BaseModel):
    provider: str = "openrouter"
    model: str = "openai/gpt-5.1"


class MCPServerConfig(BaseModel):
    name: str
    description: Optional[str] = None
    command: Optional[str] = None
    args: List[str] = Field(default_factory=list)
    env: Dict[str, str] = Field(default_factory=dict)
    url: Optional[str] = None
    transport: Optional[str] = None
    headers: Dict[str, str] = Field(default_factory=dict)
    timeout: Optional[int] = None
    max_retries: Optional[int] = None
    health_check_interval: Optional[int] = None


class MCPConfig(BaseModel):
    enabled: bool = True
    servers: List[MCPServerConfig] = Field(default_factory=list)


class ToolkitConfig(BaseModel):
    default_toolkits: List[str] = Field(default_factory=lambda: ["web"])


class AppConfig(BaseModel):
    llm: LLMConfig = Field(default_factory=LLMConfig)
    toolkits: ToolkitConfig = Field(default_factory=ToolkitConfig)
    mcp: MCPConfig = Field(default_factory=MCPConfig)


def _parse_json(text: str) -> Optional[dict]:
    if not text:
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


def _load_mcp_from_path(path_str: str) -> Optional[dict]:
    if not path_str:
        return None
    path = Path(path_str)
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def load_config() -> AppConfig:
    provider = os.getenv("SPOON_LLM_PROVIDER", "openrouter")
    model = os.getenv("SPOON_LLM_MODEL", "openai/gpt-5.1")
    toolkits_env = os.getenv("SPOON_TOOLKITS", "web")
    default_toolkits = [t.strip() for t in toolkits_env.split(",") if t.strip()]

    mcp_json = os.getenv("SPOON_MCP_CONFIG", "")
    mcp_path = os.getenv("SPOON_MCP_CONFIG_PATH", "")
    mcp_raw = _parse_json(mcp_json) or _load_mcp_from_path(mcp_path) or {}

    mcp_enabled = bool(mcp_raw.get("enabled", True))
    mcp_servers = mcp_raw.get("servers", []) if isinstance(mcp_raw, dict) else []

    return AppConfig(
        llm=LLMConfig(provider=provider, model=model),
        toolkits=ToolkitConfig(default_toolkits=default_toolkits),
        mcp=MCPConfig(enabled=mcp_enabled, servers=mcp_servers),
    )
