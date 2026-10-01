# Lecture 06 — In-Lecture Polls & Quizzes

This lecture **did include live poll/quiz questions** (multiple sets across breaks). Wording below follows the transcript; exact MCQ option text may differ on slides.

---

## Set 1 — After Jest / RTL / mocking / snapshots (first break)

### Q1 — RTL query philosophy

**Prompt (paraphrase):** React Testing Library encourages finding elements the way a user would. Which query best follows that philosophy?

**Discussed wrong options:** Inspecting wrapper/component **props** (e.g. `wrapper.find(...).props.level`)—does not emulate user behavior.

**Answer given in class:** **`screen.getByText(...)`** (query visible text the user sees).

**Note:** `findByText` is for **async/waiting**; the poll answer emphasized **`getByText`** for user-visible querying in this question.

---

### Q2 — Snapshot workflow risk

**Prompt:** A teammate’s change breaks three snapshot tests; they run Jest with **update snapshot**, all tests go green, and they push. What is the risk?

**Answer given in class:** They may **approve differences without reading them**, wiping snapshot protection and **letting genuine bugs through**.

---

### Q3 — Why mock the LLM call?

**Prompt:** Why do we mock the LLM in tests?

**Answer given in class:** So tests are **deterministic**—you avoid **LLM non-determinism** (slightly different wording breaking asserts).

---

### Q4 — What should you NOT mock in a unit test?

**Options discussed:** Anthropic API call, database query, **`Math.random`**, pure function that **formats an order ID for display**.

**Answer given in class:** **Do not mock** the **pure formatting function**—it is stable logic; **do mock** LLM, DB, and variable sources like **`Math.random`**.

---

## Set 2 — After AI-assisted testing & coverage

### Q1 — Meaning of 80% coverage

**Prompt (paraphrase):** What does it mean if 80% of your code was executed by at least one test?

**Answer given in class:** **~80% of code lines/statements** were hit by tests (**line coverage**)—not “80% of bugs found.”

---

### Q2 — 100% coverage, empty asserts

**Prompt:** A team reaches **100% coverage** by writing one test per function that calls it but **asserts nothing**. What does this demonstrate?

**Answer given in class:** **Coverage only shows lines ran**, not that behavior is **correct**—business logic still needs meaningful **`expect`** checks.

---

### Q3 — AI-drafted suite: what stays untested?

**Prompt:** When AI drafts a test suite, which area is **most likely left untested**?

**Trick discussed:** “Main intended happy path” is what AI **does** test—the **intended path** statement is true but **not** the answer to “most likely **un**tested.”

**Answer given in class:** **Error states, cancellation, retries**, and similar **edge cases** AI won’t add unless prompted.

---

### Q4 — Coverage before prompting AI

**Prompt:** In the draft → run → read coverage → prompt loop, why read the **coverage report before** asking AI for missing tests?

**Answer given in class:** The report shows **what is uncovered** so your follow-up prompt targets **specific missing behaviors/lines**.

---

## Set 3 — After CI/CD / Vercel / rollback

### Q1 — `npm ci` vs `npm install` on GitHub Actions

**Prompt:** Why **`npm ci`** rather than **`npm install`** in CI?

**Answer given in class:** **`npm ci`** enforces the **lockfile**—installs exact locked versions and **fails on lockfile/package.json mismatch** (reproducible CI). **`npm install`** is oriented toward local dev.

*(Class noted neither command “automatically runs tests” by itself—that comes from workflow `run:` steps.)*

---

### Q2 — Regression / “degradation” test for an AI feature

**Prompt:** For an AI feature regression test, what should you assert?

**Answer given in class:** Focus on **tool-call behavior, confirmation gates, malformed/empty responses not breaking UI**—**not** matching full generative reply text to a snapshot.

**Discussed trap:** “Match snapshot” applies to **stable visual markup**, not **LLM generative output**—factually true statement but **wrong choice** for this AI-behavior question.

---

### Q3 — Failing CI but PR still merged

**Prompt:** CI runs on every PR and shows red when tests fail, but a teammate **merges the failing PR**. What was missing?

**Answer given in class:** **Branch protection** requiring CI/status checks to pass before merge.

---

## Other in-lecture checks (not graded polls)

- **“This is not a quiz”** — quick check: testing stack = **test runner (Jest) + component library (RTL)**; which layer owns Arrange / Act / Assert (discussed live).
- **Show of hands:** who runs tests before demo/deploy (informal).
- **End-of-session feedback poll** — session satisfaction (not content MCQ).

---

## If your assignment only accepts “no polls”

Polls **were** used; this file documents them. If an instructor MCQ bank omits poll items, study **`study-material.md`** and **`important-questions.md`** for graded concepts.
