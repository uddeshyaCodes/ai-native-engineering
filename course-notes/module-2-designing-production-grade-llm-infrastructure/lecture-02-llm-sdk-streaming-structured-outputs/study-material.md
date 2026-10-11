# Lecture 02: LLM SDK Integration, Streaming, and Structured Outputs

**Course:** AI-Enabled Software Engineering · **Module 2:** Designing Production-Grade LLM Infrastructure  
**Instructor:** Yubesh Patta (Assistant Professor, CSE, IIT Kharagpur)  
**TA / demos:** Subhajit Shah  
**Running example:** **KaryaSetu** - paste a job posting and experience notes; get fit analysis, a streamed cover letter, and a structured fit report  
**Workshop path:** `workshops/9-karyasetu/` (also copied to `projects/005-karyasetu/`)

---

## Learning outcomes (exam-ready)

By the end of this session you should be able to:

- Contrast **local FastAPI + DB** calls with **remote LLM** calls (latency, cost, non-determinism, rate limits).
- Explain why secrets live in **`.env`** (never commit API keys) and how **Pydantic Settings** loads/validates config.
- Prefer a vendor **SDK** over raw HTTP for typed responses, streaming helpers, typed exceptions, retries/backoff, connection pooling, and API evolution.
- Design a **provider seam** (`Protocol` + adapters + `ProviderError`) so routes never import OpenAI/Anthropic directly.
- Stream LLM tokens over **SSE** (`StreamingResponse`, `event:` / `data:` frames); know when **not** to stream.
- Enforce **structured outputs** with a Pydantic schema + provider constrained decoding (`json_schema` / tool use), then **`model_validate`** again in your app.

---

## Session map

| Block | Lecture focus | KaryaSetu demo |
|-------|---------------|----------------|
| **1 - LLM SDK integration** | Remote models, `.env`, SDK vs raw HTTP, OpenAI/Anthropic adapters | Part 1: `POST /v1/analyze` |
| **2 - Streaming** | Time-to-first-token UX, SSE vs WebSockets vs plain chunks | Part 2: `POST /v1/cover-letter/stream` + demo UI |
| **3 - Structured outputs** | JSON mode limits, schema-constrained decoding, `strictify` | Part 3: `POST /v1/fit-report` |

**Run (from a part folder):** `uvicorn app.main:app --reload`  
**Mock mode:** `LLM_PROVIDER=mock` needs no API key.

---

## Recap from Lecture 01 (why it matters today)

| Piece | Role for LLM apps |
|-------|-------------------|
| **Pydantic** | Validate request/response shapes; later, constrain model JSON |
| **Dependency injection** | Reusable request-scoped logic (settings, sessions) |
| **APIRouter / versioning** | Organised, evolvable endpoints |
| **RFC 9457** | Standard machine-readable errors |
| **OpenAPI** | Docs that reflect the contract |
| **ASGI (FastAPI)** | Long-lived connections for **streaming** tokens |

Last week: local DB, fast, deterministic, free unlimited calls.  
Today: the “other side” of the endpoint is a **remote model**.

---

## Part 1: Remote models and configuration

### What changes when the backend is a model

| Local DB (Lecture 01) | Remote LLM (today) |
|-----------------------|--------------------|
| Fast, local | **Higher latency** |
| Deterministic | **Non-deterministic** |
| Free / unlimited for demos | **Costs money**; not unlimited |
| Failures are mostly your code/DB | Provider errors, auth, rate limits, outages |

### `.env` files

- Hold **credentials and knobs**: `OPENAI_API_KEY`, provider choice, model name, `MAX_TOKENS`, `TEMPERATURE`, etc.
- **Do not commit** `.env` to public or shared repos - keys would leak.
- Commit **`.env.example`** (placeholders only); keep real keys local.
- KaryaSetu uses **`pydantic-settings`** (`BaseSettings`, `env_file=".env"`) so config is typed and validated - better than bare `python-dotenv` for this course (validation for free).

---

