# Lecture 05 — Likely Exam Q&A

Answers follow the **lecture transcript** only. Where the transcript is incomplete, questions note the gap.

---

## Order Mitra & UX

**Q1. What three product requirements drive Order Mitra’s engineering design?**  
**A.** (1) Responsive, teammate-like answers via **streaming**. (2) **Real data** for order lookup via server-side code/tools, not guesses. (3) **No destructive actions** without explicit human approval (human-in-the-loop).

**Q2. Why is “wait 4–5 seconds then show the full answer at once” a UX failure for LLM chat?**  
**A.** The model already generates **token-by-token**; hiding that progress leaves the user on a **blank or frozen screen** with no feedback about whether the system is working.

**Q3. What analogy did the lecture use for streaming feedback?**  
**A.** WhatsApp **typing indicators** — continuous signal that a reply is being composed live.

---

## Polling, SSE, WebSockets

**Q4. How does polling work, and why is it a poor fit for streaming chat?**  
**A.** The client ** repeatedly HTTP-requests** “anything new?” (often on a timer). Many responses are empty, wasting **bandwidth, battery, and server capacity**; a long answer can require **dozens of round trips**.

**Q5. What is the core idea of a persistent connection for streaming?**  
**A.** Open **one connection**, leave it **open**, and let the **server push** chunks as they are ready instead of closing and reopening per poll.

**Q6. Define Server-Sent Events (SSE) in one sentence.**  
**A.** A **one-way**, **HTTP-based** stream where the **server pushes** updates to the browser over a **long-lived connection**.

**Q7. When was SSE conceptualized, standardized, and adopted for LLM streaming (per lecture)?**  
**A.** Concept ~**2004** (tickers, live scores, news); standardized with **HTML5 ~2006**; widely used for **LLM token streaming from ~2023**.

**Q8. SSE vs WebSockets — when do you pick each?**  
**A.** **SSE** when you mainly need **server → client** updates (typical chat token stream). **WebSockets** when you need **bidirectional** persistent traffic (e.g. live voice to server + replies, multiplayer streaming edits).

**Q9. Is “SSE good, WebSockets bad” correct?**  
**A.** **No.** Choose based on **direction and interaction** — WebSockets are appropriate when the client must **continuously send** data too.

**Q10. What is `EventSource`, and what happens if the SSE connection drops?**  
**A.** Browser API that opens an SSE connection and delivers **`onmessage`** events; it **reconnects automatically** after drops (highlighted in in-lecture quiz).

**Q11. What `Content-Type` header marks an SSE response?**  
**A.** **`text/event-stream`** (not one-shot JSON for a live token stream).

**Q12. Name server- and client-side pieces used in the raw SSE demo.**  
**A.** Server: **`ReadableStream`**, `controller.enqueue()`, correct SSE headers. Client: **`"use client"`** component, **`new EventSource('/api/...')`**, append chunks in **`onmessage`**.

**Q13. When is polling still reasonable?**  
**A.** When updates are **infrequent** (lecture example: on the order of **every ~10 minutes**).

---

## Vercel AI SDK

**Q14. Why was the Vercel AI SDK created?**  
**A.** Many products duplicated the same work: call a model provider, **stream tokens**, track loading/errors, format SSE — the SDK centralizes that **plumbing** (shipped **June 2023**, `npm install ai`).

**Q15. What is a “model provider” in this lecture?**  
**A.** A company/service running the model and exposing an **API** (Anthropic, OpenAI, Google, Groq, etc.) — **not** React Context providers.

**Q16. `streamText` vs `useChat` — where do they run and what do they do?**  
**A.** **`streamText`** — **server** route: call model, stream response, handle stream/SSE wiring. **`useChat`** — **client** hook: message list, input, submit, streaming **status** against your API route.

**Q17. Why must you tell AI assistants to use `streamText` / `useChat` explicitly?**  
**A.** Generic “build a chatbot” prompts may produce **polling** or non-streaming designs — worse UX and **higher cost** without benefit.

**Q18. What does `generateText` vs `generateObject` vs `streamText` each emphasize?**  
**A.** **`generateText`** — get text from the model on the server. **`generateObject`** — get **structured**, schema-shaped data (with **Zod**). **`streamText`** — **stream** model output to the client (SSE-style chat UX); in quiz framing, it is the API tied to **SSE delivery to the browser** (see `quiz.md` nuance).

---

## Structured output & confidence

**Q19. What problem does structured output solve?**  
**A.** Free-form answers are hard to parse and can **hallucinate confidently**; a **fixed schema** yields usable fields (answer, confidence, grounded-in-source).

**Q20. What is Zod’s role with `generateObject`?**  
**A.** **Validation/schema library** — defines the **exact shape** the model must return (like a form), not a database store.

**Q21. How should confidence be shown in the UI?**  
**A.** Badges with **color** (high/medium/low) **plus explicit text labels** — color alone fails for **color-blind** users.

**Q22. What should the UI do if streaming stops halfway (network error)?**  
**A.** **Keep partial content visible** and offer a **clear retry** — avoid silent failure or wiping text already shown.

**Q23. What is `groundedInSource` meant to convey?**  
**A.** Whether the answer is **supported by supplied context** vs inferred/guessed.

---

## Agents & tools

**Q24. Why isn’t the raw LLM enough for “Where is Mr. Iyer’s order?”**  
**A.** The model **has not seen your database**; it may invent plausible but **wrong** shipping statuses even with low confidence.

**Q25. Define an agent in this lecture.**  
**A.** Software where the model **chooses its next action** — e.g. calling a tool to **query real data** before answering.

**Q26. What is ReAct, and what replaced handwritten ReAct prompts in production?**  
**A.** **Reasoning + Acting** loop (ReAct paper, **Oct 2022**). **Native function calling (~2023)** made the think/act/observe loop **reliable** in products.

**Q27. What three parts does a tool definition need?**  
**A.** **Description** (when to use), **parameters/schema** (arguments, often Zod), **`execute`** (your server code — e.g. Prisma query).

**Q28. Does the model run `execute` on OpenAI/Groq’s servers?**  
**A.** **No.** The model returns a **tool call**; **your server** runs `execute` and sends the **result back** into the conversation.

**Q29. Describe the multi-step tool loop.**  
**A.** **Think** → **Act** (tool call) → **Observe** (append result) → **repeat** or produce final answer.

**Q30. What was planned for human-in-the-loop after the break (transcript incomplete)?**  
**A.** **User confirmation** before **destructive** actions such as **cancel order**; full UI/API flow was scheduled for hands-on but **not captured** in the saved transcript.
