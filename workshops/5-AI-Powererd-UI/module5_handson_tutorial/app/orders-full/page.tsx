"use client";

import Link from "next/link";
import { useState } from "react";
import { useChat } from "@ai-sdk/react";
import { DefaultChatTransport } from "ai";
import { ChatMarkdown } from "@/components/chat-markdown";

export default function OrdersFullPage() {
  const { messages, sendMessage, status, stop, regenerate, addToolOutput } =
    useChat({
      transport: new DefaultChatTransport({ api: "/api/ordermitra-full" }),
      throttle: 50,
    });
  const [input, setInput] = useState("");

  const submit = (e: React.SubmitEvent) => {
    e.preventDefault();
    if (!input.trim()) return;
    sendMessage({ text: input });
    setInput("");
  };

  const approveCancel = async (toolCallId: string, orderId: string) => {
    const res = await fetch("/api/run-cancel-order", {
      method: "POST",
      body: JSON.stringify({ orderId }),
    });
    const output = await res.json();
    addToolOutput({ tool: "cancelOrder", toolCallId, output });
  };

  const rejectCancel = (toolCallId: string) => {
    addToolOutput({
      tool: "cancelOrder",
      toolCallId,
      output: { skipped: true, reason: "User declined the confirmation." },
    });
  };

  return (
    <div className="page">
      <Link href="/" className="back">
        Back
      </Link>
      <div className="eyebrow">Chapter 4 · Human-in-the-Loop UI</div>
      <h1>OrderMitra Complete</h1>
      <p className="dek">
        cancelOrder is gated behind a confirmation card it never runs without a
        human clicking Confirm. Try: “cancel Mr. Iyer's diya order”
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
              if (part.type === "tool-cancelOrder") {
                // Only cancelOrder gets the confirmation treatment this
                // one conditional is the whole HITL safeguard.
                if (part.state === "input-available") {
                  const input = part.input as { orderId: string };
                  return (
                    <div key={i} className="confirm-card">
                      <p>
                        Run <strong>cancelOrder</strong> with:
                      </p>
                      <pre>{JSON.stringify(input, null, 2)}</pre>
                      <div className="confirm-actions">
                        <button onClick={() => rejectCancel(part.toolCallId)}>
                          Cancel
                        </button>
                        <button
                          onClick={() =>
                            approveCancel(part.toolCallId, input.orderId)
                          }
                          autoFocus
                        >
                          Confirm
                        </button>
                      </div>
                    </div>
                  );
                }
                if (part.state === "output-available") {
                  return (
                    <div key={i} className="step-badge step-done">
                      ✓ cancelOrder complete
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

      <div className="confirm-actions" style={{ marginTop: 12 }}>
        {status === "streaming" && (
          <button onClick={() => stop()}>■ Stop generating</button>
        )}
        {status === "error" && (
          <button onClick={() => regenerate()}>Retry</button>
        )}
      </div>

      <form className="chat-form" onSubmit={submit}>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="cancel Mr. Iyer's diya order"
          disabled={status !== "ready"}
        />
        <button type="submit" disabled={status !== "ready"}>
          Send
        </button>
      </form>
    </div>
  );
}
