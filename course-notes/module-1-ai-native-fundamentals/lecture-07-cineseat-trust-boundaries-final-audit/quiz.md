# Lecture 07 — In-Lecture Polls & Quizzes

Live polls ran in two blocks: after the module recap (before break), and after trust boundaries / Lighthouse (before Q&A and hands-on). Exact MCQ option text may differ on slides; stems and answers follow the transcript.

---

## Set 1 — After module recap (before break)

### Q1 — Spec → Prompt → Verify → Override: what is **verify**?

**Prompt (paraphrase):** In the specification / prompting / verifying / overriding loop for AI, what happens in the **verify** stage?

**Competing options discussed live:**

| Idea | Stage |
|------|--------|
| Run tests, read the diff, check the security surface | **Verify ✓** |
| Accept, reject, or send code back with a correction | **Override** (wrong for this question) |

**Answer given in class:** **Verify** = running tests, reading the diff, checking the security surface. Accepting/rejecting or sending corrections is **override** — a separate stage that comes after you find problems.

**Teaching point:** Verify and override are easy to conflate; remember they are **separate**.

---

### Q2 — CineSeat architecture: which pairing is a **trust boundary**?

**Prompt:** In CineSeat architecture, which is the correct trust-boundary pairing?

**Correct concept ✓:** **Tool-call arguments** (the model’s own output) → the **execute** path that acts on them — untrusted data crossing into side effects.

**Wrong trap discussed:** **TanStack Query + Zustand** — they handle caching and client preferences / UI state. They take user-facing activity but **do not verify** untrusted shapes.

**Instructor clarification:** If the option had been **Zod** (or Prisma as data-shape contract), that would align with verification. TanStack makes the DB path faster; Zustand reflects preferences on the client — neither is the trust verifier.

---

## Set 2 — After trust boundaries / Lighthouse (before Q&A)

### Q1 — Lighthouse accessibility score ~78

**Prompt (paraphrase):** What does an accessibility score around **78** mean?

**Answer given in class:** It is **not** a passing result — Lighthouse surfaces it as a **red / failing** accessibility score; you must fix the listed issues.

**Wrong competitor:** “Lighthouse doesn’t score accessibility, only performance” — **false**. Lighthouse scores accessibility, but at a **page / overall** level, not the same as component-wise axe reports.

---

### Q2 — Zod at the trust boundary

**Prompt:** Role of **Zod** relative to the trust boundary.

**Answer given in class (full agreement reported):** Zod sits on the trust boundary — it describes the **exact shape** untrusted data must have and rejects malformed values (e.g. tool args that would wipe the DB) before execution.

---

### Q3 — Lighthouse vs axe-core

**Prompt:** How do Lighthouse and axe-core differ?

**Answer given in class:** **Lighthouse** = **broad** end-to-end / page health check (performance, accessibility, best practices, SEO). **axe-core** = **component-wise** accessibility checks against WCAG (critical for the seat map). Run broad Lighthouse **and** component axe — not one or the other.

---

## Informal / non-content polls

- **Thumbs / readiness:** API keys ready (Grok, Auth secret, Google OAuth), Postgres up, seat map section complete, etc.  
- **End-of-session feedback** poll (satisfaction — not academic MCQ).

---

## Hands-on checkpoints (not Mentimeter, but treated as live checks)

| Checkpoint | Pass signal from session |
|------------|--------------------------|
| Section A | `npm run dev` on localhost; skip-to-main-content link present |
| Section B | Seat matrix selectable; axe shows no critical violations in inspect |
| Section C | Google login works; booking writes a seat / booking id |
| Section D | Reel bot lists showtimes; cancel asks confirm then removes booking |
| Section E | `npm test` / coverage green; GitHub Actions workflow runs on push |
| Audit | Lighthouse categories reviewed; Vercel needs hosted DB + OAuth redirect URLs |

---

## If your assignment only accepts “no polls”

Polls **were** used; this file documents them. For graded concepts also study **`study-material.md`** and **`important-questions.md`**.
