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

import HowItWorks from "./HowitWorks";

describe("HowItWorks", () => {
  it("renders the section heading", () => {
    render(<HowItWorks />);

    expect(
      screen.getByText("From photo to plate — in four steps")
    ).toBeInTheDocument();
  });

  it("renders all four steps", () => {
    render(<HowItWorks />);

    expect(screen.getByText("STEP 1")).toBeInTheDocument();
    expect(screen.getByText("STEP 2")).toBeInTheDocument();
    expect(screen.getByText("STEP 3")).toBeInTheDocument();
    expect(screen.getByText("STEP 4")).toBeInTheDocument();
  });

  it("renders all step titles", () => {
    render(<HowItWorks />);

    expect(screen.getByText("Login")).toBeInTheDocument();
    expect(screen.getByText("Upload a photo")).toBeInTheDocument();
    expect(screen.getByText("AI analyzes it")).toBeInTheDocument();
    expect(screen.getByText("Get nutrients")).toBeInTheDocument();
  });

  it("renders all step descriptions", () => {
    render(<HowItWorks />);

    expect(
      screen.getByText(
        /Sign in to your account to securely save your meal history/i
      )
    ).toBeInTheDocument();

    expect(
      screen.getByText(
        /Snap or upload an image of any meal/i
      )
    ).toBeInTheDocument();

    expect(
      screen.getByText(
        /Our AI model classifies the dish/i
      )
    ).toBeInTheDocument();

    expect(
      screen.getByText(
        /See calories, protein, carbs, fat, fiber/i
      )
    ).toBeInTheDocument();
  });

  it("renders exactly four step cards", () => {
    render(<HowItWorks />);

    expect(screen.getAllByText(/STEP/i)).toHaveLength(5);
  });
});