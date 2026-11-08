# Module 2: Designing Production-Grade LLM Infrastructure

Study notes derived from lecture transcripts.

**Style:** British English; use a normal hyphen (`-`) instead of long dashes.

**Source transcripts:** [`transcripts/module-2/`](../../transcripts/module-2/)

---

## Lectures

| # | Folder | Topic | Instructor (from transcript) |
|---|--------|--------|------------------------------|
| 01 | [lecture-01-fastapi-architecture-rest-api-design](./lecture-01-fastapi-architecture-rest-api-design/) | FastAPI architecture, ASGI/WSGI, Pydantic, DI, routers, versioning, RFC 9457, OpenAPI | Yubesh Patta (IIT Kharagpur); demos: Subhajit Shah |
| 02 | [lecture-02-llm-sdk-streaming-structured-outputs](./lecture-02-llm-sdk-streaming-structured-outputs/) | KaryaSetu — LLM SDKs vs raw HTTP, SSE streaming, structured outputs | Yubesh Patta (IIT Kharagpur); demos: Subhajit Shah |
| 03 | [lecture-03-prompts-as-contracts-docker-dev-mode](./lecture-03-prompts-as-contracts-docker-dev-mode/) | KaryaSetu Week 3 — prompts as contracts, injection, few-shot/CoT, Docker | Yubesh Patta (IIT Kharagpur); demos: Subhajit Shah |
| 04 | [lecture-04-multimodal-documents-ocr-celery](./lecture-04-multimodal-documents-ocr-celery/) | Multimodal documents - PDF/CSV/Excel, OCR (Pillow, OpenCV, Tesseract, vision LLMs), FastAPI + Celery | IIT Kharagpur professor (name unclear in transcript); demos: Salma |
| 05 | [lecture-05-webhooks-llm-cost-prompts-dpdp](./lecture-05-webhooks-llm-cost-prompts-dpdp/) | Webhooks and callbacks, LLM cost tracking (tiktoken, LiteLLM, Langfuse), prompt versioning and LLM-as-judge evals, DPDP Act, Presidio PII anonymisation | IIT Kharagpur professor (name unclear in transcript); demos: Salma, Dipanita, Taranum |
| Rev | [revision-class-lectures-04-05](./revision-class-lectures-04-05/) | Revision: Celery, RabbitMQ (round robin, fair dispatch, acks, durability), webhooks, integrated document pipeline | IIT Kharagpur professor (name unclear in transcript); demo: Salma |

Each lecture folder has:

| File | Purpose |
|------|---------|
| `study-material.md` | Structured exam-ready notes |
| `important-questions.md` | Practice Q&As |
| `quiz.md` | Quizzes/polls asked in the lecture |

---

## Suggested study order

1. `quiz.md` (in-lecture Mentimeter)
2. `important-questions.md`
3. `study-material.md` for gaps
