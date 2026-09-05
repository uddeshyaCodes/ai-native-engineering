// Chapter 3 · Agentic Patterns — called by useChat() on /orders-search
import {
  convertToModelMessages,
  createUIMessageStreamResponse,
  stepCountIs,
  streamText,
  toUIMessageStream,
  type UIMessage,
} from "ai";
import { groq } from "@ai-sdk/groq";
import { searchOrders } from "@/lib/tools/search-orders";

const tools = { searchOrders };

export async function POST(req: Request) {
  const { messages }: { messages: UIMessage[] } = await req.json();

  const result = streamText({
    model: groq("openai/gpt-oss-120b"),
    system:
      "You are OrderMitra, a friendly assistant for an Indian festive goods store. " +
      "When users ask about orders, call searchOrders to look up real data, then " +
      "summarize the results clearly. Do not invent order details.",
    tools,
    // Default stopWhen is stepCountIs(1) — too low for tool use.
    // Allow multiple steps: model calls tool → reads result → writes reply.
    stopWhen: stepCountIs(5),
    messages: await convertToModelMessages(messages, { tools }),
  });

  return createUIMessageStreamResponse({
    stream: toUIMessageStream({ stream: result.stream, tools }),
  });
}
