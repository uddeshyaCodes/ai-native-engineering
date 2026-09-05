# OrderMitra

Build OrderMitra yourself, one chapter at a time. Every API route you need to write is marked with a `TODO`. **The app runs at every stage**, even before you've written anything every unfinished route returns a safe placeholder instead of crashing, so you can always open any page and see something, not a blank screen or an error.

## Workshop Reference

Quick lookup for what each chapter covers, which files to open, and what you learned. Update the **Status** column as you complete chapters.

| Ch. | Topic | Demo page | Files | Status |
| --- | ----- | --------- | ----- | ------ |
| 1 | Server-Sent Events (SSE) | `/counter-demo` | `app/api/counter/route.ts`, `app/counter-demo/page.tsx` | Done |
| 2a | Vercel AI SDK — streaming chat | `/orders-basic` | `app/api/ordermitra-basic/route.ts`, `app/orders-basic/page.tsx` | Done |
| 2b | Structured output + confidence | `/confidence-demo` | `app/api/answer/route.ts`, `app/confidence-demo/page.tsx` | Done |
| 2c | Structured output (second exercise) | — (API only) | `app/api/order-summary/route.ts` | Done |
| 3 | Agentic patterns — tool calling | `/orders-search` | `lib/tools/search-orders.ts`, `app/api/ordermitra-search/route.ts`, `app/orders-search/page.tsx` | Done |
| 4 | Human-in-the-loop UI | `/orders-full` | `lib/tools/cancel-order.ts`, `app/api/ordermitra-full/route.ts`, `app/api/run-cancel-order/route.ts`, `app/orders-full/page.tsx` | Done |

---

### Chapter 1 · Server-Sent Events (SSE)

**Files:** `app/api/counter/route.ts` · `app/counter-demo/page.tsx`

**What we learned**

- **SSE** is a one-way text stream from server → browser over a long-lived HTTP GET.
- Wire format: `data: <payload>\n\n` — the blank line marks the end of one event.
- Server: `ReadableStream` + `controller.enqueue()` pushes chunks; `Content-Type: text/event-stream` tells the browser how to parse them.
- Client: `new EventSource("/api/counter")` opens the connection; `onmessage` receives each event as `event.data`.
- **Cleanup:** use `cancel()` on the stream (not a return from `start()`) to `clearInterval` when the client disconnects — otherwise you get "Controller is already closed" errors.
- The counter loops `1 → 5 → 1 → …` by resetting to `0` after `5` instead of calling `controller.close()`.

**Request flow**

```
/counter-demo  →  EventSource GET /api/counter  →  ReadableStream enqueues "data: N\n\n" every second
```

---

### Chapter 2a · Vercel AI SDK — streaming chat

**Files:** `app/api/ordermitra-basic/route.ts` · `app/orders-basic/page.tsx`

**What we learned**

- **Client:** `useChat` from `@ai-sdk/react` manages message state; `DefaultChatTransport({ api: "..." })` POSTs to your route.
- **Server:** `streamText` calls the LLM (Groq) and streams tokens as they are generated.
- `convertToModelMessages(messages)` converts the client's `UIMessage[]` format into what the model provider expects.
- **AI SDK v7 response pattern** (replaces deprecated `result.toUIMessageStreamResponse()`):
  ```ts
  createUIMessageStreamResponse({
    stream: toUIMessageStream({ stream: result.stream }),
  })
  ```
- No tools yet — OrderMitra can only chat; order lookup comes in Chapter 3.

**Request flow**

```
/orders-basic  →  useChat POST /api/ordermitra-basic  →  streamText (Groq)  →  UI message stream back to client
```

---

### Chapter 2b · Structured output + confidence indicator

**Files:** `app/api/answer/route.ts` · `app/confidence-demo/page.tsx`

**What we learned**

- **Structured output** forces the model to return typed JSON instead of free-form text.
- **AI SDK v7:** use `generateText` + `Output.object({ schema })` (replaces `generateObject`).
- **Zod schema** defines the shape: `answer`, `confidence` (`high` | `medium` | `low`), `groundedInSource` (boolean).
- `.describe()` on each Zod field gives the model hints for what to put in each property.
- **System prompt** instructs the model to answer only from the provided context and self-report confidence.
- Client sends `{ context, question }` via `fetch` POST; server returns `Response.json(output)`.
- **Grounded in source** = is the answer directly supported by the context, or did the model infer/guess?

**Request flow**

```
/confidence-demo  →  fetch POST /api/answer { context, question }  →  generateText + Output.object  →  JSON response
```

---

### Chapter 2c · Structured output — order summary

**Files:** `app/api/order-summary/route.ts` · `lib/prisma.ts` · `prisma/seed.ts`

**What we learned**

- Same **`generateText` + `Output.object`** pattern as Chapter 2b, but the context comes from **Prisma** instead of a pasted string.
- POST body: `{ customerName }` — e.g. `"Mr. Iyer"`.
- `prisma.order.findMany({ where: { customerName: { contains: customerName } } })` loads matching rows from SQLite.
- Structured fields: `summary`, `confidence`, `ordersReferenced` (how many orders the model included).
- Short-circuit when no orders match — return JSON directly without calling the LLM.
- No demo page; test with curl or any HTTP client.

**Request flow**

```
POST /api/order-summary { customerName }  →  Prisma findMany  →  generateText + Output.object  →  JSON { summary, confidence, ordersReferenced }
```

