"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

export default function CounterDemo() {
  const [numbers, setNumbers] = useState<string[]>([]);

  useEffect(() => {
    const source = new EventSource("/api/counter");
    source.onmessage = (event) => {
      console.log(event);
      setNumbers((prev) => [...prev, event.data]);
    };
    return () => source.close();
  }, []);

  return (
    <div className="page">
      <Link href="/" className="back">
        Back
      </Link>
      <div className="eyebrow">Chapter 1 · SSE</div>
      <h1>Streaming Counter</h1>
      <p className="dek">
        No AI model involved just a hand-rolled ReadableStream, counting
        1 to 5, one number per second.
      </p>

      <div className="ordermitra-panel counter-list">
        {numbers.length === 0 && (
          <p className="typing-indicator">Connecting…</p>
        )}
        {numbers.map((n, i) => (
          <p key={i}>{n}</p>
        ))}
      </div>
    </div>
  );
}
