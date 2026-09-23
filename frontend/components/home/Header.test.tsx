import { vi, describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import Header from "./Header";

vi.mock("@/hooks/useAuth", () => ({
  useAuth: () => ({
    isAuthenticated: false,
    user: null,
  }),
}));

vi.mock("next/navigation", () => ({
  useRouter: () => ({
    push: vi.fn(),
  }),
  usePathname: () => "/home",
}));

vi.mock("next/link", () => ({
  default: ({ children, href }: any) => <a href={href}>{children}</a>,
}));

describe("Header", () => {
  it("renders FoodSnapAI", () => {
    render(<Header />);
    expect(screen.getByText("FoodSnapAI")).toBeInTheDocument();
  });
});
