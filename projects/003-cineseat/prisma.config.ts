import fs from "node:fs";
import path from "node:path";
import { defineConfig } from "prisma/config";

/**
 * Why this file exists.
 *
 * `npx prisma init` creates a prisma.config.ts, and from that moment the
 * Prisma CLI stops loading env files by itself - it prints
 * "Prisma config detected, skipping environment variable loading."
 * On top of that, the Prisma CLI has never read `.env.local`; that filename
 * is a Next.js convention, not a Prisma one.
 *
 * Together those two produce:
 *
 *   Error code: P1012
 *   error: Error validating datasource `db`: the URL must start with the
 *   protocol `file:`.
 *
 * which is Prisma's confusing way of saying DATABASE_URL was UNDEFINED.
 *
 * So this file does three things, in order, and says so out loud.
 */

const root = process.cwd();

/** Node 20.12+ has process.loadEnvFile. Older Node gets a small parser. */
function loadEnvFile(file: string) {
  const full = path.join(root, file);
  if (!fs.existsSync(full)) return;

  if (typeof process.loadEnvFile === "function") {
    process.loadEnvFile(full);
    return;
  }

  for (const line of fs.readFileSync(full, "utf8").split("\n")) {
    const match = /^\s*([\w.-]+)\s*=\s*(.*)?\s*$/.exec(line);
    if (!match?.[1]) continue;
    const key = match[1];
    if (process.env[key] !== undefined) continue; // already set wins
    process.env[key] = (match[2] ?? "").trim().replace(/^["']|["']$/g, "");
  }
}

// 1. Load the project's env files. Variables already set in the shell win,
//    which is what makes `DATABASE_URL="postgres://..." npm run db:migrate`
//    work in Section H without editing anything.
loadEnvFile(".env.local");
loadEnvFile(".env");

// 2. A local default, so a missing .env.local can never block the class.
//    Deployments always set DATABASE_URL, so this only ever fires locally.
if (!process.env.DATABASE_URL) {
  process.env.DATABASE_URL = "file:./dev.db";
  console.warn(
    "[prisma.config] DATABASE_URL was not set - defaulting to file:./dev.db. " +
      "Run `cp .env.example .env.local` if you have not yet.",
  );
}

export default defineConfig({
  schema: path.join("prisma", "schema.prisma"),
  migrations: {
    seed: "node prisma/seed.mjs",
  },
  // 3. Belt and braces: passing the url here overrides the schema's
  //    env("DATABASE_URL") lookup, so the CLI cannot disagree with us about
  //    which database it is talking to.
  datasource: {
    url: process.env.DATABASE_URL,
  },
});
