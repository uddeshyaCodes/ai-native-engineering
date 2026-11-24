# Lecture 01: In-Lecture Quizzes

Live polls were run by TA **Subhajit Shah** between lecture blocks and before demos. All three quizzes use the actual questions and options from the Mentimeter decks (Parts 1-3). Correct answers were deduced from the lecture content and transcript; live-result notes come from the transcript.

---

## In-lecture Quiz 1 - After Part 1 (Foundations & Pydantic)

**When:** End of Block 1, before Campus Bank demo Part 1.  
**Facilitator:** Subhajit; Professor Patta reads results.  
**Source:** Questions and options taken verbatim from the Mentimeter deck "Part 1" (5 questions).

### Q1. Underlying toolkit for background tasks and static files

**Stem:** Which underlying toolkit is responsible for handling FastAPI's background tasks and static file serving?

| Option | |
|---|---|
| A | uvicorn |
| **B ✓** | **Starlette** |
| C | Hypercorn |
| D | OpenAPI |

**Explanation:** FastAPI is built on **Starlette**, which provides routing, middleware, background tasks and static files; FastAPI layers validation, OpenAPI and DI on top. Uvicorn/Hypercorn are ASGI *servers*; OpenAPI is a spec, not a toolkit.

---

### Q2. Base class for Pydantic schemas

**Stem:** To define a schema in Pydantic, a class must inherit from which specific base class?

| Option | |
|---|---|
| **A ✓** | **BaseModel** |
| B | SchemaModel |
| C | dataclass |
| D | StarletteModel |

**Explanation:** Pydantic models subclass **`BaseModel`**, which enforces validation at runtime. A plain `@dataclass` does **not** enforce its type hints.

---

### Q3. `@field_validator` vs `@model_validator`

**Stem:** What is the primary difference between @field.validator and @model.validator in Pydantic?

| Option | |
|---|---|
| A | @field.validator is for standard types, while @model.validator is for custom objects |
| B | @field.validator is declarative, while @model.validator is imperative |
| C | @field.validator is for inputs, and @model.validator is for outputs |
| **D ✓** | **@field.validator checks a single field, while @model.validator checks rules across multiple fields** |

**Live result:** Majority correct after zoom/readout.

**Explanation:** Single-field SKU rules → field validator; cross-field date ordering → model validator.

---

### Q4. Declarative validation in Pydantic

**Stem:** Which Pydantic feature allows for 'declarative' validation by adding specific constraints like min length or gt (greater than)?

| Option | |
|---|---|
| A | @field.validator |
| B | Literal |
| **C ✓** | **Field()** |
| D | Type hints |

**Live result:** Plurality/majority for **Field**.

**Explanation:** Instructor: "The feature that allows for declarative validation is just plain **fields** and **field validator** is just a decorator." `Field(...)` puts constraints in the model body; `@field_validator` is imperative custom logic.

---

### Q5. ASGI vs WSGI - unique ASGI capability

**Stem:** When comparing ASGI to WSGI, which feature is uniquely supported by the ASGI standard?

| Option | |
|---|---|
| A | Synchronous request handling |
| B | Single request-response cycles |
| **C ✓** | **WebSockets and long-lived connections** |
| D | Basic routing of HTTP traffic |

**Live result:** Strong majority correct.

**Explanation:** WSGI is a one-request-at-a-time sync worker model; ASGI adds **async**, **WebSockets**, and **long-lived** streams (e.g. LLM chat streaming). Some students picked "synchronous" - instructor noted that is **not** the ASGI differentiator.

---

## In-lecture Quiz 2 - After Part 2 (Dependency injection)

**When:** After DI lecture, before DB/CRUD demos.  
**Facilitator:** Subhajit; options read aloud when slides were hard to read.  
**Source:** Questions and options taken verbatim from the Mentimeter deck "Part 2" (3 questions).

### Q1. What is a "dependency"?

**Stem:** In the context of FastAPI architecture, which of the following best describes the fundamental concept of a 'dependency'?

| Option | |
|---|---|
| A | A third-party library installed via a package manager that the application imports. |
| B | A specific Python decorator used to register new routes within the main application instance. |
| **C ✓** | **Any logic or data, such as a database session or a validated token, that a function requires from an external source to complete its job.** |
| D | An external service, such as a database or an authentication provider, that is hardcoded within the logic. |

**Live result:** "This is the correct option" after sufficient responses (majority aligned with lecture).

**Explanation:** "Dependency is **not** something you install… it is information you would otherwise fetch inside the function" (DB session, auth, validated inputs), usually supplied by a callable that FastAPI runs via `Depends`.

---

### Q2. Role of the function passed to `Depends()`

**Stem:** When implementing Dependency Injection in FastAPI, what is the primary role of the function passed to the Depends() parameter?

| Option | |
|---|---|
| A | To override the global configuration of the FastAPI app instance for a specific route. |
| **B ✓** | **To serve as a reusable logic block that produces a specific value, such as a user object or database connection, for the endpoint.** |
| C | To validate that the incoming HTTP request uses a secure protocol like HTTPS. |
| D | To act as a mini-application that handles its own routing and middleware logic. |

**Explanation:** The `Depends()` callable is a reusable provider: FastAPI runs it and injects its result into the route. Option D describes `APIRouter`, not a dependency.

