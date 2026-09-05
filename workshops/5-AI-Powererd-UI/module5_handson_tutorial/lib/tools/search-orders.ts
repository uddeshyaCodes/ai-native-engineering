// Chapter 3 · Agentic Patterns — searchOrders tool (called by the model via streamText)
import { z } from "zod";
import { tool } from "ai";
import { prisma } from "@/lib/prisma";

export const searchOrders = tool({
  // description steers the model — it only calls this tool when the prompt matches
  description:
    "Search orders by customer name or status. Use this whenever the " +
    "user asks about specific orders.",
  inputSchema: z.object({
    customerName: z.string().optional(),
    status: z.string().optional(),
  }),
  // execute runs on the server when the model decides to call searchOrders
  execute: async ({ customerName, status }) => {
    const orders = await prisma.order.findMany({
      where: {
        ...(customerName
          ? { customerName: { contains: customerName } }
          : {}),
        ...(status ? { status: status.toLowerCase() } : {}),
      },
      orderBy: { createdAt: "desc" },
    });

    return {
      count: orders.length,
      orders: orders.map((order) => ({
        id: order.id,
        customerName: order.customerName,
        item: order.item,
        status: order.status,
        createdAt: order.createdAt.toISOString(),
      })),
    };
  },
});