**Try it**

```bash
curl -s -X POST http://localhost:3000/api/order-summary \
  -H "Content-Type: application/json" \
  -d '{"customerName":"Mr. Iyer"}' | jq
```

---

### Chapter 3 · Agentic patterns — tool calling

**Files:** `lib/tools/search-orders.ts` · `app/api/ordermitra-search/route.ts` · `app/orders-search/page.tsx`

**What we learned**

- **Tools** let the model call your server code instead of guessing — `tool({ description, inputSchema, execute })`.
- `description` is critical — it tells the model *when* to use the tool.
- `execute` runs a Prisma query and returns JSON the model reads on the next step.
- **`streamText({ tools })`** — same streaming chat as Ch.2a, plus a tool loop.
- Pass `tools` to **both** `streamText` and `convertToModelMessages(messages, { tools })` so tool-call history round-trips correctly.
- **`stopWhen: stepCountIs(5)`** — default is `stepCountIs(1)`, which stops before the model can call a tool and reply. Raising the step count allows: user message → tool call → tool result → assistant answer.
- Client UI shows `tool-searchOrders` parts (`Running searchOrders...` / `✓ searchOrders complete`).

**Request flow**

```
/orders-search  →  useChat POST /api/ordermitra-search
  →  streamText decides to call searchOrders
  →  execute() queries Prisma
  →  model summarizes results
  →  streamed reply to client
```

**Try it:** “find pending orders for Mr. Iyer”

---

### Chapter 4 · Human-in-the-loop

**Files:** `lib/tools/cancel-order.ts` · `app/api/ordermitra-full/route.ts` · `app/api/run-cancel-order/route.ts` · `app/orders-full/page.tsx`

**What we learned**

- **`cancelOrder` has no `execute()`** — without it, the SDK pauses and waits for the client to supply the tool result via `addToolOutput`.
- **Destructive actions** should be proposed by the model, then confirmed by a human in the UI.
- Flow: model calls `searchOrders` → finds order ID → calls `cancelOrder` → UI shows confirm card at `tool-cancelOrder` / `input-available`.
- **Confirm** → `POST /api/run-cancel-order` → `runCancelOrder()` updates Prisma → `addToolOutput` resumes the chat.
- **Cancel** → `addToolOutput({ skipped: true })` tells the model the user declined.
- `runCancelOrder` lives outside the tool definition — the only path to real cancellation.

**Request flow**

```
/orders-full  →  streamText (searchOrders + cancelOrder)
  →  cancelOrder pauses (no execute)
  →  user clicks Confirm  →  POST /api/run-cancel-order  →  Prisma update
  →  addToolOutput  →  model streams final reply
```

**Try it:** “cancel Mr. Iyer's diya order”

---

## Setup

```bash
npm install
# paste your real key: GROQ_API_KEY = your-key-here

npx prisma generate
npx prisma db push
npx tsx prisma/seed.ts

npm run dev
```

Open **http://localhost:3000**.

## What you'll build, in order

| Route                | Chapter                   | File(s) to complete                                                    |
| -------------------- | ------------------------- | ---------------------------------------------------------------------- |
| `/counter-demo`    | Ch.1 · SSE               | `app/api/counter/route.ts`                                           |
| `/orders-basic`    | Ch.2 · AI SDK            | `app/api/ordermitra-basic/route.ts`                                  |
| `/confidence-demo` | Ch.2 · Confidence        | `app/api/answer/route.ts`, <br />`app/api/order-summary/route.ts`  |
| `/orders-search`   | Ch.3 · Agentic Patterns  | `lib/tools/search-orders.ts`, `app/api/ordermitra-search/route.ts` |
| `/orders-full`     | Ch.4 · Human-in-the-Loop | `lib/tools/cancel-order.ts`, `app/api/ordermitra-full/route.ts`    |

Open each file the `TODO`, plus anything you need to know before running it. Work through them in order; each chapter builds on the last.

**Already done for you** (not part of the lesson): the chat UI pages (`app/*/page.tsx`), the database setup (`prisma/`, `lib/prisma.ts`), and `app/api/run-cancel-order/route.ts`. Read them if you're curious how the pieces fit together, but you don't need to write them.

## An important note on Chapter 4

`lib/tools/cancel-order.ts` has a `TODO` and a warning worth reading before you prompt: don't give the `cancelOrder` tool an `execute()` function. If it has one, it runs the moment the model calls it the confirmation card in `/orders-full` never actually gets a chance to block it. Leaving `execute()` off is what makes the human-in-the-loop pattern real instead of decorative. The comment in that file explains where the actual cancellation logic goes instead.

## If a page looks stuck on "TODO"

That's not broken it's the expected placeholder response for whichever route you haven't implemented yet. Once you replace a route's TODO with real code, that page's response updates automatically (no restart needed with `npm run dev`).

**One exception:** if you're using `npm run build && npm start` instead of `npm run dev`, you must re-run `npm run build` after every code change `next start` serves a frozen snapshot, not live source.

## Model

Every route uses `groq("openai/gpt-oss-120b")` via `@ai-sdk/groq`. Free API key, no card required: console.groq.com. If a model ever stops working with a `model_not_found` error, Groq's catalog changed list what's currently available with:

```bash
curl -s https://api.groq.com/openai/v1/models -H "Authorization: Bearer $GROQ_API_KEY" | jq -r '.data[].id'
```
