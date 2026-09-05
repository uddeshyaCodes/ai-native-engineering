import { runCancelOrder } from "@/lib/tools/cancel-order";

// Called only from orders-full's chat panel, only after a human clicks
// Confirm on the ConfirmToolCall card never called automatically.
export async function POST(req: Request) {
  const { orderId } = await req.json();
  const result = await runCancelOrder({ orderId });
  return Response.json(result);
}
