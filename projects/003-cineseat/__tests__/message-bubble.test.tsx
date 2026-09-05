import { fireEvent, render, screen } from "@testing-library/react";
import type { Message } from "ai";
import { MessageBubble } from "@/components/message-bubble";

/**
 * THE most important test in this build.
 *
 * It proves the safety property of Session 5's whole chapter: a destructive
 * tool call renders, and does nothing at all, until a human clicks Confirm.
 */
const cancelCallMessage = {
  id: "m1",
  role: "assistant",
  content: "I can cancel that booking for you.",
  toolInvocations: [
    {
      state: "call",
      toolCallId: "call-1",
      toolName: "cancelBooking",
      args: { bookingId: "bk_123" },
    },
  ],
} as unknown as Message;

const searchCallMessage = {
  id: "m2",
  role: "assistant",
  content: "Here is what is playing.",
  toolInvocations: [
    {
      state: "result",
      toolCallId: "call-2",
      toolName: "searchShowtimes",
      args: { film: "Dune" },
      result: [{ film: "Dune: Part Two", seatsAvailable: 40 }],
    },
  ],
} as unknown as Message;

describe("MessageBubble", () => {
  it("never cancels a booking without confirmation", () => {
    const onApproveCancel = jest.fn();
    const onRejectCancel = jest.fn();

    render(
      <MessageBubble
        message={cancelCallMessage}
        onApproveCancel={onApproveCancel}
        onRejectCancel={onRejectCancel}
      />,
    );

    // BEFORE any click: the destructive path was never taken.
    expect(onApproveCancel).not.toHaveBeenCalled();

    fireEvent.click(screen.getByRole("button", { name: "Confirm" }));

    // Only now.
    expect(onApproveCancel).toHaveBeenCalledWith("call-1", "bk_123");
  });

  it("reports a rejection instead of silently dropping it", () => {
    const onRejectCancel = jest.fn();

    render(
      <MessageBubble
        message={cancelCallMessage}
        onApproveCancel={jest.fn()}
        onRejectCancel={onRejectCancel}
      />,
    );

    fireEvent.click(screen.getByRole("button", { name: "Keep booking" }));
    expect(onRejectCancel).toHaveBeenCalledWith("call-1");
  });

  it("does not gate read-only tools", () => {
    render(
      <MessageBubble
        message={searchCallMessage}
        onApproveCancel={jest.fn()}
        onRejectCancel={jest.fn()}
      />,
    );

    expect(screen.queryByRole("button", { name: "Confirm" })).not.toBeInTheDocument();
    expect(screen.getByText(/Checked the showtimes/)).toBeInTheDocument();
  });
});
