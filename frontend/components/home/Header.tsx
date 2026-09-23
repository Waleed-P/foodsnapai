"use client";

import { useAuth } from "@/hooks/useAuth";
import LogoutButton from "./LogoutButton";
import { logout } from "@/services/auth";
import { useRouter, usePathname } from "next/navigation";
import Link from "next/link";

export default function Header() {
  const { isAuthenticated, user } = useAuth();
  const router = useRouter();
  const pathname = usePathname();

  const handleLogoutUser = async () => {
    try {
      await logout();
      router.push("/login");
    } catch (e) {
      console.log("error on logout", e);
    }
  };

  // Helper to extract uppercase initials from the full name string
  const getInitials = (name?: string) => {
    if (!name) return "U";
    return name
      .split(" ")
      .map((n) => n[0])
      .join("")
      .toUpperCase()
      .slice(0, 2);
  };

  return (
    <header className="bg-white/80 backdrop-blur-md sticky top-0 z-40 border-b border-neutral-100">
      <div className="max-w-7xl mx-auto px-6 md:px-16 py-3.5 flex justify-between items-center">
        {/* Brand Logo Identity */}
        <Link
          href="/home"
          className="flex items-center gap-2 font-bold text-neutral-900 text-base"
        >
          FoodSnapAI
        </Link>
        {isAuthenticated && (
          <>
            {/* Center Dashboard Tab Navigation */}
            <nav className="hidden md:flex items-center gap-6">
              <Link
                href="/home"
                className={`flex items-center gap-1.5 text-sm font-semibold transition-colors ${
                  pathname === "/home" || pathname === "/"
                    ? "text-neutral-900"
                    : "text-neutral-400 hover:text-neutral-600"
                }`}
              >
                <svg
                  className="w-4 h-4"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5m-13.5-9L12 3m0 0l4.5 4.5M12 3v13.5"
                  />
                </svg>
                Analyze
              </Link>

              <Link
                href="/home/history"
                className={`flex items-center gap-1.5 text-sm font-semibold transition-colors ${
                  pathname === "/home/history"
                    ? "text-neutral-900"
                    : "text-neutral-400 hover:text-neutral-600"
                }`}
              >
                <svg
                  className="w-4 h-4"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    d="M12 6v6h4.5m4.5 0a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
                History
              </Link>
            </nav>
            {/* Right User Status Badging & Logout Controller */}
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-2">
                {/* Initials Placeholder Container Box Matching layout circles */}
                <div className="w-8 h-8 rounded-full bg-[#EAF2EA] text-green-700 flex items-center justify-center font-bold text-xs shadow-sm select-none border border-green-100">
                  {getInitials(user?.name)}
                </div>
                <span className="text-sm font-bold text-neutral-800 hidden sm:inline">
                  {user?.name || "Guest User"}
                </span>
              </div>

              <div className="border-l border-neutral-200 pl-4">
                <LogoutButton onLogout={handleLogoutUser} />
              </div>
            </div>
          </>
        )}
      </div>
    </header>
  );
}
