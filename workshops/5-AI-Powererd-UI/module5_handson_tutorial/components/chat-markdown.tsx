"use client";

import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

// Full markdown rendering (tables, lists, bold, etc.) via react-markdown + remark-gfm.
// This is the approach recommended in the AI SDK cookbook — useChat has no built-in renderer.
export function ChatMarkdown({ text }: { text: string }) {
  return (
    <div className="chat-prose">
      <ReactMarkdown remarkPlugins={[remarkGfm]}>{text}</ReactMarkdown>
    </div>
  );
}
