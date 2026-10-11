# Lecture 01: FastAPI Architecture and REST API Design

**Course:** AI-Enabled Software Engineering · **Module 2:** Designing Production-Grade LLM Infrastructure  
**Instructor:** Yubesh Patta (Assistant Professor, CSE, IIT Kharagpur)  
**TA / demos:** Subhajit Shah  
**Session structure:** Three blocks (~25-35 min each) + live Campus Bank API demos (8 incremental parts)

---

## Learning outcomes (exam-ready)

By the end of this session you should be able to:

- Explain **why** FastAPI is fast (architecture, not “faster Python alone”) and when **not** to adopt it.
- Contrast **WSGI vs ASGI** and name workloads ASGI enables.
- Describe FastAPI’s stack: **Starlette**, **Pydantic**, **OpenAPI**, **dependency injection**.
- Map **HTTP methods** to REST-style operations and read basic FastAPI routes.
- Use **Pydantic** for validation, coercion, serialization; choose **declarative vs imperative** rules.
- Apply **dependency injection** with `Depends`, chaining, `yield` cleanup, and `app.dependency_overrides` for tests.
- Organise apps with **APIRouter**, **URI versioning**, **CRUD separation**, and **RFC 9457** error shapes.
- Use **OpenAPI / Swagger UI** (`/docs`) and enrich docs (metadata, response examples).

---

## Session map

| Block | Lecture focus | Demo parts (Campus Bank) |
|-------|---------------|---------------------------|
| **1 - Foundations** | Why FastAPI, ASGI/WSGI, Starlette, HTTP methods, type hints, Pydantic | Part 1 toy app; Part 2 Pydantic schemas |
| **2 - Dependency injection** | DI motivation, `Depends`, chaining, testing overrides | Part 3 DB + DI; Part 4 CRUD layer; Part 5 update/delete |
| **3 - Routers & contracts** | APIRouter, versioning, RFC 9457, OpenAPI | Part 6 routers (users/accounts); Part 7 versioning; Part 8 enhanced docs |

**Run command (demo):** `uvicorn main:app --reload` (file `main.py`, app object `app`).

---

## Part 1: Why FastAPI exists

### Headline advantages

| Advantage | Mechanism |
|-----------|-----------|
| **Performance** | Native **async/await** on **ASGI**; often compared with Node.js/Go in benchmarks |
| **Faster development & quality** | **Python type hints** → editor autocomplete; **Pydantic** validates models |
| **Auto documentation** | **Swagger UI** at `/docs`; test endpoints in browser (often no Postman needed) |
| **Spec-compliant API description** | Default **OpenAPI** schema generation |

**Exam trap:** Speed comes mainly from **ASGI architecture** (and async I/O), not from Python interpreters suddenly becoming dramatically faster (though newer Python versions did improve).

### When **not** to use FastAPI

- Simple, **working synchronous** apps with no need for async or heavy validation → “if it works, don’t touch.”
- Use FastAPI when **async**, **validation**, and **concurrent I/O** (e.g. RAG, LLM endpoints, many external API calls) matter.

### FastAPI vs Flask vs Django (lecture comparison)

| | Flask | Django (DRF) | FastAPI |
|---|--------|--------------|---------|
| Core style | Sync-first | ORM-tight, strong for CRUD | **Async by default** |
| Validation | Manual / extensions | Framework patterns | **Pydantic built-in** |
| API docs | Manual (extensions) | Varies | **Auto OpenAPI + Swagger** |
| Async | Limited | Less emphasis | **First-class** |

### Four components of FastAPI

1. **Starlette** - HTTP core (routing stack, middleware, WebSockets, background tasks, static files)  
2. **Pydantic** - data validation / parsing / serialization  
3. **OpenAPI** - machine-readable API contract  
4. **Dependency injection** - reusable request-scoped logic  

---

## ASGI vs WSGI

| | **WSGI** (Web Server Gateway Interface, ~2003) | **ASGI** (Async Server Gateway Interface) |
|---|--------------------------------------------------|-------------------------------------------|
| Model | **Single-lane:** one request fully handled before worker takes next | **Superset of WSGI** + async, WebSockets, long-lived connections |
| Typical servers | Traditional Python web stacks | e.g. **Uvicorn** |
| Framework examples | Flask, Django (classic) | **FastAPI** (built on ASGI) |
| Good for | Classic request/response web | Streaming, chat, **LLM token streaming**, real-time |

