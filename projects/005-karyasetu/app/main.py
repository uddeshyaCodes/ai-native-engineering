"""
KaryaSetu — job-fit analysis over OpenAI / Anthropic / mock.

    uvicorn app.main:app --reload
    open http://127.0.0.1:8000/docs

Inspect the constrained JSON Schema with:

    python -m app.fit
"""

from __future__ import annotations

import time
from collections.abc import Iterator
from functools import lru_cache
from pathlib import Path
from typing import Literal

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from .fit import FitReport, FitReportResponse, strictify
from .providers import ProviderError, build_provider
from .sse import SSE_HEADERS, sse_event

STATIC_DIR = Path(__file__).parent / "static"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    llm_provider: Literal["mock", "openai", "anthropic"] = "mock"

    openai_api_key: str | None = None
    openai_model: str = "gpt-4o-mini"

    anthropic_api_key: str | None = None
    anthropic_model: str = "claude-sonnet-4-5"

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


REPORT_SYSTEM = (
    "You are a blunt technical recruiter producing a structured fit report. "
    "You judge only what the notes actually say. You never invent evidence. "
    "When there is no evidence for a requirement, say so."
)


def report_prompt(job_description: str, experience_notes: str) -> str:
    """
    Notice what is NOT here: no "respond in JSON", no example object, no "do
    not use markdown fences". The schema carries all of that -- and carries
    it in a way the decoder enforces rather than merely reads.
    """
    return (
        f"=== JOB POSTING ===\n{job_description.strip()}\n\n"
        f"=== CANDIDATE NOTES ===\n{experience_notes.strip()}\n\n"
        "Assess the fit."
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


class ReportRequest(BaseModel):
    job_description: str = Field(min_length=50, max_length=8000)
    experience_notes: str = Field(min_length=20, max_length=8000)


provider = build_provider(get_settings())

app = FastAPI(
    title="KaryaSetu API",
    description="Honest feedback on whether you should apply — analyze, stream a cover letter, structured fit report.",
)


@app.exception_handler(ProviderError)
def handle_provider_error(request: Request, exc: ProviderError) -> JSONResponse:
    return JSONResponse(status_code=exc.status, content={"detail": exc.message})


@app.get("/health", tags=["ops"])
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/v1/analyze", response_model=AnalyzeResponse)
def analyze(payload: AnalyzeRequest) -> AnalyzeResponse:
    """Complete as of Part 1."""
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
    Complete as of Part 2.

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
            print(f"[letter] {len(full)} chars generated")
            yield sse_event({"chars": len(full)}, event="done")

        except ProviderError as exc:
            yield sse_event({"detail": exc.message}, event="error")

    return StreamingResponse(
        event_source(), media_type="text/event-stream", headers=SSE_HEADERS
    )


@app.post("/v1/fit-report", response_model=FitReportResponse)
def fit_report(payload: ReportRequest) -> FitReportResponse:
    """Schema-constrained fit report; `model_validate` still runs after the provider returns."""
    started = time.perf_counter()
    prompt = report_prompt(payload.job_description, payload.experience_notes)
    schema = strictify(FitReport.model_json_schema())
    result = provider.structured(
        system=REPORT_SYSTEM, user=prompt, schema=schema, name="fit_report"
    )
    return FitReportResponse(
        report=FitReport.model_validate(result),
        provider=provider.name,
        model=provider.model,
        latency_ms=int((time.perf_counter() - started) * 1000),
    )


@app.get("/", include_in_schema=False)
def demo_page() -> FileResponse:
    """A ~130-line page that consumes the stream. Deliberately no framework."""
    return FileResponse(STATIC_DIR / "index.html")
