import {
  simulateReadableStream,
  toUIMessageStream,
  createUIMessageStreamResponse,
  type TextStreamPart,
  type ToolSet,
} from "ai";

/**
 * Placeholder chat response used by not-yet-implemented API routes.
 *
 * This is NOT part of the lesson it's scaffolding so the app never
 * crashes while a route is still a TODO. Once you replace a route's TODO
 * with real streamText()/tool code, this helper is no longer used there.
 */
export function notImplementedChatResponse(message: string) {
  const chunks: TextStreamPart<ToolSet>[] = [
    { type: "start" },
    { type: "text-start", id: "todo-0" },
    { type: "text-delta", id: "todo-0", text: message },
    { type: "text-end", id: "todo-0" },
    {
      type: "finish",
      finishReason: "stop",
      rawFinishReason: undefined,
      totalUsage: {
        inputTokens: 0,
        inputTokenDetails: {
          noCacheTokens: 0,
          cacheReadTokens: 0,
          cacheWriteTokens: 0,
        },
        outputTokens: 0,
        outputTokenDetails: { textTokens: 0, reasoningTokens: 0 },
        totalTokens: 0,
      },
    },
  ];

  const stream = simulateReadableStream({
    chunks,
    initialDelayInMs: 100,
    chunkDelayInMs: 50,
  });

  return createUIMessageStreamResponse({
    stream: toUIMessageStream({ stream }),
  });
}