**Uniquely ASGI (vs classic WSGI):** **WebSockets** and **long-lived connections** (not “sync-only one-shot” limitation).

```text
  Client ──► ASGI server (uvicorn) ──► Starlette ──► FastAPI routes
                    │
                    └── async I/O, websockets, streaming
```

---

## Starlette (routing layer)

- FastAPI is **not** a from-scratch HTTP stack; it **inherits from Starlette**.
- Starlette handles: **middleware** (CORS, logging, compression), **routing**, **WebSockets**, **background tasks** (after response sent), **static files** (JS, CSS, HTML, images).
- **FastAPI does not replace Starlette routing** - “Starlette routing all the way down.”

### HTTP methods (REST vocabulary)

| Method | Typical use (lecture examples) |
|--------|--------------------------------|
| **GET** | Read resource (load page, list users) |
| **POST** | Create / submit (login, create user) |
| **PUT** | Update/replace (edit profile) |
| **DELETE** | Remove resource |

Minimal route pattern:

```python
@app.get("/hi")
def hi():
    return "Hello, I am a FastAPI server"
```

Browser: `http://<host>/hi` → function runs → JSON/text response.

---

## Python type hints vs Pydantic

### Dynamic typing problem for APIs

- Python accepts mixed types at runtime; API builders discover bugs **when users call**, not when code is written.
- **Type hints** help editors but **Python does not enforce** them natively.

### Dataclasses vs Pydantic `BaseModel`

| | `@dataclass` | Pydantic `BaseModel` |
|---|--------------|----------------------|
| Groups fields | Yes | Yes |
| Enforces types at instantiation | **No** (hints are documentation) | **Yes** |
| Positional constructor args | Allowed | **Not accepted** - use **keyword** args |
| Network JSON validation | No | **Yes** (required fields, types, rules) |

### Three jobs Pydantic does for APIs

1. **Validation** - required fields, types, business rules  
2. **Coercion/parsing** - e.g. `"45000.0"` string → `45000.0` float  
3. **Serialization** - Python objects → JSON responses (`model_dump()`)

**Note:** Pydantic is **not FastAPI-specific**; usable in any Python app.

### Declarative vs imperative validation

| Style | Tools | Use when |
|-------|-------|----------|
| **Declarative** | Type hints + `Field(...)` constraints, `Literal`, `EmailStr`, etc. | Rule fits in one phrase: “price > 0”, “non-empty string”, enum status |
| **Imperative** | `@field_validator`, `@model_validator` | Custom logic, cross-field rules (e.g. end date after start date) |

**Rule of thumb:** simple constraint → **declarative `Field`**; `if` chains / multi-field logic → **validators**.

Examples from lecture:

- `Field(min_length=1)`, `Field(gt=0)` - price strictly **greater than** 0  
- `Literal["pending", "set"]` - fixed enum for order status  
- `@field_validator` - e.g. SKU must start with `P`  
- `@model_validator` - rules spanning multiple fields  
- **`field_validator`** → one field; **`model_validator`** → multiple fields  

---

## Part 2: Dependency injection (DI)

### What “dependency” means here

**Not** a pip/npm package. A **dependency** is anything your endpoint needs **before** it can run:

- Parsed/validated request data  
- Auth / authorization  
- DB session, related records  
- Logging, metrics, tracing  

### Problems when dependencies are **hidden inside** functions

| Problem | Effect |
|---------|--------|
| Harder to test | Can’t swap real DB/users for fakes |
| Invisible breakers | Distant changes break endpoints quietly |
| Repeated logic | Same auth/DB boilerplate everywhere |
| Weaker docs | OpenAPI can’t surface hidden requirements |

### Fix (one sentence)

**Pass data in from outside** - usually via small producer functions - instead of fetching inside the endpoint.

### FastAPI pattern

```python
def read_profile(user = Depends(get_current_user)):
    ...
```

- Endpoint **does not call** `get_current_user()` directly.  
- FastAPI sees `Depends(...)`, runs dependency **before** route body, injects result.  
- Dependencies can **chain** (`get_current_user` depends on `get_db`).  
- **`yield` in `get_db`:** provide session during request; **cleanup after** request completes (close session).

