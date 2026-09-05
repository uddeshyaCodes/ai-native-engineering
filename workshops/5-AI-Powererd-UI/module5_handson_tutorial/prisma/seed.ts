import { PrismaClient } from "@prisma/client";

const prisma = new PrismaClient();

async function main() {
  await prisma.order.deleteMany();

  await prisma.order.createMany({
    data: [
      { customerName: "Mr. Iyer", item: "47 brass diyas", status: "pending" },
      { customerName: "Mr. Iyer", item: "Birthday candles", status: "shipped" },
      { customerName: "Priya Sharma", item: "Wireless mouse", status: "delivered" },
      { customerName: "Arjun Mehta", item: "Desk lamp", status: "pending" },
      { customerName: "Fatima Khan", item: "Bluetooth speaker", status: "shipped" },
      { customerName: "Rahul Verma", item: "Notebook set", status: "delivered" },
    ],
  });

  console.log("Seeded orders.");
}

main()
  .catch((e) => {
    console.error(e);
    process.exit(1);
  })
  .finally(() => prisma.$disconnect());
