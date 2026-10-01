# Lecture 06: Testing, CI/CD & Deployment (Order Mitra)

**Course:** Introduction to AI Native Software Engineering · **Module 1**  
**App:** Order Mitra — conversational order assistant (Next.js, Prisma, AI tools, HITL)

---

## Lecture arc (three chapters)

1. **How to test Order Mitra** (Jest, React Testing Library, mocking, async, snapshots, coverage)
2. **Whether AI can help write tests** (prompts, limits, human supervision)
3. **Regression patterns + GitHub Actions CI/CD + Vercel (“Versal”) deployment** (branch protection, rollback)

**80/20 rule (from lecture):** ~20% of effort is development (what prior classes emphasized); ~**80%** is testing and iterative improvement before safe deployment.

---

## Order Mitra recap (why testing is hard)

| Capability | What to trust in production |
|------------|----------------------------|
| **Talk** | SSE streaming replies word-by-word |
| **Look up (agentic)** | Model decides when to call `searchOrders` against real Prisma DB |
| **Act destructively (HITL)** | `cancelOrder` only after human confirms |

Example flow: user asks for Mr. Iyer’s pending orders → streamed reply + **confidence badge** (high/medium/low) + real DB search (“search order complete”). All three must stay trustworthy after every change—not only on a laptop.

**Manual testing** (typing in chat, every confidence level, search variants, cancel confirm/reject/double-click) explodes combinatorially; you need **automated, repeatable checks**.

**“It works on my machine”** is not a deployment strategy—it is a last resort when demos fail.

---

## Delivery pipeline (lecture boxes)

```
Write code → Run tests locally → git push → GitHub Actions (CI) → Vercel deploy (CD)
```

| Stage | Role |
|-------|------|
| **Local tests** | You run Jest before others see the change |
| **git push** | Shares committed code; nothing deploys yet |
| **CI (Continuous Integration)** | GitHub Actions re-runs the same tests on GitHub’s servers—no one has to remember |
| **CD (Continuous Deployment)** | If CI passes, production can update automatically (e.g. Vercel) |

If **CI fails**, **CD must not run**—real users never see the broken build; developers get notified.

---

## What is a test? (formal definition)

A **test** is a small script that **acts on your code** (input: text, click, hover, etc.) and **checks the result** against expected behavior.

- **Pass:** observed behavior matches expected → green  
- **Fail:** mismatch → red  

Examples from lecture:

- Clicking **Confirm** actually triggers cancel flow  
- Confidence badge shows correct color for **low**  
- Empty search returns **empty list**, not an error  

**Write checks once; let the machine re-run them in under a second after every change.**

---

## Testing environment: two parts

| Part | Tool in stack | Job |
|------|---------------|-----|
| **Test runner** | **Jest** | Finds `*.test.ts(x)`, runs tests, `expect`, mocking, coverage, watch mode, snapshots |
| **Component testing toolkit** | **React Testing Library (RTL)** | Renders components in a fake environment, queries UI like a user |

**Jest alone** is enough for pure logic (`expect(2+2).toBe(4)`) but **cannot** render UI or simulate clicks. **RTL** fills that gap.

### Jest engine (four steps)

1. Scan project  
2. Find test files  
3. Run each test function (`expect` defines pass/fail)  
4. Print summary (pass/fail counts)

### File layout

- Prefer **`ComponentName.test.tsx` next to `ComponentName.tsx`** (Jest picks up `*.test.ts` / `*.test.tsx`)  
- One **test file per component**; **one `test(...)` block per behavior**, not one giant test  
- Name tests as **sentences describing behavior** (e.g. “shows high confidence in green when level is high”)

### Arrange → Act → Assert

| Step | Typical tool | Example |
|------|--------------|---------|
| **Arrange** | `render(...)` (RTL) | Build fake in-memory component (no real browser) |
| **Act** | `userEvent.click(...)` (preferred) or `fireEvent` | One user action |
| **Assert** | `expect(...)` + RTL queries | What on screen should match expectations |

Not every test needs **Act** (badge-only tests can be Arrange + Assert).

**RTL philosophy:** query what the **user sees**—e.g. `screen.getByText('high confidence')`—not CSS classes or internal props (`wrapper.find(...).props.level` does **not** emulate user behavior).

