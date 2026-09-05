// prisma/seed.ts
// Run with: npx prisma db seed
// Creates one demo user + a few orders so /orders has something to render.

import { PrismaClient, OrderStatus } from "@prisma/client";

const prisma = new PrismaClient();

async function main() {
  const user = await prisma.user.upsert({
    where: { email: "demo@acme.dev" },
    update: {},
    create: {
      email: "demo@acme.dev",
      name: "Demo User",
    },
  });

  await prisma.order.deleteMany({ where: { userId: user.id } });

  await prisma.order.createMany({
    data: [
      { userId: user.id, total: 142.0, status: OrderStatus.PAID },
      { userId: user.id, total: 89.5, status: OrderStatus.SHIPPED },
      { userId: user.id, total: 26.0, status: OrderStatus.PENDING },
    ],
  });

  console.log(`Seeded 3 orders for ${user.email} (id: ${user.id})`);
}

main()
  .catch((e) => {
    console.error(e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
