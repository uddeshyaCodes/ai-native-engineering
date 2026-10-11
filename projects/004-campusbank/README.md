# 004 - CampusBank

FastAPI sample banking API from **Module 2: Designing Production-Grade LLM Infrastructure** (Campus Bank workshop, part 8).

Copied from `workshops/8-FastAPI-demo_stub/part_8_openapi_docs` with OpenAPI TODOs completed (TODO comments kept).

## Features

- Users API **v1** and **v2** (v2 adds `id` and `account_count`)
- Accounts under `/api/v1/users/{username}/accounts` (max 5 per user; savings/current)
- Pydantic validation, SQLAlchemy + SQLite, dependency-injected DB sessions
- OpenAPI docs at `/docs`

## Run locally

```bash
cd projects/004-campusbank
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

## Layout

| Path | Role |
|------|------|
| `main.py` | FastAPI app + OpenAPI description |
| `schemas.py` | Pydantic request/response models |
| `models.py` | SQLAlchemy ORM |
| `database.py` | Engine, session, `get_db` |
| `crud.py` | Persistence helpers |
| `routers/v1/` | Users v1 + accounts |
| `routers/v2/` | Users v2 |
