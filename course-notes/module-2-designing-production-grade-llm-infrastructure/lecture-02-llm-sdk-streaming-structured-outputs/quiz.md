# Lecture 02: In-Lecture Quizzes

Live polls were run between lecture blocks and demos (Professor Patta / TA Subhajit Shah). Questions and options below are taken verbatim from the Mentimeter deck "Session 2" (12 questions across Parts 1-3). **Correct answers follow the answer-key slide that sits after each question in the deck**; live-result notes come from the transcript where recorded.

---

## In-lecture Quiz 1 - After Part 1 (SDK / KaryaSetu providers)

**When:** After Part 1 demo discussion (provider seam, `.env`, OpenAI/Anthropic adapters).

### Q1. SDK benefit for unstable networks

**Stem:** Which specific benefit of using a model SDK, rather than raw httpx or requests calls, addresses the issue of unstable network conditions?

| Option | |
|---|---|
| A | No Built-in retries that understand HTTP errors. |
| B | Enforcement of a 'strict' mode that prevents the model from hallucinating technical facts. |
| C | Automatic translation of model output into different natural lannguages for global users. |
| **D ✓** | **Built-in retries with exponential backoff that understand HTTP errors.** |

**Explanation (answer key):** SDKs include logic to distinguish errors that should be retried (like 429 or 503) from those that shouldn't (like 400).

---

### Q2. Required parameter in Anthropic Messages API

**Stem:** Which parameter is strictly REQUIRED in the Anthropic Messages API but optional or handled differently in OpenAI?

| Option | |
|---|---|
| A | model |
| B | temperature |
| **C ✓** | **max_tokens** |
| D | system_prompt |

**Explanation (answer key):** `max_tokens` is required by the Anthropic adapter; the others are not.

---

### Q3. Role of `ProviderError`

**Stem:** What is the primary role of the custom ProviderError exception defined in the application?

| Option | |
|---|---|
| **A ✓** | **To wrap vendor-specific exceptions to see only one error type.** |
| B | To automatically log the error message with the number of tokens used during a failed request. |
| C | To provide a way to bypass the FastAPI exception handler for faster debugging. |
| D | To identify which specific line of code in the SDK caused the failure. |

**Live result:** Most correct; instructor re-emphasised the "one error type" motivation (e.g. adding DeepSeek later).

**Explanation:** By catching SDK errors and raising a `ProviderError`, the developer keeps vendor implementation details out of the app. Routes catch `ProviderError` only - not OpenAI's hierarchy and Anthropic's hierarchy separately.

---

### Q4. Configuration library in KaryaSetu

**Stem:** Which library is mentioned as being used for the 'KaryaSetu' application's configuration and environment variable management?

| Option | |
|---|---|
| A | os.environ |
| B | python-dotenv |
| **C ✓** | **pydantic-settings** |
| D | FastAPI.Config |

**Live result:** Confusing for some (many know `python-dotenv`); majority for **pydantic-settings**.

**Explanation:** `SettingsConfigDict(env_file=".env")` on a `BaseSettings` class loads configuration from `.env`, and pydantic-settings adds **validation**, which plain dotenv does not.

---

## In-lecture Quiz 2 - After Part 2 (Streaming)

**When:** After streaming UX + SSE vs WebSockets discussion; before / during Part 2 demo wrap-up.

### Q5. Return type of `create(..., stream=True)`

**Stem:** In the context of the OpenAI SDK, what fundamental change occurs to the return type of the chat.completions.create method when stream=True is passed?

| Option | |
|---|---|
| A | It returns a model containing the final character count. |
| B | It returns a generator function of strings instead of a single string. |
| C | It returns a standard HTTP response object that must be manually parsed. |
| D | It returns an iterator of chunks instead of a single response object. |

**Answer key says: Option 2 (B)** - "The method does not wait for all strings to be ready to return a list; it provides them one by one."

> ⚠️ **Check this one.** Technically **D** is the more accurate answer: with `stream=True` the SDK returns a `Stream` you iterate over, yielding **chunk objects** (`ChatCompletionChunk`, with text in `choice.delta.content`), not plain strings. B is what the deck's key records, and the "one by one" idea is the same, so use B if matching the course key and D if matching the SDK.

---

### Q6. Why a context manager for Anthropic streaming

**Stem:** Why does the Anthropic provider adapter use a context manager (the with statement) for its streaming implementation?

| Option | |
|---|---|
| A | It is required to encrypt the tokens before they are yielded. |
| B | It speeds up the generation process by 90 milliseconds. |
| **C ✓** | **It ensures the underlying HTTP connection is properly closed if the client hangs up mid-generation.** |
| D | It allows the provider to switch models dynamically during a single request. |

**Explanation (answer key):** The context manager guarantees cleanup so the connection isn't leaked, even on unexpected disconnects.

---

### Q7. HTTP mechanism behind streaming

**Stem:** What is the underlying HTTP mechanism that enables streaming responses in modern web frameworks like FastAPI?

