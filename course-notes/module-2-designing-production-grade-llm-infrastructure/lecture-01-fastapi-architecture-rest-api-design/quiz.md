# Lecture 01: In-Lecture Quizzes

Live polls were run by TA **Subhajit Shah** between lecture blocks and before demos. The transcript records **correct answers and explanations** for several items; **slide stems/options for early questions are not fully spoken**. Where stems are missing, questions below are **reconstructed from the immediately preceding lecture content** (same approach as Module 1 notes) and labelled accordingly.

---

## In-lecture Quiz 1 - After Part 1 (Foundations & Pydantic)

**When:** End of Block 1, before Campus Bank demo Part 1.  
**Facilitator:** Subhajit; Professor Patta reads results.

### Q1. (Stem not on audio - reconstructed)

**Likely topic:** Primary source of FastAPI’s performance vs “Python got faster alone.”

| | |
|---|---|
| **Correct concept ✓** | **ASGI/async architecture** (and ASGI servers such as Uvicorn), not Python interpreter speed alone |

**Live result:** “All of you got it right.”

**Explanation (lecture):** Newer Python helps marginally; the big gain is **async-capable ASGI**, not the language alone.

---

### Q2. (Stem not on audio - reconstructed)

**Likely topic:** Whether FastAPI implements routing completely separately from Starlette.

| | |
|---|---|
| **Correct ✓** | **False** - FastAPI uses **Starlette routing** “all the way down” |

**Live result:** “Democracy wins” - majority correct.

**Explanation:** Starlette does core HTTP routing/middleware; FastAPI layers validation, OpenAPI, and DI on top.

---

### Q3. (Stem not on audio - reconstructed)

**Likely topic:** Whether `@dataclass` type annotations enforce field types at runtime.

| | |
|---|---|
| **Correct ✓** | **No** - dataclass hints are **not enforced**; wrong types can construct without error |

**Live result:** Majority correct (“democracy wins”).

**Explanation:** Motivates **Pydantic `BaseModel`**, which enforces validation.

---

### Q4. `@field_validator` vs `@model_validator`

**Stem (from instructor readout):** What is the distinction between field-level and model-level Pydantic validators?

| | |
|---|---|
| **Correct ✓** | **`@field_validator` checks a single field; `@model_validator` checks rules across multiple fields** |

**Live result:** Majority correct after zoom/readout.

**Explanation:** Single-field SKU rules → field validator; cross-field date ordering → model validator.

---

### Q5. Declarative validation in Pydantic

**Stem (partial on audio):** Which feature supports **declarative** validation - **`Field(...)` constraints** or **`@field_validator`**?

| Option (inferred) | |
|-------------------|---|
| `@field_validator` | Imperative - custom function logic |
| **`Field` ✓** | **Declarative - constraints in the model body** |

**Instructor wording:** “The feature that allows for declarative validation is just plain **fields** and **field validator** is just a decorator.” **Answer announced: `Field` / fields (declarative), not field_validator.**

**Live result:** Plurality/majority for **Field**.

---

### Q6. ASGI vs WSGI - unique ASGI capability

**Stem (on audio):** When comparing ASGI to WSGI, which feature is **uniquely** supported by ASGI?

**Options spoken:**

1. Synchronous request handling  
2. Single request-response cycle  
3. **WebSockets and long-lived connections**  
4. Basic routing of HTTP traffic  

| | |
|---|---|
| **Correct ✓** | **WebSockets and long-lived connections** |

**Live result:** Strong majority correct.

**Explanation:** WSGI is one-request-at-a-time sync worker model; ASGI adds **async**, **WebSockets**, and **long-lived** streams (e.g. LLM chat streaming). Some students picked “synchronous” - instructor noted that is **not** the ASGI differentiator.

---

## In-lecture Quiz 2 - After Part 2 (Dependency injection)

**When:** After DI lecture, before DB/CRUD demos.  
**Facilitator:** Subhajit; options read aloud when slides were hard to read.

### Q1. What is a “dependency” in FastAPI DI?

**Options (partial):**

- **A:** A third-party library installed via pip/npm  
- **B-D:** *(Not fully spoken - likely descriptions such as “data the framework injects before your route runs”)*  

