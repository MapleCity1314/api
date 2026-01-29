# AGENTS

This repo contains a SpoonOS ReAct API server and supporting Python code.

## Layout
- `spoonos_server/`: FastAPI server, agents, tools, and configs.
- `main.py`: Uvicorn entrypoint (`main:app`).
- `pyproject.toml` / `requirements.txt`: Python packaging and dependencies.
- `.env.example`: Environment variable template.

## Python API (root)
- Create venv (PowerShell):
  - `python -m venv .venv`
  - `./.venv/Scripts/Activate.ps1`
- Install deps:
  - `pip install -e .`
  - Optional extras: `pip install ".[memory]"`
- Configure API key in `.env`:
  - `OPENROUTER_API_KEY=sk-xxxx`
- Run demo:
  - `uvicorn spoonos_server.server.app:app --host 0.0.0.0 --port 8000`
  - Or `uvicorn main:app --host 0.0.0.0 --port 8000`

## Skills (project)
- Local skills live in `spoonos_server/skills/<skill-name>/SKILL.md`.
- Add a skill by creating a new folder with a `SKILL.md` file.
- Skill discovery is file-based (see `spoonos_server/skills/registry.py`).

## Notes
- Prefer minimal, focused changes.
- Keep commands OS-appropriate (PowerShell on Windows).
