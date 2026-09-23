"use client";
import { motion } from "framer-motion";

const steps = [
  { step: "STEP 1", icon: "🔑", title: "Login", desc: "Sign in to your account to securely save your meal history and personal stats." },
  { step: "STEP 2", icon: "☁️", title: "Upload a photo", desc: "Snap or upload an image of any meal — homemade or restaurant-style." },
  { step: "STEP 3", icon: "🧠", title: "AI analyzes it", desc: "Our AI model classifies the dish across 101 known food categories in seconds." },
  { step: "STEP 4", icon: "📈", title: "Get nutrients", desc: "See calories, protein, carbs, fat, fiber and more — instantly." }
];

export default function HowItWorks() {
  return (
    <section id="howitworks" className="py-20 bg-white px-6 md:px-16 text-center">
      <span className="text-xs font-bold text-green-600 uppercase tracking-widest">How It Works</span>
      <h2 className="text-4xl font-extrabold text-neutral-950 mt-2 mb-4">
        From photo to plate — in four steps
      </h2>
      <p className="text-neutral-500 max-w-xl mx-auto mb-16">
        A simple, frictionless flow designed to make nutrition tracking effortless.
      </p>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 max-w-7xl mx-auto">
        {steps.map((item, idx) => (
          <motion.div
            key={idx}
            className="relative bg-white border border-neutral-100 rounded-3xl p-6 text-left shadow-sm hover:shadow-md transition-shadow"
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: "-100px" }}
            transition={{ duration: 0.5, delay: idx * 0.1 }}
          >
            <span className="absolute -top-3 left-6 bg-black text-white text-[10px] font-black px-2 py-0.5 rounded-md tracking-wider">
              {item.step}
            </span>
            <div className="w-12 h-12 rounded-xl bg-linear-to-br from-amber-400 to-amber-600 flex items-center justify-center text-xl text-white mb-4 shadow-sm">
              {item.icon}
            </div>
            <h3 className="text-lg font-bold text-neutral-900 mb-2">{item.title}</h3>
            <p className="text-neutral-500 text-sm leading-relaxed">{item.desc}</p>
          </motion.div>
        ))}
      </div>
    </section>
  );
}