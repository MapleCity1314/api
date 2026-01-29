import json
import uuid
from typing import AsyncIterator, Dict, List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse

from spoonos_server.agents.react_agent import create_react_agent, stream_agent_events
from spoonos_server.config import load_config
from spoonos_server.schemas import ChatMessage, StreamRequest

app = FastAPI(title="SpoonOS ReAct Agent Server")
config = load_config()

# In-memory store to allow future session/memory extensions.
SESSION_STORE: Dict[str, List[ChatMessage]] = {}


def _merge_messages(
    session_id: str, messages: Optional[List[ChatMessage]]
) -> List[ChatMessage]:
    history = SESSION_STORE.get(session_id, [])
    if messages:
        history = history + messages
    SESSION_STORE[session_id] = history
    return history


def _json_default(value: object) -> object:
    model_dump = getattr(value, "model_dump", None)
    if callable(model_dump):
        return model_dump()
    to_dict = getattr(value, "to_dict", None)
    if callable(to_dict):
        return to_dict()
    as_dict = getattr(value, "dict", None)
    if callable(as_dict):
        return as_dict()
    return str(value)


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.post("/v1/agent/stream")
async def stream_agent(request: StreamRequest) -> StreamingResponse:
    if not request.message and not request.messages:
        raise HTTPException(status_code=400, detail="message or messages required.")

    session_id = request.session_id or str(uuid.uuid4())
    if request.messages:
        _merge_messages(session_id, request.messages)

    user_message = (
        request.message
        if request.message
        else request.messages[-1].content  # type: ignore[index]
    )

    agent = create_react_agent(
        config=config,
        system_prompt=request.system_prompt,
        provider=request.provider,
        model=request.model,
        toolkits=request.toolkits,
        mcp_enabled=request.mcp_enabled,
        sub_agents=request.sub_agents,
    )

    async def event_stream() -> AsyncIterator[str]:
        async for event in stream_agent_events(agent, user_message, request.timeout):
            payload = json.dumps(event, ensure_ascii=False, default=_json_default)
            if request.stream_mode == "sse":
                yield f"data: {payload}\n\n"
            else:
                yield payload

    media_type = "text/event-stream" if request.stream_mode == "sse" else "text/plain"
    return StreamingResponse(event_stream(), media_type=media_type)
