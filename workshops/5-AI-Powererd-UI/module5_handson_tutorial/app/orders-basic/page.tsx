"use client";

import { useState } from "react";
import Link from "next/link";
import { useChat } from "@ai-sdk/react";
import { DefaultChatTransport } from "ai";
import { ChatMarkdown } from "@/components/chat-markdown";

export default function OrdersBasicPage() {
  const { messages, sendMessage, status } = useChat({
    transport: new DefaultChatTransport({ api: "/api/ordermitra-basic" }),
    throttle: 50,
  });
  const [input, setInput] = useState("");

  const submit = (e: React.FormEvent) => {
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
      <div className="eyebrow">Chapter 2 · Vercel AI SDK</div>
      <h1>OrderMitra Talks</h1>
      <p className="dek">
        streamText on the server, useChat on the client. No tools yet OrderMitra can only talk.
      </p>

      <div className="ordermitra-panel">
        {messages.map((m) => (
          <div key={m.id} className={`bubble bubble-${m.role}`}>
            {m.parts.map((part, i) =>
              part.type === "text" ? (
                <ChatMarkdown key={i} text={part.text} />
              ) : null
            )}
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
          placeholder="Ask OrderMitra something…"
          disabled={status !== "ready"}
        />
        <button type="submit" disabled={status !== "ready"}>
          Send
        </button>
      </form>
    </div>
  );
}
