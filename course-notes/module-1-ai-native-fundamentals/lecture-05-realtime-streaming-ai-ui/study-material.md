# Lecture 05: Real-Time Streaming AI UI (Order Mitra)

**Topic:** User-facing systems — streaming chat UX, SSE vs polling vs WebSockets, Vercel AI SDK, structured output & confidence, agents/tool calling, human-in-the-loop (intro).

**Running example:** **Order Mitra** — a conversational assistant on the orders dashboard for online shopping / order lookup.

> **Transcript note:** The saved transcript ends mid-sentence during the ReAct / multi-step tool loop. Human-in-the-loop UI and the post-break hands-on are **introduced** in the lecture but **not fully transcribed** here. Exam prep below reflects what was actually covered on the recording.

---

## 1. Product → engineering requirements

PM ask (paraphrased): *“Add a chat assistant to the orders dashboard.”*

| PM requirement | Engineering meaning |
|----------------|-------------------|
| Answer like a **helpful teammate**, not a search box | **Streaming UX** — tokens appear as generated; user never stares at a blank screen |
| **Look up specific orders** when asked | Model must **run real code** (e.g. DB queries), not guess from weights |
| **Never take destructive action without asking** | **Human-in-the-loop (HITL)** — writes/changes need a user checkpoint |

Destructive example named in lecture: **cancel order**.

---

## 2. System shape (five building blocks)

1. **Browser** — chat UI (Next.js client component, `"use client"`).
2. **SSE stream** — server → browser, token-by-token updates.
3. **AI SDK route** — server handler that talks to the model and streams.
4. **Tool calls** — model requests server functions (e.g. `searchOrders`) for real data.
5. **Model provider** — Anthropic, OpenAI, Google Gemini, Groq, etc. (API you pay for; **not** the React Context “provider”).

Prior course context reused: App Router, routes under `app/api/.../route.ts`, Prisma, OAuth, TanStack Query, accessible UI, verifying AI-generated code.

---

## 3. Why streaming matters for LLM chat

- LLMs are **next-token predictors** — they generate **one token at a time** internally.
- **Old pattern:** wait for the full completion, then send one blob → user sees **3–5+ seconds of nothing**, then everything at once → feels broken.
- **Streaming:** send each piece to the browser **as it is ready** → WhatsApp-style “someone is typing” continuous feedback.
- Literature cited in lecture: ~**3×** improvement in **perceived** responsiveness with streaming vs long wait-then-dump.

**UX details:**

- Show **loading / streaming status** (cursor, “thinking”, typing indicator).
- Avoid silent failures — user must know work is in progress or that something failed.

---

## 4. Polling vs persistent connection

### Polling

- Browser **repeatedly asks** the server: “Anything new?” (e.g. every second).
- Each poll: **open request → response → close connection** → repeat.
- Problems for chat: many round trips return **“nothing yet”** → wasted bandwidth, battery, server load; scales badly (many tabs × many polls).

**When polling is OK (lecture):** infrequent updates (e.g. roughly **once every ~10 minutes**).

### Persistent connection

- **One connection stays open**; server **pushes** data when ready — no re-asking for each chunk.

---

## 5. Server-Sent Events (SSE)

**SSE** = rules for **server → client**, **one-way** push over **plain HTTP** (no WebSocket protocol upgrade).

| Fact | Detail |
|------|--------|
| Origin | Concept ~**2004** (stock tickers, live scores, news); standardized **HTML5 (~2006)** |
| LLM chat adoption | From **~2023** onward — transport under **most streaming chat UIs** |
| Direction | **Unidirectional:** server speaks; client does not send on the same SSE channel |
| vs polling | SSE = **one persistent connection**; polling = **many short-lived requests** |

**Examples given:** Cricinfo live scores, stock tickers, GitHub Actions log tail, ChatGPT/Claude/Grok-style word-by-word replies — **page updates without refresh** → often SSE.

**Wire / headers (lecture + demo):**

