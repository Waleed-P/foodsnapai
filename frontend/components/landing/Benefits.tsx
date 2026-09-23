"use client";
import { motion } from "framer-motion";

const benefits = [
  { icon: "🛡️", title: "Hit your daily goals", desc: "Make sure every plate gets you closer to your protein, fiber and vitamin targets." },
  { icon: "🥗", title: "Build healthier habits", desc: "Spot patterns in what you eat and make small upgrades that compound over time." },
  { icon: "📉", title: "Track without effort", desc: "No manual logging. Just a photo. Your history builds itself, meal by meal." }
];

export default function Benefits() {
  return (
    <section id="benefits" className="py-20 bg-[#F9FBF9] px-6 md:px-16 text-center">
      <span className="text-xs font-bold text-green-600 uppercase tracking-widest">Why FoodSnapAI</span>
      <h2 className="text-4xl font-extrabold text-neutral-950 mt-2 mb-16">
        Eat smarter, every meal
      </h2>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto">
        {benefits.map((benefit, idx) => (
          <motion.div
            key={idx}
            className="bg-white border border-neutral-100 rounded-3xl p-8 text-left shadow-sm"
            initial={{ opacity: 0, scale: 0.95 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5, delay: idx * 0.1 }}
          >
            <div className="w-10 h-10 rounded-xl bg-green-50 text-green-700 flex items-center justify-center text-lg mb-6 border border-green-100">
              {benefit.icon}
            </div>
            <h3 className="text-xl font-bold text-neutral-900 mb-3">{benefit.title}</h3>
            <p className="text-neutral-500 text-sm leading-relaxed">{benefit.desc}</p>
          </motion.div>
        ))}
      </div>
    </section>
  );
}