# Lecture 03: In-Lecture Quizzes

Live polls were run between lecture blocks and demos (Professor Patta / TA Subhajit Shah). Questions and options below are taken verbatim from the Mentimeter deck "Session 3" (14 questions across Parts 1-3). **This deck has no answer-key slides**, so correct answers are deduced from the lecture notes and transcript. Items where the deck's poll settings or wording make the answer ambiguous are flagged with ⚠️.

---

## Quiz 1 - After Part 1 (system prompts / injection)

### Q1. What does the System prompt define?

| Option | |
|---|---|
| A | Specific question, instruction, or task that a human sends to an AI model or agent during a conversation |
| B | Defines a fixed structure that always contains code |
| **C ✓** | **Defines what the model must do.** |
| D | None of the above |

**Explanation:** The system prompt holds developer-owned standing rules (who the model is; must / must-not), weighted above user content. A describes a *user* prompt.

---

### Q2. Components of a System Prompt

**Stem:** Which of the following are components of a System Prompt?

| Option | |
|---|---|
| **A ✓** | **Role** |
| **B ✓** | **Task** |
| **C ✓** | **Rules** |
| D | Question |

⚠️ **Poll set to single choice.** Role, Task and Rules are all components; **Question is the odd one out** (not part of the lectured anatomy). Live note from the earlier notes: slide formatting was messy; instructor confirmed **role, task, rules** (plus untrusted / if-unsure in the wider talk).

---

### Q3. What test suites for a prompt catch

**Stem:** Test suites for a prompt are used to catch traps such as ...

| Option | |
|---|---|
| **A ✓** | **Sycophancy** |
| **B ✓** | **Prompt Injection** |
| C | FastAPI Crashes |
| D | Latency of LLMs |

⚠️ **Poll set to single choice**, but **A and B are both correct**: the eval suite's trap cases cover the flattery (sycophancy) bug and prompt injection. FastAPI crashes and LLM latency are not what the labelled verdict suite measures.

---

### Q4. Which rule can a JSON Schema NOT express?

| Option | |
|---|---|
| A | match_score is an integer from 0 to 100 |
| B | verdict is one of three values |
| **C ✓** | **verdict must agree with match_score** |
| D | skills has three to six items |

**Explanation:** Cross-field business rules need app-level validators (e.g. a Pydantic `@model_validator`). Ranges (`ge`/`le`), enums and item counts (`minItems`/`maxItems`) all **can** be expressed in the schema.

---

### Q5. Why did KaryaSetu v1 flatter Priya?

| Option | |
|---|---|
| A | The model hallucinated |
| B | The temperature was too high |
| **C ✓** | **The spec asked for encouragement and never asked for honesty** |
| D | The schema was too loose |

**Explanation:** The sycophancy was a **spec bug**, not a model bug: the prompt contract asked for encouragement and never required honesty.

---

## Quiz 2 - After Part 2 (few-shot / reasoning)

### Q6. Choosing few-shot examples

**Stem:** What are the appropriate strategies to choosing examples for few shot?

| Option | |
|---|---|
| A | Give only strong examples |
| B | Include one strong and one weak |
| **C ✓** | **Cover the label space of strong, boundary and weak cases** |
| D | Include one strong and one boundary case |

**Explanation:** Covering strong, boundary and weak cases (including cases coaches disagree on) teaches the model the rule, not one wording.

---

### Q7. Does the first example hold the most weight?

**Stem:** In Few Shot Prompting, the first example holds the most weight?

| Option | |
|---|---|
| A | True |
| **B ✓** | **False** |

⚠️ **Inferred, not in the course notes.** Models tend to weight the *most recent* (last) examples more, and the notes never say the first example is special. Treat **False** as the safe answer.

---

### Q8. What counts as a "bug" in the contract?

**Stem:** In the context of few shot prompting, which of the following is considered as a "bug" in the contract?

| Option | |
|---|---|
| A | Giving 15 examples |
| B | Irrelevant Example |
| **C ✓** | **Wrong Example** |
| D | Providing the same example twice |