## Part 1: SDK vs raw HTTP

**Goal:** Python program → ask a remote model → get text back.

### Raw request (possible, but painful)

1. Read API key from env.
2. `requests.post` (or similar) to the provider URL.
3. Set headers (`Authorization`, `Content-Type`).
4. Build JSON body (model, messages/prompt).
5. Parse `response.text` / JSON yourself and dig out nested fields (e.g. `choices[0].message.content`).

Demo prompt used in lecture: *“How many R’s are in the word strawberry?”* (Groq keys used in class).

### What the SDK buys you

None of this is impossible by hand - the SDK is **tested and maintained for you**.

| Benefit | Raw HTTP | With SDK |
|---------|----------|----------|
| **Typed response** | String / dict you parse yourself; IDE cannot guide nested fields | Object types (e.g. chat completion) with attributes → IDE autocomplete |
| **Streaming** | Parse raw SSE lines yourself | Iterate already-parsed chunk objects |
| **Typed exceptions** | Branch on status codes (e.g. **401** = bad key) | Catch provider types (e.g. authentication error) |
| **Exponential backoff** | Easy to write a dumb retry loop (even on 401) | Retries with backoff; **skips** non-retryable errors (bad key) |
| **Connection pooling** | New TCP handshake per `post` | Reuse pooled connections across calls |
| **API versioning / aliases** | Brittle string paths into JSON; rename of `content` → `text` breaks you | SDK maintainers can keep aliases so old client code survives renames |

**Exponential backoff (exam):** attempt 1 fails → wait 1s; attempt 2 → 2s; attempt 3 → 4s; … Do **not** hammer a server (or a known-bad API key) in a tight loop.

---

## Part 1: Provider seam (KaryaSetu architecture)

Routes should **not** `import openai` / `import anthropic` directly.

| Piece | Role |
|-------|------|
| **`Completion`** | Normalised result: `text`, `model`, `provider` |
| **`ProviderError`** | Vendor-neutral exception (wrap OpenAI/Anthropic/mock errors) |
| **`LLMProvider` Protocol** | `complete` (and later `stream`, `structured`) |
| **`build_provider(settings)`** | Switch on `LLM_PROVIDER` → mock / openai / anthropic |
| **Adapters** | `openai_provider.py`, `anthropic_provider.py` - only files that import SDKs |
| **`MockProvider`** | Runs with no key for demos and CI |

**Why a custom `ProviderError`?** Wrap vendor-specific exceptions into **one** type so you can add DeepSeek, Google, Meta later without leaking five exception hierarchies into routes.

**OpenAI vs Anthropic (lecture points):** Anthropic often treats `system` as a **top-level** parameter (not a message), requires `max_tokens`, and returns a **list of content blocks** you filter by type.

**Endpoint (Part 1):** `POST /v1/analyze` - system + user prompt from job description + notes; return analysis + provider metadata + latency.

---

## Part 2: Streaming responses

### UX motivation (Priya story)

- Full answer may take **~6-10 seconds**; **time to first token** may be **~300 ms**.
- Non-streaming: blank screen → user thinks the app is broken → closes the tab.
- Streaming: first words appear quickly; **total server time may be unchanged**, but perceived UX is alive.
- Streaming does **not** make the model faster - it stops **holding** tokens until the end.

### How streaming works under the hood

1. Model generates **one token at a time**.
2. Non-streaming: provider **buffers** everything, then one response.
3. Streaming: provider **forwards each token** as produced (HTTP **chunked transfer**; often **no** fixed `Content-Length` - length unknown ahead of time).
4. **ASGI** (from Lecture 01) enables long-lived write-over-time; classic WSGI one-shot return does not fit this pattern well.

### Ways a server can push chunks

| Approach | Notes |
|----------|--------|
| **Plain chunked text** | Simplest; **no room** for named metadata or in-band errors |
| **SSE (Server-Sent Events)** | Named `event:` + `data:` frames; **server → client** only; browser auto-reconnect helpers; **best fit for LLM output** |
| **WebSockets** | Different protocol; **bidirectional** - use when client and server must talk mid-stream |

