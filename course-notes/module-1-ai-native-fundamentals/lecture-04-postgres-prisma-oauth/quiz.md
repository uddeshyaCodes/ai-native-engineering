# Lecture 04 — In-Lecture Polls & Quizzes

The Module 4 transcript includes **four poll blocks** run by TAs (“folks, I take over to you” / iTech side). Options below are reconstructed from spoken text; exact letter labels may differ on slides.

**Not counted as content quizzes:** session feedback poll during the hands-on (“share your feedback in the polls section”).

---

## Block A — After Prisma (before OAuth chapter)

**Host transition:** Short quiz after schema, migration, and SQL injection discussion.

### A1. Where do you define your data models in a Prisma project?

**Stated result:** First option (“previous one”) was **correct**; class answered unanimously.

**Answer:** **`schema.prisma`**

---

### A2. What doesn’t Prisma do?

**Distractors (spoken):** e.g. helps SQL injection / treats input as bound values / **designs the user interface of your app**

**Stated result:** Most correct; wrong pick was **designs the UI**.

**Answer:** Prisma does **not** design your app UI.

---

### A3. How does Prisma help with SQL injection? (discussion question)

**Stated teaching:** Best answer — treats user input as **bound values**, not raw SQL. “Hides database from internet” is **not** the core reason.

---

### A4. Each Prisma migration is saved as what?

**Options (spoken):** plain SQL file you can review in version control · temporary file deleted after run · image/hidden system file

**Stated result:** ~90% chose plain SQL file.

**Answer:** **Version-controlled plain `.sql` migration file** (not deleted after apply).

---

## Block B — OAuth recap (before break)

**Host:** “5 minutes for quiz” after OAuth/JWT/session recap.

### B1. What is the main benefit of OAuth?

**Options (spoken):**

1. Makes your website load faster  
2. **App never sees the user’s password**  
3. Stores passwords more securely on your server  
4. Removes the need for any login  

**Stated result:** Two contenders (options 2 and 3); instructor clarified **option 2**.

**Answer:** **The app never sees the user’s password** when using a provider like Google. OAuth does **not** automatically secure password storage on **your** DB.

---

### B2. “Sign in with Google” on a website is an example of what?

**Options (spoken):** database backup · **OAuth in action** · caching strategy · (CS-related distractor garbled in transcript)

**Stated result:** “Wisdom of the crowd wins” — correct.

**Answer:** **OAuth in action**

---

### B3. With OAuth, who manually checks the user’s password?

**Options (spoken):** trusted provider (Google) · your Next.js app · user’s identity provider · no one / passwords don’t exist  

**Stated result:** Most picked **trusted provider**.

**Clarification:** “Passwords don’t exist” is misleading—you may still log into Google; provider checks password. Your app checks passwords only in **custom credentials** flow.

**Answer:** **Trusted provider (e.g. Google)**

---

### B4. Recommended authentication approach in this lecture?

**Options (spoken):** write login from scratch · store plain text for speed · skip authentication · **delegate to trusted provider using NextAuth/Auth.js**

**Stated result:** Clear winner (~70%).

**Answer:** **Delegate to a trusted provider using Auth.js / NextAuth**

---

## Block C — TanStack Query & Zustand (before AI schema chapter)

**Host:** “Quick” understanding check after PawMatch demo.

### C1. What type of data is TanStack Query designed to manage?

**Stated result:** “Okie Dokie, that is correct” after quick poll.

**Answer:** **Server state** (data from API/database—not purely local UI state).

---

### C2. What does TanStack Query do with fetched data?

**Options (spoken):** fetches and **deletes immediately** · prints terminal events for developers · **stores in cache so it can be reused**

**Stated result:** Class answered correctly (“you guys are good”).

**Answer:** **Caches** server data for reuse, deduplication, and coordinated refetch—not delete on fetch.

---

### C3. Where should you stop fetching data? (poll wording in transcript)

**Options (spoken):** inside **`useEffect`** · inside the database · inside CSS · inside HTML `<head>`

**Note:** Instructor did not read out a single winning option clearly in the transcript. The lecture’s teaching is to **avoid the `useEffect` + manual `fetch` anti-pattern** and use **`useQuery`** (with `QueryClientProvider`) instead.

**Best exam alignment:** **Do not** rely on ad-hoc **`useEffect` fetching** for server data; use **TanStack Query**.

---

### C4. What hook should you use for data that comes from your server?

**Stated result:** Fast correct response.

**Answer:** **`useQuery`** (TanStack Query)

---

## Block D — AI schema review (end of lecture)

**Host:** “Last quiz to check understanding on schema review” (iTech); includes “finish this slow dot decimal” drift toward **Decimal** for money.

### D1. Money / currency in AI schemas should prefer which type?

**Context:** Poll mentioned “slow dot decimal” and “drift” away from float.

**Answer:** **`Decimal`**, not **`Float`**, for currency (fixed precision).

---

### D2. What do AI agents commonly forget to add?

**Stated result:** “This is good” after poll—aligned with index discussion.

**Answer:** **Indexes (`@@index`)** on columns used heavily in queries/filters.

---

### D3. Before running an AI-generated migration, what should you always do?

**Stated result:** Positive response—“nothing replaces you in the process.”

**Answer:** **Review the generated migration SQL** (and schema)—do not approve on compile/migrate success alone.

---

### D4. Why do migrations need extra care compared to UI bugs?

**Stated result:** “Awesome” — class understood.

**Answer:** Schema errors may **look fine in review** but cause **slow queries or data corruption later** when real data exists—unlike many visible UI bugs.

---

## Interactive Q&A (not MCQ polls)

These were **live questions**, not slide polls:

1. **Multi-agent orchestration** — Can schema best practices be a master orchestration prompt? **Yes**, but still validate **real workload**, indexes, and cardinality; users may behave unlike agents.  
2. **Custom OAuth / credentials** — Must you validate password on server? **Yes** — bcrypt hash + compare to stored hash; use salting per slides.

---

## Summary

| Block | Topic | # questions |
|-------|--------|-------------|
| A | Prisma models, SQL safety, migrations | 4 |
| B | OAuth benefits & roles | 4 |
| C | TanStack vs Zustand / hooks | 4 |
| D | AI schema review | 4 |

**Total documented in-lecture quiz items:** **16**, plus **2** Q&A clarifications.
