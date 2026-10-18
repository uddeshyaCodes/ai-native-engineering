# Lecture 03: In-Lecture Quizzes

Live polls were run between lecture blocks and demos (Professor Patta / TA Subhajit Shah). Stems below follow the transcript readouts; some slides had formatting glitches that the instructor acknowledged live.

---

## Quiz 1 - After Part 1 (system prompts / injection)

### Q1. What is a system prompt?

| | |
|---|---|
| **Correct concept ✓** | Developer **standing instructions** that define who the model is and what it must / must not do (not “always contains code”) |

**Explanation:** Fixed developer-owned structure/rules; weighted above user content.

---

### Q2. Components of a system prompt (multi-select)

| Option | |
|--------|---|
| **ROLE ✓** | Persona |
| **TASK ✓** | What to do |
| **RULES ✓** | Testable constraints |
| Question / free Q&A section | **Not** part of the lectured anatomy |

**Live note:** Slide formatting was messy; instructor confirmed **role, task, rules** (plus untrusted / if-unsure in the wider talk).

---

### Q3. What can an eval / test suite catch in this story? (multi-select)

| Option | |
|--------|---|
| **Sycophancy / flattery ✓** | Encouraging-spec bug |
| **Prompt injection ✓** | Trap cases in evals |
| FastAPI races | Not what the prompt suite measures |
| LLM latency | Not the focus of the labelled verdict suite |

---

### Q4. Which rule can a JSON schema **not** fully express (as discussed)?

| | |
|---|---|
| **Correct ✓** | Cross-field business rules like **“verdict must agree with match_score”** (needs app validators / model validators beyond simple type ranges) |

**Contrast:** `match_score` as int in 0-100 **can** be expressed in schema (`ge` / `le`).

---

## Quiz 2 - After Part 2 (few-shot / reasoning)

Stems were partly “demo + discussion”; reconstructed from the measurement grid talk:

### Q5. (Reconstructed) Should you always turn reasoning on?

| | |
|---|---|
| **Correct concept ✓** | **No** - measure accuracy **and** latency/cost; one run of a small grid can mislead |

### Q6. (Reconstructed) How should few-shot examples be formatted?

| | |
|---|---|
| **Correct ✓** | With the **same** user-message rendering as live traffic (delimiters/stripping included) |

---

## Quiz 3 - After Part 3 (Docker)

### Q7. Python 3.9 vs `str | None` syntax

| | |
|---|---|
| **Correct ✓** | **`TypeError`** on 3.9 (union `|` syntax needs newer Python); not a Pydantic validation error by itself |

---

### Q8. What is a Docker **container**? (multi-select)

| Option | |
|--------|---|
| Frozen filesystem + start command | That is an **image**, not a container |
| **Running instance of an image ✓** | |
| **Disposable ✓** | Can remove and recreate |
| **Shares the host kernel ✓** | Unlike a full classic VM story |

---

### Q9. Purpose of `.dockerignore`

| | |
|---|---|
| **Correct ✓** | Exclude files from the **build context** so they do not enter the image (e.g. `.env` / API keys) |

---

### Q10. New package added to `requirements.txt` - what must you do?

| Option | |
|--------|---|
| Hot reload alone | **No** |
| Restart same container | **No** |
| **`docker compose up --build` (rebuild) ✓** | New deps need a new image layer |
| Edit `.dockerignore` | Unrelated |

---

## Quick self-check

| Claim | True / False |
|-------|----------------|
| Streaming always speeds up the model | **False** (Week 2 + recap) |
| Prompt injection is only “direct” typing by the user | **False** - also indirect |
| Strip delimiters once is enough | **False** - until stable |
| Edit `fit_v1.md` in place after release | **False** - version to v2 |
| `RUN rm .env` after copying it into an earlier layer is safe | **False** |
