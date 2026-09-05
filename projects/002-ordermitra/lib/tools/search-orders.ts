import { ORDERS, type Order } from "../orders";

export type SearchOrdersInput = {
  customerName?: string;
  status?: Order["status"];
};

/**
 * Session 5's searchOrders tool, with the model-facing wrapper stripped off.
 * Chapter 2 audits this function: the "found something" path is the obvious
 * one to test, and the "found nothing" path is the one that gets forgotten.
 */
export const searchOrders = {
  name: "searchOrders",
  description: "Find orders belonging to a customer, optionally filtered by status.",

  async execute(input: SearchOrdersInput): Promise<Order[]> {
    const { customerName, status } = input;

    let results = ORDERS;

    if (customerName) {
      const needle = customerName.trim().toLowerCase();
      results = results.filter((order) =>
        order.customerName.toLowerCase().includes(needle)
      );
    }

    if (status) {
      results = results.filter((order) => order.status === status);
    }

    // Returning [] rather than null or throwing is a deliberate contract:
    // the UI renders "no orders found" from an empty array.
    return results;
  },
};
