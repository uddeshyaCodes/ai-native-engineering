# Module 1: AI-Native Development Fundamentals, Vibe Coding & Real-Time Systems

Study notes derived from lecture transcripts for graded assignment prep (10 MCQs).

**Source transcripts:** [`transcripts/module-1/`](../../transcripts/module-1/) (`lecture-01-….txt` … `lecture-06-….txt`)

---

## Lectures

| # | Folder | Topic | Instructor (from transcript) |
|---|--------|--------|------------------------------|
| 01 | [lecture-01-foundation-models-token-economics](./lecture-01-foundation-models-token-economics/) | Foundation models, token economics, hallucinations, AI pair programming, build vs buy | Prof. Rajat Shukla Chakraborty |
| 02 | [lecture-02-js-ts-nextjs-app-router](./lecture-02-js-ts-nextjs-app-router/) | Node.js event loop / streams, defensive TypeScript, Next.js App Router | Prof. Rohit Shubhra Chakraborty |
| 03 | [lecture-03-accessible-components-with-ai](./lecture-03-accessible-components-with-ai/) | Tailwind, shadcn/ui, WCAG, axe-core accessibility testing | Dr. Mainak Mandal |
| 04 | [lecture-04-postgres-prisma-oauth](./lecture-04-postgres-prisma-oauth/) | Prisma, OAuth/Auth.js, TanStack Query, Zustand, AI schema design | (Module 4 session) |
| 05 | [lecture-05-realtime-streaming-ai-ui](./lecture-05-realtime-streaming-ai-ui/) | Order Mitra — SSE streaming, AI SDK, agents / tools, confidence UI | (Module 5 session) |
| 06 | [lecture-06-testing-cicd-deployment](./lecture-06-testing-cicd-deployment/) | Jest/RTL, AI-assisted tests, GitHub Actions CI, Vercel CD | (Module 6 session) |

Each lecture folder has:

| File | Purpose |
|------|---------|
| `study-material.md` | Structured exam-ready notes |
| `important-questions.md` | Practice Q&As aligned to graded MCQs |
| `quiz.md` | Quizzes/polls actually asked in the lecture (with answers when stated) |

---

## Known transcript gaps

- **Lecture 03:** Recording ends mid Q&A; Chapter 4 (end-to-end AI-generated UI verification) is announced but not fully present in the transcript. Some poll stems incomplete.
- **Lecture 05:** Transcript cuts off during the multi-step agent/tool section; HITL cancel-order hands-on detail is partial.
- Lecture titles / instructor names not always spoken clearly — folders use topics from the opening agenda; update titles later if you have the official syllabus names.

---

## Suggested study order for the 10-MCQ assignment

1. Lecture 01 quizzes + token / hallucination / Spec→Verify→Override sections  
2. Lecture 05 (SSE vs polling vs WebSockets, streaming, tools)  
3. Lecture 02 (event loop, strict TS, App Router streaming)  
4. Lectures 03–04–06 for accessibility, data/auth, and testing/CI traps  

Start with each folder’s `quiz.md`, then skim `important-questions.md`, then use `study-material.md` to fill gaps.
