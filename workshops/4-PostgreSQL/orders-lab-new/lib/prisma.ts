// lib/prisma.ts
// Singleton so Next.js hot-reload in dev doesn't spawn a new PrismaClient
// (and a new connection pool) on every file change.

import { PrismaClient } from "@prisma/client";

const globalForPrisma = globalThis as unknown as { prisma?: PrismaClient };

export const prisma = globalForPrisma.prisma ?? new PrismaClient();

if (process.env.NODE_ENV !== "production") globalForPrisma.prisma = prisma;
