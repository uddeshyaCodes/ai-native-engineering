// Chapter 2 · Vercel AI SDK — called by useChat() on /orders-basic
import {
  convertToModelMessages,
  createUIMessageStreamResponse,
  streamText,
  toUIMessageStream,
  type UIMessage,
} from "ai";
import { groq } from "@ai-sdk/groq";

export async function POST(req: Request) {
  // useChat (DefaultChatTransport) POSTs the full conversation as UIMessage[]
  const { messages }: { messages: UIMessage[] } = await req.json();

  // streamText calls the LLM and streams tokens back as they are generated
  const result = streamText({
    model: groq("openai/gpt-oss-120b"),
    system:
      "You are OrderMitra, a friendly assistant for an Indian festive goods store. " +
      "You can chat with customers, but you cannot look up or change orders yet. " +
      "If asked about specific orders, say that feature is coming soon.",
    // UIMessage[] (client format) → model messages (provider format)
    messages: await convertToModelMessages(messages),
  });

  // AI SDK v7: convert raw stream → UI chunks → HTTP Response for useChat
  return createUIMessageStreamResponse({
    stream: toUIMessageStream({ stream: result.stream }),
  });
}
