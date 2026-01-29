import inspect
from typing import Any, Dict, List

from spoonos_server.config import MCPConfig, MCPServerConfig

try:
    from spoon_ai.tools.mcp_tool import MCPTool
except Exception:  # pragma: no cover - optional dependency
    MCPTool = None


def _build_mcp_config(server: MCPServerConfig) -> Dict[str, Any]:
    config: Dict[str, Any] = {}

    if server.command:
        config["command"] = server.command
        config["args"] = server.args
        config["env"] = server.env
    if server.url:
        config["url"] = server.url
    if server.transport:
        config["transport"] = server.transport
    if server.headers:
        config["headers"] = server.headers
    if server.timeout is not None:
        config["timeout"] = server.timeout
    if server.max_retries is not None:
        config["max_retries"] = server.max_retries
    if server.health_check_interval is not None:
        config["health_check_interval"] = server.health_check_interval

    return config


def _instantiate_mcp_tool(
    name: str, description: str, mcp_config: Dict[str, Any]
) -> Any:
    if MCPTool is None:
        return None

    try:
        sig = inspect.signature(MCPTool)
        kwargs: Dict[str, Any] = {}
        if "name" in sig.parameters:
            kwargs["name"] = name
        if "description" in sig.parameters:
            kwargs["description"] = description
        if "mcp_config" in sig.parameters:
            kwargs["mcp_config"] = mcp_config
        else:
            kwargs.update(mcp_config)
        return MCPTool(**kwargs)
    except Exception:
        try:
            return MCPTool(mcp_config=mcp_config)
        except Exception:
            return None


def load_mcp_tools(mcp_config: MCPConfig) -> List[Any]:
    if not mcp_config.enabled or MCPTool is None:
        return []

    tools: List[Any] = []
    for server in mcp_config.servers:
        config = _build_mcp_config(server)
        description = server.description or f"MCP server {server.name}"
        tool = _instantiate_mcp_tool(server.name, description, config)
        if tool is not None:
            tools.append(tool)

    return tools
