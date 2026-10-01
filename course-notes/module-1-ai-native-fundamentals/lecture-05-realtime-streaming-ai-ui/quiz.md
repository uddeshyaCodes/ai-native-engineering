# Lecture 05 — In-Lecture Quizzes (Mentimeter)

The lecture included **two Mentimeter quizzes**. The transcript records **professor-stated correct answers**; full question stems and all distractors were **not** read aloud verbatim. Use this file to align with what was graded in class.

---

## Quiz 1 — SSE & transport (before first hands-on)

| # | Stated correct answer | Key idea tested |
|---|----------------------|-----------------|
| **1** | **Option B** | SSE origins: concept **~2004** for **stock tickers, live scores, news feeds**; widespread use for **LLMs from ~2023** onward. |
| **2** | **Option C** | **SSE** uses a **persistent connection**; **polling** **repeatedly opens new requests** (ask → reply → close → repeat). |
| **3** | Affirmed **“Yes”** (SSE sufficient for LLMs) | For typical LLM **output streaming**, you only need **one-way server → client** data; **WebSockets** are **bidirectional** and **overkill** for that pattern alone. |
| **4** | **EventSource** behavior | **`EventSource` reconnects automatically** if the SSE connection drops. |
| **5** | **Option C** | SSE responses use **`Content-Type: text/event-stream`**. |

Professor noted all five matched the “wisdom of the crowd” in session.

---

## Quiz 2 — Vercel AI SDK, structured output, errors (mid-lecture, before break)

| # | Stated correct answer | Key idea tested |
|---|----------------------|-----------------|
| **1** | **`streamText`** (not `useChat`) | **`useChat`** and **`EventSource`** are **client-side**. **`streamText`** and **`generateObject`** are **server-side**. For **SSE-style streaming to the browser**, the quiz answer emphasized **`streamText`** as handling that transport path; **`generateObject`** is for **structured model output**, not replacing the streaming chat pipe. *(Many students picked `useChat` — professor clarified client vs server.)* |
| **2** | **`useChat`** | Client hook that owns **message streaming UI** and talks to your chat API route. |
| **3** | **`generateObject` with a Zod schema** | **Zod** defines **types/schema** for structured LLM responses. |
| **4** | **Option B** | Showing confidence by **color alone** is a **UI mistake** — **color-blind users** cannot rely on color only; use **text labels** too. |
| **5** | **Option C** | When a stream **stops halfway**: **keep partial content visible** and offer a **clear retry** action. |

---

## Quiz 3 — Agents / HITL

**None in transcript.** The recording ends during the **agents / tool-calling** lecture segment, before any third quiz was run.

---

## Study tip

If your graded MCQ bank mirrors these polls, prioritize:

- SSE vs polling vs WebSockets **tradeoffs**
- **`text/event-stream`**, **EventSource**, **persistent vs repeated connections**
- **`streamText` / `generateObject` / `useChat`** — **server vs client**
- **Zod + structured confidence** and **accessible** confidence UI
- **Stream error UX** (partial content + retry)