- `Content-Type: text/event-stream` — tells browser to treat response as SSE (not one-shot `application/json`).
- **`Cache-Control`** — avoid caching live streams.
- **`Connection`** — keep connection open so server can keep sending.
- Chunks formatted as SSE **`data:`** events; demo stressed **`\\n\\n`** to delimit events/chunks.
- Server: **`ReadableStream`** with `controller.enqueue()` per chunk, then `controller.close()` when done.
- Client: **`EventSource(url)`** — built-in; **`onmessage`** receives chunks; **auto-reconnects** if connection drops.

**Next.js mapping:**

- **Route** (`app/api/.../route.ts`) — server-side streaming handler.
- **Client component** — `EventSource` or AI SDK hooks.

---

## 6. SSE vs WebSockets

| | **SSE** | **WebSockets** |
|---|--------|----------------|
| Direction | Server → client (one-way) | **Bidirectional** — both sides anytime |
| Setup | Simpler; plain HTTP | More setup, infra, complexity |
| Good for | LLM **token stream to UI**, live feeds | Live **voice** (mic → server + reply), multiplayer co-editing, anything needing **continuous client → server** stream |

**Lecture guidance:**

- Typical **text chat** streaming: **SSE is enough**; WebSockets can be **overkill**.
- **Wrong mantra:** “SSE always good, WebSockets always bad” — choose by **data flow direction** and interaction pattern.

---

## 7. Vercel AI SDK (`ai` package)

- **Why:** Every AI chat product repeats the same plumbing (call model, stream tokens, loading/error states, SSE formatting). Hand-rolling `ReadableStream` + SSE every time is repetitive.
- **History:** Vercel (Next.js) noticed the pattern across Jasper, Perplexity, Runway, etc.; **AI SDK shipped June 2023** (`npm install ai`).
- **Provider-agnostic:** Same patterns for Claude, OpenAI, Groq, etc. via provider packages (e.g. `@ai-sdk/anthropic`, `@ai-sdk/groq`).

### Server vs client (exam-critical)

| API | Side | Role |
|-----|------|------|
| **`streamText`** | Server | Calls model, streams tokens; handles SSE/stream response plumbing (replaces hand-built `ReadableStream` for chat) |
| **`generateText`** | Server | Non-streaming (or generic) text generation from model |
| **`generateObject`** | Server | **Structured output** — model fills a schema (with **Zod**) |
| **`useChat`** | Client | Messages, input, submit, streaming UI state; points at your API route |
| **`EventSource`** | Client | Raw SSE consumer (demo counter) |

**Typical chat route pattern (lecture):**

- `POST` → read messages from request JSON.
- `streamText({ model, system, messages, ... })`.
- Return stream response (lecture: `toDataStreamResponse()` / UI message stream helpers in hands-on).

**Typical client pattern:**

- `useChat({ api: '/api/ordermitra' })` → `messages`, `input`, `handleSubmit`, **`status`** (e.g. streaming).

**Steering AI code generation:** If you only say “build a chatbot”, models may use **polling** or non-streaming patterns — specify **`streamText` + `useChat`** explicitly.

**Hands-on:** Groq API key in `.env.local` (`GROQ_API_KEY`); console at `console.groq.com` — copy key once; can use Groq-hosted open models (e.g. GPT-OSS 120B mentioned in demo).

---

## 8. Hallucination, structured output, confidence

**Problem:** Models sound confident when wrong (e.g. “Mr. Iyer’s order shipped yesterday” with no DB access).

**Structured output:** Force a **shape**, not a free-text blob — like giving the model a **form** to fill.

- **`generateObject`** + **Zod** schema (validation library — describes types/shape, does not store data).
- Example fields from lecture:
  - `answer` (string)
  - `confidence`: `high` | `medium` | `low`
  - `groundedInSource`: boolean (is answer supported by provided context?)

**UI — confidence badges:**

- Color: green / amber / red mapped to enum.
- **Accessibility:** Do **not** rely on color alone — also show text like `Confidence: low` (color-blind users).

