// Chapter 2c · Confidence Indicator (second exercise) — POST /api/order-summary
// Same structured-output pattern as app/api/answer/route.ts, but grounded in Prisma order data
import { generateText, Output } from "ai";
import { groq } from "@ai-sdk/groq";
import { z } from "zod";
import { prisma } from "@/lib/prisma";

const orderSummarySchema = z.object({
  summary: z
    .string()
    .describe("A brief natural-language summary of this customer's orders"),
  confidence: z
    .enum(["high", "medium", "low"])
    .describe("How confident you are that the summary matches the order data"),
  ordersReferenced: z
    .number()
    .int()
    .min(0)
    .describe("How many orders from the data were included in the summary"),
});

export async function POST(req: Request) {
  const { customerName }: { customerName: string } = await req.json();

  // Load matching orders from SQLite via Prisma (seeded in prisma/seed.ts)
  const orders = await prisma.order.findMany({
    where: { customerName: { contains: customerName } },
  });

  // No LLM call needed when there is nothing to summarize
  if (orders.length === 0) {
    return Response.json({
      summary: `No orders found for "${customerName}".`,
      confidence: "high" as const,
      ordersReferenced: 0,
    });
  }

  // Turn DB rows into plain text context for the model (like context in /api/answer)
  const orderContext = orders
    .map(
      (order) =>
        `- ${order.item} (${order.status}), placed ${order.createdAt.toISOString()}`
    )
    .join("\n");

  const { output } = await generateText({
    model: groq("openai/gpt-oss-120b"),
    system:
      "Summarize the customer's orders using only the order data provided. " +
      "Set ordersReferenced to how many orders you mention. " +
      "Lower confidence if the data is sparse or ambiguous.",
    output: Output.object({ schema: orderSummarySchema }),
    prompt: `Customer: ${customerName}\n\nOrders:\n${orderContext}`,
  });

  return Response.json(output);
}
