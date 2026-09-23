"use client";

import { useState, useEffect } from "react";
import Header from "@/components/home/Header";
import { getUserFoodHistory } from "@/services/food";
import { FoodHistoryResult, HistoryItem } from "@/types/FoodHistoryResult";
import { formatDate } from "@/utils/helpers";

export default function HistoryPage() {
  const [historyItems, setHistoryItems] = useState<HistoryItem[]>([]);
  const get_foods = async () => {
    try {
      const result: FoodHistoryResult = await getUserFoodHistory();
      setHistoryItems(result.data.history);
    } catch (e) {
      console.log(e);
    }
  };
  useEffect(() => {
    get_foods();
  }, []);

  return (
    <div className="bg-[#F9FBF9] text-neutral-800 min-h-screen font-sans antialiased">
      <Header />

      {/* Main page content container matching the exact dashboard wide gutters */}
      <main className="max-w-7xl mx-auto px-6 md:px-16 py-12 space-y-10">
        {/* Page Title Block matching image_f38142.jpg styling */}
        <section className="text-left space-y-2">
          <h1 className="text-4xl font-extrabold text-neutral-950 tracking-tight">
            Your meal history
          </h1>
          <p className="text-neutral-500 text-base font-medium">
            Every meal you've analyzed, all in one place.
          </p>
        </section>

        {/* History Cards Responsive Grid Matrix */}
        {historyItems.length === 0 ? (
          <div className="text-center py-20 bg-white border border-neutral-100 rounded-4xl p-8 max-w-xl">
            <span className="text-3xl">🍽️</span>
            <h3 className="text-lg font-bold text-neutral-800 mt-2">
              No history found
            </h3>
            <p className="text-sm text-neutral-400 mt-1">
              Meals you analyze will be displayed here.
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {historyItems.map((item) => (
              <article
                key={item.id}
                className="bg-white rounded-4xl border border-neutral-100/70 shadow-sm overflow-hidden flex flex-col group hover:shadow-md transition-shadow duration-200"
              >
                {/* Image Container Aspect Box */}
                <div className="aspect-4/3 w-full bg-neutral-100 relative overflow-hidden">
                  <img
                    src={item.image_url}
                    alt={item.name}
                    className="w-full h-full object-cover transition-transform duration-300 group-hover:scale-[1.02]"
                    loading="lazy"
                  />
                </div>

                {/* Information Content Blocks */}
                <div className="p-5 flex-1 flex flex-col justify-between space-y-4">
                  {/* Title & Date Metadata Row */}
                  <div className="flex items-center justify-between gap-2">
                    <h2 className="text-lg font-bold text-neutral-900 truncate capitalize">
                      {item.name}
                    </h2>
                    <time className="text-xs font-semibold text-neutral-400 shrink-0">
                      {formatDate(item.created_at)} <br />
                      <span className={`${item.confidence < 80 ? "text-red-600" :"text-green-600"}`}>Confidence : {item.confidence ? item.confidence : "0"}</span>
                    </time>
                  </div>
                  <div>
                    <span className={`${item.status === "completed" ? "bg-[#e5fae5]" : item.status ==="pending" ? "bg-[#faf4e5]" : "bg-[#fae7e5]"}  inline-flex items-center text-[11px] font-bold text-neutral-700 px-2.5 py-1 rounded-md`}>
                      Status : {" "}
                      <span className="ml-1">
                        {item.status}
                      </span>
                    </span>
                  </div>

                  {/* Micro Nutrients Horizontal Wrap Badges Container */}
                  <div className="flex flex-wrap gap-x-2 gap-y-1.5 pt-1">
                    <span className="inline-flex items-center text-[11px] font-bold text-neutral-700 bg-[#FAF3E5] px-2.5 py-1 rounded-md">
                      calories{" "}
                      <span className="font-extrabold ml-1">
                        {item.calories}
                      </span>
                    </span>
                    <span className="inline-flex items-center text-[11px] font-bold text-neutral-700 bg-[#EAF2EA] px-2.5 py-1 rounded-md">
                      protein{" "}
                      <span className="font-extrabold ml-1">
                        {item.protein}g
                      </span>
                    </span>
                    <span className="inline-flex items-center text-[11px] font-bold text-neutral-700 bg-[#FAF3E5] px-2.5 py-1 rounded-md">
                      carbs{" "}
                      <span className="font-extrabold ml-1">
                        {item.carbohydrates}g
                      </span>
                    </span>
                    <span className="inline-flex items-center text-[11px] font-bold text-neutral-700 bg-[#FAF3E5] px-2.5 py-1 rounded-md">
                      fat{" "}
                      <span className="font-extrabold ml-1">{item.fats}g</span>
                    </span>
                  </div>
                </div>
              </article>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}
