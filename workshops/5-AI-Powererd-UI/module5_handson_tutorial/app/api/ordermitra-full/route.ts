// Chapter 4 · Human-in-the-Loop — called by useChat() on /orders-full
import {
  convertToModelMessages,
  createUIMessageStreamResponse,
  stepCountIs,
  streamText,
  toUIMessageStream,
  type UIMessage,
} from "ai";
import { groq } from "@ai-sdk/groq";
import { cancelOrder } from "@/lib/tools/cancel-order";
import { searchOrders } from "@/lib/tools/search-orders";

const tools = { searchOrders, cancelOrder };

export async function POST(req: Request) {
  const { messages }: { messages: UIMessage[] } = await req.json();

  const result = streamText({
    model: groq("openai/gpt-oss-120b"),
    system:
      "You are OrderMitra, a friendly assistant for an Indian festive goods store. " +
      "When users ask about orders, call searchOrders first to look up real data. " +
      "When they ask to cancel an order, search if needed to find the correct order ID, " +
      "then call cancelOrder with that ID. cancelOrder only proposes the cancellation — " +
      "a human must confirm before it runs. Never invent order IDs.",
    tools,
    // Extra steps: search → propose cancel → wait for human → summarize result
    stopWhen: stepCountIs(10),
    messages: await convertToModelMessages(messages, { tools }),
  });

  return createUIMessageStreamResponse({
    stream: toUIMessageStream({ stream: result.stream, tools }),
  });
}
