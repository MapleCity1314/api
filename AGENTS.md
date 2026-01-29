# AGENTS

This repo contains a Python API demo and a Next.js web app.

## Layout
- `api/`: Python demo scripts and requirements.
- `spoon-agent-web/`: Next.js app (App Router).
- `codex_wrapper.ps1`: helper script.

## Python API (api/)
- Create venv (PowerShell):
  - `python -m venv .venv`
  - `./.venv/Scripts/Activate.ps1`
- Install deps:
  - `pip install -e .`
  - Optional extras: `pip install ".[memory]"`
- Configure API key in `api/.env`:
  - `OPENROUTER_API_KEY=sk-xxxx`
- Run demo:
  - `python api/streaming_chatbot.py`

## Web app (spoon-agent-web/)
- Install deps: `npm install`
- Run dev server: `npm run dev`
- Edit entry page: `spoon-agent-web/app/page.tsx`

## Notes
- Prefer minimal, focused changes.
- Keep commands OS-appropriate (PowerShell on Windows).