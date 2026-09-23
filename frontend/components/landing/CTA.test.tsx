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

import CTA from "./CTA";

describe("CTA", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("renders the heading", () => {
    render(<CTA />);

    expect(
      screen.getByText(/Ready to take a bite/i)
    ).toBeInTheDocument();
  });

  it("renders the description", () => {
    render(<CTA />);

    expect(
      screen.getByText(
        /Join FoodSnapAI and turn every meal into insight/i
      )
    ).toBeInTheDocument();
  });

  it("renders the Take a Bite button", () => {
    render(<CTA />);

    expect(
      screen.getByRole("button", {
        name: /take a bite/i,
      })
    ).toBeInTheDocument();
  });

  it("navigates to login when button is clicked", async () => {
    const user = userEvent.setup();

    render(<CTA />);

    await user.click(
      screen.getByRole("button", {
        name: /take a bite/i,
      })
    );

    expect(pushMock).toHaveBeenCalledWith("/login");
  });
});