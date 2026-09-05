/**
 * @jest-environment node
 */
import { OFFLINE_NOTICE, offlineStreamResponse } from "@/lib/ai/offline-stream";

/** Turn the data-stream wire format back into the text the user would read. */
function readStreamedText(body: string) {
  return body
    .split("\n")
    .filter((line) => line.startsWith("0:"))
    .map((line) => JSON.parse(line.slice(2)) as string)
    .join("");
}

describe("offlineStreamResponse", () => {
  it("speaks the AI SDK data stream protocol", async () => {
    const response = offlineStreamResponse("Hello there");

    expect(response.status).toBe(200);
    expect(response.headers.get("x-vercel-ai-data-stream")).toBe("v1");

    const body = await response.text();

    // Text arrives as `0:"..."` lines; the message ends with a `d:` line.
    expect(body).toContain('0:"Hello ');
    expect(body).toContain('d:{"finishReason":"stop"');
    expect(readStreamedText(body)).toBe("Hello there");
  });

  it("streams the offline notice as recoverable text, not an error", async () => {
    const body = await offlineStreamResponse(OFFLINE_NOTICE).text();

    // Note the reassembly: each word is its own chunk on the wire, which is
    // exactly why the panel shows text appearing a word at a time.
    expect(readStreamedText(body)).toContain("offline mode");
  });
});
