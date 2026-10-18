# Lecture 07 — Likely Exam Q&A (CineSeat, Trust Boundaries, Final Audit)

Answers follow **lecture content** (module recap, CineSeat integration, Lighthouse/axe, hands-on).

---

### 1. What is the purpose of Module 1’s final lecture beyond another feature demo?

**Answer:** To practise **integration architecture** — wiring UI, auth, data, agent tools, tests, and deploy so you see bugs that only appear **across trust boundaries**, not in isolated labs.

---

### 2. Name the three model tiers and what each optimises for.

**Answer:** **Frontier** (max capability, high cost), **open weight** (control / hosting economics), **specialised** (one domain, e.g. code). Choose by **cost, capability, and risk** together.

---

### 3. Why can per-token pricing look cheap but hurt in production?

**Answer:** Cost scales with users × tokens; **output** tokens often cost several times **input**. At hundreds or thousands of chatbot users the bill compounds quickly.

---

### 4. Define hallucination vs calibration (as in the recap).

**Answer:** **Hallucination** = false/ungrounded content stated confidently. **Calibration** = confidence matches real accuracy; often fixed by **grounding** (e.g. RAG over your data) instead of pure model memory.

---

### 5. List Spec → Prompt → Verify → Override and what each stage owns.

**Answer:** **Spec** = required behaviours + edge cases. **Prompt** = turn spec into requests; generate code and tests. **Verify** = run tests / inspect diffs / security surface. **Override** = accept, reject, or send corrections to the AI.

---

### 6. In the Spec→…→Override loop, what happens in the **verify** stage?

**Answer:** **Run tests, read the diff/results, check the security surface** — you **find** problems. You do **not** yet accept/reject or send the fix request; that is **override**.

---

### 7. When should deterministic rules win over AI, and when should AI win?

**Answer:** **Rules** for unambiguous gates (crash, missing component → block ship). **AI** for ambiguous natural language and creative work.

---

### 8. In Next.js App Router terms used in class, what are “routes” vs “components”?

**Answer:** Default **server components** were called **routes**; interactive **client** pieces were called **components** — use `"use client"` only when interactivity requires it.

---

### 9. Map WCAG, ARIA, and axe-core.

**Answer:** **WCAG** = accessibility **spec** (course aims at **AA**). **ARIA** = markup attributes implementing roles/state for assistive tech. **axe-core** = automated engine matching implementation to WCAG on real components.

---

### 10. Why put `aria-label` / `aria-pressed` / booked-seat handling on seat buttons?

**Answer:** Sighted users see layout/colour; screen-reader users need explicit **row/seat**, **selected** state, and honest **booked** announcements — especially when native `disabled` would skip seats in the tab order.

---

### 11. What does Prisma provide in this stack?

**Answer:** A **single source of truth** for data shape (schema, relations, cardinality) before shipping migrations and real bookings.

---

### 12. What is a trust boundary?

**Answer:** The line where you **stop assuming** external data/intent is safe and **must verify**. Outside = untrusted; inside = already validated. It is a **verifier**, not caching or cosmetic UI state.

---

### 13. List three CineSeat trust-boundary crossings from the lecture.

**Answer:** (1) **User input → reel bot**, (2) **reel bot → tool calls**, (3) **tool results → database** (plus agent→UI consistency).

---

### 14. Why are TanStack Query and Zustand **not** trust-boundary sitters in the quiz sense?

**Answer:** They improve **fetch/cache** and **client preferences**. They do **not** validate untrusted shapes. **Zod** (and schema/auth checks) do.

---

### 15. Give a correct trust-boundary pairing involving tools.

**Answer:** **Model tool-call arguments** → **execute** function that acts on the DB/UI — arguments are untrusted model output and must be validated before execution.

---

### 16. What fallback rule should architects always design?

**Answer:** **Fail loudly and safely** — refuse bad queries, inform the user, **log**. Never fail silently or leave failure behaviour unspecified.

---

### 17. Example fallbacks: stream timeout, bad tool args, unconfirmed cancel, AI down?

**Answer:** Partial stream + **retry**; **Zod** reject (no run); **no cancel** (safe default); rest of booking UI still works without the chatbot.

---

### 18. How should production model swaps be designed?

**Answer:** Shared streaming/SDK surface so changing provider/model is a **tiny** code change (and optionally pre-installed adapters). Do not hard-wire business logic to one model name string. Env vars alone cannot swap missing SDK imports.

---

### 19. What four categories does Lighthouse score?

**Answer:** **Performance, accessibility, best practices, SEO** (each roughly 0–100).

---

### 20. Is an accessibility score of 78 a “pass”?

**Answer:** **No.** Lecture treated ~78 as a **failing / red** result — fix the listed checks. Lighthouse **does** score accessibility; it is not performance-only.

---

### 21. Lighthouse vs axe-core — which for what?

**Answer:** **Lighthouse** = broad page health. **axe-core** = **component-level** WCAG violations (e.g. seat map). Use both; neither replaces the other.

---

### 22. Why run Lighthouse against a production build locally?

**Answer:** Dev mode is not what users get. Build + start, then audit the served URL for a realistic score.

---

### 23. What must change in Google OAuth when you deploy off localhost?

**Answer:** Add the **production / Vercel origin and redirect URIs** in Google Cloud credentials. Leaving only `localhost:3000` breaks post-login redirect after deploy.

---

### 24. Why might a Vercel deploy fail even if the app worked locally?

**Answer:** Production needs a reachable **hosted database** and env vars (`DATABASE_URL`, Grok, Auth, Google). Local Postgres is not available to Vercel by default.

---

### 25. What HITL pattern must the reel bot’s cancel path use?

**Answer:** Model may **propose** cancel; UI requires **explicit confirm** before the destructive tool runs — same spirit as Order Mitra’s cancel gate.

---

### 26. Poll-style: teammate says TanStack + Zustand sit on the trust boundary because they take user input — what is wrong?

**Answer:** Input should already be validated (**Zod** etc.). Caching and client state libraries are not the verification layer.

---

### 27. Poll-style: verify stage = “accept or send code back” — correct?

**Answer:** **No** — that is **override**. Verify only discovers problems via tests/diff/security review.

---

### 28. How can you reduce AI coding-agent cost while finishing CineSeat?

**Answer:** Do not dump the **entire** repo into context every time; scope prompts to the **local flow** needed for the change (TA closing tip).
