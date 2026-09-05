// Chapter 4 · Human-in-the-Loop — cancelOrder has NO execute() on purpose
import { tool } from "ai";
import { z } from "zod";
import { prisma } from "@/lib/prisma";

// IMPORTANT: no execute() here — the model proposes cancelOrder, the UI shows a
// confirmation card, and runCancelOrder() runs only after the user clicks Confirm.
export const cancelOrder = tool({
  description:
    "Cancel an order by its ID. DESTRUCTIVE this permanently changes " +
    "the order's status to cancelled. Requires human confirmation before " +
    "it runs; you are only proposing this action, not performing it.",
  inputSchema: z.object({
    orderId: z.string().describe("The ID of the order to cancel"),
  }),
});

// Called only from app/api/run-cancel-order after human confirmation — not from the tool itself
export async function runCancelOrder({ orderId }: { orderId: string }) {
  const existing = await prisma.order.findUnique({ where: { id: orderId } });

  if (!existing) {
    return { error: "Order not found", orderId };
  }

  const order = await prisma.order.update({
    where: { id: orderId },
    data: { status: "cancelled" },
  });

  return {
    orderId: order.id,
    customerName: order.customerName,
    item: order.item,
    status: order.status,
  };
}
