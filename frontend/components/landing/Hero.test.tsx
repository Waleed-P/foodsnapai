import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, it, expect, vi, beforeEach } from "vitest";

const pushMock = vi.fn();

// Mock Next.js router
vi.mock("next/navigation", () => ({
  useRouter: () => ({
    push: pushMock,
  }),
}));

// Mock Next.js Image
vi.mock("next/image", () => ({
  default: (props: any) => <img {...props} />,
}));

// Mock Framer Motion
vi.mock("framer-motion", () => ({
  motion: {
    div: ({ children, ...props }: any) => (
      <div {...props}>{children}</div>
    ),
  },
}));

import Hero from "./Hero";

describe("Hero", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("renders the main heading", () => {
    render(<Hero />);

    expect(screen.getByText(/Snap your food/i)).toBeInTheDocument();
    expect(screen.getByText(/Know what's in it/i)).toBeInTheDocument();
  });

  it("renders the description", () => {
    render(<Hero />);

    expect(
      screen.getByText(/FoodSnapAI identifies your meal/i)
    ).toBeInTheDocument();
  });

  it("renders both buttons", () => {
    render(<Hero />);

    expect(
      screen.getByRole("button", { name: /take a bite/i })
    ).toBeInTheDocument();

    expect(
      screen.getByRole("button", { name: /see how it works/i })
    ).toBeInTheDocument();
  });

  it("navigates to register when Take a Bite is clicked", async () => {
    const user = userEvent.setup();

    render(<Hero />);

    await user.click(
      screen.getByRole("button", {
        name: /take a bite/i,
      })
    );

    expect(pushMock).toHaveBeenCalledWith("/register");
  });

  it("renders statistics", () => {
    render(<Hero />);

    expect(screen.getByText("101")).toBeInTheDocument();
    expect(screen.getByText("~2s")).toBeInTheDocument();
    expect(screen.getByText("6+")).toBeInTheDocument();
  });

  it("renders hero image", () => {
    render(<Hero />);

    expect(
      screen.getByAltText("Pizza FoodSnapAI Analysis")
    ).toBeInTheDocument();
  });

  it("renders AI prediction badge", () => {
    render(<Hero />);

    expect(screen.getByText(/Pizza - 98%/i)).toBeInTheDocument();
  });
});