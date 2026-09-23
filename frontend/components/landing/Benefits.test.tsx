import { render, screen } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";

// Mock framer-motion
vi.mock("framer-motion", () => ({
  motion: {
    div: ({ children, ...props }: any) => (
      <div {...props}>{children}</div>
    ),
  },
}));

import Benefits from "./Benefits";

describe("Benefits", () => {
  it("renders the section heading", () => {
    render(<Benefits />);

    expect(screen.getByText("Why FoodSnapAI")).toBeInTheDocument();

    expect(
      screen.getByText("Eat smarter, every meal")
    ).toBeInTheDocument();
  });

  it("renders all benefit titles", () => {
    render(<Benefits />);

    expect(
      screen.getByText("Hit your daily goals")
    ).toBeInTheDocument();

    expect(
      screen.getByText("Build healthier habits")
    ).toBeInTheDocument();

    expect(
      screen.getByText("Track without effort")
    ).toBeInTheDocument();
  });

  it("renders all benefit descriptions", () => {
    render(<Benefits />);

    expect(
      screen.getByText(/Make sure every plate gets you closer/i)
    ).toBeInTheDocument();

    expect(
      screen.getByText(/Spot patterns in what you eat/i)
    ).toBeInTheDocument();

    expect(
      screen.getByText(/No manual logging. Just a photo/i)
    ).toBeInTheDocument();
  });

  it("renders all three benefit cards", () => {
    render(<Benefits />);

    expect(screen.getAllByRole("heading", { level: 3 })).toHaveLength(3);
  });
});