# KaryaSetu

Paste in a job posting and your messy experience notes, get back honest
feedback on fit. KaryaSetu is a small FastAPI service, built in three
parts, each adding one capability:

| Part | Concept | Adds |
|---|---|---|
| [1](#part-1--llm-sdk-integration) | LLM SDK integration | `POST /v1/analyze` — talk to OpenAI and Anthropic behind one interface |
| [2](#part-2--streaming-responses) | Streaming responses | `POST /v1/cover-letter/stream` — stream tokens over SSE |
| [3](#part-3--structured-outputs-with-pydantic) | Structured outputs with Pydantic | `POST /v1/fit-report` — a schema-constrained JSON object, not prose |

Each `partN/` folder is a complete, independently runnable snapshot — `part3`
contains all three endpoints, `part2` contains the first two, and so on. Every
part has exactly two `TODO`s, marked in the code with a comment block like:

```python
# ------------------------------------------------------------------
# TODO 1: ...
# ------------------------------------------------------------------
raise NotImplementedError("TODO 1: see app/...")
```

Fill in the body, delete the `raise`, and move on.

## Setup

One virtual environment and one `requirements.txt` cover all three parts:

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

One shared `.env` lives at the workshop root; every part reads that file.
Copy the example once, then run each part from its own folder:

```bash
cp .env.example .env        # once, at the workshop root
cd part1                    # or part2, part3
uvicorn app.main:app --reload
```

`.env` defaults to `LLM_PROVIDER=mock`, so everything below runs with **no
API key**. To try a real provider, edit the root `.env` and uncomment the
matching key.

## A note on `async`

This codebase is deliberately synchronous. FastAPI runs a plain `def` route in
a worker thread, which is exactly where blocking code belongs — and calling a
model blocks for several seconds. See the "Do We Need async?" slide.

---

## Part 1 — LLM SDK Integration

Part 1 builds the plumbing that lets FastAPI talk to a model provider without
marrying one, and wires up the OpenAI and Anthropic SDKs behind it.

```
part1/app/
  main.py                       settings, prompt, app, routes -- all in one place
  providers/
    __init__.py                 the seam: Protocol, Completion, ProviderError
    mock.py                     runs with no API key
    openai_provider.py          the only two files that
    anthropic_provider.py       import a vendor SDK
```

**What you will fill in**

| TODO | File | What it does |
|---|---|---|
| 1 | `providers/openai_provider.py` | The `chat.completions.create` call |
| 2 | `providers/anthropic_provider.py` | The `messages.create` call |

**Run it**

```bash
cd part1
uvicorn app.main:app --reload
```

Open <http://127.0.0.1:8000/docs>. `GET /health` and `GET /v1/provider` work
immediately, on the mock provider.

```bash
curl -s -X POST http://127.0.0.1:8000/v1/analyze \
  -H 'content-type: application/json' -d @../sample_request.json | python -m json.tool
```

**Things worth breaking on purpose**

- Send a 5-character `job_description`. Who rejects it — you, or the provider?
  (Check whether you were billed.)
- Set a deliberately wrong API key, restart with `LLM_PROVIDER=openai`, and
  call `/v1/analyze`. You get a 502 with `{"detail": "..."}`, not a raw 401 —
  the adapter's `except openai.APIError` catches it before it ever reaches
  your caller.

---

## Part 2 — Streaming Responses

Part 1 is already complete in this folder. Part 2 adds one endpoint:
`POST /v1/cover-letter/stream`.

**What you will fill in**

| TODO | File | What it does |
|---|---|---|
| 1 | `main.py` | Build the SSE generator and return a `StreamingResponse` |
| 2 | `providers/openai_provider.py` | `stream=True` + iterate deltas |

The mock provider already streams, and Anthropic's `stream()` is given (read
it after TODO 2, for comparison) — so both TODOs work with **no API key**.

**Run it**

```bash
cd part2
uvicorn app.main:app --reload
```

Open <http://127.0.0.1:8000/> — a small page that consumes the stream and
reports **time to first token** separately from **total time**. That gap is
the whole argument for streaming.

Swagger UI buffers, so it will lie to you about the stream. Watch the raw
protocol with curl instead:

```bash
curl -N -X POST http://127.0.0.1:8000/v1/cover-letter/stream \
  -H 'content-type: application/json' -d @../sample_request.json
```

`-N` disables curl's own buffering. Everything between your generator and the
user's eyeball wants to buffer — that is what `X-Accel-Buffering: no` is for.

**About client disconnects**

There is no explicit disconnect check, and none is needed. Starlette stops
pulling from your generator when the client goes away, so generation halts
after at most one more chunk — **you stop paying for free.**

What you do *not* get is a reliable place to notice it. An abandoned sync
generator is never closed explicitly, so a `finally` block fires whenever the
garbage collector gets round to it. If you need deterministic disconnect
logging, that is a genuine reason to reach for the async client and
`await request.is_disconnected()`.

**Things worth breaking on purpose**

- Change the trailing `\n\n` in `sse_event` to a single `\n`. The browser
  fires zero events and nothing reports an error. Remember this the day it
  happens to you.
- Start a generation, hit **Stop**, and watch the server log stop.
- Comment out `X-Accel-Buffering: no` and think about what nginx would do.
- Run `curl` **without** `-N` and compare.

---

## Part 3 — Structured Outputs with Pydantic

Parts 1 and 2 are complete in this folder. Part 3 adds the endpoint the
frontend actually wants: `POST /v1/fit-report`. It returns a `FitReport`
object — a score, a skills table, a gap list — instead of a paragraph
somebody has to parse.

Read this before you write any code:

```bash
cd part3
python -m app.fit
```

That prints the JSON Schema the model is constrained by, before and after we
fix it up for strict mode. **Every `description=` string in `app/fit.py` is
in there.** Those are not comments. They are prompt.

**What you will fill in**

| TODO | File | What it does |
|---|---|---|
| 1 | `main.py` | Send the schema, validate the result with `model_validate` |
| 2 | `providers/openai_provider.py` | `response_format` + `json_schema` + `strict` |

Anthropic's `structured()` is given (read it after TODO 2, for comparison) —
so both TODOs work with **no API key**, against the mock.

**Run it**

```bash
cd part3
uvicorn app.main:app --reload
```

```bash
curl -s -X POST http://127.0.0.1:8000/v1/fit-report \
  -H 'content-type: application/json' -d @../sample_request.json | python -m json.tool
```

**Things worth breaking on purpose**

- Delete `strictify(...)` and pass the raw Pydantic schema to OpenAI. Read the
  400 — it names the exact rule you broke.
- Set every `description=` to `""` and compare output quality. This is the most
  convincing experiment in the session.
- Change `match_score` to `str`. The model returns `"sixty-two"`. The schema is
  obeyed; your intent is not.
- In `app/providers/mock.py`, change `_CANNED_REPORT["match_score"]` to `137`
  (perfect JSON, impossible number) and call `/v1/fit-report` again.
  `model_validate` raises even though the JSON parsed cleanly — that is the
  whole argument for validating *after* constrained decoding, not instead of
  it. Notice it comes back as a raw 500, though: this minimal version has no
  handler for Pydantic's `ValidationError`, so as an exercise, add one that
  returns a clean 502 instead.
