"""
KaryaSetu -- Week 3, Part 3: the same app, everywhere.

Parts 1 and 2 are complete in this folder. The Python is unchanged. What is
new is everything AROUND it:

    Dockerfile            how to build the image             (TODO 1)
    compose.yaml          how to run it while you develop    (TODO 2)
    .dockerignore         what must never enter an image
    Dockerfile.leaky      the mistake, kept on purpose for the demo
    nginx/default.conf    a production-shaped front door (docker compose --profile proxy)

    docker compose up --build
    open http://127.0.0.1:8000/docs

Then `pytest` -- it lints your Docker files without needing Docker.
"""

from __future__ import annotations

import json
import time
from collections.abc import Iterator
from functools import lru_cache
from pathlib import Path
from typing import Literal

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
from pydantic import BaseModel, Field, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict

from .fit import FitReportResponse, strictify
from .prompting import DEFAULT_PROMPT_VERSION, MAX_SHOTS, PromptNotFound
from .providers import Message, ProviderError, build_provider
from .report import assemble_prompt, generate_report
from .sse import SSE_HEADERS, sse_event

STATIC_DIR = Path(__file__).parent / "static"

# Shared workshop-root .env (partN/app/main.py → ../..), then optional part-local override.
_WORKSHOP_ROOT = Path(__file__).resolve().parents[2]
_ENV_FILES = (
    _WORKSHOP_ROOT / ".env",
    Path(__file__).resolve().parents[1] / ".env",
)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=_ENV_FILES, extra="ignore")

    llm_provider: Literal["mock", "openai", "anthropic"] = "mock"

    # Dev-mode switch. On: /v1/fit-report/preview exists. Off (the default,
    # and what production gets): it does not. Read from APP_DEBUG.
    debug: bool = Field(default=False, validation_alias="APP_DEBUG")

    openai_api_key: str | None = None
    openai_base_url: str | None = None  # OpenRouter, Groq, a local server...
    openai_model: str = "gpt-4o-mini"

    anthropic_api_key: str | None = None
    anthropic_model: str = "claude-haiku-4-5-20251001"

    # Generous on purpose: a truncated JSON object is not "a bit wrong", it is
    # unparseable. Longer prompts and reasoning fields make truncation likelier.
    max_tokens: int = Field(default=1500, gt=0)
    # OpenAI only: the current Anthropic SDK no longer accepts sampling parameters.
    temperature: float = Field(default=0.4, ge=0.0, le=2.0)


@lru_cache
def get_settings() -> Settings:
    return Settings()


# --- Weeks 1-2, unchanged ----------------------------------------------------

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


LETTER_SYSTEM = (
    "You write cover letters that sound like a competent human wrote them in "
    "one sitting. No buzzwords, no 'I am writing to express my interest'. "
    "Only use experience the candidate actually claims. Four short paragraphs."
)


def letter_prompt(job_description: str, experience_notes: str) -> str:
    return (
        f"=== JOB POSTING ===\n{job_description.strip()}\n\n"
        f"=== CANDIDATE NOTES ===\n{experience_notes.strip()}\n\n"
        "Write the cover letter. Open with the single most relevant thing the "
        "candidate has actually done."
    )


class AnalyzeRequest(BaseModel):
    job_description: str = Field(min_length=50, max_length=8000)
    experience_notes: str = Field(min_length=20, max_length=8000)


class AnalyzeResponse(BaseModel):
    analysis: str
    provider: str
    model: str
    latency_ms: int


class LetterRequest(BaseModel):
    job_description: str = Field(min_length=50, max_length=8000)
    experience_notes: str = Field(min_length=20, max_length=8000)


provider = build_provider(get_settings())

app = FastAPI(
    title="KaryaSetu API",
    description="Honest feedback on whether you should apply. Week 3: prompts as contracts.",
)


@app.exception_handler(ProviderError)
def handle_provider_error(request: Request, exc: ProviderError) -> JSONResponse:
    return JSONResponse(status_code=exc.status, content={"detail": exc.message})


@app.exception_handler(PromptNotFound)
def handle_prompt_not_found(request: Request, exc: PromptNotFound) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": str(exc)})


@app.exception_handler(ValidationError)
def handle_broken_contract(request: Request, exc: ValidationError) -> JSONResponse:
    """
    The model returned well-formed JSON that broke a rule -- a score of 137,
    or a strong_match with most requirements missing. That is an upstream
    failure, so 502, not our 500. (Week 2 left this as an exercise.)
    """
    problems = "; ".join(e["msg"] for e in exc.errors())
    return JSONResponse(
        status_code=502,
        content={"detail": f"The model's report broke the contract: {problems}"},
    )


