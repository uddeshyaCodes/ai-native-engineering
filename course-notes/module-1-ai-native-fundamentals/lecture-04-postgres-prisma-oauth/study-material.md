# Lecture 04: Postgres Data Layer, Prisma, OAuth, TanStack Query, Zustand & AI Schema Design

**Course:** AI-Native Software Engineering (Module 1)  
**Topic:** Real data (Postgres + Prisma), authentication (OAuth / Auth.js), client vs server state (TanStack Query + Zustand), and reviewing AI-generated schemas  
**Transcript:** [`transcripts/module-1/lecture-04-postgres-prisma-oauth.txt`](../../../transcripts/module-1/lecture-04-postgres-prisma-oauth.txt)

---

## Learning arc (four chapters)

1. **Prisma ORM** — schema, migrations, typed client, CRUD, Studio  
2. **Authentication** — OAuth 2.0, JWT vs DB sessions, NextAuth/Auth.js, optional credentials provider  
3. **TanStack Query + Zustand** — server state vs client state (PawMatch demo app)  
4. **AI-assisted schema design** — cardinality, indexes, types, migration review  

**Why this order:** You need **data** before **access control**; you need **auth** before **fetching protected data** in the UI; schema review closes the loop on Prisma.

**End-to-end stack (recap):** Browser → Next.js routes → **Prisma** → Postgres; **Auth.js** gates routes; **TanStack Query** loads server data; **Zustand** holds local UI preferences.

---

## Chapter 1: Prisma ORM

### Origin story

- **Graphcool (2016):** GraphQL backend-as-a-service; team realized developers valued **managed database workflows** more than GraphQL itself.  
- **Rebrand → Prisma:** Database tooling for **your own Postgres** (not replacing the DB).  
- **Prisma 2 (2020):** Standalone **type-safe ORM** mapping app models ↔ relational tables.

### GraphQL vs REST (motivation only)

- REST: many fixed endpoints to assemble related data.  
- GraphQL: one request describing the **shape** of data across tables; server returns exactly that.

### Why ORM / Prisma if you already know SQL?

- Handwritten SQL (especially string-concatenated queries) remains a top web weakness.  
- Lecture cites **~65%** of web app attacks involving **SQL injection** (and high breach cost); ORMs **reduce common mistakes**, not all risk.  
- **~18%** of apps using an ORM can still be vulnerable if raw queries are mixed in.  
- **Type safety:** user input treated as **data**, not executable SQL text (parameterized / bound values).

**SQL injection example (anti-pattern):**  
`WHERE email = ${email}` with input like `' OR 1=1 --` can return all rows.  
**Prisma:** `findUnique({ where: { email } })` — email handled as a bound value.

### Core concepts

| Term | Meaning |
|------|--------|
| **ORM** | Maps object/models in code to relational tables |
| **`schema.prisma`** | **Single source of truth** for models, relations, client, migrations |
| **Migration** | Versioned, **reviewable `.sql`** generated when schema changes |
| **Prisma Client** | Generated, **fully typed** query API (`create`, `findMany`, `update`, `delete`) |
| **Relation** | Foreign-key link between models — must be **declared** in schema |
| **Prisma Studio** | Visual browser for data (e.g. `npx prisma studio`, often `localhost:5555`) |

### Prisma setup workflow (8 steps)

1. Install & init (`prisma`, `@prisma/client`, `npx prisma init`)  
2. Set **`DATABASE_URL`** in `.env`  
3. Define models in **`schema.prisma`** (AI can draft; **you verify**)  
4. **`npx prisma migrate dev --name …`** — generates SQL, applies locally, regenerates client  
5. Use **typed client** in server actions/routes (not raw `db.query` in components)  
6. **Iterate:** edit schema → migrate dev → review new migration SQL  
7. **Sanity-check data** in **Prisma Studio** (human step; AI doesn’t replace this)  
8. **Deploy:** **`npx prisma migrate deploy`** in production (applies pending migrations only)

### Dev vs production migrations

| Command | When |
|---------|------|
| **`migrate dev`** | Local/dev: diff schema, create migration, apply, regenerate client |
| **`migrate deploy`** | Production: apply **pending** migrations only |
| **Never** | Run **`migrate dev`** in production |

Each migration = **plain SQL file** in version control (reversible history).

### `migrate dev` vs `db push`

| | **`migrate dev`** | **`db push`** |
|--|-------------------|---------------|
| **Version history** | Yes — team-friendly | No — quick prototype |
| **Use when** | Shared repo, PRs, production path | Lone-wolf local experiments |
| **Risk** | Lower if reviewed | Easy to forget state; lecture ties sloppy DB practice to security exposure |

### CRUD mapping

- Postgres: INSERT / SELECT / UPDATE / DELETE  
- Prisma: `.create`, `.findMany` / `.findUnique`, `.update`, `.delete`

### Prisma vs Drizzle vs raw SQL (lecture comparison)

