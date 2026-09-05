import { ORDERS } from "../orders";
import { searchOrders } from "./search-orders";

test("returns all orders when no filters are given", async () => {
  const results = await searchOrders.execute({});
  expect(results).toEqual(ORDERS);
});

test("filters by customer name, case-insensitively", async () => {
  const results = await searchOrders.execute({ customerName: "iyer" });
  expect(results).toHaveLength(2);
  expect(results.every((order) => order.customerName === "Mr. Iyer")).toBe(
    true,
  );
});

test("trims whitespace from the customer name", async () => {
  const results = await searchOrders.execute({ customerName: "  Priya  " });
  expect(results).toHaveLength(1);
  expect(results[0].id).toBe("OM-1042");
});

test("filters by status", async () => {
  const results = await searchOrders.execute({ status: "shipped" });
  expect(results).toHaveLength(1);
  expect(results[0].id).toBe("OM-1042");
});

test("applies customer name and status together", async () => {
  const results = await searchOrders.execute({
    customerName: "Iyer",
    status: "packed",
  });
  expect(results).toHaveLength(1);
  expect(results[0]).toMatchObject({
    id: "OM-1041",
    customerName: "Mr. Iyer",
    status: "packed",
  });
});

test("returns an empty array when nothing matches", async () => {
  const results = await searchOrders.execute({
    customerName: "Nobody",
  });
  expect(results).toEqual([]);
});
