import { render, screen } from "@testing-library/react";
import { ReelBotPanel } from "@/components/reelbot-panel";

// Mock the SDK hook so this test never touches the network - and therefore
// never spends a Groq token. Same shape as Session 6's jest.mock("ai").
jest.mock("ai/react", () => ({
  useChat: () => ({
    messages: [
      { id: "1", role: "assistant", content: "3 showtimes found." },
    ],
    input: "",
    handleInputChange: jest.fn(),
    handleSubmit: jest.fn(),
    status: "ready",
    error: undefined,
    reload: jest.fn(),
    addToolResult: jest.fn(),
  }),
}));

describe("ReelBotPanel", () => {
  it("renders the assistant reply", () => {
    render(<ReelBotPanel />);
    expect(screen.getByText("3 showtimes found.")).toBeInTheDocument();
  });

  it("puts the transcript in a live region", () => {
    render(<ReelBotPanel />);
    expect(screen.getByRole("log")).toHaveAttribute("aria-live", "polite");
  });
});
