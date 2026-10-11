# Lecture 02: Important Exam Q&A

Practice questions aligned with lecture emphasis and in-class quizzes. Answers are concise for MCQ revision.

---

## Remote models & config

### Q1. How do today’s remote LLM calls differ from last week’s local DB calls?

**A.** They are typically **slower**, **non-deterministic**, **cost money**, and are **not unlimited** - unlike local, fast, deterministic, free demo DB calls.

### Q2. Why use a `.env` file for API keys?

**A.** So **credentials are not hard-coded** or committed to repos. Keep `.env` local; ship `.env.example` without secrets.

### Q3. Which library does KaryaSetu use to load `.env` with validation?

**A.** **`pydantic-settings`** (`BaseSettings`) - not only `python-dotenv` (dotenv alone does not validate types/constraints).

---

## SDK vs raw HTTP

### Q4. Name four benefits of a vendor SDK over raw `POST` requests.

**A.** Any four: **typed responses**, **streaming helpers**, **typed exceptions**, **exponential backoff / smart retries**, **connection pooling**, **API evolution / aliases**.

### Q5. What is the downside of treating a raw HTTP body as a plain string?

**A.** You must **parse JSON yourself** and know the exact nested path (e.g. `choices[0].message.content`); the IDE cannot guide attributes.

### Q6. Why is retrying forever on HTTP 401 (bad API key) a bad idea?

**A.** Auth failure will not succeed by retrying - you need a **valid key**. SDKs typically **do not retry** non-retryable errors like bad auth.

### Q7. What is exponential backoff?

**A.** After failures, wait **increasing** delays (e.g. 1s, 2s, 4s, 8s…) instead of tight-loop retries - useful for temporary server load.

### Q8. Can you achieve everything an SDK does with raw HTTP?

**A.** **Yes in principle** - but you must implement parsing, retries, pooling, streaming, and error mapping yourself. SDKs are maintained and tested for you.

---

## Provider seam

### Q9. Why introduce a custom `ProviderError`?

**A.** To **wrap vendor-specific exceptions** into one app-level type so routes do not depend on OpenAI/Anthropic exception hierarchies, and new vendors can be added cleanly.

### Q10. What should application routes import for LLM calls?

**A.** The **provider seam** (`complete` / `stream` / `structured` on a protocol) - **not** `import openai` / `import anthropic` in route files.

### Q11. What does `MockProvider` buy you?

**A.** The app runs with **`LLM_PROVIDER=mock`** and **no API key** for demos, teaching, and offline work.

---

## Streaming & SSE

### Q12. What UX problem does streaming solve?

**A.** Long waits with a **blank UI** feel broken. Streaming improves **time-to-first-token** visibility even if **total** generation time is unchanged.

### Q13. Does streaming make the model generate faster?

**A.** **No** - it stops buffering the full answer on the server; tokens are forwarded as produced.

### Q14. Why is SSE a better default than plain chunked text for LLM apps?

**A.** SSE supports **named events** and structured **data** frames (start/token/done/error). Plain chunks have little room for metadata or in-band errors.

### Q15. When would you choose WebSockets over SSE for AI?

**A.** When the channel must be **bidirectional** mid-stream (client and server both send continuously). If only the **server** pushes tokens → SSE.

### Q16. Should you always stream every LLM endpoint?

**A.** **No.** Stream when a human reads incrementally (e.g. cover letter). Do **not** stream when the UI needs a **complete validated object** first (e.g. fit report).

### Q17. If the provider fails on token 400 of an SSE response, can you return HTTP 502?

**A.** Usually **no** - status was already **200** once streaming started. Send an in-band **`error` event** instead.

---

## Structured outputs

### Q18. What is wrong with “JSON mode” alone for UI fields?

**A.** You get a JSON object, but **keys and enums are not reliably enforced** (e.g. `rating` vs `score`).

### Q19. How does a Pydantic `FitReport` help the model?

**A.** It becomes a **JSON Schema** (with field descriptions as prompt) that constrains decoding - e.g. fixed `verdict` literals and `match_score` 0-100.

### Q20. Why still call `model_validate` after constrained decoding?

**A.** Constrained decoding guarantees **shape**; app validation still catches nonsense values and works for providers (e.g. mock) without strict mode.

### Q21. How does Anthropic’s structured approach differ (lecture)?

**A.** Often **tool use**: force a tool whose input schema is your shape and read the **tool arguments**, rather than free-form JSON text.