**Errors / stream failures:**

- Network drop mid-stream → **keep partial content**, offer **clear retry**.
- Rate limits / 5xx → user-visible message, retry — not “nothing is happening”.
- User navigates away → `useChat` **status** can surface errors; don’t silently discard partial work.

**Recap stack:**

1. User message → backend.
2. **`generateText`** or **`generateObject`** to talk to model (structured when you need typed fields).
3. **`streamText`** to stream conversational replies to client.
4. **`useChat`** on client (handles SSE under the hood for chat).

Also mentioned: **generative / stream UI** (React components, not just plain text) as a further step.

---

## 9. Agents, tools, and function calling

**Problem:** Order Mitra has a “brain” (LLM) but no “eyes” — it cannot see your Prisma DB unless you **tool** it.

**Agent (lecture):** Software that **decides its own next action** — e.g. when a fact is needed, run a DB query instead of trusting memory.

**History:**

- **ReAct** paper (Yao et al., Princeton, **Oct 2022**) — **Reason + Act** loop.
- **Native function calling** (~**2023**, OpenAI & Google) — reliable **think → call tool → observe → repeat** in production; largely replaced hand-written ReAct prompting strings.

**Tool = function you expose to the model:**

- Model **never runs your code on its GPU host** — it returns a **tool call request** (name + args).
- **Your server** executes `execute`, returns result to model.

**`searchOrders` pattern (lecture):**

```ts
tool({
  description: 'Search orders by customer name or status…',
  parameters: z.object({
    customerName: z.string().optional(),
    status: z.enum(['pending', 'shipped', 'delivered']).optional(),
  }),
  execute: async ({ customerName, status }) =>
    prisma.order.findMany({ where: { … } }),
})
```

- **`description`** — when the model should use the tool.
- **`parameters` / input schema** — Zod-shaped arguments.
- **`execute`** — real Prisma (or other) code.

**Multi-step loop:**

1. **Think** — model reasons about next step.
2. **Act** — model calls tool with arguments.
3. **Observe** — tool result appended to context.
4. **Repeat or answer** — another tool call or final user-facing reply.

(Pass tools into **`streamText({ tools })`** in the full app; transcript cut before detailed route/UI for tools and HITL.)

---

## 10. Human-in-the-loop (coverage in transcript)

- Required for **data-changing** actions vs read-only lookup.
- Lecture plan: confirm in UI before **destructive** ops (e.g. **cancel order**); agents can harm UX or server state if unchecked.
- **Implementation details** (confirm cards, `addToolOutput`, separate run route) were scheduled for hands-on **after** the break — **not present in the truncated transcript**.

---

## 11. Hands-on milestones (lecture demos)

1. **SSE counter** — `app/api/counter/route.ts`: `ReadableStream`, `text/event-stream`, stream `1…5` with delays; client `EventSource`.
2. **Plain streaming chat** — `streamText` + Groq model + system prompt “Order Mitra assistant”; ~6–10 lines of backend after frontend ready.
3. (Planned in lecture arc) Tools + HITL on Order Mitra — transcript incomplete.

---

## 12. Quick decision guide

| Need | Choose |
|------|--------|
| Server pushes LLM tokens / live one-way updates | **SSE** (+ AI SDK `streamText` / `useChat`) |
| Continuous two-way stream (voice, multiplayer) | **WebSockets** |
| Rare updates | **Polling** |
| Typed confidence / fields from model | **`generateObject` + Zod** |
| Real order data | **`tool()` + DB execute** |
| Delete/cancel/ mutate production data | **Human confirmation (HITL)** |

---

## 13. Glossary (lecture spellings normalized)

| Term | Meaning |
|------|---------|
| SSE / Server-Sent Events | One-way HTTP push stream |
| Model provider | Vendor hosting the LLM (Anthropic, OpenAI, Groq, …) |
| Structured output | JSON-like fields constrained by schema |
| Tool / function calling | Model requests server-side function execution |
| HITL | User approves risky actions before execution |
