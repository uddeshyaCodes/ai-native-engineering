"use client";

import type { Message } from "ai";
import { ConfirmToolCall } from "@/components/confirm-tool-call";
import { ToolCallDisplay } from "@/components/tool-call-display";

export type MessageBubbleProps = {
  message: Message;
  onApproveCancel: (toolCallId: string, bookingId: string) => void;
  onRejectCancel: (toolCallId: string) => void;
};

export function MessageBubble({
  message,
  onApproveCancel,
  onRejectCancel,
}: MessageBubbleProps) {
  return (
    <div className={`bubble bubble--${message.role}`}>
      {message.content && <p className="bubble__text">{message.content}</p>}

      {message.toolInvocations?.map((invocation) => {
        // Gate by tool NAME. searchShowtimes renders normally; only the
        // destructive one gets a confirmation card. Slide 40.
        const needsConfirmation =
          invocation.toolName === "cancelBooking" && invocation.state === "call";

        if (!needsConfirmation) {
          return <ToolCallDisplay key={invocation.toolCallId} invocation={invocation} />;
        }

        const bookingId = String(
          (invocation.args as { bookingId?: unknown } | undefined)?.bookingId ?? "",
        );

        return (
          <ConfirmToolCall
            key={invocation.toolCallId}
            bookingId={bookingId}
            onApprove={() => onApproveCancel(invocation.toolCallId, bookingId)}
            onReject={() => onRejectCancel(invocation.toolCallId)}
          />
        );
      })}
    </div>
  );
}
