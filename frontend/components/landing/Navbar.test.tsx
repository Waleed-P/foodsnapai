import { vi, describe, it, expect, beforeEach } from "vitest";
import { render, screen } from "@testing-library/react";
import Navbar from "./Navbar";
import userEvent from "@testing-library/user-event";
const pushMock = vi.fn();
vi.mock("next/navigation", () => ({
  useRouter: () => ({
    push: pushMock,
  }),
}));
describe("Landing page navbar component", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("renders FoodSnapAI text", () => {
    render(<Navbar />);
    expect(screen.getByText("FoodSnapAI")).toBeInTheDocument();
  });

  it("renders all navigation links", () => {
    render(<Navbar />);
    expect(screen.getByText("How it works")).toBeInTheDocument();
    expect(screen.getByText("Benefits")).toBeInTheDocument();
    expect(screen.getByText("Foods")).toBeInTheDocument();
  });

  it("render login button", () => {
    render(<Navbar />);
    expect(
      screen.getByRole("button", { name: /login/i }),
    ).toBeInTheDocument();
  });

  it("render take a bite button", () => {
    render(<Navbar />);
    expect(
      screen.getByRole("button", { name: /take a bite/i }),
    ).toBeInTheDocument();
  });

    it("navigates to login when Take login button is clicked", async () => {
    const user = userEvent.setup();

    render(<Navbar />);

    await user.click(screen.getByRole("button", { name: /login/i }));

    expect(pushMock).toHaveBeenCalledWith("/login");
  });

  it("navigates to register when Take a Bite is clicked", async () => {
    const user = userEvent.setup();

    render(<Navbar />);

    await user.click(screen.getByRole("button", { name: /take a bite/i }));

    expect(pushMock).toHaveBeenCalledWith("/register");
  });
});
