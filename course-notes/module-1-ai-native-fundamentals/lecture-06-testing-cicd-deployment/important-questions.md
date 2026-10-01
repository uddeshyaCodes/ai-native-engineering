# Lecture 06 — Likely Exam Q&A (Testing, CI/CD, Deployment)

Answers follow **lecture content** (Order Mitra, Jest/RTL, GitHub Actions, Vercel).

---

### 1. Why does the course spend so much time on testing if AI speeds up coding?

**Answer:** Software effort is often described as ~**20% development** and ~**80% testing and iterative improvement**. AI accelerates building features; automated verification is what makes deployment safe.

---

### 2. What three capabilities make Order Mitra hard to test manually?

**Answer:** (1) **Streaming conversational UI** (SSE), (2) **Agentic lookup** (`searchOrders` against Prisma), (3) **Destructive actions with HITL** (`cancelOrder` only after confirm). Each needs trustworthy behavior in production, not just on a laptop.

---

### 3. What is wrong with “it works on my machine” as a release strategy?

**Answer:** It is not a deployment strategy—it means manual verification failed to cover real inputs (e.g. “Mr. Iyer typed something nobody tried”). Automated tests encode fixed checks that rerun on every change.

---

### 4. What are the two parts of the front-end testing stack in this lecture?

**Answer:** **Jest** (test runner: discover tests, `expect`, mocks, coverage, snapshots) and **React Testing Library** (render components, query/interact like a user).

---

### 5. What can Jest do alone, and what requires RTL?

**Answer:** Jest handles logic and assertions on plain values. It **cannot** render React components or simulate clicks. RTL provides **render**, queries (`getByText`, etc.), and user interactions (with **`userEvent`** preferred over **`fireEvent`**).

---

### 6. Explain Arrange, Act, Assert with an example.

**Answer:** **Arrange:** `render(<ViewToggle />)`. **Act:** `await userEvent.click(screen.getByText('switch to compact'))`. **Assert:** `expect(screen.getByText('switch to comfortable')).toBeInTheDocument()`. Simple display tests may skip Act.

---

### 7. Why does RTL prefer `getByText('high confidence')` over checking CSS classes or `.props.level`?

**Answer:** RTL tests **what the user sees**, not implementation details. Prop/class assertions don’t emulate user-visible behavior.

---

### 8. What is line coverage, and what threshold did the lecture recommend?

**Answer:** **Line coverage** = percentage of code lines executed by at least one test. Target **≥ 80%** as a reasonable minimum; CI can enforce via Jest `coverageThreshold`.

---

### 9. Can you have 100% coverage and still ship bugs?

**Answer:** **Yes.** Tests that call code but **assert nothing meaningful** (or only “didn’t crash”) raise coverage without validating behavior. **Strong `expect` assertions** on business rules are mandatory.

---

### 10. Why is asserting exact LLM reply text a bad test strategy?

**Answer:** LLM output is **non-deterministic**—wording changes while the app may still be correct. Tests fail for harmless variation. You should test that **your UI renders the mocked/fixed response**, not live model prose.

---

### 11. How do mocking and `findByText` address two different test failures?

**Answer:** **Mocking** fixes **wording/variability** (fixed assistant message via `jest.mock` / mocked `useChat`). **`findByText` / `waitFor`** fix **timing** (streaming/async UI not ready on immediate `getByText`).

---

### 12. When should you use snapshot tests, and when should you avoid them?

**Answer:** **Use** for stable markup (headers, settings layout) to catch unintended UI drift. **Avoid** for **dynamic chat content** where text is supposed to change every time. Blind `jest -u` updates can approve real bugs.

---

### 13. In a unit test, what should you mock vs not mock (lecture examples)?

**Answer:** **Mock:** external LLM APIs, DB queries (speed/predictability), `Math.random`, dates, external HTTP. **Do not mock:** a **pure formatter** (e.g. order ID → display string)—test real logic with fixed inputs.

---

### 14. Why mock the LLM in tests?

**Answer:** So tests are **deterministic**, fast, and independent of API keys/network— you control the assistant message and test **your rendering and wiring**, not the model’s creativity.

---

### 15. Who should write automated tests for a feature?

**Answer:** The **developer who built the feature**—tests are **part of finishing the feature**, not a handoff-only QA task. QA lacks your semantic intent; you lack their unlisted edge inputs unless you encode both in tests.

---

### 16. Can AI write your entire test suite without supervision?

**Answer:** **Partially.** AI helps with boilerplate and happy paths, but **you** must supply business asserts, security-sensitive checks, and **edge cases** (empty search, double confirm, stop/retry). Lecture answer: **yes, with human supervision**—coverage reports guide follow-up prompts.

---

### 17. What is regression, and what three causes were listed for AI apps?

**Answer:** **Regression** = software **regressed** from working to broken without an obvious code edit to that feature. Causes: **(1) prompt drift**, **(2) model version changes**, **(3) tool call failures** (timeouts/rate limits) that fail silently.

---

### 18. What should AI regression tests verify beyond “the UI loads”?

**Answer:** Tool calls use **correct argument shapes**; **confirmation gates** block destructive tools; **empty/malformed model responses** don’t crash the UI; structured response **fields** remain valid (shape checks—not chat text snapshots).

---

### 19. What happens in CI when tests fail?

**Answer:** **CD must not deploy**—users don’t see the broken version; developers are notified. CI is the automated gate on every push/PR.

---

### 20. Why use `npm ci` in GitHub Actions instead of `npm install`?

**Answer:** **`npm ci`** installs **locked** versions from `package-lock.json` and **fails** if lockfile and `package.json` disagree—reproducible CI builds. **`npm install`** is for local development and may change the lockfile.

---

### 21. Where do you put CI workflows, and what must a minimal test workflow do?

**Answer:** **`.github/workflows/*.yml`**. Trigger on **push/PR**, checkout, setup Node, **`npm ci`**, **`npm test -- --coverage`**.

---

### 22. How should API keys be supplied to CI?

**Answer:** **GitHub Actions secrets** (repo settings)—referenced in YAML as `${{ secrets.... }}`. **Never** commit raw keys in workflow files (especially public repos).

---

### 23. What is branch protection for?

**Answer:** Requires **CI status checks to pass before merge**—prevents merging a PR with a red CI even if a teammate clicks merge anyway.

---

### 24. What is Vercel’s role after GitHub Actions?

**Answer:** **Continuous deployment:** connect repo; when CI passes, Vercel **builds and deploys**; env vars live in Vercel settings; PRs get **preview URLs** for manual verification.

---

### 25. What is instant rollback on Vercel?

**Answer:** Vercel retains **past deployments**; you can **point production back** to a previously working deployment **without a new build**—last safety net when CD checks were rushed or wrong.

---

### 26. Poll-style: Teammate runs `jest -u` after snapshot failures and pushes—what’s the risk?

**Answer:** They may **approve diffs without review**, overwriting snapshot protection and **masking real UI bugs**.

---

### 27. Poll-style: 100% coverage with tests that assert nothing—what does that show?

**Answer:** **Coverage only measures lines executed**, not **correct behavior**—tests can pass while logic is wrong.

---

### 28. Poll-style: CI shows red on a PR but merge still happened—what was missing?

**Answer:** **Branch protection** requiring CI checks to pass before merge.
