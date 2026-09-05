import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { CancelOrderDialog } from "./cancel-order-dialog";

test("confirm button is disabled until the acknowledgement is ticked", () => {
  render(
    <CancelOrderDialog
      orderId="OM-1041"
      customerName="Mr. Iyer"
      onConfirm={jest.fn()}
      onDismiss={jest.fn()}
    />,
  );

  expect(
    screen.getByRole("button", { name: "Cancel the order" }),
  ).toBeDisabled();
});

test("onConfirm does not fire while the confirm button is disabled", async () => {
  const onConfirm = jest.fn();

  render(
    <CancelOrderDialog
      orderId="OM-1041"
      customerName="Mr. Iyer"
      onConfirm={onConfirm}
      onDismiss={jest.fn()}
    />,
  );

  const confirm = screen.getByRole("button", { name: "Cancel the order" });
  expect(confirm).toBeDisabled();

  await userEvent.click(confirm);

  expect(onConfirm).not.toHaveBeenCalled();
});
