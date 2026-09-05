import { render, screen } from "@testing-library/react";
import { ConfidenceBadge } from "./confidence-badge";

test("high level shows High confidence with badge-green", () => {
  render(<ConfidenceBadge level="high" />);
  const badge = screen.getByText("High confidence");
  expect(badge).toBeInTheDocument();
  expect(badge).toHaveClass("badge-green");
});

test("medium level shows Medium confidence with badge-amber", () => {
  render(<ConfidenceBadge level="medium" />);
  const badge = screen.getByText("Medium confidence");
  expect(badge).toBeInTheDocument();
  expect(badge).toHaveClass("badge-amber");
});

test("low level shows Low confidence with badge-red", () => {
  render(<ConfidenceBadge level="low" />);
  const badge = screen.getByText("Low confidence");
  expect(badge).toBeInTheDocument();
  expect(badge).toHaveClass("badge-red");
});
