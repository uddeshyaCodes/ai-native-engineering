# Lecture 02: Important Exam Q&A

Questions aligned with lecture emphasis and Mentimeter explanations. Answers are concise for MCQ revision.

---

## Node.js event loop & timers

### Q1. What sits between Node.js JavaScript and the operating system, and what is its role?

**A.** **libuv** translates JavaScript I/O into OS system calls and coordinates completion with the **event loop** (single-threaded JS, concurrent I/O via libuv).

### Q2. List the six event-loop phases in order (as taught in this lecture).

**A.** (1) **Timers** (`setTimeout`/`setInterval`), (2) **Pending callbacks**, (3) **Idle, prepare** (internal), (4) **Poll** (I/O callbacks, e.g. `fs.readFile`), (5) **Check** (`setImmediate`), (6) **Close callbacks** (e.g. socket close).

### Q3. What is printed by `console.log('A'); setImmediate(() => console.log('B')); console.log('C');`?

**A.** **A, C, B** — sync code runs first; `setImmediate` only registers for the check phase.

### Q4. Inside an `fs.readFile` callback, you register both `setImmediate` and `setTimeout(fn, 0)`. Which runs first?

**A.** **`setImmediate`** (check phase of current iteration) before **`setTimeout`** (timers phase of **next** iteration).

### Q5. Where does `process.nextTick` run relative to the event loop phases?

**A.** **Between** iterations—after the current turn finishes, **before** the next iteration’s timers phase. The nextTick queue must empty before the loop continues.

### Q6. Why is recursive `process.nextTick` dangerous?

**A.** It can **starve the event loop**—the loop never advances to poll/check, so **I/O callbacks never run**.

### Q7. What output order does the lecture give for sync `A`, two consecutive `process.nextTick` (`B`, `C`), then sync `D`?

**A.** **A, D, B, C** — sync through `D`, then drain the nextTick queue (FIFO: B then C).

### Q8. What does “run to completion” mean for Node’s JavaScript thread?

**A.** Once JS starts executing a synchronous chunk, it generally **does not yield mid-function** to handle I/O; I/O completions are scheduled for **later loop iterations**.

---

## Streams & middleware

### Q9. Name the four stream types and give the lecture’s example of duplex.

**A.** Readable, writable, **duplex**, transform. **`net.Socket`** (client–server connection) is **duplex** (read and write).

### Q10. What is the main advantage of `stream.pipeline()` over chaining `.pipe()`?

**A.** **`pipeline`** forwards errors, **stops** the chain, and **destroys** streams on failure with cleaner cleanup; `.pipe()` needs per-stream error handlers and may leave partial/junk output.

### Q11. In Express middleware `(req, res, next)`, what happens if you never call `next()`?

**A.** The request **hangs**—the chain never reaches route handlers or response completion.

### Q12. What did the auth middleware demo require for `/hello` to succeed?

**A.** Pass **`token=secret`** (correct token query/param); otherwise unauthorized.

---

## TypeScript (strict, generics, unions)

### Q13. What does `"strict": true` in `tsconfig.json` accomplish (per lecture)?

**A.** Enables **strict type checking**—catches hazards involving **`any`**, **null**, **`never`**, and related unsound patterns **at compile time** instead of at runtime.

### Q14. Why is `function first(arr: any[]): any` worse than `function first<T>(arr: T[]): T | undefined`?

**A.** **`any`** severs the link between **input element type** and **return type**; **generics** preserve `T` so callers get accurate types (e.g. `number` vs `string`).

### Q15. What does `T extends { length: number }` mean on a generic?

**A.** **`T` must be a type that has a numeric `length` property** (e.g. string, array)—rejecting types like plain `number`.

### Q16. What is a discriminated union and why share a field like `status` or `kind`?

**A.** A union of object variants distinguished by a **common literal property**; TypeScript **narrows** each branch so you cannot treat `success` like `idle` or access fields that do not exist on that variant.

### Q17. Why assign the `default` case of an exhaustive `switch` on a discriminated union to `never`?

**A.** If a **new variant** is added to the union but the switch is not updated, assigning to **`never`** causes a **compile error**—forcing exhaustiveness.

### Q18. What is the `never` (bottom) type?

**A.** A type representing values that **cannot exist**; used for impossible branches and exhaustiveness checks.

---

## Next.js App Router

### Q19. What is the default rendering location in the App Router, and how do you opt into the client?

**A.** **Server** by default (RSC/server components). Add **`'use client'`** at the top of a file for client-only features (e.g. `useState`).

### Q20. Where should URL-specific changing data live—`layout.tsx` or `page.tsx`?

**A.** **`page.tsx`**. Shell, providers, shared layout → **`layout.tsx`**.

### Q21. What is the purpose of `loading.tsx` in the streaming demo?

**A.** **Suspense fallback**—placeholder UI while slow server components stream in.

### Q22. How did the dashboard demo behave on refresh?

**A.** **Static shell/nav** appeared immediately; **stats** after ~**2 seconds**; **news** after ~**5 seconds** (intentional `sleep` in server components).

### Q23. Name the four rendering strategies discussed (static → dynamic).

**A.** **Static** (build-time HTML), **revalidated** (cached + periodic refresh), **on-demand** (regenerate when triggered), **dynamic** (per-user, cookies/headers, no shared cache—e-commerce/travel).

### Q24. Why use streaming SSR with Suspense instead of one blocking SSR response?

**A.** Users get a **navigable shell** immediately; slow data **streams in** when ready—better UX than a blank page while DB queries run.

---

## Cross-cutting

### Q25. What two topics did the instructor call the main conceptual takeaways?

**A.** **Event loop** behavior (including not blocking it) and **streaming SSR / Suspense**; plus **defensive TypeScript** for correctness before deployment.
