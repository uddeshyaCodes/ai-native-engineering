import { groq } from "@ai-sdk/groq";
import { convertToCoreMessages, streamText, type Message } from "ai";
import { z } from "zod";
import { ERROR_NOTICE, OFFLINE_NOTICE, offlineStreamResponse } from "@/lib/ai/offline-stream";
import { cancelBookingTool } from "@/lib/tools/cancel-booking";
import { searchShowtimes } from "@/lib/tools/search-showtimes";

export const runtime = "nodejs"; // Prisma needs Node, not Edge.
export const maxDuration = 30;

/**
 * Trust boundary #1: User input -> ReelBot (slide 16).
 * The request body is untrusted. Loose, but validated - we never hand
 * `await req.json()` straight to the model.
 */
const chatRequestSchema = z.object({
  messages: z
    .array(z.object({ role: z.string(), content: z.string() }).passthrough())
    .min(1)
    .max(50),
});

const SYSTEM_PROMPT = [
  "You are ReelBot, the booking assistant for CineSeat, a cinema chain.",
  "Answer in two or three short sentences. No markdown headings.",
  "Use the searchShowtimes tool whenever the user asks what is playing.",
  "To cancel a booking, call the cancelBooking tool with the exact booking id.",
  "Never claim a booking is cancelled until the tool has returned a result -",
  "the customer has to confirm it first, and they may say no.",
  "If you do not know something, say so.",
].join(" ");

export async function POST(req: Request) {
  const body = await req.json().catch(() => null);
  const parsed = chatRequestSchema.safeParse(body);

  if (!parsed.success) {
    return new Response("Invalid chat request.", { status: 400 });
  }

  // Fallback #1: no key, no crash. The chat still streams a real answer.
  if (!process.env.GROQ_API_KEY) {
    return offlineStreamResponse(OFFLINE_NOTICE);
  }

  try {
    const result = streamText({
      model: groq(process.env.GROQ_MODEL ?? "openai/gpt-oss-20b"),
      system: SYSTEM_PROMPT,
      messages: convertToCoreMessages(parsed.data.messages as unknown as Message[]),
      tools: {
        searchShowtimes,
        cancelBooking: cancelBookingTool,
      },
      maxSteps: 3,
    });

    return result.toDataStreamResponse({
      // Never leak a provider stack trace to a customer in a cinema lobby.
      getErrorMessage: () => ERROR_NOTICE,
    });
  } catch (error) {
    // Fallback #2: Groq unreachable, rate limited, model retired.
    console.error("[reelbot] falling back:", error);
    return offlineStreamResponse(ERROR_NOTICE);
  }
}
