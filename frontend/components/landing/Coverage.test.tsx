import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, it, expect, vi, beforeEach } from "vitest";

const pushMock = vi.fn();

vi.mock("next/navigation", () => ({
  useRouter: () => ({
    push: pushMock,
  }),
}));

vi.mock("framer-motion", () => ({
  motion: {
    div: ({ children, ...props }: any) => (
      <div {...props}>{children}</div>
    ),
  },
}));

import Coverage from "./Coverage";

describe("Coverage", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("renders the heading", () => {
    render(<Coverage />);

    expect(
      screen.getByText(/101 dishes our AI knows by heart/i)
    ).toBeInTheDocument();
  });

  it("renders the description", () => {
    render(<Coverage />);

    expect(
      screen.getByText(/FoodSnapAI is trained to recognize 101 popular dishes/i)
    ).toBeInTheDocument();
  });

  it("renders the See all 101 foods button", () => {
    render(<Coverage />);

    expect(
      screen.getByRole("button", {
        name: /see all 101 foods/i,
      })
    ).toBeInTheDocument();
  });

  it("navigates to /foods when button is clicked", async () => {
    const user = userEvent.setup();

    render(<Coverage />);

    await user.click(
      screen.getByRole("button", {
        name: /see all 101 foods/i,
      })
    );

    expect(pushMock).toHaveBeenCalledWith("/foods");
  });

  it("renders all 12 dish names", () => {
    render(<Coverage />);

    expect(screen.getByText("apple_pie")).toBeInTheDocument();
    expect(screen.getByText("baby_back_ribs")).toBeInTheDocument();
    expect(screen.getByText("baklava")).toBeInTheDocument();
    expect(screen.getByText("beef_carpaccio")).toBeInTheDocument();

    expect(screen.getByText("beef_tartare")).toBeInTheDocument();
    expect(screen.getByText("beet_salad")).toBeInTheDocument();
    expect(screen.getByText("beignets")).toBeInTheDocument();
    expect(screen.getByText("bibimbap")).toBeInTheDocument();

    expect(screen.getByText("bread_pudding")).toBeInTheDocument();
    expect(screen.getByText("breakfast_burrito")).toBeInTheDocument();
    expect(screen.getByText("bruschetta")).toBeInTheDocument();
    expect(screen.getByText("caesar_salad")).toBeInTheDocument();
  });
});