**Rule of thumb:** server talks, client listens → **SSE**. Both talk at once → **WebSockets**.

### SSE wire shape (curl / raw protocol)

Typical KaryaSetu frames:

```text
event: start
data: {"provider":"mock","model":"..."}

event: token
data: {"text":"Dear"}

event: done
data: {"chars":123}
```

On failure mid-stream you cannot change the HTTP status (headers already sent as **200**) - send an **`error` event** in-band instead.

### SDK streaming

- Add `stream=True` (OpenAI-style) or use Anthropic’s stream context manager.
- Iterate chunks; yield only **truthy** `delta.content` (skip role-only / empty / usage-only chunks).
- FastAPI: return `StreamingResponse(..., media_type="text/event-stream", headers=SSE_HEADERS)` with `Cache-Control: no-cache` and often `X-Accel-Buffering: no`.

**Endpoint (Part 2):** `POST /v1/cover-letter/stream` + demo page at `/`.

### Should you always stream?

**No.**

| Stream? | When |
|---------|------|
| **Yes** | A human is **reading progressively** (cover letter, chat prose) |
| **No** | UI needs a **complete valid object** before render (fit report card with score) - partial JSON is useless |

KaryaSetu choice: **cover letter streams**; **fit report does not**.

---

## Part 3: Structured outputs

### Why free-form text is not enough

If the frontend needs fields like `verdict`, `match_score`, `skills`, asking in prose (“please reply as JSON”) is unreliable - keys and enums drift.

### JSON mode vs schema-constrained decoding

| Approach | What you get |
|----------|----------------|
| **JSON mode** (`json_object`) | Valid JSON blob; **keys not enforced** (rating vs score) |
| **JSON Schema / strict mode** | Decoder constrained to your schema (enums, ranges, required keys) |
| **Anthropic tool-use pattern** | Define a tool whose `input_schema` is your shape; force `tool_choice`; read **tool arguments** |

### Pydantic as the form the model fills

Example ideas from lecture / `fit.py`:

- `verdict`: `Literal["strong_match", "possible_match", "weak_match"]` - no inventing “poor_match”
- `match_score`: `ge=0`, `le=100`
- Field **`description=` strings are prompt** - they serialise into the JSON Schema the model sees

**`strictify`:** OpenAI strict mode wants every property **required** and `additionalProperties: false` on objects; Pydantic’s default schema does not - walk the schema (and `$defs`) to bridge the gap.

**Still call `FitReport.model_validate(raw)`** after the provider returns: constrained decoding guarantees **shape**, not that `137` is a sensible score or that mock providers enforced anything.

**Endpoint (Part 3):** `POST /v1/fit-report`.

**Help the model:** if only a few possibilities exist, encode them in the schema - models are trained to always say *something*; schema steers *what* they can say.

---

## End-to-end mental model

```text
Client ──► FastAPI routes
              │
              ├── Settings (.env via pydantic-settings)
              │
              └── LLMProvider seam
                    ├── MockProvider
                    ├── OpenAIProvider  (SDK) ──► remote model
                    └── AnthropicProvider (SDK) ──► remote model

/v1/analyze          → complete()      → prose
/v1/cover-letter/*   → stream() + SSE  → tokens
/v1/fit-report       → structured()    → dict → FitReport.model_validate
```

---

## Key takeaways

1. Remote LLMs are **slow, costly, and non-deterministic** - design for that.
2. **SDKs** beat raw HTTP for production plumbing (types, errors, retries, pooling, streaming helpers).
3. Keep a **provider seam** so vendor SDKs stay at the edge.
4. **SSE** is the usual transport for LLM tokens; mid-stream failures are **events**, not new status codes.
5. Stream when humans read incrementally; **buffer** when the UI needs a whole structured object.
6. **Pydantic schemas + constrained decoding** beat “please return JSON” prompts; still validate in your app.
