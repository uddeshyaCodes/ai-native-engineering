# Lecture 01: Important Exam Q&A

Practice questions aligned with lecture emphasis and in-class quizzes. Answers are concise for MCQ revision.

---

## FastAPI advantages & when to use

### Q1. Where does FastAPI’s benchmark-level performance primarily come from?

**A.** The **ASGI/async architecture** (and servers like Uvicorn), not mainly from Python itself becoming dramatically faster.

### Q2. Name four headline advantages of FastAPI from the lecture.

**A.** (1) Performance via async/ASGI, (2) faster development + quality via type hints and Pydantic, (3) auto interactive docs (Swagger UI), (4) **OpenAPI**-compliant schema generation.

### Q3. When might you **not** migrate to FastAPI?

**A.** When a **simple synchronous app already works** and you don’t need async, validation, or heavy concurrent I/O - “if it works, don’t touch.”

### Q4. Why is FastAPI often chosen for AI/RAG/LLM backends?

**A.** Many **concurrent I/O** calls to external services; async model fits juggling lots of parallel requests and streaming responses.

---

## WSGI vs ASGI

### Q5. Describe the WSGI request-handling model in one phrase.

**A.** **Single-lane:** one request is fully processed and responded to before that worker handles the next (no native multitasking on one worker for async/long-lived work).

### Q6. Is ASGI only a replacement for WSGI?

**A.** **No** - ASGI is a **superset**: it does WSGI-style work **plus** native async, **WebSockets**, and **long-lived connections**.

### Q7. Which ASGI capability supports LLM chat streaming?

**A.** **Long-lived connections** and streaming responses (words/tokens sent incrementally).

### Q8. Which server interface does FastAPI use, and name one ASGI server from the demo.

**A.** **ASGI**; demo uses **Uvicorn** (`uvicorn main:app --reload`).

---

## Starlette & HTTP

### Q9. Does FastAPI implement routing completely separately from Starlette?

**A.** **No** - FastAPI uses **Starlette routing** underneath.

### Q10. List four responsibilities Starlette handles (any four from lecture).

**A.** Middleware stack (e.g. CORS, logging, compression), **routing**, **WebSockets**, **background tasks**, **static file** serving.

### Q11. Match HTTP methods: list users, create user, update profile, delete resource.

**A.** GET (read/list), POST (create), PUT (update), DELETE (delete).

---

## Type hints, dataclasses, Pydantic

### Q12. Does Python natively enforce function type hints at runtime?

**A.** **No** - hints are mainly for tooling/documentation unless you use external checkers or Pydantic.

### Q13. Do `@dataclass` field type annotations enforce types at instantiation?

**A.** **No** - wrong types can slip through; hints are not enforced by Python.

### Q14. What happens if you construct a Pydantic model with positional arguments?

**A.** **Validation error** - Pydantic models require **keyword** arguments.

### Q15. Name the three roles Pydantic plays for web APIs.

**A.** **Validation**, **coercion/parsing**, **serialization** (e.g. `model_dump()` for JSON responses).

### Q16. Declarative vs imperative validation - when use each?

**A.** **Declarative** (`Field`, `Literal`, built-in types) for simple one-line rules; **imperative** (`field_validator`, `model_validator`) for complex or multi-field logic.

### Q17. What is the difference between `@field_validator` and `@model_validator`?

**A.** **Field validator** targets **one field**; **model validator** checks rules across **multiple fields** at once.

### Q18. What does `Field(gt=0)` mean for a price field?

**A.** Price must be **strictly greater than 0** (not ≥ 0).

### Q19. Is Pydantic exclusive to FastAPI?

**A.** **No** - usable in any Python application.

---

## Dependency injection

### Q20. In this lecture, is a FastAPI “dependency” a pip-installable package?

**A.** **No** - it’s **data or services** (DB session, user, auth) that the framework **injects** before your route runs.

### Q21. In `read_profile(user = Depends(get_current_user))`, who calls `get_current_user`?

**A.** **FastAPI** calls it automatically; the route body does **not** call it directly.

### Q22. Why use `yield` in a `get_db` dependency?

**A.** Provide the DB session during the request, then **run cleanup** (e.g. close session) **after** the request finishes.

### Q23. How do tests swap a real DB/auth dependency without editing routes?

**A.** **`app.dependency_overrides[original_dep] = fake_dep`**.

### Q24. Name two problems with hiding dependencies inside endpoint functions.

**A.** **Harder to test** (can’t mock easily) and **weaker OpenAPI/docs** (hidden requirements).

---

## Routers, CRUD, versioning

### Q25. Can an `APIRouter` run as a standalone server?

**A.** **No** - it must be **included** in the main app via `include_router`.

### Q26. Why use APIRouter instead of one giant `main.py`?

**A.** **Modularity**, parallel team work, **reusability**, scalable `main.py`, and **separation of concerns** for debugging.

### Q27. What happens if you change a live API in place without versioning?

**A.** **Existing clients break** immediately.

### Q28. Name the three API versioning strategies from the lecture.

**A.** **URI/path**, **header/media type**, **query parameter**.

### Q29. Which versioning strategy did the demo use?

**A.** **URI versioning** (`/v1/...`, `/v2/...` with separate router modules).

### Q30. Why separate `crud.py` from route handlers?

**A.** **Separation of concerns** - database/business persistence logic is not mixed with HTTP layer; routes stay thin and testable.

---

## RFC 9457 & OpenAPI

### Q31. List the five RFC 9457 problem detail fields taught in lecture.

**A.** `type`, `title`, `status`, `detail`, `instance`.

### Q32. What media type signals RFC 9457 problem JSON?

**A.** **`application/problem+json`**.

### Q33. Does FastAPI’s default error JSON fully comply with RFC 9457?

**A.** **No** - default is often only **`detail`**; full compliance needs **custom exception handlers**.

### Q34. Where do you interactively test endpoints without Postman in FastAPI?

**A.** **`/docs`** (Swagger UI generated from OpenAPI).

### Q35. Must custom RFC 9457 error responses be added to OpenAPI manually?

**A.** **Yes** - auto docs won’t fully describe custom error shapes unless you **document them explicitly**.

---

## Demo specifics (Campus Bank)

### Q36. What storage was used in Part 1 vs Part 3?

**A.** Part 1: **in-memory Python list** (data lost on restart); Part 3+: **SQLite** file via SQLAlchemy.

### Q37. What was the minimum age business rule in schemas?

**A.** Users must be **at least 13** (`field_validator` on age).

### Q38. How did V2 user responses differ from V1 in Part 7?

**A.** V2 included **`id`** and **`account_count`** in addition to username, email, age.