### Testing: `app.dependency_overrides`

Replace `get_current_user` with `fake_get_current_user` for tests **without changing endpoint code**.

---

## Part 3: Routers, versioning, errors, OpenAPI

### APIRouter

- **Groups related endpoints** (users, accounts, auth) - “mini FastAPI” (`APIRouter`).
- **Cannot run standalone** - routes go live via `app.include_router(...)`.
- Benefits: **modularity**, **team collaboration** (fewer merge conflicts), **reusability** (same health router in multiple services), **scalability** (tiny `main.py`), **separation of concerns** (debug users in `users.py` only).

### API versioning strategies

| Strategy | How client selects version | Pros / cons |
|----------|----------------------------|-------------|
| **URI/path** | `/v1/users`, `/v2/users` | **Simplest**, visible in URL |
| **Header / media type** | Same URL; version in header | Clean URL; **less visible** |
| **Query parameter** | `?version=2` | Easy to forget; often **default fallback** |

**Why version:** Changing a **live API in place** **breaks existing clients**. Versioning lets old clients keep working while new ones opt in.

**FastAPI URI versioning:** separate routers/files per version + **`prefix="/v1"`** / `include_router`.

**Demo contrast:** V1 user response = username, email, age; V2 adds **id** and **account_count**.

### RFC 9457 - Problem Details for HTTP APIs

**Problem:** Each developer returns errors in different JSON shapes (`error`, `message`, `detail`, …) → clients need custom parsers per endpoint.

**Fix:** One **standard error envelope** for the whole API.

**Five fields (lecture):**

| Field | Role |
|-------|------|
| `type` | URI identifying problem category |
| `title` | Short human-readable summary |
| `status` | HTTP status code |
| `detail` | More explanation |
| `instance` | URI identifying this specific request |

**Media type:** `application/problem+json`

**FastAPI default:** Often `{ "detail": "..." }` only - **not RFC 9457-compliant**. Implement **custom exception handlers** to emit all five fields.

### OpenAPI documentation

- Generated from routes, types, dependencies (where exposed).  
- **Swagger UI** at `/docs` - interactive try-it-out.  
- Versioned routers appear as **separate path groups**.  
- Custom RFC error shapes must be **documented explicitly** (defaults won’t describe them).  
- Enhance with app `title`, `description`, `version`; per-route `summary`, `status_code`, `responses`; schema **`model_config` / examples** for sample responses.

**Closing takeaway (instructor):** Pydantic → validated data; DI → reusable request logic; Routers → structure; RFC 9457 → stable error contract; OpenAPI → self-writing documentation.

---

## Campus Bank demo - technical takeaways

| Part | Key idea |
|------|----------|
| 1 | In-memory `list`, `@app.post("/users")`, `@app.get("/users")`, raw dict bodies |
| 2 | `schemas.py`: `User`, `Account`, `UserCreate`; `Field`, patterns, `@field_validator` (age ≥ 13); `response_model=list[User]`; `model_dump()` |
| 3 | SQLAlchemy + SQLite; `get_db` **yield** session; ORM models mirror schemas |
| 4 | **`crud.py`** - DB logic out of routes |
| 5 | Full CRUD + `HTTPException` for not found |
| 6 | **`APIRouter`** - separate `users` and `accounts` modules |
| 7 | **`routers/v1` vs `v2`** - different response schemas |
| 8 | Rich OpenAPI metadata and response examples |

**Business rules (demo):** max **5 accounts** per user; account types savings/current; persistent SQLite file while app runs.

---

## Quick reference cheat sheet

| Term | One-line meaning |
|------|------------------|
| ASGI | Async gateway; websockets + long-lived connections |
| WSGI | Sync one-request-at-a-time worker model |
| Starlette | FastAPI’s HTTP/routing/middleware foundation |
| Pydantic | Validates/coerces/serializes request & response models |
| `Depends` | Declares injectable dependency; framework calls it |
| `APIRouter` | Grouped routes; mounted with `include_router` |
| RFC 9457 | Standard JSON error “problem details” format |
| `/docs` | Swagger UI for OpenAPI |