| | Prisma | Drizzle | Raw SQL |
|--|--------|---------|---------|
| Type safety | Generated client | Schema-inferred | None |
| Migrations | Built-in, versioned SQL | Built-in | Manual |
| Learning curve | Low (lecture) | Steeper | No guardrails |
| When raw SQL | Rare — only if performance truly demands it | | |

### AI’s role in Prisma (human-in-the-loop)

| Step | AI OK? | Human must |
|------|--------|------------|
| Install / commands | Yes | Know what ran |
| Draft schema | Yes | Verify FKs, indexes, cardinality, types |
| Run migration | AI suggests command | **Review migration SQL** |
| Typed client code | Yes (read schema) | Test + Studio |
| Deploy | AI suggests command | **Trigger** deploy; never fully autonomous |

**Example schema review issue:** Comment model with `authorId` / `postId` — ensure **relations + indexes** on FK columns used in queries.

---

## Chapter 2: Authentication & OAuth

### Why auth matters (stats from lecture)

- **22%** of breaches start with stolen/compromised credentials  
- **88%** of basic web app attacks involve stolen credentials  
- Long mean time to detect credential breaches (**292 days** cited)  
- Scale of leaked passwords on criminal markets (2024 figure cited in lecture)

### OAuth history

- Pre-OAuth: third parties asked for **your password** (delegated API access).  
- **OAuth 1.0 (2007)** → **OAuth 2.0 (2012, RFC)** — limited **tokens**, not passwords.  
- **“Sign in with Google/Meta/GitHub”** — user authenticates **at the provider**; your app gets authorization, not the password.

### OAuth 2.0 roles (four roles)

1. **Resource owner** — user (has credentials)  
2. **Client** — your Next.js app (requests access on user’s behalf)  
3. **Authorization server** — issues tokens (e.g. Google)  
4. **Resource server** — holds protected resources/APIs  

**OAuth** = **authorization** (valid token → access). **OpenID Connect** + **Auth.js** cover **identity** (who the user is) and OAuth flows.

### OAuth flow (six steps, lecture)

1. User clicks **Sign in with Google**  
2. App **redirects** to provider consent  
3. User **approves**  
4. Provider redirects back with **authorization code**  
5. App **exchanges code for tokens** (server-to-server) — access token, ID token  
6. App **creates session** (JWT or DB)

**Key point:** Authorization code exchange is **server-to-server**; secrets stay off the client.

### JWT (JSON Web Token)

- Standard (RFC cited in lecture) for signed, compact claims.  
- **Three parts:** header, payload, signature (Base64url segments).  
- Self-contained session data (e.g. user id); signature verifiable **without DB lookup** per request.

### JWT session vs database session

| | **JWT (cookie)** | **Database session** |
|--|------------------|----------------------|
| Speed | No DB read each request | DB read per authenticated request |
| Revocation | Hard until expiry | **Instant** (delete session row) |
| Use when | High-throughput public APIs | Need immediate revoke / stricter session control |

Lecture: high-throughput “is logged in?” checks often use **JWT**; use **DB sessions** when you must **revoke** quickly.

### Auth.js / NextAuth setup (pattern)

1. Install **Auth.js v5** (`next-auth@beta` — confirm v5, not accidental v4)  
2. **Register OAuth app** in Google Cloud Console (manual): client ID/secret, **redirect URI** must **exactly** match app URL (common prod bug: localhost URI not added for live domain)  
3. Generate **`AUTH_SECRET`** (`npx auth secret`) — separate for prod  
4. Env vars: `AUTH_GOOGLE_ID`, `AUTH_GOOGLE_SECRET`, `AUTH_SECRET`, **`AUTH_URL` / NextAuth URL** (AI often omits)  
5. **`auth.ts`**: providers (Google), **`session: { strategy: "jwt" }`** or `"database"` — strategy changes architecture  
6. Route handler: `app/api/auth/[...nextauth]/route.ts`  
7. **JWT callbacks** — e.g. put DB `userId` on `session.user.id`  
8. **Protect routes** — `auth()` in server components; redirect or show `signIn("google")`  
9. **Prisma adapter** when using DB sessions / user records  

**Ecosystem note:** NextAuth.js → **Auth.js**; ecosystem moving toward **Better Auth** — concepts transfer; verify current docs with AI.

### Custom email/password (credentials provider)

When you **don’t** use Google, **you** become the security team:

- **bcrypt** (e.g. **12 salt rounds**) — never MD5/SHA-1 for passwords  
- Store **hashes + salt** only on server; **`bcrypt.compare`** in `authorize`  
- Rate limiting (e.g. max attempts per email)  
- You must build: reset flow, email verification, lockout, suspicious login — Google does this for OAuth  

**When credentials provider is justified:** internal tools, product requires email/password alongside OAuth, full control over login UI (often **both** Google + credentials).

**LinkedIn / Adobe / Reddit** breach stories: unsalted SHA-1, encrypted-with-leaked-key, vs proper hashing — **implementation quality matters**.

### Protecting data in the app

Check **session** before rendering protected pages; tie queries to **session user id** (hands-on: TanStack `queryKey` includes `userId` from session).

