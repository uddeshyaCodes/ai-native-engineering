# Lecture 03: Prompts as Contracts, and Docker Dev-Mode

**Course:** AI-Enabled Software Engineering · **Module 2:** Designing Production-Grade LLM Infrastructure  
**Instructor:** Yubesh Patta / Jibesh (Assistant Professor, CSE, IIT Kharagpur)  
**TA / demos:** Subhajit Shah  
**Running example:** **KaryaSetu** Week 3 - versioned system prompts, injection-safe user assembly, few-shot + reasoning, Docker  
**Workshop path:** `workshops/10-karyasetu-w3-stub/` (solutions: `workshops/10-karyasetu-w3-solutions/`)

> **Transcript note:** Source is a WEBVTT capture (`lecture-03-prompts-as-contracts-docker-dev-mode.txt`). Names like “Talker” = **Docker**, “feed/fit” = **fit** report, “few short” = **few-shot**.

---

## Learning outcomes (exam-ready)

By the end of this session you should be able to:

- Treat a **prompt as a contract**: specify (system prompt), constrain (schema/validators), test (evals), ship (Docker).
- Write a structured **system prompt** (ROLE / TASK / RULES / UNTRUSTED INPUT / IF UNSURE) with **testable** rules.
- Explain **sycophancy / flattery bugs** as **spec bugs**, not model bugs.
- Defend against **prompt injection** (direct vs indirect; OWASP LLM Top 10 #1): fence, strip-until-stable, least privilege, eval trap cases.
- **Version** prompts (`fit_v1` → `fit_v2`); never silently edit a released prompt.
- Use **few-shot** examples (strong / boundary / weak) formatted like live input; use **reasoning-first** schema fields carefully (cost, latency, truncation).
- Explain **Docker image vs container**, layers, `.dockerignore` for secrets, and **rebuild** after dependency changes.

---

## Session map

| Block | Lecture focus | KaryaSetu demo |
|-------|---------------|----------------|
| **1 - System prompts** | Prompt roles, anatomy, injection defences, versioning, evals | Part 1: `fit_v2.md`, `render_user_message()` |
| **2 - Few-shot & CoT** | Examples as contract; reasoning-first schema; measure with a grid | Part 2: `build_history()`, `with_reasoning()` |
| **3 - Docker** | Image/container, Dockerfile layers, compose, secrets | Part 3: `Dockerfile`, `compose.yaml` |

**Week 2 recap (why this lecture):** SDKs beat raw HTTP; streaming helps UX but does not speed the model; Pydantic field descriptions act as prompt; cover letter streamed, fit report buffered; **system prompt was hard-coded in `main.py`**.

**Framing question this week:** *Who wrote the instructions the model follows, and how do we know they are any good?*

---

## Prompt as a contract (overview)

| Step | Meaning |
|------|---------|
| **Specify** | System prompt states what the model **must** do |
| **Constrain** | Schema + validators enforce what a prompt can only ask for |
| **Test** | Evals measure how often the model **obeys** |
| **Ship** | Docker makes “works on my laptop” mean “works everywhere” |

---

## Part 1: System prompts (the spec)

### Three prompt roles

| Role | Who writes it | Trust |
|------|---------------|-------|
| **System** | Developer standing rules (who the model is; must / must-not) | **Trusted** - highest weight |
| **User** | End-user content (job posting + experience notes) | **Untrusted** |
| **Assistant** | Prior model outputs in a multi-turn history | Model’s own past words |

Models are trained to weight **system above user**. Never treat user text as instructions.

### Anatomy of a good system prompt

Typical sections (Week 3 workshop):

1. **ROLE** - persona (e.g. blunt technical recruiter assessing fit)  
2. **TASK** - one or two sentences: what to do  
3. **RULES** - concrete, **testable** rules (what to do, not only what to avoid)  
4. **UNTRUSTED INPUT** - declare fenced regions as **data, never commands**  
5. **IF UNSURE** - say so / do not invent (models are trained to always answer)

Output shape is largely the **Pydantic / JSON schema** from Week 2 (not a free-form “OUTPUT” prose section).

**Vague vs testable:** “Be accurate” is vague. “`match_score` must be 0-100 and agree with `verdict` bands” is testable.

### Flattery / sycophancy bug (Madhu & Priya story)

- Spec said: *“Be warm and encouraging… many students are anxious.”*  
- Priya: job needs 8+ years; she has 2 → model still returns **strong match**.  
- That is a **spec bug** (sycophancy / flattery), not an LLM mysteriously “broken.”  
- Fix: rewrite the contract (`fit_v2`), do not merely hope the model ignores encouragement.

### Prompt injection

- **Definition:** user content alters model behaviour/output in unintended ways.  
- **OWASP LLM Top 10 (2025):** prompt injection listed as **#1**.  
- **Direct:** user types “ignore previous instructions…” in notes.  
- **Indirect:** injection hidden inside a **job posting** someone else wrote.  
- Takeaway: **never concatenate raw user text** into the model call without fencing/sanitising.

### Defence layers (shrink blast radius; do not claim “impossible”)

1. **Fence** - wrap posting/notes in delimiters (e.g. `<JOB_POSTING>…</JOB_POSTING>`); system prompt says content inside is **data only**.  
2. **Strip until stable** - remove delimiter-like tags from user text **in a loop**. One pass is unsafe: attackers can craft text that **reassembles** a tag after a single strip.  
3. **Least privilege** - model should only do what it needs (e.g. write a report), not arbitrary tool/web power.  
4. **Evals / trap cases** - labelled cases that try injection and flattery.  
5. **Layering** shrinks blast radius; **no prompt makes injection impossible**.

### Version prompts like code

- Released `fit_v1` (encouraging) → bug found → ship **`fit_v2`**, do **not** silently edit v1 (old callers may depend on it).  
- Versioning enables **A/B eval** (`--prompt v1` vs `--prompt v2`).  
- Path traversal like `?prompt_version=../../.env` must be rejected (allow-list versions).

### Evals = tests for prompts

- Run the **same** `assemble_prompt` / `generate_report` path the API uses against labelled cases (`cases.jsonl`).  
- Ten cases ≈ smoke test; one flip = 10 points.  
- Models are non-deterministic: **run twice**.  
- **Mock** only proves plumbing; real keys measure prompt quality.

### Dev preview

- `APP_DEBUG=true` enables `/v1/fit-report/preview` to inspect the exact prompt without calling the model for a full product path (or to inspect assembly).  
- Production should keep preview off.

---

## Part 2: Few-shot and chain-of-thought

### Few-shot examples as contract

Story: coaches Anil & Sunita agree on many verdicts; Madhu wants the model to “sound like us.”

| Practice | Why |
|----------|-----|
| Cover **strong**, **boundary**, **weak** | Model learns the rule, not one wording |
| Include cases coaches **disagree** on | Boundary calibration |
| Same formatter as live input (`render_user_message`) | Different formats teach nothing |
| Correct examples only | A wrong example is a **bug in the contract** |
| Match schema (incl. reasoning field if used) | Examples should look like real outputs |

### Reasoning-first (chain-of-thought via schema)

- LLMs generate **left-to-right**. If `verdict` is first, later tokens **defend** that commitment.  
- Better for multi-step judgement: put a **`reasoning`** field **first** (`think before you judge`), then verdict/score.  
- Keyword/field **order matters** for providers that serialise schema field order.

### Costs and when CoT helps

| Concern | Effect |
|---------|--------|
| Output tokens | Reasoning uses more tokens → **cost** |
| Latency | More tokens → **slower** |
| `max_tokens` | Higher chance of **truncated JSON** (unparseable) |
| Simple lookups | Little benefit (e.g. 2+5 “step by step”) |
| Multi-step judgement | Often helps - **measure** |
| Native reasoning models | Extra “reason in schema” can be redundant |

**Measure with a grid:** 0-shot vs 4-shot × reasoning off/on; compare accuracy, catastrophic failures, and latency. Prefer choices that balance **accuracy + cost + UX**, not accuracy alone. Run the grid **twice**.

---

## Part 3: Docker (ship the contract)

### Image vs container

| Term | Meaning |
|------|---------|
| **Image** | Frozen filesystem + start command; built **layer by layer**; build once, run many times |
| **Container** | **Running instance** of an image; disposable; shares host kernel (faster than classic VMs) |

Layers are **immutable**: deleting a file in a later layer does **not** remove it from earlier layers (secrets copied then `rm`’d can still leak).

### Dockerfile essentials (lecture)

- Base image (Python version)  
- Copy `requirements.txt` **before** app code → dependency layer **caches**  
- `pip install`  
- Dev may also install `requirements-dev.txt`  
- Prod copies app, may run as non-root user, **no** `--reload`  
- Dev `CMD` often uses uvicorn `--reload` + bind `0.0.0.0`

### Secrets

- **Never** bake `.env` / API keys into the image (anyone who pulls can read them).  
- Use **`.dockerignore`** so `.env` never enters the build context.  
- Inject config at **run time** (`env_file` in Compose / `--env-file`).

### Compose

- Declares `ports`, `env_file` (e.g. `../.env`), `volumes` (bind-mount for live prompt/code edits in dev).  
- `docker compose config` expands the resolved config.  
- New package in `requirements.txt` → **rebuild** (`docker compose up --build`); hot reload / restart alone will **not** install new deps.

---

## Key takeaways

1. A prompt is a **contract** - write it like a spec, version it, test it, ship it.  
2. Sycophantic “encouraging” wording is a **spec bug**.  
3. User content is **untrusted**; fence + strip-until-stable + least privilege + evals.  
4. Few-shot examples and reasoning-first fields change behaviour - **measure** cost/latency.  
5. Docker packages the runtime; keep secrets out of the image; rebuild when dependencies change.
