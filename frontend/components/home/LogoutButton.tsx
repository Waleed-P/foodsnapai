'use client';
import { useAuth } from "@/hooks/useAuth";

interface LogoutButtonProps {
  onLogout?: () => void;
}

export default function LogoutButton({ onLogout }: LogoutButtonProps) {
  const { logoutUser } = useAuth();
  const handleLogout = async () => {
    // 1. Clear any local auth tokens or state here
    // localStorage.removeItem('token');
    
    // 2. Execute any passed-down logout logic (e.g., NextAuth signOut() or state reset)
    if (onLogout) {
      onLogout();
      logoutUser();
    } else {
      // Fallback redirect if no custom handler is provided
      window.location.href = '/login';
    }
  };

  return (
    <button
      onClick={handleLogout}
      className="flex items-center gap-2 px-3 py-1.5 rounded-md text-sm font-medium cursor-pointer text-slate-600 hover:text-red-600 hover:bg-red-50 focus:outline-none focus:ring-2 focus:ring-red-200 transition-all duration-200"
      aria-label="Log out of your account"
    >
      {/* Dynamic inline SVG logout icon */}
      <svg 
        xmlns="http://www.w3.org/2000/svg" 
        fill="none" 
        viewBox="0 0 24 24" 
        strokeWidth={2} 
        stroke="currentColor" 
        className="w-4 h-4"
      >
        <path 
          strokeLinecap="round" 
          strokeLinejoin="round" 
          d="M15.75 9V5.25A2.25 2.25 0 0 0 13.5 3h-6a2.25 2.25 0 0 0-2.25 2.25v13.5A2.25 2.25 0 0 0 7.5 21h6a2.25 2.25 0 0 0 2.25-2.25V15M12 9l-3 3m0 0 3 3m-3-3h12.75" 
        />
      </svg>
      <span>Logout</span>
    </button>
  );
}