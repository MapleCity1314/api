from typing import Any, Dict, List, Optional

from spoon_ai.chat import ChatBot

from spoonos_server.config import AppConfig
from spoonos_server.schemas import SubAgentSpec
from spoonos_server.tools.toolkits import load_toolkits, resolve_toolkits
from spoonos_server.mcp.loader import load_mcp_tools

try:
    from spoon_ai.agents.spoon_react import SpoonReactAI
except Exception:  # pragma: no cover - optional dependency
    SpoonReactAI = None

try:
    from spoon_ai.tools.base import BaseTool
except Exception:  # pragma: no cover - optional dependency
    BaseTool = None


if BaseTool:
    class SubAgentTool(BaseTool):
        name: str = "sub_agent"
        description: str = "Call a named sub-agent with a message."
        parameters: dict = {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Sub-agent name"},
                "message": {"type": "string", "description": "Message to send"},
            },
            "required": ["name", "message"],
        }

        def __init__(self, agents: Dict[str, Any]) -> None:
            super().__init__()
            self._agents = agents

        async def execute(self, name: str, message: str) -> str:
            agent = self._agents.get(name)
            if not agent:
                return f"Unknown sub-agent: {name}"
            return await agent.run(request=message)
else:
    SubAgentTool = None


def _create_subagent(
    spec: SubAgentSpec, config: AppConfig, system_prompt: str
) -> Optional[Any]:
    if SpoonReactAI is None:
        return None

    provider = spec.provider or config.llm.provider
    model = spec.model or config.llm.model
    toolkits = resolve_toolkits(spec.toolkits, config.toolkits.default_toolkits)
    tools = load_toolkits(toolkits)

    mcp_enabled = spec.mcp_enabled
    if mcp_enabled is None:
        mcp_enabled = config.mcp.enabled
    if mcp_enabled:
        tools.extend(load_mcp_tools(config.mcp))

    agent = SpoonReactAI(
        name=spec.name,
        llm=ChatBot(llm_provider=provider, model_name=model),
        tools=tools,
        max_steps=6,
    )
    if system_prompt:
        agent.system_prompt = system_prompt
    return agent


def create_subagents(
    specs: Optional[List[SubAgentSpec]], config: AppConfig
) -> Dict[str, Any]:
    if not specs:
        return {}

    agents: Dict[str, Any] = {}
    for spec in specs:
        prompt = spec.system_prompt or ""
        agent = _create_subagent(spec, config, prompt)
        if agent is not None:
            agents[spec.name] = agent

    return agents
