# Lecture 07: CineSeat — Integration Architecture, Trust Boundaries & Final Audit

**Course:** Introduction to AI Native Software Engineering · **Module 1** (final session)  
**App:** **CineSeat** — cinema self-service booking portal with an AI “reel bot” (Next.js, Prisma, Auth.js, Grok, Jest, Lighthouse/axe, Vercel)  
**Hands-on lead (transcript):** Rajdeep; theory / architecture Q&A with the module professor

> **Transcript note:** Source file had ASR noise — “Cenesit / Cinescid / SIN asset” → **CineSeat**; “real bot” → **reel bot**; “Talker/Versal” → **Vercel**; “X code / export / Axe score” → **axe-core**; “Zot / Zod” → **Zod**; “Groc / Graph” → **Grok**; “decap” → **recap**.

---

## Lecture arc

1. **Module recap** — models, tokens, Spec→Prompt→Verify→Override, Next.js stack, accessibility, Prisma/Auth, Order Mitra lessons  
2. **Integration architecture** — trust boundaries, fallback behaviour, model-swap design  
3. **Final audit tools** — Lighthouse (broad) vs axe-core (component)  
4. **Hands-on** — build CineSeat end to end from an empty folder (sections A–E + CI + deploy checklist)

**Why this session exists:** Prior lectures taught pieces in silos. Bugs that only appear when auth, DB, agent tools, and UI meet are **trust-boundary** failures. You learn them by wiring one full product.

---

## Module 1 recap (exam anchors)

### Model selection

| Tier | Examples (as framed in lecture) | Trade-off |
|------|--------------------------------|-----------|
| **Frontier** | GPT, Claude, Gemini | High capability, high token cost |
| **Open weight** | Llama, Mistral, open GPT-OSS class | Data control; pay for hosting (some platforms free tiers) |
| **Specialised** | Domain / code LLMs | Narrow strength |

**Rule:** Weigh **cost, capability, and risk** together. Prototyping and production need not use the same tier.

### Tokens & hallucination

- ~**3–4 characters** per token; ~**1000 words ≈ 1300 tokens** (order-of-magnitude from lecture)  
- **Output tokens** often cost **4–5×** input  
- Cost ≈ `(tokens / 1_000_000) × rate` — cheap per call, expensive at user scale  
- **Hallucination:** false / fabricated / ungrounded claims stated **confidently**  
- **Calibration:** stated confidence matches real accuracy; ground with **RAG** (e.g. search only this repo) instead of model memory alone

### Spec → Prompt → Verify → Override

| Stage | What you do |
|-------|-------------|
| **Spec** | Exact behaviours + edge cases (unknown question, no facts, etc.) — not a prompt yet |
| **Prompt** | Turn spec into requests; generate code **and** tests per behaviour |
| **Verify** | Run tests, read diffs / results, check security surface — **find** problems |
| **Override** | Accept, reject, or send corrections back to the AI — **fix** problems |

**Critical distinction (in-lecture quiz):** Verify ≠ Override. Accepting / rejecting code is **override**.

**When rules beat AI:** unambiguous deterministic gates (segfault, missing component → do not ship). **AI wins** on ambiguous natural language and creative tasks.

### Stack thumb rules (condensed)

| Layer | Points hammered again |
|-------|------------------------|
| **Next.js** | Default **server components** (“routes”); `"use client"` only when interactivity needs it |
| **TypeScript** | `strict: true`; `noUncheckedIndexedAccess` |
| **Zod** | Shape validation at untrusted edges — not the same job as TanStack Query or Zustand |
| **Accessibility** | WCAG (aim **AA**), **ARIA** implements roles/state, **axe-core** verifies components |
| **Prisma** | Single source of truth for data shape; model relations / cardinality before ship |
| **Auth.js / NextAuth** | Delegate identity (e.g. Google); **JWT** session strategy as used in labs |
| **Order Mitra lessons** | Streaming UI, tools, HITL cancel — then **test + CI + Vercel** (Lecture 06) |

**Localhost joke:** Two developers both “ship” `localhost:3000` — a real app must leave the laptop.

---

## CineSeat product brief

Cinema chain (Inox-style) needs a self-service portal:

- Browse showtimes, pick seats on a **real seat map**, book  
- Persona: **Mrs Fernandez** always wants the same corner seat after many viewings  
- **Reel bot** recommends films, checks showtimes, can **cancel** bookings (with confirmation), optional discounts  
- Must work for **screen-reader** users selecting seats  
- Stack today: **Grok** (open models), Prisma + Postgres, Google OAuth, Jest tests, GitHub Actions, Vercel

**Usability requirement:** seat map navigable under WCAG / ARIA / axe — not just pretty squares.

---

## Trust boundaries

### Definition

A **trust boundary** is the line where you **stop assuming** data or intent is safe. Outside = **untrusted** (must verify). Inside = already validated.

It is a **verifier**, not a cache and not a UI preference store.

### CineSeat boundaries (lecture map)

| Crossing | Why untrusted | Typical control |
|----------|---------------|-----------------|
| **User → reel bot** | Free-form chat (“burn a million tokens”) | Prompt policy, rate limits, scrub / refine query |
| **Reel bot → tool calls** | Model may invent `cancel` / delete | Zod on tool args; allow-list tools |
| **Tool → database** | Wrong writes / wrong IDs | Auth session checks; Prisma transactions; deny by default |
| **Agent → UI** | UI shows booked when DB did not | Confirm success from real mutation result |