| Option | |
|---|---|
| A | The use of BaseSettings` to increase the timeout limit of the gateway server. |
| B | A technique that periodically refreshes the client's browser cache. |
| C | The RFC 9457 standard for machine-readable problem details in HTTP responses. |
| **D ✓** | **Chunked transfer encoding, which allows the server to send data without knowing the final Content-Length.** |

**Explanation (answer key):** The server keeps the connection open and sends data in parts, which requires omitting the total-size header.

---

### Q8. SSE vs WebSockets

**Stem:** When should an architect choose Server-Sent Events (SSE) over WebSockets for an LLM integration?

| Option | |
|---|---|
| **A ✓** | **When the communication is primarily one-way (server to client) and requires automatic browser reconnection.** |
| B | When the client needs to send frequent, low-latency updates back to the server during the generation process. |
| C | When the response data contains binary files, such as generated images or audio clips. |
| D | When the application must support legacy browsers that do not have an event loop. |

**Explanation (answer key):** SSE is simpler and more robust for streaming LLM text where the client just listens for the output of a prompt.

---

### Discussion poll - Should you always stream LLM responses?

*(Thumbs-up / thumbs-down poll from the lecture, not in the Menti deck.)*

| | |
|---|---|
| **Correct ✓** | **No** - do not always stream |

**Live result:** Many thumbs-up for "always stream"; instructor corrected to **no**.

**Explanation:** Stream when a human reads tokens progressively (cover letter). Do **not** stream when the UI needs a finished validated object (fit report). Providers can stream JSON fragments, but partial structured UI is useless until valid.

---

## In-lecture Quiz 3 - After Part 3 (Structured outputs)

**When:** Around Part 3 demo / wrap-up.

### Q9. Why still call `model_validate()`

**Stem:** Why is a call to Pydantic's model_validate() still recommended after the LLM return?

| Option | |
|---|---|
| A | Constrained decoding only ensures the JSON parses, not that it follows a specific schema. |
| **B ✓** | **The decoder guarantees the structural shape but does not enforce business logic like range constraints ($ge=0, le=100$).** |
| C | Strict Mode only works with flat objects and fails to validate nested Pydantic models automatically. |
| D | OpenAI converts all numeric outputs to strings, requiring a validation step to cast them back to integers. |

**Explanation (answer key):** The LLM is forced to follow the schema types, but Pydantic validation is needed for field-level rules like minimums and maximums.

---

### Q10. Role of `Field(description="...")`

**Stem:** What is the primary role of a Pydantic Field(description="...") when generating structured outputs?

| Option | |
|---|---|
| A | It defines the variable name that will be used in the generated JSON object. |
| B | It acts as a metadata tag for the frontend to render tooltips for the user. |
| **C ✓** | **It functions as a prompt that is embedded directly into the JSON Schema sent to the LLM.** |
| D | It serves as internal developer documentation that is stripped out before reaching the model. |

**Explanation (answer key):** Field descriptions are treated as part of the instructions the model uses to understand how to populate specific keys.

---

### Q11. What triggers constrained decoding in the OpenAI adapter

**Stem:** In the OpenAI adapter implementation, which parameter in the response_format dictionary triggers 'constrained decoding'?

| Option | |
|---|---|
| A | "type": "json_object" |
| **B ✓** | **"strict": True** |
| C | "name": name |
| D | "max_tokens": self.s.max_tokens |

**Explanation (answer key):** Setting `strict` to true within the `json_schema` configuration enables constrained decoding. Plain `json_object` (JSON mode) yields valid JSON but does **not** enforce your keys/enums.

---

### Q12. Two endpoints: `/v1/cover-letter/stream` and `/v1/fit-report`

**Stem:** Why does the source recommend having two separate endpoints: /v1/cover-letter/stream and /v1/fit-report?

| Option | |
|---|---|
| A | To keep the code base organized by file type. |
| **B ✓** | **Because paragraphs (cover letters) benefits from streaming, while reports (fit reports) require structure.** |
| C | To allow the cover letter to be written in a different language. |
| D | Because the fit report is too confidential to be streamed. |

**Explanation (answer key):** Prose is for human reading as it arrives (**SSE stream**); structured data is for software consumption and must be complete to be useful (**buffered** JSON).

---

## Quick self-check (from lecture claims)

| Claim | True / False |
|-------|----------------|
| Streaming reduces total model compute time | **False** - UX / TTFB perception changes |
| SSE is typically one-way (server → client) | **True** |
| Mid-stream provider failure can freely change HTTP status | **False** - use in-band error event |
| Field `description=` on Pydantic models can act as prompt in the schema | **True** |

---

## Summary

| Quiz | When | Questions | Main topics |
|------|------|-----------|-------------|
| **1** | After Part 1 | **4** | SDK retries, Anthropic `max_tokens`, `ProviderError`, pydantic-settings |
| **2** | After Part 2 | **4** (+1 discussion poll) | `stream=True` return type, context manager, chunked encoding, SSE vs WebSockets, "always stream?" |
| **3** | After Part 3 | **4** | `model_validate()`, `Field(description)`, `strict: True`, two endpoints |

**Total Menti questions:** **12** (4 + 4 + 4), plus 1 discussion poll.
