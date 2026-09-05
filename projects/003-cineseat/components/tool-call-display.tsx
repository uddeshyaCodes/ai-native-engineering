"use client";

import type { ToolInvocation } from "ai";

const LABELS: Record<string, string> = {
  searchShowtimes: "Checked the showtimes",
  cancelBooking: "Cancellation",
};

export function ToolCallDisplay({ invocation }: { invocation: ToolInvocation }) {
  const label = LABELS[invocation.toolName] ?? invocation.toolName;
  const done = invocation.state === "result";

  return (
    <div className="tool-call">
      <span className="tool-call__label">
        {done ? label : `${label}...`}
      </span>
      {done && (
        <details>
          <summary>What came back</summary>
          <pre>{JSON.stringify(invocation.result, null, 2)}</pre>
        </details>
      )}
    </div>
  );
}
