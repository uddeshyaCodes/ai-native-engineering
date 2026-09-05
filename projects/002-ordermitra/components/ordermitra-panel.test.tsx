import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { useChat } from "ai/react";
import { OrderMitraPanel } from "./ordermitra-panel";

jest.mock("ai/react", () => ({
  useChat: jest.fn(),
}));

// react-markdown is ESM-only; Jest can't parse it. Render plain text instead.
jest.mock("./chat-markdown", () => ({
  ChatMarkdown: ({ text }: { text: string }) => <p>{text}</p>,
}));

const mockedUseChat = useChat as jest.MockedFunction<typeof useChat>;

let chat: {
  messages: { id: string; role: string; content: string }[];
  input: string;
  handleInputChange: jest.Mock;
  handleSubmit: jest.Mock;
  status: string;
  stop: jest.Mock;
  reload: jest.Mock;
  error: Error | undefined;
};

beforeEach(() => {
  chat = {
    messages: [],
    input: "",
    handleInputChange: jest.fn(),
    handleSubmit: jest.fn((event?: { preventDefault?: () => void }) => {
      event?.preventDefault?.();
    }),
    status: "ready",
    stop: jest.fn(),
    reload: jest.fn(),
    error: undefined,
  };

  mockedUseChat.mockReturnValue(chat as ReturnType<typeof useChat>);
});

test("shows empty state when there are no messages", () => {
  render(<OrderMitraPanel />);
  expect(
    screen.getByText("Ask about an order to get started."),
  ).toBeInTheDocument();
});

test("renders a user message and an assistant reply", () => {
  chat.messages = [
    { id: "1", role: "user", content: "find Mr. Iyer's orders" },
    { id: "2", role: "assistant", content: "Mr. Iyer has 2 open orders." },
  ];

  render(<OrderMitraPanel />);

  expect(screen.getByText("You")).toBeInTheDocument();
  expect(screen.getByText("find Mr. Iyer's orders")).toBeInTheDocument();
  expect(screen.getByText("Mr. Iyer has 2 open orders.")).toBeInTheDocument();
  expect(screen.getByRole("heading", { name: "OrderMitra" })).toBeInTheDocument();
});

test("shows a high-confidence badge for a clear assistant reply", () => {
  chat.messages = [
    { id: "1", role: "assistant", content: "Mr. Iyer has 2 open orders." },
  ];

  render(<OrderMitraPanel />);
  expect(screen.getByText("High confidence")).toHaveClass("badge-green");
});

test("shows typing status while streaming", () => {
  chat.status = "streaming";
  render(<OrderMitraPanel />);
  expect(screen.getByRole("status")).toHaveTextContent(
    "OrderMitra is typing…",
  );
});

test("calls handleInputChange when the user types", async () => {
  render(<OrderMitraPanel />);

  await userEvent.type(
    screen.getByLabelText("Ask a question"),
    "find orders",
  );

  expect(chat.handleInputChange).toHaveBeenCalled();
});

test("calls handleSubmit when Send is clicked with input", async () => {
  chat.input = "find Mr. Iyer's orders";
  render(<OrderMitraPanel />);

  await userEvent.click(screen.getByRole("button", { name: "Send" }));

  expect(chat.handleSubmit).toHaveBeenCalled();
});

test("disables Send when input is empty", () => {
  render(<OrderMitraPanel />);
  expect(screen.getByRole("button", { name: "Send" })).toBeDisabled();
});

test("disables the form while streaming", () => {
  chat.input = "find orders";
  chat.status = "streaming";
  render(<OrderMitraPanel />);

  expect(screen.getByLabelText("Ask a question")).toBeDisabled();
  expect(screen.getByRole("button", { name: "Send" })).toBeDisabled();
});

test("calls stop when Stop generating is clicked", async () => {
  chat.status = "streaming";
  render(<OrderMitraPanel />);

  await userEvent.click(
    screen.getByRole("button", { name: "Stop generating" }),
  );

  expect(chat.stop).toHaveBeenCalled();
});

test("calls reload when Retry is clicked", async () => {
  chat.error = new Error("network failed");
  render(<OrderMitraPanel />);

  await userEvent.click(screen.getByRole("button", { name: "Retry" }));

  expect(chat.reload).toHaveBeenCalled();
});
