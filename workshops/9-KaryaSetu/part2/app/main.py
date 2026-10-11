"""
KaryaSetu -- Part 2: streaming responses.

    uvicorn app.main:app --reload
    open http://127.0.0.1:8000/

Part 1's endpoint (`/v1/analyze`) is unchanged in this folder. This part adds
POST /v1/cover-letter/stream, the only thing with a TODO.

Heads up: Swagger UI buffers, so it cannot show you a live stream. Use the
demo page at / or `curl -N` instead.
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

from .providers import ProviderError, build_provider
from .sse import SSE_HEADERS, sse_event

STATIC_DIR = Path(__file__).parent / "static"

# Shared workshop root .env (partN/app/main.py → ../../.env)
_ENV_FILE = Path(__file__).resolve().parents[2] / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=_ENV_FILE, extra="ignore")

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
    description="Honest feedback on whether you should apply. Part 2: streaming responses.",
)


@app.exception_handler(ProviderError)
def handle_provider_error(request: Request, exc: ProviderError) -> JSONResponse:
    return JSONResponse(status_code=exc.status, content={"detail": exc.message})


@app.get("/health", tags=["ops"])
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/v1/analyze", response_model=AnalyzeResponse)
def analyze(payload: AnalyzeRequest) -> AnalyzeResponse:
    """The Part 1 endpoint, unchanged. Keep it around -- side by side with
    the streaming version, the difference is visceral rather than theoretical."""
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
    Stream a cover letter to the client, token by token.

    TODO 1: build the generator and return it as a StreamingResponse.

    Write an inner generator function, `event_source()`, that yields SSE
    frames built with `sse_event(data, event=...)`: a "start" frame with the
    provider and model, a "token" frame for each chunk that comes out of
    `provider.stream(system=LETTER_SYSTEM, user=prompt)` -- collect the
    chunks into a list as you go -- and a "done" frame once the loop ends,
    carrying the total character count. Wrap the whole body in
    `try: ... except ProviderError as exc:` and yield an "error" frame
    instead of letting the exception escape. Finally, return
    `StreamingResponse(event_source(), media_type="text/event-stream",
    headers=SSE_HEADERS)`.

    The thing to internalise: the moment the first byte leaves this function
    the status code is decided. It is 200. Forever. If the provider dies on
    token 400 you cannot go back and make it a 502 -- the header is long
    gone. Streaming trades away a clean failure mode, and you buy it back
    with an error EVENT, in-band, inside the try/except.

    Note there is no explicit disconnect check, and none is needed. Starlette
    stops pulling from the generator the moment the client goes away, so
    generation halts after at most one more chunk -- you stop paying for
    free. What you do NOT get is a reliable hook to log it: an abandoned sync
    generator is never closed explicitly, so a `finally` block fires whenever
    the garbage collector gets round to it.
    """
    prompt = letter_prompt(payload.job_description, payload.experience_notes)  # noqa: F841

    def event_source() -> Iterator[str]:
        collected: list[str] = []
        try:
            yield sse_event(
                {"provider": provider.name, "model": provider.model}, event="start"
            )
            for chunk in provider.stream(system=LETTER_SYSTEM, user=prompt):
                collected.append(chunk)
                yield sse_event({"text": chunk}, event="token")

            full_text = "".join(collected)
            print(f"[letter] {full_text}")
            yield sse_event({"chars": len(full_text)}, event="done")
        except ProviderError as exc:
            yield sse_event({"detail": exc.message}, event="error")

    return StreamingResponse(
        event_source(), media_type="text/event-stream", headers=SSE_HEADERS
    )


@app.get("/", include_in_schema=False)
def demo_page() -> FileResponse:
    """A ~130-line page that consumes the stream. Deliberately no framework."""
    return FileResponse(STATIC_DIR / "index.html")
