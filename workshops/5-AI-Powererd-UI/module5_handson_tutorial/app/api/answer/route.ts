// Chapter 2 · Confidence Indicator — called by fetch("/api/answer") on /confidence-demo
import { generateText, Output } from "ai";
import { groq } from "@ai-sdk/groq";
import { z } from "zod";

// Zod schema defines the JSON shape the model must return (structured output)
// .describe() hints help the model fill each field correctly
const answerSchema = z.object({
  answer: z.string().describe("A concise answer to the question"),
  confidence: z
    .enum(["high", "medium", "low"])
    .describe("How confident you are based on the context"),
  groundedInSource: z
    .boolean()
    .describe(
      "True if the answer is directly supported by the context; false otherwise"
    ),
});

export async function POST(req: Request) {
  const { context, question }: { context: string; question: string } =
    await req.json();

  // generateText + Output.object = non-streaming structured JSON (replaces generateObject in v7)
  const { output } = await generateText({
    model: groq("openai/gpt-oss-120b"),
    system:
      "Answer the question using only the provided context. " +
      "If the context does not contain enough information, say so in the answer, " +
      "set confidence to low, and set groundedInSource to false.",
    output: Output.object({ schema: answerSchema }),
    prompt: `Context:\n${context}\n\nQuestion: ${question}`,
  });

  // Client reads this as { answer, confidence, groundedInSource }
  return Response.json(output);
}
