# Lecture 04 — Important Questions (Exam-style)

Answers are grounded in the Module 4 transcript. Wording of distractors may differ on the actual MCQ.

---

### 1. Where do you define data models in a Prisma project?

**Answer:** In **`schema.prisma`** (the Prisma schema file). It is the single source of truth for models, relations, migrations, and the generated client.

---

### 2. Which statement best describes how Prisma helps prevent SQL injection?

**Answer:** It treats user input as **safe, bound values** in typed queries—not as raw SQL text concatenated into commands. (Hiding Postgres from the internet is not the primary anti-injection mechanism.)

---

### 3. What is NOT something Prisma does?

**Answer:** It does **not** design your app’s **user interface**. It is database/ORM tooling, not a UI framework.

---

### 4. How is each Prisma migration stored?

**Answer:** As a **plain SQL file** under version control that you can review—not a temporary file deleted after apply, and not an opaque binary/image.

---

### 5. When should you use `migrate dev` vs `migrate deploy`?

**Answer:** **`migrate dev`** during local development when changing `schema.prisma`. **`migrate deploy`** in production to apply pending migrations. **Never run `migrate dev` in production.**

---

### 6. When is `db push` appropriate vs `migrate dev`?

**Answer:** **`db push`** only for quick **solo prototyping** without migration history. Teams and production paths should use **`migrate dev`** for versioned SQL.

---

### 7. Why does the lecture insist on Prisma even if you know Postgres?

**Answer:** Raw SQL from app code is a major **SQL injection** risk; Prisma adds **compile-time typed access** and **versioned migrations**, reducing common developer mistakes (ORM does not eliminate all vulnerabilities).

---

### 8. What is the main benefit of OAuth with a provider like Google (per lecture quiz discussion)?

**Answer:** Your app **never sees the user’s password**—the user authenticates at the trusted provider. OAuth does **not** by itself mean passwords are stored more securely **on your server** (that requires your own hashing if you store passwords).

---

### 9. “Sign in with Google” on a third-party site is an example of what?

**Answer:** **OAuth in action** (delegated authorization/authentication via a provider)—not a database backup or caching strategy.

---

### 10. In the default OAuth provider flow, who verifies the user’s password?

**Answer:** The **trusted provider** (e.g. Google)—not your Next.js app. (Your app verifies passwords only if you implement a **credentials** provider yourself.)

---

### 11. What authentication approach did the lecture recommend as the default?

**Answer:** **Delegate to a trusted provider** using **Auth.js / NextAuth**—not plain-text storage, skipping auth, or a from-scratch login with no security design.

---

### 12. Name the four OAuth 2.0 roles.

**Answer:** **Resource owner** (user), **client** (your app), **authorization server** (token issuer), **resource server** (protected APIs/data).

---

### 13. JWT session vs database session—when prefer each?

**Answer:** **JWT** for high-throughput, stateless verification without a DB hit each request. **Database sessions** when you need **immediate revocation** (compromised account).

---

### 14. What are the three parts of a JWT?

**Answer:** **Header**, **payload**, **signature** (signed claims; verifier checks signature with secret/public key).

---

### 15. What is a common production OAuth misconfiguration?

**Answer:** **Redirect URI** registered for `localhost` but **not** for the live domain—or any mismatch between Google console redirect URI and `AUTH_URL`/callback URL.

---

### 16. How should passwords be stored for a custom credentials provider?

**Answer:** **bcrypt** hashed with **salt** (e.g. 12 rounds)—store hash on server only; compare with **`bcrypt.compare`** in `authorize`. Never MD5/SHA-1/plain text.

---

### 17. What type of state does TanStack Query manage?

**Answer:** **Server state**—data fetched from APIs/DB (puppies, orders, posts), including caching, refetch, and invalidation.

---

### 18. What type of state does Zustand manage in the lecture’s split?

**Answer:** **Client state** shared across components (e.g. grid vs list view)—not data that belongs in Postgres.

---

### 19. Why must `QueryClient` be created with `useState` in the provider pattern shown?

**Answer:** On shared/SSR servers, a **module-level singleton** would let **different users share one cache**—a serious isolation bug. Per-render/per-user `useState` avoids that.

---

### 20. After a successful `useMutation`, why call `invalidateQueries`?

**Answer:** Cached **read** data is stale; invalidation triggers **refetch** so the UI matches the updated server (e.g. adoption status on puppy list).

---

### 21. What is an optimistic update?

**Answer:** Update the UI **immediately**, run the mutation in the background, **rollback** from a snapshot if the mutation fails—better perceived responsiveness (heart button example).

---

### 22. What is wrong with modeling money as `Float` in Prisma/Postgres?

**Answer:** Floating-point **cannot represent decimals exactly**—totals drift by cents; use **`Decimal`** with fixed precision.

---

### 23. Why is `@unique` on `puppyId` in a foster-stay table a cardinality bug?

**Answer:** It forces **at most one foster row per puppy**, contradicting “multiple foster stays over time” (should be one-to-many puppy → stays).

---

### 24. Why add an index on `puppyId` if queries filter by it?

**Answer:** Avoids **full table scans** as data grows; lecture showed large latency difference with vs without index on filter column.

---

### 25. Before running an AI-generated migration, what should you always do?

**Answer:** **Read and review the generated migration SQL** (and schema)—not approve on “it compiled” alone.

---

### 26. Why do schema/migration bugs need more care than UI bugs?

**Answer:** They may **pass compile/migrate** but cause **slow queries or corrupted data months later** after real data exists—hard to undo and not obvious in UI code review.

---

### 27. What do AI agents commonly forget in schemas (per end-of-lecture poll topic)?

**Answer:** **`@@index` / indexes** on columns heavily used in queries—agents don’t know your workload unless you specify it.

---

### 28. For custom OAuth/credentials login, must you validate the password on the server?

**Answer:** **Yes.** Hash the incoming password with bcrypt and **`compare`** to the stored hash in `authorize`; the client sends plaintext over TLS, server never stores plaintext.

---

### 29. `useQuery` vs `useMutation`—when use which?

**Answer:** **`useQuery`** for **reads** (fetch/cache). **`useMutation`** for **writes** (create/update/delete) that change server data.

---

### 30. Should puppy adoption records be stored in Zustand?

**Answer:** **No.** Adoption/favorites belong in **server state** (DB + TanStack Query/mutations). Zustand is for **client-only** preferences like layout toggle.
