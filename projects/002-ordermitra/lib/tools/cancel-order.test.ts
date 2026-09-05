import { cancelOrder } from "./cancel-order";

test("refuses an order that has already shipped", async () => {
  const result = await cancelOrder.execute({ orderId: "OM-1042" });

  expect(result).toEqual({
    ok: false,
    reason: "Order OM-1042 has already shipped and cannot be cancelled.",
  });
});

test("refuses an order that has already been delivered", async () => {
  const result = await cancelOrder.execute({ orderId: "OM-1043" });

  expect(result).toEqual({
    ok: false,
    reason: "Order OM-1043 has already delivered and cannot be cancelled.",
  });
});

test("refuses an unknown order id", async () => {
  const result = await cancelOrder.execute({ orderId: "OM-9999" });

  expect(result).toEqual({
    ok: false,
    reason: "No order found with id OM-9999.",
  });
});
