# Deploy checklist

Print this. Tick it out loud.

## Before you click Deploy

- [ ] `npm run build` passes locally
- [ ] `npm test` is green
- [ ] CI is green on `main`
- [ ] `git status --short` shows no `.env.local`
- [ ] `package-lock.json` is committed
- [ ] `prisma/schema.prisma` is the **Postgres** version (see Section H, step 1)

## In the Vercel dashboard

- [ ] Project imported, Next.js auto-detected, no config changed
- [ ] `DATABASE_URL` set to the production Postgres string
- [ ] `AUTH_SECRET` set — a **new** one, not the dev value
- [ ] `AUTH_GOOGLE_ID` / `AUTH_GOOGLE_SECRET` set, with the production redirect URI registered in Google Cloud Console
- [ ] `GROQ_API_KEY` present (via the native integration or pasted)
- [ ] Redeployed **after** adding the variables — env vars are read at build time

## After it is live

- [ ] Home page lists showtimes (if it says "Database not ready", you have not migrated)
- [ ] Sign-in completes and comes back to your app, not to localhost
- [ ] A seat books, and survives a hard reload
- [ ] ReelBot streams an answer
- [ ] Ask ReelBot to cancel a booking — the card appears and **nothing happens** until Confirm
- [ ] Lighthouse against the live URL, not localhost
- [ ] Pull `GROQ_API_KEY` out and redeploy: browsing and booking still work. Put it back.

That last one is the deploy-day version of slide 18. If the AI feature going down takes the booking flow with it, you did not ship a portal with an assistant — you shipped an assistant with a portal attached.