**`userEvent` vs `fireEvent`:** prefer **`userEvent`**—closer to real browser interaction.

---

## Confidence badge (first test example)

```tsx
render(<ConfidenceBadge level="high" />);
expect(screen.getByText(/high confidence/i)).toBeInTheDocument();
```

AI prompt pattern: *“Write a Jest + RTL test confirming ConfidenceBadge renders ‘high confidence’ when level is high”* — then **verify** it asserts on visible text, not implementation details.

---

## Coverage

- **Line coverage:** % of code lines executed by at least one test  
- **Target:** **≥ 80%** is a reasonable minimum (lecture default); CI can enforce thresholds in Jest config  
- Coverage report shows **0% files** (e.g. `OrderMitraPanel.tsx` untouched) → write focused tests for those lines  

**Critical:** High coverage with **weak asserts** is worthless (e.g. 100% coverage by calling functions and `expect`ing nothing meaningful). **Coverage ≠ correct behavior.**

**Improve coverage loop:**

1. `npm test -- --coverage`  
2. Read **uncovered line numbers** and behaviors  
3. Add one focused test per gap (or prompt AI with explicit edge cases)  
4. Re-run until threshold met  

---

## Non-deterministic AI output

Same user message → LLM may **word answers differently** → asserting exact reply text (`Mr. Iyer has one pending order…`) makes tests **fragile**.

**Insight:** You are not testing the LLM’s prose—you test **your app displays whatever comes back correctly**.

**Fix 1 — Mock the model (Jest):**

- `jest.mock('ai', …)` / mock `useChat` to return a **fixed** assistant message  
- No real Anthropic/OpenAI call in unit tests  
- Mock = predictable “stunt double” used **only in tests**

**Fix 2 — Async / streaming timing:**

- Replies arrive over time (SSE / `useChat` streams even mocked content)  
- **`getByText`** checks immediately → race condition  
- Use **`findByText`** (waits until element appears) and/or **`waitFor`**

**Two problems, two fixes:** wording → **mock**; timing → **`findBy` / `waitFor`**.

Other mock targets: `Date.now`, `Math.random`, payment gateways, external APIs (no real network in unit tests).

---

## Snapshot testing (Jest)

- First run saves a **serialized render** (“photo”); later runs **diff** against it  
- Good for **stable** UI: headers, settings layout, markup that must not drift  
- **Bad for dynamic chat content**—replies change every time → snapshots always fail  
- **`jest -u` / update snapshot:** only when you **understand and approve** the visual change—blind updates hide real bugs  

---

## Thumb rules (lecture recap)

| Situation | Approach |
|-----------|----------|
| Simple deterministic UI | `render` + `getByText` + `expect` |
| User clicks / typing | `userEvent` + assert visible change |
| LLM in component | Mock SDK / `useChat` |
| Content appears later | `findBy*` / `waitFor`, not `getBy*` |
| Stable markup must not change | Snapshot |
| Chat reply text | Mock + assert **your** rendering, not live LLM wording |

---

## Who writes tests?

- **Feature author** writes tests—not a separate QA team alone (QA lacks product semantics; devs lack QA’s adversarial inputs)  
- **Finishing a feature includes tests**—not an optional chore  

---

## AI-assisted test writing

**AI is good at (with clear prompts):**

- Render/prop happy paths  
- Click/type interaction tests  
- Pure function input/output tests  
- Boilerplate from templates you can read  

**Strong prompt ingredients:** component name, props, **mock LLM/Date/random**, **`findBy` for async**, named **edge cases** (empty list, API failure, double-click confirm, stop streaming, retry).

**AI is weak / you must own:**

- **Business rules in asserts** (e.g. should cancelled orders appear in search?)  
- **Security** (auth, permissions, PII)—review line-by-line or write yourself  
- Code you **don’t understand**—you can’t judge if the test is right  
- **Edge cases** AI won’t invent unless prompted (cancel, retry, malformed responses)  

**Workflow:** AI draft → you verify asserts → coverage report → prompt for **uncovered lines** → repeat.  
**Answer from lecture:** *Yes, AI can write tests—with human supervision.*

