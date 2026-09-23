"use client";

import { useState } from "react";
import Header from "@/components/home/Header";
import foodItemsData from "@/data/food_items.json";

export default function SupportedFoodsPage() {
  const [searchQuery, setSearchQuery] = useState("");
  const data = foodItemsData as any;

  const allFoods: string[] = Array.isArray(data) ? data : data?.foods || [];

  const filteredFoods = allFoods.filter((food) =>
    food.toLowerCase().includes(searchQuery.toLowerCase()),
  );

  return (
    <div className="bg-[#F9FBF9] text-neutral-800 min-h-screen font-sans antialiased">
      <Header />

      <main className="max-w-7xl mx-auto px-6 md:px-16 py-12 space-y-8">
        <section className="text-left space-y-2">
          <h1 className="text-4xl font-extrabold text-neutral-950 tracking-tight">
            101 supported foods
          </h1>
          <p className="text-neutral-500 text-base font-medium">
            These are the dishes our AI model is trained to recognize.
          </p>
        </section>

        <div className="relative max-w-7xl w-full bg-white rounded-2xl border border-neutral-100/80 shadow-sm flex items-center px-4 py-3.5 focus-within:border-green-500/50 transition-colors">
          <span className="text-neutral-400 mr-3 shrink-0">
            <svg
              className="w-5 h-5"
              fill="none"
              stroke="currentColor"
              strokeWidth="2.5"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
              />
            </svg>
          </span>

          <input
            type="text"
            placeholder="Search dishes..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full bg-transparent outline-none text-neutral-800 text-base placeholder-neutral-400 font-medium"
          />

          <div className="text-xs font-bold text-neutral-400 select-none bg-neutral-50 px-2.5 py-1.5 rounded-lg border border-neutral-100 shrink-0 ml-2">
            {filteredFoods.length} / {allFoods.length}
          </div>
        </div>

        {filteredFoods.length === 0 ? (
          <div className="text-center py-16 bg-white border border-neutral-100/70 rounded-[2rem] p-8">
            <span className="text-2xl">🔍</span>
            <p className="text-neutral-500 font-semibold mt-2">
              No matching dishes found
            </p>
            <p className="text-xs text-neutral-400 mt-0.5">
              Try searching with a different keyword format.
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
            {filteredFoods.map((food, index) => (
              <div
                key={index}
                className="bg-white border border-neutral-100/80 rounded-xl px-5 py-3.5 text-left text-sm font-bold text-neutral-800 shadow-sm hover:border-neutral-200 transition-all cursor-default select-all truncate capitalize"
              >
                {food}
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}
