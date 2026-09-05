# Orders Lab

A hands-on lab covering an AI-assisted database schema (Prisma), migrations,
authentication (NextAuth + Google), and protected data fetching (TanStack
Query) — built on Next.js and PostgreSQL.

---

## Prerequisites

- **Node.js** (LTS) — npm comes bundled with it
- **PostgreSQL**
- **A Google account** — used to set up OAuth login

---

## Setup

### 1. Create the database

Open **SQL Shell (psql)**, press Enter through the prompts to accept
defaults, enter your Postgres password, then run:

```sql
CREATE DATABASE orders_lab;
```

### 2. Install dependencies

```bash
npm install
```

### 3. Configure environment variables

```bash
cp .env.example .env
```

Fill in `.env`:

- `DATABASE_URL` — your real Postgres password:
  `postgresql://postgres:YOUR_PASSWORD@localhost:5432/orders_lab`
- `NEXTAUTH_URL` — `http://localhost:3000`
- `AUTH_SECRET` — generate with `npx auth secret`
  *(if that command outputs `BETTER_AUTH_SECRET`, rename it to `AUTH_SECRET` — this project reads that exact name)*
- `GOOGLE_CLIENT_ID` / `GOOGLE_CLIENT_SECRET` — see [Google OAuth setup](#6-google-oauth-setup) below

### 4. Run the migration

```bash
npx prisma migrate dev --name add_order
```

Optional: inspect the database visually with `npx prisma studio`.

### 5. Seed demo data

```bash
npm run seed
```

This creates a demo user (`demo@acme.dev`) with 3 fake orders. If you want
data to show up after logging in with your **own** Google account, open
`prisma/seed.ts`, replace both instances of `demo@acme.dev` with your real
email, and re-run `npm run seed`.

### 6. Google OAuth setup

1. Go to [console.cloud.google.com](https://console.cloud.google.com/) and create a new project
2. **APIs & Services → OAuth consent screen** → User type **External** → fill in app name and your email → continue through the remaining screens with defaults
3. **APIs & Services → Credentials → + Create Credentials → OAuth client ID** → Application type **Web application**
4. Under **Authorized redirect URIs**, add exactly:
   ```
   http://localhost:3000/api/auth/callback/google
   ```
5. Copy the generated **Client ID** and **Client Secret** into `.env`

### 7. Run the app

```bash
npm run dev
```

Visit `http://localhost:3000/orders`. Logged out, you'll be redirected to
`/login`. After signing in with Google, your seeded orders should render.

---

## The Lab: AI-Drafted Schema, Reviewed

This is the core exercise: use an AI tool to draft a database model, then
review and correct it before trusting it.

### Step 1 — Prompt for the schema

Give this prompt to an AI pair-programming tool (Claude Code, Cursor, etc.):

```
Add an Order model to prisma/schema.prisma.

- Order belongs to a User (many orders per user)
- Fields: total (currency, precise), status (bounded:
  pending, paid, shipped, cancelled), createdAt
- Index any foreign key and the status field
- Use appropriate types for currency and enums
```

A common first draft looks like this:

```prisma
model Order {
  id     String @id @default(cuid())
  userId String
  total  Float
  status String
  user   User   @relation(fields: [userId], references: [id])
}
```

Two problems: `total Float` loses precision on currency math, and
`status String` accepts any string, with no index on either column.

### Step 2 — Review the diff

"Reviewing the diff" means looking at exactly what changed — old line vs.
new line — before accepting it, not just re-reading the final file.

**If your AI tool is integrated into your editor** (Claude Code, Cursor,
Copilot Chat), it shows this automatically: red lines for removals, green
for additions, inline, before you accept anything.

**If you're pasting AI output in by hand**, use git to see the diff yourself:

```bash
git init
git add prisma/schema.prisma
git commit -m "before AI draft"
# paste the AI's draft into the file, save
git diff prisma/schema.prisma
```

Either way, check the draft against this list:

- [ ] Does `status` use an enum, not a free-text string?
- [ ] Is `total` typed as `Decimal`, not `Float`?
- [ ] Is there an `@@index([userId])` on `Order`?
- [ ] Does the relation direction match the domain?

### Step 3 — Apply the reviewed schema

The corrected version, already in `prisma/schema.prisma`:

```prisma
enum OrderStatus {
  PENDING
  PAID
  SHIPPED
  CANCELLED
}

model Order {
  id        String      @id @default(cuid())
  userId    String
  total     Decimal     @db.Decimal(10, 2)
  status    OrderStatus @default(PENDING)
  createdAt DateTime    @default(now())
  user      User        @relation(fields: [userId], references: [id])

  @@index([userId])
  @@index([status])
}
```

### Step 4 — Run the migration

```bash
npx prisma migrate dev --name add_order
npm run seed
```

Open the generated `prisma/migrations/*/migration.sql` and read it — this
is the actual SQL that changed your database, not something to skip past.

### Step 5 — Protected route + data fetching

Already wired in this project:

- `auth.ts` — NextAuth config, Google provider, database sessions
- `app/orders/page.tsx` — server-side session check, redirects to `/login` if absent
- `app/orders/orders-list.tsx` — client component, `useQuery`, loading and error states
- `app/api/orders/route.ts` — reads the user id from the **session**, never
  from a client-supplied parameter

This last point is a deliberate security choice worth understanding: an API
route that trusted a client-passed `userId` (e.g. `/api/orders?userId=...`)
would let anyone view anyone else's orders just by changing the URL. Deriving
identity from the server-side session instead closes that off.

---

## Production readiness checklist

| Layer | Check |
|---|---|
| Schema | Enum for bounded fields, Decimal for currency, indexes on all foreign keys |
| Auth | Route redirects unauthenticated users, session checked server-side before render |
| Data fetching | `queryKey` includes all relevant params, loading and error states both handled |

---

## Security note

`.env` contains real secrets (database password, OAuth client secret,
`AUTH_SECRET`) and is excluded via `.gitignore` — never commit it. If you're
forking or cloning this repo, always start from `.env.example` and fill in
your own values.