---

## Chapter 3: TanStack Query & Zustand

### Problem (2019 Redux era)

- Putting **all** data in a global client store treats **server data as owned state** — but server data is a **snapshot**, can go stale, and is **shared** across users/tabs.  
- **`useEffect` + `fetch` per component:** duplicated requests, inconsistent loading/error handling, stale data, no shared cache.  
- **TanStack Query (2022)** — server-state library; **Zustand** — lightweight **client** state.

### Server state vs client state

| | **Server state** | **Client state** |
|--|------------------|------------------|
| **Examples** | Puppies, orders, posts, hearts/favorites in DB | Grid vs list view, modal open, form UI |
| **Source of truth** | Postgres (via API/Prisma) | Browser only |
| **Tool** | **TanStack Query** | **Zustand** (or `useState` locally) |
| **Can change without user** | Yes (another user updates DB) | User-controlled |

**Rule:** Data that belongs in the DB → **`useMutation` / `useQuery`**, not Zustand. View preference → **Zustand**, not TanStack.

### TanStack Query essentials

- **`useQuery`**: fetch + cache + loading/error; **`queryKey`** identifies cache entries (e.g. `["puppies"]`, or `["orders", userId]`)  
- **`QueryClientProvider`**: share cache across components  
- **`useState(() => new QueryClient())`**: **per-request/per-user** client on SSR — **don’t** use a module-level singleton (cross-user cache leak)  
- **`useMutation`**: writes (create/update/delete)  
- **`queryClient.invalidateQueries`**: after mutation, mark cache stale → refetch  
- **Optimistic updates:** snapshot cache → update UI immediately → mutate → rollback on error  

**Hooks rule of thumb:**

- Data from server → **`useQuery`**  
- Pure local UI → **`useState`**  
- Same fetched data in many components → **`useQuery`** (shared cache), not prop drilling  

### Zustand essentials

- **`create()`** store with fields + setters (e.g. `view`, `setView`)  
- **No provider required** — import hook in any component  
- vs **Context:** context re-renders all consumers on any change — costly for frequent updates  
- vs **prop drilling:** pass props through many layers — Zustand avoids for **client-only** shared state  

**PawMatch demo flow:** puppy list (`useQuery`) → apply (`useMutation` + invalidate) → favorite heart (optimistic mutation) → grid/list toggle (**Zustand**).

---

## Chapter 4: AI-assisted Prisma schema design

### “Good schema” ≠ “migrates cleanly”

Good means:

- Correct **relationships (cardinality)**  
- **Fast common queries** (indexes)  
- **Types match reality** (dates, money, enums)

AI is strong at **syntax** and first drafts; weak at **your workload** unless you specify it.

### Four common AI mistakes (foster-history example)

1. **Wrong cardinality** — e.g. `@unique` on `puppyId` when a puppy can have **many** foster stays over time  
2. **Missing index** — filter by `puppyId` on large tables → full scan vs indexed lookup (lecture: ~340× example)  
3. **Dates as `String`** — sorting/range queries break; use **`DateTime`**  
4. **Money as `Float`** — rounding errors; use **`Decimal`** (e.g. `@db.Decimal(10, 2)`)  

Also watch: wrong **onDelete** (`Cascade` vs `Restrict`), optional vs required fields, M2M modeled as 1:N duplication.

### Review checklist (before approving AI schema)

- Can there be **many** X per Y? Should any field be **`@unique`**?  
- Which columns appear in **WHERE / JOIN / ORDER BY**? Add **`@@index`**  
- Are dates **`DateTime`**, money **`Decimal`**, statuses **`enum`** when fixed set?  
- **Read generated migration SQL** — compile success is a “vibe check”, not sign-off  

### Stronger prompts

Include: multiple foster stays, index on filter column, **`DateTime` not strings**, **`Decimal` not float** for stipend.

### Postgres tools mentioned

- **`EXPLAIN ANALYZE`** — inspect real query execution plan  
- **`enum`** — DB-enforced allowed values  

### Multi-agent orchestration (Q&A)

You can encode checklist in orchestration prompts, but **real user workload** may differ from agent assumptions — periodically validate **indexes and cardinality** against production-like traffic.

---

## Hands-on lab (TA demo, transcript tail)

- Postgres DB **`demo_test`**, `.env` **`DATABASE_URL`**, Prisma schema + **`migrate dev`**, review SQL, **seed**, **Prisma Studio**  
- Orders app: auth redirect on `/orders`, Google OAuth console setup, **`AUTH_SECRET`**, client ID/secret  
- TanStack query keyed by **session user id**; re-seed with your logged-in email  
- Stack recap: **Prisma** (DB) + **Auth.js** (session) + **Google OAuth** (identity) + **TanStack Query** (per-user fetch)

---

## Key commands reference

```bash
npx prisma init
npx prisma migrate dev --name add_comment
npx prisma migrate deploy
npx prisma studio
npm install @tanstack/react-query
npm install zustand
npx auth secret
```
