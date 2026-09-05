/**
 * ReelBot's fallback behaviour (slide 17-18).
 *
 * When GROQ_API_KEY is missing or Groq itself fails, we do NOT return a 500
 * and leave the chat panel spinning. We return a real, well-formed stream
 * that says what happened. Fail loudly and safely.
 *
 * The wire format below is the Vercel AI SDK v4 data stream protocol:
 *   0:"some text"\n        -> a text chunk
 *   d:{"finishReason":...} -> the message is done
 * `useChat` on the client cannot tell the difference between this and Groq.
 */
export function offlineStreamResponse(text: string): Response {
  const encoder = new TextEncoder();
  const chunks = text.match(/\S+\s*/g) ?? [text];

  const stream = new ReadableStream<Uint8Array>({
    async start(controller) {
      for (const chunk of chunks) {
        controller.enqueue(encoder.encode(`0:${JSON.stringify(chunk)}\n`));
        await new Promise((resolve) => setTimeout(resolve, 25));
      }
      controller.enqueue(
        encoder.encode(
          `d:${JSON.stringify({
            finishReason: "stop",
            usage: { promptTokens: 0, completionTokens: 0 },
          })}\n`,
        ),
      );
      controller.close();
    },
  });

  return new Response(stream, {
    status: 200,
    headers: {
      "Content-Type": "text/plain; charset=utf-8",
      "x-vercel-ai-data-stream": "v1",
    },
  });
}

export const OFFLINE_NOTICE =
  "ReelBot is in offline mode - no GROQ_API_KEY is set, so I am replying " +
  "from a script instead of a model. Everything else on this page still " +
  "works: browse showtimes, pick a seat, book it. Add a key to .env.local " +
  "and restart the dev server to bring me online.";

export const ERROR_NOTICE =
  "ReelBot could not reach Groq just now. Nothing was changed. Try again in " +
  "a moment, or carry on booking without me - the seat map does not need me.";
