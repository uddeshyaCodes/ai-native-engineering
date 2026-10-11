# Lecture 02: In-Lecture Quizzes

Live polls were run between lecture blocks and demos (Professor Patta / TA Subhajit Shah). The transcript records **correct answers and explanations** for several items; some stems/options are incomplete on audio. Where stems are thin, questions below are **reconstructed from the immediately preceding lecture content** (same approach as other notes) and labelled accordingly.

---

## In-lecture Quiz 1 - After Part 1 (SDK / KaryaSetu providers)

**When:** After Part 1 demo discussion (provider seam, `.env`, OpenAI/Anthropic adapters).

### Q1. Why create a custom `ProviderError`?

**Stem (lecture):** Motivation for a custom error type wrapping vendor failures.

| | |
|---|---|
| **Correct ✓** | **Wrap vendor-specific errors into one error type** so the app (and future vendors) share a single surface |

**Live result:** Most correct; instructor re-emphasised the “one error type” motivation (e.g. adding DeepSeek later).

**Explanation:** Routes catch `ProviderError` only - not OpenAI’s hierarchy and Anthropic’s hierarchy separately.

---

### Q2. Which library is used for KaryaSetu application configuration?

**Stem (lecture):** “Which library is mentioned as being used for the KaryaSetu application’s configurations?”

| Option (from discussion) | |
|--------------------------|---|
| `python-dotenv` alone | Possible elsewhere, but **not** what the demo uses for Settings |
| **`pydantic-settings` ✓** | **`BaseSettings` reads `.env` with validation** |

**Live result:** Confusing for some (many know `python-dotenv`); majority for **pydantic-settings**.

**Explanation:** Instructor showed `BaseSettings` / `SettingsConfigDict(env_file=".env")` and noted pydantic-settings gives **validation**, which plain dotenv does not.

---

## In-lecture Quiz / discussion 2 - Streaming

**When:** After streaming UX + SSE vs WebSockets discussion; before / during Part 2 demo wrap-up.

### Q3. Should you always stream LLM responses?

**Stem (lecture):** Thumbs-up / thumbs-down: always stream?

| | |
|---|---|
| **Correct ✓** | **No** - do not always stream |

**Live result:** Many thumbs-up for “always stream”; instructor corrected to **no**.

**Explanation:** Stream when a human reads tokens progressively (cover letter). Do **not** stream when the UI needs a finished validated object (fit report). Providers can stream JSON fragments, but partial structured UI is useless until valid.

---

## In-lecture Quiz 3 - Structured outputs (Part 3)

**When:** Around Part 3 demo / wrap-up. Individual Mentimeter stems are not fully transcribed; the following are reconstructed from the structured-output block.

### Q4. (Reconstructed) JSON mode vs schema-constrained decoding

| | |
|---|---|
| **Correct concept ✓** | JSON mode yields a JSON object but **does not enforce your keys/enums**; pass a **JSON Schema** (from Pydantic) for constrained decoding |

### Q5. (Reconstructed) Cover letter vs fit report transport

| Endpoint | |
|----------|---|
| Cover letter | **SSE stream** |
| Fit report | **Buffered** structured JSON (no progressive stream) |

---

## Quick self-check (from lecture claims)

| Claim | True / False |
|-------|----------------|
| Streaming reduces total model compute time | **False** - UX / TTFB perception changes |
| SSE is typically one-way (server → client) | **True** |
| Mid-stream provider failure can freely change HTTP status | **False** - use in-band error event |
| Field `description=` on Pydantic models can act as prompt in the schema | **True** |
