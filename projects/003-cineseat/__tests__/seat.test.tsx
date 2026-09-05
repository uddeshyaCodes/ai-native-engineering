import { fireEvent, render, screen } from "@testing-library/react";
import { Seat } from "@/components/seat";

describe("Seat", () => {
  it("announces row, number and status", () => {
    render(<Seat row="D" number={4} status="available" />);
    expect(
      screen.getByRole("button", { name: "Row D, Seat 4, available" }),
    ).toBeInTheDocument();
  });

  it("stays reachable when booked, so a screen reader still announces it", () => {
    render(<Seat row="D" number={4} status="booked" />);
    const seat = screen.getByRole("button", { name: "Row D, Seat 4, booked" });

    // aria-disabled, not `disabled` - a disabled button is skipped by the
    // keyboard entirely, which is the exact silence we set out to fix.
    expect(seat).toHaveAttribute("aria-disabled", "true");
    expect(seat).not.toBeDisabled();
  });

  it("does not select a booked seat", () => {
    const onSelect = jest.fn();
    render(<Seat row="D" number={4} status="booked" onSelect={onSelect} />);

    fireEvent.click(screen.getByRole("button", { name: /booked/ }));
    expect(onSelect).not.toHaveBeenCalled();
  });

  it("selects an available seat", () => {
    const onSelect = jest.fn();
    render(<Seat row="A" number={1} status="available" onSelect={onSelect} />);

    fireEvent.click(screen.getByRole("button", { name: /available/ }));
    expect(onSelect).toHaveBeenCalledTimes(1);
  });
});