---

## Regression testing

**Regression:** something **used to work** and **quietly stops** without a deliberate code change to that feature (`git blame` shows nothing on the broken path).

### Three regression causes (AI-heavy apps)

1. **Prompt drift** — system prompt tweaked elsewhere changes LLM behavior globally  
2. **Model version change** — provider updates model behind the same API name  
3. **Tool call failure** — rate limits/timeouts turn tool calls into silent failures (UI keeps “working” but wrong)

**What regression tests should guard:**

- Tool calls **fire with correctly shaped arguments**  
- **Confirmation gates** block destructive tools without human approval  
- **Empty / malformed model responses** don’t break the UI  
- Shape/fields of structured responses (type-checking mindset; not snapshotting chat prose)

**CI runs these on every push** so broken changes cannot ship—**regression tests in CI**, not “whatever someone remembers to run.”

---

## GitHub Actions (CI)

- Workflows live in **`.github/workflows/`** (e.g. `test.yml`)  
- Language: **YAML** — indentation = structure (like Python nesting)  
- Typical workflow: **`on: push` + `pull_request`** → job on **`ubuntu-latest`** →  
  `actions/checkout` → `actions/setup-node` (Node **20** in lecture) → **`npm ci`** → **`npm test -- --coverage`**

### `npm ci` vs `npm install` (CI)

- **`npm ci`:** installs **exact** versions from `package-lock.json`; fails loudly if lockfile disagrees with `package.json` — **use on CI**  
- **`npm install`:** for local dev; may update lockfile  

### Secrets

- **Never** hard-code API keys in committed workflow files (public repos leak keys)  
- Store in **Repo → Settings → Secrets and variables → Actions**  
- Reference as `${{ secrets.ANTHROPIC_API_KEY }}` (name from lecture)

### Branch protection

- **Settings → Branches → protection rules**  
- Require **status checks** (CI workflow name, e.g. `test`) to pass **before merge**  
- Merge button **disabled** until CI green—stops “merge failing PR anyway”  

---

## Vercel continuous deployment (“Versal” in transcript)

- Connect GitHub repo at **vercel.com**; auto-detects Next.js  
- After **CI passes**, Vercel builds/deploys; env vars (API keys, `DATABASE_URL`) in **Vercel project settings**  
- **Preview URLs** per PR for human check before production  
- **Instant rollback:** Vercel keeps past deployments—point production at a **known-good** deployment without waiting for a new CI build (last safety net if someone rushed CD checks)

### CI vs CD responsibilities (lecture)

| Concern | Where |
|---------|--------|
| Component tests, mocks, coverage threshold | **CI** (workflow) |
| Rare live LLM calls in CI | Generally **avoid**; mock instead |
| Post-deploy “still broken in prod” | **CD** preview + **rollback** |

**AI helps CI/CD:** generate workflow YAML, explain failing CI logs, suggest missing regression tests (e.g. prompt drift).

---

## Prior modules (context for deployment)

Lecture recap: AI pair programming, Next.js App Router, server components, TypeScript, accessible components, Prisma, OAuth, TanStack Query, Order Mitra (SSE, search tool, ask-before-act). **Today:** prove it works before deploy.

*(Lecture wording: “routes” = user-side front end; “components” = server-side—note this as stated in class slides/transcript.)*

---

## Hands-on structure (in session)

- **Chapter 1:** Confidence badge tests (high/medium/low); mock `useChat` for Order Mitra panel  
- **Chapter 2:** AI-generated suite + **`npm test -- --coverage`** + iterate on gaps  
- **Chapter 3:** `.github/workflows/test.yml`, Jest **coverageThreshold** (~80%), push repo, Actions run; Vercel import  

Commands emphasized: `npm install`, `npm test`, `npm test -- --coverage`, `npm run dev`.

---

## Key vocabulary

| Term | Meaning |
|------|---------|
| **CI** | Continuous integration—auto test on each change |
| **CD** | Continuous deployment—auto ship when CI passes |
| **HITL** | Human-in-the-loop before destructive actions |
| **Mock** | Fake dependency with fixed behavior in tests |
| **Regression** | Working behavior silently breaks |
| **Line coverage** | % of lines executed by tests |