---

### Q3. `yield` vs `return` in a dependency

**Stem:** In FastAPI, how does the yield keyword modify the behavior of a dependency function compared to using return?

| Option | |
|---|---|
| A | It forces the dependency to return a generator object instead of the actual data to the endpoint. |
| B | It converts the dependency into a background task that runs after the response is sent. |
| C | It increases the performance of the dependency by caching the result for subsequent requests. |
| **D ✓** | **It allows the dependency to provide a value and then execute additional cleanup logic after the response has been delivered.** |

**Live result:** "Democracy wins"; instructor: "I specifically did not talk much about **yield** but somehow you got it correct."

**Explanation:** `get_db` **yields** the session; code after `yield` runs **after** the response - essential for closing DB connections. FastAPI hands the endpoint the yielded value, not a generator.

---

## In-lecture Quiz 3 - After Part 3 (Routers, versioning, RFC 9457, OpenAPI)

**When:** End of lecture, before demo Parts 6-8.  
**Facilitator:** Subhajit / Professor Patta.  
**Source:** Questions and options taken verbatim from the Mentimeter deck "Part 3" (5 questions).

### Q1. Routers and team collaboration

**Stem:** How does the use of routers improve team collaboration in large FastAPI projects?

| Option | |
|---|---|
| A | It forces every developer to use the same IDE settings for consistency. |
| B | It allows multiple developers to work in the same main.py file simultaneously without merge conflicts. |
| **C ✓** | **Different developers can own and maintain different router files corresponding to their assigned logical domains.** |
| D | It provides a built-in chat interface within the Swagger UI for developers. |

**Live result:** "Majority of you are correct."

**Explanation:** An `APIRouter` is a container for a domain's routes (users, orders, etc.), so each developer owns a separate file instead of everyone editing `main.py`. It only becomes live once plugged into the main app with `app.include_router(...)`.

---

### Q2. RFC 7807 in July 2023

**Stem:** According to the presentation, what happened to RFC 7807 in July 2023?

| Option | |
|---|---|
| A | It was deprecated and removed from use in web APIs. |
| **B ✓** | **It was obsoleted and replaced by RFC 9457, though the underlying format remained unchanged.** |
| C | It was merged into the OpenAPI 3.1 specification. |
| D | It was modified to require XML instead of JSON. |

**Explanation:** **RFC 9457** obsoletes RFC 7807 but keeps the same Problem Details format: `type`, `title`, `status`, `detail`, `instance`, served as `application/problem+json`. This stops every endpoint inventing its own error shape (`error` vs `message` vs `detail`).

---

### Q3. Purpose of `responses=...` in the endpoint decorator

**Stem:** In a FastAPI endpoint decorator, what is the purpose of using the responses=... parameter in conjunction with custom error standards?

| Option | |
|---|---|
| A | To bypass the need for an @app.exceptionhandler. |
| B | To automatically retry failed requests based on the status code. |
| **C ✓** | **To explicitly document the shape of error responses (like RFC 9457) in the OpenAPI schema for consumers.** |
| D | To define the internal Python logic used to calculate the response. |

**Explanation:** FastAPI's default error JSON is just `{"detail": "..."}`. Custom exception handlers produce RFC 9457 bodies at runtime; `responses=...` documents those shapes in OpenAPI. It does not replace the handlers.

---

### Q4. Hidden cost of changing a live API without versioning

**Stem:** Why is it considered a 'hidden cost' to modify a live API's response shape without implementing a versioning strategy?

| Option | |
|---|---|
| A | It increases the memory overhead of the Uvicorn server. |
| B | It violates the idempotent nature of GET requests. |
| **C ✓** | **It immediately breaks the contract for every existing client application built against that specific response shape.** |
| D | It causes the OpenAPI documentation to stop generating correctly. |

**Live result:** "Democracy" / strong majority correct.

**Explanation:** Versioning lets **old clients keep working** while new clients opt into `/v2` (or header/query strategies).

---

### Q5. APIRouter feature for grouping a version under a path

**Stem:** Which feature of the APIRouter class is most directly utilized to ensure all endpoints within a version are grouped under a specific path?

| Option | |
|---|---|
| A | The tags parameter. |
| **B ✓** | **The prefix parameter.** |
| C | The dependency overrides parameter. |
| D | The versionid parameter. |

**Explanation:** `APIRouter(prefix="/v1")` prepends the path to every route in that router. `tags` only groups endpoints in the docs UI, and `versionid` is not a real parameter.

*(Stem on the Menti slide contains a stray character in "directly"; normalised here.)*

---

## Summary

| Quiz | When | Questions documented | Main topics |
|------|------|----------------------|-------------|
| **1** | After Pydantic / before demo | **5** | Starlette toolkit, `BaseModel`, validators, declarative `Field`, ASGI vs WSGI |
| **2** | After DI lecture | **3** | Meaning of dependency, role of `Depends()`, `yield` for DB cleanup |
| **3** | After routers/RFC/OpenAPI | **5** | Router collaboration, RFC 7807 → 9457, `responses=`, versioning breakage, router `prefix` |

**Total in-lecture quiz questions:** **13** (5 + 3 + 5)

**Not included:** 5-minute break setup, zip download instructions, end-of-session “thanks / next lecture LLM” - not graded content quizzes.
