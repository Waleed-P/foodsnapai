"use client";

import React from "react";
import { motion } from "framer-motion";
import { useRouter } from "next/navigation";

const dishesRow1 = ["apple_pie", "baby_back_ribs", "baklava", "beef_carpaccio"];
const dishesRow2 = ["beef_tartare", "beet_salad", "beignets", "bibimbap"];
const dishesRow3 = [
  "bread_pudding",
  "breakfast_burrito",
  "bruschetta",
  "caesar_salad",
];

export default function Coverage() {
  const router = useRouter();
  return (
    <section id="foods" className="py-20 bg-white px-6 md:px-16 overflow-hidden">
      <div className="max-w-7xl mx-auto flex flex-col lg:flex-row items-center justify-between gap-12">
        {/* Left Content */}
        <div className="max-w-md space-y-4 text-left">
          <span className="text-xs font-bold text-green-600 uppercase tracking-widest">
            Coverage
          </span>
          <h2 className="text-4xl font-extrabold text-neutral-950 leading-tight">
            101 dishes our AI knows by heart
          </h2>
          <p className="text-neutral-500 text-sm leading-relaxed">
            FoodSnapAI is trained to recognize 101 popular dishes from around
            the world — pizza, sushi, ramen, tacos, salads and many more.
          </p>
          <button
            onClick={() => {
              router.push("/foods");
            }}
            className="cursor-pointer mt-4 px-5 py-2.5 bg-white border border-neutral-200 text-neutral-800 text-sm font-medium rounded-xl shadow-sm hover:bg-neutral-50 transition-colors flex items-center gap-2"
          >
            See all 101 foods <span>→</span>
          </button>
        </div>

        {/* Right Animated Pill Rows */}
        <div className="w-full lg:w-1/2 flex flex-col gap-3">
          {[dishesRow1, dishesRow2, dishesRow3].map((row, rIdx) => (
            <motion.div
              key={rIdx}
              className="flex gap-3 justify-center lg:justify-start"
              initial={{ x: rIdx % 2 === 0 ? -30 : 30, opacity: 0 }}
              whileInView={{ x: 0, opacity: 1 }}
              viewport={{ once: true }}
              transition={{ duration: 0.8, ease: "easeOut" }}
            >
              {row.map((dish, dIdx) => (
                <div
                  key={dIdx}
                  className="px-6 py-3 border border-neutral-200 bg-white rounded-full text-sm font-medium text-neutral-800 shadow-sm whitespace-nowrap min-w-[110px] text-center"
                >
                  {dish}
                </div>
              ))}
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
