"""
KaryaSetu -- Part 1: talking to a model provider from FastAPI.

    uvicorn app.main:app --reload
    open http://127.0.0.1:8000/docs

Boots with LLM_PROVIDER=mock, so it runs before you have any keys.
"""

from __future__ import annotations

import time
from functools import lru_cache
from pathlib import Path
from typing import Literal

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from .providers import ProviderError, build_provider

# Shared workshop root .env (partN/app/main.py → ../../.env)
_ENV_FILE = Path(__file__).resolve().parents[2] / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=_ENV_FILE, extra="ignore")

    # "mock" needs no key and no network, so the app runs before you have
    # credentials. It is the default on purpose.
    llm_provider: Literal["mock", "openai", "anthropic"] = "mock"

    openai_api_key: str | None = None
    openai_model: str = "gpt-4o-mini"

    anthropic_api_key: str | None = None
    anthropic_model: str = "claude-sonnet-4-5"   # model IDs move; check the docs

    max_tokens: int = Field(default=800, gt=0)
    temperature: float = Field(default=0.4, ge=0.0, le=2.0)


@lru_cache
def get_settings() -> Settings:
    return Settings()


ANALYST_SYSTEM = (
    "You are a blunt, experienced technical recruiter. Compare the "
    "candidate's notes against the job posting and report honestly on fit. "
    "Never invent experience the candidate did not claim. Be specific and brief."
)


def analyze_prompt(job_description: str, experience_notes: str) -> str:
    return (
        f"=== JOB POSTING ===\n{job_description.strip()}\n\n"
        f"=== CANDIDATE NOTES ===\n{experience_notes.strip()}\n\n"
        "Give a one-sentence verdict, two matching strengths, and one gap."
    )


class AnalyzeRequest(BaseModel):
    job_description: str = Field(min_length=50, max_length=8000)
    experience_notes: str = Field(min_length=20, max_length=8000)


class AnalyzeResponse(BaseModel):
    analysis: str
    provider: str
    model: str
    latency_ms: int


# One provider instance for the life of the process. Built at import time --
# once per process, like a database connection pool -- rather than inside the
# route, which would open a fresh HTTP connection pool on every request.
provider = build_provider(get_settings())

app = FastAPI(
    title="KaryaSetu API",
    description="Honest feedback on whether you should apply. Part 1: LLM SDK integration.",
)


@app.exception_handler(ProviderError)
def handle_provider_error(request: Request, exc: ProviderError) -> JSONResponse:
    """Vendor exceptions never reach here -- each adapter already translated
    its own SDK's errors into this one type."""
    return JSONResponse(status_code=exc.status, content={"detail": exc.message})


@app.get("/health", tags=["ops"])
def health() -> dict[str, str]:
    """A health check that calls the model is not a health check, it is a bill."""
    return {"status": "ok"}


@app.get("/v1/provider")
def which_provider() -> dict[str, str]:
    """Handy on stage: prove which backend is actually wired up."""
    return {"provider": provider.name, "model": provider.model}


@app.post("/v1/analyze", response_model=AnalyzeResponse)
def analyze(payload: AnalyzeRequest) -> AnalyzeResponse:
    """Notice what is NOT here: no `import openai`, no vendor exception
    handling. That is the whole point of the adapter."""
    started = time.perf_counter()
    prompt = analyze_prompt(payload.job_description, payload.experience_notes)
    result = provider.complete(system=ANALYST_SYSTEM, user=prompt)
    return AnalyzeResponse(
        analysis=result.text,
        provider=result.provider,
        model=result.model,
        latency_ms=int((time.perf_counter() - started) * 1000),
    )
