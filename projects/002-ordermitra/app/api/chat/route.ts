import { groq } from "@ai-sdk/groq";
import { streamText, tool } from "ai";
import { z } from "zod";
import { searchOrders } from "@/lib/tools/search-orders";

export const maxDuration = 30;

export async function POST(req: Request) {
  if (!process.env.GROQ_API_KEY) {
    return new Response(
      "Missing GROQ_API_KEY. Add it to .env.local and restart npm run dev.",
      { status: 500 },
    );
  }

  const { messages } = await req.json();

  const result = streamText({
    model: groq("openai/gpt-oss-120b"),
    system:
      "You are OrderMitra, an assistant for a small Indian retail shop. " +
      "Use the searchOrders tool to answer questions about orders. " +
      "Never invent an order that the tool did not return. " +
      "Format replies in GitHub-flavored Markdown: use headings, bold, " +
      "bullet lists, and tables when showing order details.",
    messages,
    maxSteps: 5,
    tools: {
      searchOrders: tool({
        description: searchOrders.description,
        parameters: z.object({
          customerName: z.string().nullish(),
          status: z
            .enum(["placed", "packed", "shipped", "delivered"])
            .nullish(),
        }),
        execute: async (input) =>
          searchOrders.execute({
            customerName: input.customerName ?? undefined,
            status: input.status ?? undefined,
          }),
      }),
    },
  });

  return result.toDataStreamResponse({
    getErrorMessage: (error) => {
      console.error("[/api/chat]", error);
      return error instanceof Error ? error.message : "An error occurred.";
    },
  });
}
