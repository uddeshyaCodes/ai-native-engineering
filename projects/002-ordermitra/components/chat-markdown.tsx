"use client";

import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

/** GitHub-flavored markdown for assistant replies (tables, lists, bold, code). */
export function ChatMarkdown({ text }: { text: string }) {
  return (
    <div className="chat-prose">
      <ReactMarkdown remarkPlugins={[remarkGfm]}>{text}</ReactMarkdown>
    </div>
  );
}
