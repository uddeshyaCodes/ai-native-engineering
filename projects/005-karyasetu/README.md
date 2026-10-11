# 005 - KaryaSetu

Paste a job posting and messy experience notes; get honest fit feedback.

Copied from `workshops/9-karyasetu/part3` (LLM SDK integration + SSE streaming + structured outputs).

## Features

- `POST /v1/analyze` — one-shot fit analysis (OpenAI / Anthropic / mock)
- `POST /v1/cover-letter/stream` — cover letter streamed over SSE
- `POST /v1/fit-report` — schema-constrained JSON fit report (Pydantic + strict mode)
- Provider seam so routes never import vendor SDKs directly
- Demo UI at `/` for the stream; OpenAPI at `/docs`

## Run locally

```bash
cd projects/005-karyasetu
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) or the stream demo at [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

Defaults to `LLM_PROVIDER=mock` (no API key). For a real provider, edit `.env`.

Sample request:

```bash
curl -s -X POST http://127.0.0.1:8000/v1/analyze \
  -H 'content-type: application/json' -d @sample_request.json
```

## Layout

| Path | Role |
|------|------|
| `app/main.py` | Settings, prompts, routes |
| `app/fit.py` | FitReport schema + `strictify` for OpenAI strict mode |
| `app/sse.py` | SSE frame helper + stream headers |
| `app/providers/` | Protocol + mock / OpenAI / Anthropic adapters |
| `app/static/` | Streaming demo page |
| `sample_request.json` | Shared curl body |
