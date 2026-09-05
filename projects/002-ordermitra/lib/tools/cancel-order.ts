import { ORDERS, type Order } from "../orders";

export type CancelResult =
  | { ok: true; order: Order }
  | { ok: false; reason: string };

/**
 * Session 5's destructive tool. Unlike searchOrders, calling this by mistake
 * costs a real customer a real order — which is why the UI puts a confirmation
 * gate in front of it, and why both the tool and the gate get regression tests.
 */
export const cancelOrder = {
  name: "cancelOrder",
  description: "Cancel an order that has not shipped yet.",

  async execute({ orderId }: { orderId: string }): Promise<CancelResult> {
    const order = ORDERS.find((o) => o.id === orderId);

    if (!order) {
      return { ok: false, reason: `No order found with id ${orderId}.` };
    }

    // The guard that matters. Once something is on a truck, cancelling it in
    // our database does not bring it back.
    if (order.status === "shipped" || order.status === "delivered") {
      return {
        ok: false,
        reason: `Order ${orderId} has already ${order.status} and cannot be cancelled.`,
      };
    }

    return { ok: true, order };
  },
};
