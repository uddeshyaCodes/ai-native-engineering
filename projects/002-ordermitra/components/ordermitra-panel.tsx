"use client";

import { useChat } from "ai/react";
import { ChatMarkdown } from "./chat-markdown";
import { ConfidenceBadge, type ConfidenceLevel } from "./confidence-badge";

/**
 * Session 5's streaming chat panel.
 *
 * Everything above the "--- recovery controls ---" comment is the happy path:
 * type a question, watch a reply stream in. Everything below it is what happens
 * when the user changes their mind or the request fails.
 *
 * An AI asked to "cover sending a message and showing the reply" will test the
 * first part thoroughly and never touch the second. That is Chapter 2.
 */
export function OrderMitraPanel() {
  const {
    messages,
    input,
    handleInputChange,
    handleSubmit,
    status,
    stop,
    reload,
    error,
  } = useChat({ api: "/api/chat" });

  const isStreaming = status === "submitted" || status === "streaming";

  function confidenceFor(content: string): ConfidenceLevel {
    if (content.includes("not sure") || content.includes("could not")) return "low";
    if (content.includes("might")) return "medium";
    return "high";
  }

  return (
    <section className="panel">
      <h1>OrderMitra</h1>

      <ul className="messages">
        {messages.length === 0 && (
          <li className="empty">Ask about an order to get started.</li>
        )}

        {messages.map((message) => (
          <li key={message.id} className={`message message-${message.role}`}>
            <span className="role">
              {message.role === "user" ? "You" : "OrderMitra"}
            </span>
            {message.role === "assistant" ? (
              <ChatMarkdown text={message.content} />
            ) : (
              <p>{message.content}</p>
            )}
            {message.role === "assistant" && (
              <ConfidenceBadge level={confidenceFor(message.content)} />
            )}
          </li>
        ))}
      </ul>

      {isStreaming && <p role="status">OrderMitra is typing…</p>}

      <form onSubmit={handleSubmit}>
        <label htmlFor="question">Ask a question</label>
        <input
          id="question"
          value={input}
          onChange={handleInputChange}
          placeholder="find Mr. Iyer's orders"
          disabled={isStreaming}
        />
        <button type="submit" disabled={isStreaming || input.trim() === ""}>
          Send
        </button>
      </form>

      {/* --- recovery controls -------------------------------------------- */}
      {/* The lines below are the coverage gap Chapter 2 is built around.     */}

      {isStreaming && (
        <button type="button" onClick={() => stop()}>
          Stop generating
        </button>
      )}

      {error && (
        <div role="alert" className="error">
          <p>Something went wrong: {error.message}</p>
          <button type="button" onClick={() => reload()}>
            Retry
          </button>
        </div>
      )}
    </section>
  );
}