⚠️ **Poll allowed up to 4 selections.** The notes state it directly: *"Correct examples only - a wrong example is a **bug in the contract**."* B and D are poor practice but are not named as bugs in the notes; A is not a bug. If the instructor accepted several, C is the one the notes back.

---

### Q9. Where does a `reasoning` field go?

**Stem:** You add a reasoning field to the schema. Where must it go?

| Option | |
|---|---|
| A | Last, so it summarises |
| **B ✓** | **First, before the fields that depend on it** |
| C | Anywhere: order doesn't matter |
| D | In the system prompt instead |

**Explanation:** Tokens are generated in order. An early verdict forces later text to **defend** it; reasoning-first gives the model room to think before judging. Field order matters for providers that serialise schema field order.

---

### Q10. Why not measure on the examples inside the prompt?

| Option | |
|---|---|
| A | It's slower |
| **B ✓** | **The model has already seen the answers.** |
| C | The eval set is too small |
| D | Examples can't be scored |

**Explanation:** Few-shot examples are leaked answers. Evaluate on a **held-out** set the prompt has never seen.

---

## Quiz 3 - After Part 3 (Docker)

### Q11. Python 3.9 vs `str | None`

**Stem:** Output of this command: `docker run --rm python:3.9-slim python -c "print(str|None)"`

| Option | |
|---|---|
| A | ValidationError |
| B | str \| None |
| **C ✓** | **TypeError** |
| D | PrintException |

**Explanation:** `X | Y` on types needs Python 3.10+. On 3.9 the `|` operator fails at runtime with `TypeError: unsupported operand type(s) for |: 'type' and 'NoneType'`. It is not a Pydantic `ValidationError`.

---

### Q12. True statements about a Docker container

**Stem:** Which of the statements are true about a docker container?

| Option | |
|---|---|
| A | It is a frozen filesystem plus a start command |
| **B ✓** | **It is a running instance of an image** |
| **C ✓** | **It is disposable** |
| **D ✓** | **It shares the host kernel** |

**Explanation:** Option A describes an **image**, not a container. B, C and D are true (a container is a running, disposable instance that shares the host kernel, unlike a full VM). *(Poll allowed up to 4 selections.)*

---

### Q13. Purpose of `.dockerignore`

| Option | |
|---|---|
| **A ✓** | **Preventing files from getting into the container** |
| B | Acts as a swap file |
| C | Used for setting up Docker container |
| D | Used for running tests |

**Explanation:** It excludes files from the **build context** so they never enter the image (e.g. `.env` / API keys).

---

### Q14. New package added to `requirements.txt`

| Option | |
|---|---|
| A | Nothing: hot reload will pick it up |
| B | Restart the container |
| **C ✓** | **Rebuild the image: docker compose up --build** |
| D | Edit .dockerignore |

**Explanation:** Dependencies are baked into the image, so a new package needs a new image layer. Hot reload and a plain restart reuse the old image.

---

## Quick self-check

| Claim | True / False |
|-------|----------------|
| Streaming always speeds up the model | **False** (Week 2 + recap) |
| Prompt injection is only "direct" typing by the user | **False** - also indirect |
| Strip delimiters once is enough | **False** - until stable |
| Edit `fit_v1.md` in place after release | **False** - version to v2 |
| `RUN rm .env` after copying it into an earlier layer is safe | **False** |

---

## Summary

| Quiz | When | Questions | Main topics |
|------|------|-----------|-------------|
| **1** | After Part 1 | **5** | System prompt, its components, eval traps, what JSON Schema can't express, sycophancy cause |
| **2** | After Part 2 | **5** | Choosing few-shot examples, example weighting, wrong examples, reasoning-first schema, held-out evals |
| **3** | After Part 3 | **4** | `str \| None` on 3.9, container facts, `.dockerignore`, rebuild on new dependency |

**Total Menti questions:** **14** (5 + 5 + 4)
