"use client";

import { useChat } from "ai/react";
import { MessageBubble } from "@/components/message-bubble";

export function ReelBotPanel() {
  const {
    messages,
    input,
    handleInputChange,
    handleSubmit,
    status,
    error,
    reload,
    addToolResult,
  } = useChat({
    api: "/api/reelbot",
    // Lets the conversation continue automatically after the browser sends a
    // tool result back. Without this, ReelBot goes silent after a cancel.
    maxSteps: 3,
  });

  async function approveCancel(toolCallId: string, bookingId: string) {
    try {
      const response = await fetch("/api/bookings/cancel", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ bookingId }),
      });
      const result = (await response.json()) as { ok: boolean; message: string };
      addToolResult({ toolCallId, result });
    } catch {
      addToolResult({
        toolCallId,
        result: { ok: false, message: "The cancellation request did not go through." },
      });
    }
  }

  function rejectCancel(toolCallId: string) {
    // The safe default. Nothing is cancelled, and the model is told why.
    addToolResult({
      toolCallId,
      result: { ok: false, message: "The customer declined. The booking is unchanged." },
    });
  }

  return (
    <section aria-labelledby="reelbot-heading" className="reelbot">
      <h2 id="reelbot-heading">ReelBot</h2>
      <p className="muted">
        Ask what is playing, or ask to cancel a booking by its id.
      </p>

      <div className="reelbot__log" role="log" aria-live="polite" aria-atomic="false">
        {messages.length === 0 && (
          <p className="muted">Try: &ldquo;What is playing tonight?&rdquo;</p>
        )}
        {messages.map((message) => (
          <MessageBubble
            key={message.id}
            message={message}
            onApproveCancel={approveCancel}
            onRejectCancel={rejectCancel}
          />
        ))}
        {status === "streaming" && (
          <p className="muted typing">ReelBot is typing...</p>
        )}
      </div>

      {/* Fallback behaviour, visible: partial content stays on screen and a
          Retry button appears. Slide 18, first row. */}
      {error && (
        <div className="reelbot__error" role="alert">
          <p>ReelBot stopped mid-answer. Nothing was changed.</p>
          <button type="button" className="button button--quiet" onClick={() => reload()}>
            Retry
          </button>
        </div>
      )}

      <form onSubmit={handleSubmit} className="reelbot__form">
        {/* FIXED in Section G: a placeholder is not a label. It disappears
            the moment you type, and many screen readers ignore it. */}
        <label className="visually-hidden" htmlFor="reelbot-input">
          Ask ReelBot a question
        </label>
        <input
          id="reelbot-input"
          className="reelbot__input"
          value={input}
          onChange={handleInputChange}
          placeholder="Ask ReelBot..."
          autoComplete="off"
        />
        <button type="submit" className="button" disabled={status !== "ready"}>
          Send
        </button>
      </form>
    </section>
  );
}
