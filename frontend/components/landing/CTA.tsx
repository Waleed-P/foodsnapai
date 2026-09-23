"use client";

import { motion } from "framer-motion";
import { useRouter } from "next/navigation";

export default function CTA() {
  const router = useRouter()
  return (
    <section className="py-16 bg-white px-6 md:px-16 flex justify-center">
      <motion.div
        className="w-full max-w-5xl rounded-3xl bg-linear-to-r from-green-600 to-amber-500 text-white p-12 text-center relative overflow-hidden shadow-xl"
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        transition={{ duration: 0.6 }}
      >
        <div className="relative z-10 flex flex-col items-center max-w-md mx-auto space-y-6">
          <div className="text-3xl">📷</div>
          <h2 className="text-3xl md:text-4xl font-bold tracking-tight">
            Ready to take a bite?
          </h2>
          <p className="text-white/80 text-sm font-medium">
            Join FoodSnapAI and turn every meal into insight.
          </p>
            <button onClick={()=>{router.push("/login")}} className="cursor-pointer px-6 py-3 bg-white text-neutral-900 text-sm font-semibold rounded-xl shadow-md hover:bg-neutral-50 transition-colors flex items-center gap-2">
              Take a Bite <span>→</span>
            </button>
        </div>

        {/* Decorative backdrop glow */}
        <div className="absolute top-0 right-0 bottom-0 left-0 bg-[radial-gradient(circle_at_top_right,rgba(255,255,255,0.15),transparent_50%)]" />
      </motion.div>
    </section>
  );
}
