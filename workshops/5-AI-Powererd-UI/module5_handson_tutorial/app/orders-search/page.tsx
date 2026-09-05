"use client";

import { useState } from "react";
import Link from "next/link";
import { useChat } from "@ai-sdk/react";
import { DefaultChatTransport } from "ai";
import { ChatMarkdown } from "@/components/chat-markdown";

export default function OrdersSearchPage() {
  const { messages, sendMessage, status } = useChat({
    transport: new DefaultChatTransport({ api: "/api/ordermitra-search" }),
    throttle: 50,
  });
  const [input, setInput] = useState("");

  const submit = (e: React.SubmitEvent) => {
    e.preventDefault();
    if (!input.trim()) return;
    sendMessage({ text: input });
    setInput("");
  };

  return (
    <div className="page">
      <Link href="/" className="back">
        ← Back
      </Link>
      <div className="eyebrow">Chapter 3 · Agentic Patterns</div>
      <h1>OrderMitra Searches</h1>
      <p className="dek">
        The searchOrders tool, wired in with a maxSteps-style bound. Try: “find
        pending orders for Mr. Iyer”
      </p>

      <div className="ordermitra-panel">
        {messages.map((m) => (
          <div key={m.id} className={`bubble bubble-${m.role}`}>
            {m.parts.map((part, i) => {
              if (part.type === "text") {
                return <ChatMarkdown key={i} text={part.text} />;
              }
              if (part.type === "tool-searchOrders") {
                if (
                  part.state === "input-available" ||
                  part.state === "input-streaming"
                ) {
                  return (
                    <div key={i} className="step-badge step-pending">
                      Running searchOrders...
                    </div>
                  );
                }
                if (part.state === "output-available") {
                  return (
                    <div key={i} className="step-badge step-done">
                      ✓ searchOrders complete
                    </div>
                  );
                }
              }
              return null;
            })}
          </div>
        ))}
        {status === "streaming" && (
          <p className="typing-indicator">OrderMitra is typing…</p>
        )}
      </div>

      <form className="chat-form" onSubmit={submit}>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="find pending orders for Mr. Iyer"
          disabled={status !== "ready"}
        />
        <button type="submit" disabled={status !== "ready"}>
          Send
        </button>
      </form>
    </div>
  );
}
