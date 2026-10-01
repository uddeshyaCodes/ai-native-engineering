# Lecture 02: In-Lecture Mentimeter Quizzes

Two quizzes were run live (5 questions each, ~1 minute per question). The transcript records **correct options** and **post-quiz explanations**; exact slide wording is not always verbatim. Question stems below are **reconstructed from lecture + TA explanation** where the slide text was not spoken.

---

## Quiz 1 — After Module 1 (Node.js)

**Facilitator:** TA (Shohikoth); **Professor explanation** after quiz.

### Q1. What is the correct order of the six Node.js event-loop phases?

| Option | Phase order (interpretation) |
|--------|------------------------------|
| A–D | (Various wrong orderings on slide) |
| **B ✓** | **Timers → Pending callbacks → Idle/prepare → Poll → Check → Close callbacks** |

**Explanation (lecture):**

- **Timers:** `setTimeout` / `setInterval` callbacks registered here.  
- **Pending callbacks:** deferred system/network callbacks (mostly internal).  
- **Idle, prepare:** internal libuv.  
- **Poll:** I/O such as **`fs.readFile`** completions.  
- **Check:** **`setImmediate`**.  
- **Close:** e.g. **`socket.on('close')`**.

**Live result:** Correct answer announced as **option B**.

---

### Q2. Inside an `fs.readFile` callback, both `setImmediate` and `setTimeout(..., 0)` are scheduled. Which runs first?

| | |
|---|---|
| **B ✓** | **`setImmediate` runs before `setTimeout`** |

**Explanation:**

- `readFile` callback runs in **poll** phase.  
- Next phase in the **same** iteration is **check** → `setImmediate`.  
- Current iteration’s **timers** phase already passed → `setTimeout` runs in the **next** iteration’s timers phase.  
- Order of registration inside the callback does not change this.

**Live result:** **Option B** (TA: “obviously option B is the right answer” after Q1).

---

### Q3. Which statement about `process.nextTick` is correct?

| | |
|---|---|
| **C ✓** | **`process.nextTick` callbacks run between event-loop phases / between iterations; recursive `nextTick` can block the main thread and prevent I/O from being serviced** |

**Explanation:**

- nextTick fires **between any two stages** (between end of one iteration and start of next).  
- Until the nextTick queue empties, the loop **cannot** proceed normally → **recursive nextTick** blocks I/O and prevents the loop from advancing.

**Live result:** **Option C** (“almost all of you… option C”).

---

### Q4. What kind of stream is a TCP `net.Socket`?

| | |
|---|---|
| **Duplex ✓** | **Duplex** — bidirectional client↔server communication (read and write) |

**Explanation:** Connection must be **two-way**, not one-way readable or writable only.

**Live result:** **91** correct; answer **duplex** (option label on slide not spoken).

---

### Q5. What is the main advantage of `stream.pipeline()` over `readable.pipe()`?

| | |
|---|---|
| **Correct concept ✓** | **`pipeline` automatically forwards errors, stops the chain, and destroys streams on failure; `pipe` does not propagate errors cleanly and may leave partial/junk files** |

**Explanation (professor after quiz):**

- **`stream.pipeline`:** errors propagate; streams **destroyed** on failure; cleanup unwinds properly.  
- **`.pipe()`:** errors may fail at a stage without proper propagation/cleanup (demo: input failed but output still attempted).

**Live result:** “Last question of this quiz”; majority correct (specific letter not repeated on audio for Q5).

---

## Quiz 2 — After Module 2 (TypeScript)

**Facilitator:** TA (Shoaibak); explanations before break.

### Q1. Does setting `"strict": true` in `tsconfig.json` enable strict type checking?

| | |
|---|---|
| **B ✓** | **Yes — strict mode enables strict type checking and catches `any`, null, and `never`-related hazards at compile time** |

**Explanation:** Lecture `strict-demo.ts` with `tsc --strict` shows compile-time failures for unsafe code.

**Live result:** **Option B** on question 1.

---

### Q2. For `function first`, what problem does using a **generic** instead of **`any`** solve?

| | |
|---|---|
| **B ✓** | **Generics preserve the relationship between input type and return type; `any` can return anything regardless of input** |

**Explanation:** Passing `number[]` should yield `number | undefined`, not `any`.

**Live result:** **Option B** on question 2.

---

### Q3. In `function longest<T extends { length: number }>(...)`, what does `extends { length: number }` do?

| | |
|---|---|
| **C ✓** | **Restricts `T` to types that have a `length` property of type `number` (e.g. strings, arrays); rejects types without it (e.g. plain numbers)** |

**Explanation:** Comparison uses `.length`; constraint **personalizes** the generic.

**Live result:** **Option C** on question 3.

---

### Q4. What is the purpose of assigning the **`default`** branch of a switch over a discriminated union to a variable of type **`never`**?

| | |
|---|---|
| **C ✓** | **To detect at compile time when a new union variant was added but not handled in the switch** |

**Explanation:** If someone adds a new `kind`/`status` variant in one file but forgets to update `area()` / handler, **`never`** assignment fails compilation.

**Live result:** **Option C** on question 4.

---

### Q5. Why must each variant in a discriminated union share a common literal property (e.g. `status`)?

| | |
|---|---|
| **B ✓** | **So TypeScript (and your code) can discriminate/filter variants—e.g. success vs failure—and run the correct branch with the correct fields** |

**Explanation:** Network fetch example: if `status === 'success'` do one thing, if `'error'` another—without a shared discriminator you cannot safely narrow.

**Live result:** **Option B** on the last question (TA closed quiz after ~30s wait).

---

## Summary

| Quiz | When | Questions | Topics |
|------|------|-----------|--------|
| **1** | After middleware / Node module | **5** | Event-loop phases, `setImmediate` vs `setTimeout` in I/O, `process.nextTick`, duplex streams, `pipeline` vs `pipe` |
| **2** | After TypeScript module | **5** | `strict`, generics vs `any`, `extends` constraints, `never` exhaustiveness, discriminant literal |

**Total in-lecture Mentimeter questions:** **10**

**Not included:** End-of-session learner feedback poll and hands-on setup (not graded content quizzes).
