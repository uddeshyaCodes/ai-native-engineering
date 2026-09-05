# GitHub Secrets & Branch Protection — the five-click version

## 1. Add the Groq key as a repository secret

**Settings → Secrets and variables → Actions → New repository secret**

| Name | Value |
|---|---|
| `GROQ_API_KEY` | your key from console.groq.com |

Same flow as Session 6's Anthropic key. Only the name changed.

> **Does the current workflow need it?** No — every test mocks the model, which
> is the point of Section E. Add it anyway: the moment someone adds an
> integration test or a preview deploy, it is already there, and adding a
> secret is not the thing you want to be doing at that moment.

## 2. Never let a secret near the repo any other way

- `.env.local` is in `.gitignore`. Confirm before your first push: `git status --short`
- If a key ever does get committed, rotating it is the fix. Deleting the commit is not — it is already in the fork network and in the push logs.

## 3. Require the check before merging

**Settings → Branches → Add branch ruleset (or Add rule) → `main`**

- Require a pull request before merging
- Require status checks to pass → select **Test**

Session 6's exact 5-click setup. Nothing CineSeat-specific.

## What this buys you

A pipeline that keeps checking after you have stopped paying attention. On a solo project that sounds like ceremony. On the day someone asks an AI assistant to "just quickly refactor the message bubble", it is the thing that notices the confirmation gate stopped gating.
