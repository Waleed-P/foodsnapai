"use client";

import { createContext, useContext, useEffect, useState } from "react";
import { usePathname, useRouter } from "next/navigation";
import { getMe } from "@/services/auth";

interface User {
  id: string;
  name: string;
  email: string;
}

interface AuthContextType {
  user: User | null;
  loading: boolean;
  isAuthenticated: boolean;
  refreshUser: () => Promise<void>;
  logoutUser: () => void;
}

const AuthContext = createContext<AuthContextType | null>(null);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const pathname = usePathname();
  const router = useRouter()

  const [loading, setLoading] = useState(true);

  const refreshUser = async () => {
    try {
      const { data } = await getMe();
      setUser(data);
    } catch (error) {
      console.log(
        "🔴 AuthProvider caught interceptor failure. Cleaning up state...",
      );
      setUser(null); // Clear context state

      const publicRoutes = ["/login", "/register"];
      if (!publicRoutes.includes(pathname)) {
        setTimeout(() => {
          router.push("/login");
        }, 0);
      }
    }
  };

  useEffect(() => {
    const publicRoutes = ["/login", "/register","/","/foods"];
    if (publicRoutes.includes(pathname)) {
      setLoading(false);
    } else {
      (async () => {
        console.log(pathname);
        await refreshUser();
        setLoading(false);
      })();
    }
  }, [pathname]);

  const logoutUser = () => {
    setUser(null);
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        loading,
        isAuthenticated: !!user,
        refreshUser,
        logoutUser,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);

  if (!context) {
    throw new Error("useAuth must be used inside AuthProvider");
  }

  return context;
}
