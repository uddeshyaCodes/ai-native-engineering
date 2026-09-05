// Chapter 1 · SSE — called by EventSource("/api/counter") on /counter-demo
export async function GET() {
  // Declared outside ReadableStream so cancel() can clear it on disconnect
  let interval: ReturnType<typeof setInterval>;

  // ReadableStream = push bytes to the client over a long-lived HTTP connection
  const stream = new ReadableStream({
    start(controller) {
      let counter = 1;

      // SSE wire format: "data: <payload>\n\n" — the blank line ends one event
      // EventSource on the client parses this into event.data
      controller.enqueue(`data: ${counter}\n\n`);

      interval = setInterval(() => {
        counter++;
        controller.enqueue(`data: ${counter}\n\n`);

        // Loop 1 → 5 → 1 → … instead of closing the stream
        if (counter >= 5) {
          counter = 0;
        }
      }, 1000);
    },
    // Fires when the client disconnects (navigate away, tab close, source.close())
    cancel() {
      clearInterval(interval);
    },
  });

  // text/event-stream tells the browser to treat the body as Server-Sent Events
  return new Response(stream, {
    headers: {
      "Content-Type": "text/event-stream",
      "Cache-Control": "no-cache",
      Connection: "keep-alive",
    },
  });
}
