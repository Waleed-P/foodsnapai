"use client";

import { useRouter } from "next/navigation";

export default function Navbar() {
  const router = useRouter()
  return (
    <nav className="w-full h-16 bg-[#F9FBF9] flex items-center justify-between px-6 md:px-16 border-b border-neutral-100">
      <div className="flex items-center gap-2 font-bold text-neutral-900 text-lg">
        FoodSnapAI
      </div>

      <div className="hidden md:flex items-center gap-8 text-sm font-medium text-neutral-600">
        <a href="#howitworks" className="hover:text-neutral-900 transition-colors">
          How it works
        </a>
        <a href="#benefits" className="hover:text-neutral-900 transition-colors">
          Benefits
        </a>
        <a href="#foods" className="hover:text-neutral-900 transition-colors">
          Foods
        </a>
      </div>

      <div className="flex items-center gap-4 text-sm font-medium">
          <button onClick={()=>{router.push("/login")}} className="text-neutral-600 cursor-pointer hover:text-neutral-900 transition-colors flex items-center gap-1.5">
            <span>→]</span> Login
          </button>
          <button onClick={()=>{router.push("/register")}} className="px-4 py-2 cursor-pointer bg-linear-to-r from-green-700/90 to-amber-600/90 text-white rounded-lg shadow-sm hover:opacity-95 transition-opacity">
            Take a Bite
          </button>
      </div>
    </nav>
  );
}