| | |
|---|---|
| **Correct ✓** | **Not a pip/npm package** - dependency means **information/services your endpoint needs**, usually provided by a **callable** that FastAPI runs via `Depends` |

**Live result:** “This is the correct option” after sufficient responses (majority aligned with lecture).

**Explanation:** “Dependency is **not** something you install… it is information you would otherwise fetch inside the function” (DB session, auth, validated inputs).

---

### Q2. Why does `get_db` use `yield`?

**Stem (inferred from lecture example + instructor comment):** In a dependency that opens a database session, what is the role of **`yield`**?

**Options (partial):**

- **A:** *(Mentioned on slide - some students selected this; treated as wrong in debrief)*  
- **Correct concept ✓** | **`yield` provides the session to the route, then runs **cleanup code after the request** (e.g. close session)** |

**Live result:** “Democracy wins”; instructor: “I specifically did not talk much about **yield** but somehow you got it correct.”

**Explanation:** `get_db` **yields** the session; code after `yield` runs **after** the response - essential for closing DB connections.

---

## In-lecture Quiz 3 - After Part 3 (Routers, versioning, RFC 9457, OpenAPI)

**When:** End of lecture, before demo Parts 6-8.  
**Facilitator:** Subhajit / Professor Patta.

### Q1. (Stem not fully on audio)

**Likely topic:** **`APIRouter` cannot run standalone** - must be mounted with `app.include_router(...)`.

| | |
|---|---|
| **Correct concept ✓** | Router is a **container** for routes; it becomes active only when **included** in the main FastAPI app |

**Live result:** “Majority of you are correct.”

**Explanation:** “Can an API router run on its own? **Well no**… only becomes live once you plug it into the main application using **include_router**.”

---

### Q2. Changing a live API without a versioning strategy

**Stem (paraphrased on audio):** You modify a **live API in place** without versioning - what is the main problem?

| | |
|---|---|
| **Correct ✓** | **Existing clients that depend on the endpoint break immediately** |

**Live result:** “Democracy” / strong majority correct.

**Explanation:** Versioning lets **old clients keep working** while new clients opt into `/v2` (or header/query strategies).

---

### Q3. (Stem not fully on audio - reconstructed)

**Likely topic:** FastAPI **default** error JSON vs **RFC 9457**.

| | |
|---|---|
| **Correct concept ✓** | Default is typically **`{"detail": "..."}`** only - **does not** include all five RFC 9457 fields; use **custom exception handlers** for compliance |

**Live result:** “Majority… correct” (exact option letter not on audio).

**Explanation:** Standard uses **`type`, `title`, `status`, `detail`, `instance`** and media type **`application/problem+json`**.

---

### Q4. (Stem not fully on audio - reconstructed)

**Likely topic:** RFC 9457 field set or Problem Details media type.

| | |
|---|---|
| **Correct concept ✓** | Five fields: **`type`, `title`, `status`, `detail`, `instance`**; content type **`application/problem+json`** |

**Live result:** “Wow… still majority… correct option.”

**Explanation:** Stops every endpoint from inventing its own error JSON shape (`error` vs `message` vs `detail` keys).

---

## Summary

| Quiz | When | Questions documented | Main topics |
|------|------|----------------------|-------------|
| **1** | After Pydantic / before demo | **6** | Performance/ASGI, Starlette routing, dataclasses, validators, declarative `Field`, ASGI vs WSGI |
| **2** | After DI lecture | **2** | Meaning of dependency, `yield` for DB cleanup |
| **3** | After routers/RFC/OpenAPI | **4** | APIRouter mounting, versioning breakage, RFC 9457 / default errors |

**Total in-lecture quiz questions:** **12** (6 + 2 + 4)

**Transcript gaps:** Quiz 1 Q1-Q3 and Quiz 3 Q1/Q3/Q4 **option text** were not fully spoken; stems marked reconstructed. Quiz 2 Q1 **non-winning options** incomplete on audio.

**Not included:** 5-minute break setup, zip download instructions, end-of-session “thanks / next lecture LLM” - not graded content quizzes.
