# Lecture 03: Important Exam Q&A

Practice questions aligned with lecture emphasis and in-class quizzes. Answers are concise for MCQ revision.

---

## Prompt as contract

### Q1. What four steps summarise “prompt as a contract” in this lecture?

**A.** **Specify** (system prompt), **constrain** (schema/validators), **test** (evals), **ship** (Docker).

### Q2. Name the three prompt roles and who controls each.

**A.** **System** (developer, trusted), **user** (external input, untrusted), **assistant** (prior model outputs).

### Q3. Which role is weighted highest by the model, and why does that matter?

**A.** **System** above user - developer standing rules should outrank user text; still defend because injection can override behaviour.

---

## System prompts & flattery

### Q4. List the main sections of a well-structured system prompt from the lecture.

**A.** **ROLE**, **TASK**, **RULES**, **UNTRUSTED INPUT**, **IF UNSURE** (plus output via schema from Week 2).

### Q5. Why is “be accurate” a weak rule?

**A.** It is **vague** and hard to test. Prefer concrete, checkable rules (score bands, evidence requirements, etc.).

### Q6. Priya has 2 years; posting needs 8+; model returns strong match after “be warm and encouraging.” Bug type?

**A.** **Spec / flattery (sycophancy) bug** - the system prompt asked for encouragement; not primarily a mysterious model failure.

---

## Injection & defences

### Q7. What is prompt injection, and where does OWASP rank it for LLMs (as stated in lecture)?

**A.** User prompts alter LLM behaviour/output unintendedly; lecture cites it as **#1** on OWASP’s LLM Top 10 (2025).

### Q8. Direct vs indirect injection?

**A.** **Direct:** attacker types the override themselves. **Indirect:** instruction hidden in content they did not author (e.g. a job posting).

### Q9. Why strip delimiter tags in a **loop** (“until stable”)?

**A.** A **single** strip can reassemble a new delimiter from crafted fragments; looping until no tags remain closes that hole.

### Q10. Does a perfect system prompt make injection impossible?

**A.** **No** - layered defences **shrink blast radius**; always assume residual risk and use evals/trap cases.

### Q11. Why version `fit_v1` → `fit_v2` instead of editing v1 in place?

**A.** Released prompts are contracts; silent edits can **break** dependents; versions enable comparison and rollback.

---

## Evals

### Q12. What should an eval run through?

**A.** The **same** assembly/generation path the API uses, against **human-labelled** cases.

### Q13. Why re-run evals twice on a real model?

**A.** Models are **non-deterministic** - if the score moves, that is the finding.

### Q14. What do mock-provider evals prove?

**A.** Mostly **plumbing** - the mock does not judge prompt quality.

---

## Few-shot & reasoning

### Q15. What mix of few-shot examples should you include?

**A.** At least **strong**, **boundary**, and **weak** (or partial) cases; vary wording; include coach-disagreement boundaries.

### Q16. Why format examples with the same function as live user input?

**A.** Otherwise the model learns a **different format** than production and examples teach little.

### Q17. Why put `reasoning` before `verdict` in the schema?

**A.** Tokens are generated in order; an early verdict forces later text to **defend** it. Reasoning-first gives room to think first.

### Q18. Name three downsides of always enabling chain-of-thought / reasoning fields.

**A.** Higher **token cost**, higher **latency**, greater risk of **truncated JSON** at `max_tokens`; little gain on trivial tasks.

---

## Docker

### Q19. Image vs container?

**A.** **Image** = frozen filesystem + start command (built in layers). **Container** = running instance of that image (disposable; shares host kernel).

### Q20. Why can `RUN rm .env` after `COPY . .` still leak a key?

**A.** Layers are immutable; the secret remains in an **earlier layer** of the image.

### Q21. What is `.dockerignore` for in this lecture’s security story?

**A.** Keep `.env` / secrets (and clutter) **out of the build context** so they never enter the image.

### Q22. You add a package to `requirements.txt`. Hot reload does not pick it up. What must you do?

**A.** **Rebuild** the image (e.g. `docker compose up --build`). Restarting the same container is not enough.
