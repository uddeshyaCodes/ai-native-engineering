"use client";

import { useState } from "react";
import Link from "next/link";

type Answer = {
  answer: string;
  confidence: "high" | "medium" | "low";
  groundedInSource: boolean;
};

const SAMPLE_CONTEXT =
  "Order #4021: Mr. Iyer, 47 brass diyas, status pending, placed 2 days ago. " +
  "Order #4022: Mr. Iyer, birthday candles, status shipped.";

export default function ConfidenceDemo() {
  const [context, setContext] = useState(SAMPLE_CONTEXT);
  const [question, setQuestion] = useState("Has Mr. Iyer's diya order shipped yet?");
  const [result, setResult] = useState<Answer | null>(null);
  const [loading, setLoading] = useState(false);

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setResult(null);
    const res = await fetch("/api/answer", {
      method: "POST",
      body: JSON.stringify({ context, question }),
    });
    const data = await res.json();
    setResult(data);
    setLoading(false);
  };

  return (
    <div className="page">
      <Link href="/" className="back">
        ← Back
      </Link>
      <div className="eyebrow">Chapter 2 · Confidence Indicator</div>
      <h1>generateObject Demo</h1>
      <p className="dek">
        Structured output the model self-reports a confidence rating and
        whether the answer is grounded in the given context.
      </p>

      <form className="confidence-form" onSubmit={submit}>
        <label>Context</label>
        <textarea value={context} onChange={(e) => setContext(e.target.value)} />
        <label>Question</label>
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
        />
        <button type="submit" disabled={loading}>
          {loading ? "Asking…" : "Ask OrderMitra"}
        </button>
      </form>

      {result && (
        <div className="confidence-result">
          <span className={`badge badge-${result.confidence}`}>
            {result.confidence} confidence
          </span>
          <p>{result.answer}</p>
          <p className="typing-indicator">
            Grounded in source: {result.groundedInSource ? "yes" : "no"}
          </p>
        </div>
      )}
    </div>
  );
}