**Cross-layer bug examples:**

1. Booking query runs **before** auth session succeeds  
2. Agent tools share DB with UI and cancel when user only searched showtimes  
3. Agent reports success; seat map never updates  

### What is *not* a trust boundary (quiz trap)

| Layer | Job | Trust verification? |
|-------|-----|---------------------|
| **TanStack Query** | Fetch / cache server data | No — speed / sync |
| **Zustand** | Client preferences / UI state | No — local UX |
| **Zod** | Parse & validate untrusted shapes | **Yes** |
| **Prisma schema** | Typed persistence shape | Part of the data contract (lecture treated Zod/Prisma as boundary-adjacent; TanStack/Zustand are not) |

Correct **pairing** example: **tool-call arguments** (model output) → **execute** function that mutates state — that hop needs verification.

---

## Fallback behaviour

When the verifier rejects unsafe input/intent: **fail loudly and safely** — tell the user, **log**, do not pretend success.

**Never** leave failure mode to “whatever the system invents.”

| Failure | Example fallback (lecture) |
|---------|----------------------------|
| Provider times out mid-stream | Partial content + **retry** affordance |
| Tool args malformed (`delete entire DB`) | **Zod** rejects; no execution |
| Cancel proposed, user never confirms | **Safe default: nothing happens** (HITL) |
| Whole AI feature down | Rest of CineSeat (browse/book) still works |

### Model swap as architecture

Write providers so switching Grok ↔ Anthropic (etc.) is a **small change** (shared `streamText` / SDK pattern), not logic forked on model name strings. Optionally keep multiple adapters imported so production can flip one line after outage. Env vars alone do not swap proprietary SDK imports — code + deps must be ready.

---

## Lighthouse vs axe-core

| Tool | Scope | Best for |
|------|-------|----------|
| **Lighthouse** | Page-level audit in Chrome DevTools / CLI / Node; scores **0–100** on **performance, accessibility, best practices, SEO** | Fast overall health check before launch |
| **axe-core** | Component / DOM rule engine vs WCAG | Seat map buttons, ARIA pressed/disabled, focus order |

**Both needed:** Lighthouse = broad strokes; axe = component prescriptions. Run **repeatedly**, not once at kickoff.

**Score myth:** Accessibility **78** is **not** a pass — Lighthouse flags it (red) with failing checks to fix. Lighthouse **does** score accessibility (not performance-only).

### Local Lighthouse flow (as taught)

1. `npm run build` then serve production (`npm start`)  
2. Run Lighthouse against the URL (CLI / `npx lighthouse …`)  
3. Fix broad issues, then run **axe** for component gaps  

Common findings: colour contrast on booked seats / confirm buttons, missing visible focus, missing alt text.

**axe tip for booked seats:** native `disabled` removes seat from tab order (sighted users see grey; keyboard users skip). Prefer **`aria-disabled`** + keep focusable + guard `onClick` so screen-reader users still land on “booked” seats.

---

## Hands-on structure (CineSeat)

| Section | Goal |
|---------|------|
| **A — Scaffold** | `create-next-app`, strict TS, `.env.local`, `.gitignore`, baseline layout (“skip to main content”) |
| **B — Accessible seat map** | Seat status union, `Seat` / `SeatMap`, axe in-browser during dev, Jest seat tests |
| **C — Prisma + OAuth** | Showtime / Seat / Booking schema (avoid free-text status mistake from Lecture 04), migrate + seed, Google Auth.js, `bookSeat` trust checks |
| **D — Reel bot (Grok)** | Streaming API route, chat panel, `searchShowtimes`, **cancel with double confirmation** (HITL) |
| **E — Tests + CI** | Mock Grok / stream; message bubble, panel, offline stream tests; coverage; `.github/workflows/test.yml` |
| **Audit + deploy** | Lighthouse report; Vercel env vars; hosted Postgres (local DB will not reach Vercel); Google OAuth **redirect URLs** must include production origin, not only `localhost:3000` |

**Keys called out:** Grok API key, `AUTH_SECRET` (`npx auth secret`), Google OAuth client ID/secret, `DATABASE_URL`. Docker not required in this session.

---

## End-to-end mental model

```
Accessible UI (WCAG / ARIA / axe)
        ↓
Auth session (Google / JWT)
        ↓
Prisma + Postgres (showtimes, seats, bookings)
        ↓
Reel bot (Grok stream + tools)  ← trust boundaries + Zod + HITL
        ↓
Jest + GitHub Actions CI
        ↓
Lighthouse / axe audit → Vercel CD
```

---

## Key vocabulary

| Term | Meaning |
|------|---------|
| **Trust boundary** | Line where untrusted input must be verified before use |
| **Fallback behaviour** | Designed safe response when verification fails or dependencies die |
| **HITL** | Human-in-the-loop before destructive tools (cancel booking) |
| **Lighthouse** | Broad page scores (perf / a11y / best practices / SEO) |
| **axe-core** | Automated WCAG checks at component level |
| **Verify vs Override** | Find problems vs decide accept / reject / re-prompt |
| **Reel bot** | CineSeat’s cinema assistant agent |