@app.get("/health", tags=["ops"])
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/v1/analyze", response_model=AnalyzeResponse)
def analyze(payload: AnalyzeRequest) -> AnalyzeResponse:
    """Complete as of Week 2 (Part 1)."""
    started = time.perf_counter()
    prompt = analyze_prompt(payload.job_description, payload.experience_notes)
    result = provider.complete(system=ANALYST_SYSTEM, user=prompt)
    return AnalyzeResponse(
        analysis=result.text,
        provider=result.provider,
        model=result.model,
        latency_ms=int((time.perf_counter() - started) * 1000),
    )


@app.post("/v1/cover-letter/stream")
def stream_cover_letter(payload: LetterRequest):
    """
    Complete as of Week 2 (Part 2).

    The moment the first byte leaves this function the status code is
    decided -- 200, forever -- so a mid-stream failure travels as an error
    EVENT rather than a different status code.
    """
    prompt = letter_prompt(payload.job_description, payload.experience_notes)

    def event_source() -> Iterator[str]:
        collected: list[str] = []
        try:
            yield sse_event(
                {"provider": provider.name, "model": provider.model}, event="start"
            )
            for chunk in provider.stream(system=LETTER_SYSTEM, user=prompt):
                collected.append(chunk)
                yield sse_event({"text": chunk}, event="token")

            full = "".join(collected)
            print(f"[letter] {len(full)} chars generated", flush=True)
            yield sse_event({"chars": len(full)}, event="done")

        except ProviderError as exc:
            yield sse_event({"detail": exc.message}, event="error")

    return StreamingResponse(
        event_source(), media_type="text/event-stream", headers=SSE_HEADERS
    )


# --- Week 3 ------------------------------------------------------------------


class ReportRequest(BaseModel):
    job_description: str = Field(min_length=50, max_length=8000)
    experience_notes: str = Field(min_length=20, max_length=8000)


class PromptPreview(BaseModel):
    """Exactly what WOULD be sent to the model. No model call, no cost."""

    prompt_version: str
    shots: int
    reasoning: bool
    system: str
    history: list[Message]
    user: str
    schema_fields: list[str]  # in the order the model must fill them in
    approx_input_tokens: int


# `version` reaches the filesystem, so the pattern is a security control, not
# decoration. It is checked here at the edge and again inside load_prompt().
PromptVersion = Query(
    DEFAULT_PROMPT_VERSION,
    pattern=r"^v\d+$",
    description="Which released prompt to use. Pin it. Never edit a released version in place.",
)
Shots = Query(
    0, ge=0, le=MAX_SHOTS, description="Worked examples to include. Every one is billed on every call."
)
Reasoning = Query(
    False, description="Make the model think first, in a field that precedes the verdict."
)


@app.post("/v1/fit-report", response_model=FitReportResponse)
def fit_report(
    payload: ReportRequest,
    prompt_version: str = PromptVersion,
    shots: int = Shots,
    reasoning: bool = Reasoning,
) -> FitReportResponse:
    started = time.perf_counter()
    prompt = assemble_prompt(
        payload.job_description,
        payload.experience_notes,
        version=prompt_version,
        shots=shots,
        reasoning=reasoning,
    )
    run = generate_report(provider, prompt)
    return FitReportResponse(
        report=run.report,
        provider=provider.name,
        model=provider.model,
        prompt_version=prompt.version,
        shots=prompt.shots,
        reasoning=prompt.reasoning,
        latency_ms=int((time.perf_counter() - started) * 1000),
        # Working aid, not contract: dev-mode only.
        scratchpad=run.scratchpad if get_settings().debug else None,
    )


@app.post("/v1/fit-report/preview", response_model=PromptPreview, tags=["dev-mode"])
def fit_report_preview(
    payload: ReportRequest,
    prompt_version: str = PromptVersion,
    shots: int = Shots,
    reasoning: bool = Reasoning,
) -> PromptPreview:
    """
    Dry run: show the exact prompt the model would receive, without calling it.

    Dev-mode only (APP_DEBUG=true). A production endpoint that echoes your
    system prompt is a gift to anyone trying to attack it.
    """
    if not get_settings().debug:
        raise HTTPException(status_code=404, detail="Not found")
    prompt = assemble_prompt(
        payload.job_description,
        payload.experience_notes,
        version=prompt_version,
        shots=shots,
        reasoning=reasoning,
    )
    schema = strictify(prompt.schema_model.model_json_schema())
    sent = (
        prompt.system
        + prompt.user
        + "".join(m["content"] for m in prompt.history)
        + json.dumps(schema)
    )
    return PromptPreview(
        prompt_version=prompt.version,
        shots=prompt.shots,
        reasoning=prompt.reasoning,
        system=prompt.system,
        history=prompt.history,
        user=prompt.user,
        schema_fields=list(schema["properties"]),
        approx_input_tokens=len(sent) // 4,  # ~4 chars per token: an estimate, not a bill
    )


@app.get("/", include_in_schema=False)
def demo_page() -> FileResponse:
    """A ~130-line page that consumes the stream. Deliberately no framework."""
    return FileResponse(STATIC_DIR / "index.html")
