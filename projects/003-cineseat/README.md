# 003 — CineSeat

Cinema booking portal from **Module 7** (IIT Kharagpur × upGrad): accessible seat map, Prisma + NextAuth, ReelBot on Groq with a human confirmation gate, Jest tests, and audit fixes.

Built by applying workshop sections **A → G** under `Upgrad-L7-cineseat-project/`. Local DB is SQLite. Section **H** (Vercel + Postgres) is optional — see `docs/`.

## Run locally

```bash
cd projects/003-cineseat
cp .env.example .env.local   # already done if you followed setup
npm install
npm run db:migrate && npm run db:seed
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

**No API keys required.** Empty Google credentials → demo sign-in. Empty `GROQ_API_KEY` → ReelBot offline-mode stream. Booking still works.

Optional:

```bash
# Free key: https://console.groq.com/keys
GROQ_API_KEY="gsk_..."
```

## Commands

| Command | Does |
|---|---|
| `npm run dev` | Dev server (axe-core in the console) |
| `npm run build` / `npm start` | Production build — audit against this |
| `npm test` | 11 tests, no network, no API key |
| `npm run test:coverage` | Coverage report |
| `npm run db:migrate` | Create / migrate SQLite |
| `npm run db:seed` | Three films, seats, seeded bookings |
| `npm run db:reset` | Wipe and re-seed |
| `npm run audit:a11y` | axe-core CLI against a running server |

## Deploy (Section H)

SQLite does not work on Vercel. Checklist and env template:

- `docs/DEPLOY-CHECKLIST.md`
- `docs/env.production.example.txt`
- `docs/SECRETS.md`

Swap with `prisma/schema.postgres.prisma`, point `DATABASE_URL` at Postgres, migrate, then import the repo on Vercel.

## Workshop source

Letter-by-letter packet: `../../Upgrad-L7-cineseat-project/`
