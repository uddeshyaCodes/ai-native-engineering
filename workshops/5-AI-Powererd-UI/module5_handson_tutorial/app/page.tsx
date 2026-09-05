import Link from "next/link";

export default function Home() {
  return (
    <div className="page">
      <div className="eyebrow">Module 5 · Live Demo</div>
      <h1>OrderMitra</h1>
      <p className="dek">
        Real-time streaming, AI-powered UI &amp; agentic interaction
        patterns one chapter per demo, in order.
      </p>
      <div className="nav-grid">
        <Link href="/counter-demo" className="nav-card">
          <div className="chapter-tag">Chapter 1 · SSE</div>
          <h3>Streaming Counter</h3>
          <p>Hand-rolled Server-Sent Events, no AI model involved.</p>
        </Link>
        <Link href="/orders-basic" className="nav-card">
          <div className="chapter-tag">Chapter 2 · Vercel AI SDK</div>
          <h3>OrderMitra Talks</h3>
          <p>useChat + streamText a real streaming chat, no tools yet.</p>
        </Link>
        <Link href="/confidence-demo" className="nav-card">
          <div className="chapter-tag">Chapter 2 · Confidence Indicator</div>
          <h3>generateObject Demo</h3>
          <p>Structured output answer, confidence, groundedInSource.</p>
        </Link>
        <Link href="/orders-search" className="nav-card">
          <div className="chapter-tag">Chapter 3 · Agentic Patterns</div>
          <h3>OrderMitra Searches</h3>
          <p>The searchOrders tool live, real Prisma data.</p>
        </Link>

        <Link href="/orders-full" className="nav-card">
          <div className="chapter-tag">Chapter 4 · Human-in-the-Loop</div>
          <h3>OrderMitra Complete</h3>
          <p>cancelOrder gated behind confirmation, plus Stop/Retry.</p>
        </Link>
      </div>
    </div>
  );
}
