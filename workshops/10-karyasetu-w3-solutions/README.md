# KaryaSetu — Week 3 Solutions

**Instructor copy. Do not share with students.**

Identical to the student boilerplate, except every TODO now has working code
underneath it. As in Week 2, the TODO comment blocks are left exactly as
students see them, and the solution follows immediately, closed with:

```python
        # -- end of solution
```

(The `raise NotImplementedError(...)` stub is the only thing removed. In
`fit_v2.md` there is no end marker, because it would be sent to the model.)
Diff `dist/student` against `dist/solutions` to see precisely what gets typed
in each demo.

| Part | Concept | TODO 1 | TODO 2 |
|---|---|---|---|
| 1 | System prompts | `app/prompts/fit_v2.md` | `render_user_message()` in `app/prompting.py` |
| 2 | Few-shot & chain-of-thought | `build_history()` in `app/prompting.py` | `with_reasoning()` in `app/fit.py` |
| 3 | Docker dev-mode | `Dockerfile` (two blocks: dependency layer, dev `CMD`) | `compose.yaml` (`ports`, `env_file`, `volumes`) |

The demo scripts are in [INSTRUCTOR_NOTES.md](INSTRUCTOR_NOTES.md).

## What changed from Week 2's code (read this before class)

- **Shared `.env` across parts.** A single `.env` at the project root (copied
  from `.env.example`) is shared by `part1`, `part2`, and `part3` without
  needing duplicate `.env` files in each folder. `compose.yaml` mounts `../.env`.
- **Anthropic adapter: `temperature` removed.** The current Anthropic SDK
  (`anthropic==1.7.0`) no longer accepts `temperature`; Week 2's
  `temperature=` line raises `TypeError`. `Settings.temperature` now affects
  OpenAI only. If any student is still on Week 2's code with an unpinned
  `anthropic`, delete the three `temperature=` lines in
  `providers/anthropic_provider.py`.
- **`.env.example` defaults to `mock`.** Week 2's example said `openai`, which
  crashes on startup without a key.
- **`FitReport.match_score` no longer says "be strict; do not inflate".** That
  calibration moved into the Part 1 system prompt. Left in the schema it would
  quietly fix the Flattery Bug and the demo would not reproduce.
- **New invariants on `FitReport`** (verdict must agree with score; a
  `strong_match` cannot have most requirements missing), and a handler turning
  Pydantic's `ValidationError` into a clean 502 — Week 2's README left that as
  an exercise.
- **Adapters** notice output cut off by `max_tokens` (default raised to 1500),
  and OpenAI refusals. `OPENAI_BASE_URL` lets the OpenAI adapter talk to any
  OpenAI-compatible endpoint (OpenRouter, Groq, a local server).
- **Dependencies are pinned with `==`.**
- **`sse.py`'s comment about nginx is corrected** — see Part 3 in the notes.

## Verification status — what was and was not tested

Checked in a sandbox, before you got this:

- All three solution trees pass their test suites (37 / 68 / 85), in a **fresh**
  virtualenv installed from the pinned requirements, including when a `.env`
  selects a real provider with no key.
- The student trees boot, and fail *only* the TODO tests. Deliberately wrong
  answers (single-pass stripping, reasoning placed last, `COPY . .` before
  `pip install`, key pasted into compose, ...) are each caught by a test.
- The OpenAI and Anthropic adapters were run against the real SDKs with a fake
  HTTP transport: request shape (system placement, few-shot turns, strict schema,
  forced tool choice) and the truncation/refusal guards.
- Both Dockerfiles pass `hadolint`; `compose.yaml` validates against the official
  Compose specification schema.
- `nginx/default.conf` was run, unchanged apart from hostname and port, in front
  of the real app: **51 ms** to first token with the header, **2,789 ms** (one
  lump) without it.

**Not** tested, because the sandbox had no API keys, network access to the
vendors, or Docker:

- **Anything against a real model.** The eval labels and few-shot examples are
  hand-written. Run `python -m app.evals --prompt v1` and `--prompt v2` with your
  key **before class**, and if a label looks wrong to you, fix the label.
- **`docker build` / `docker compose up` themselves.** Run both once on the
  machine you will teach from, with the images already pulled.
