"use client";
import Image from "next/image";
import { motion } from "framer-motion";
import { useRouter } from "next/navigation";

export default function Hero() {
  const router = useRouter();
  return (
    <section className="relative min-h-[90vh] flex flex-col md:flex-row items-center justify-between px-6 md:px-16 py-12 bg-[#F9FBF9] overflow-hidden">
      {/* Left Content */}
      <motion.div
        className="max-w-xl space-y-6"
        initial={{ opacity: 0, x: -50 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 0.6 }}
      >
        <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium text-green-700 bg-green-50 border border-green-200">
          🌱 AI-powered nutrition
        </span>
        <h1 className="text-5xl md:text-6xl font-extrabold text-neutral-900 tracking-tight leading-tight">
          Snap your food. <br />
          <span className="text-transparent bg-clip-text bg-linear-to-r from-green-600 to-amber-500">
            Know what's in it.
          </span>
        </h1>
        <p className="text-neutral-600 text-lg leading-relaxed">
          FoodSnapAI identifies your meal from a single photo and breaks down
          every nutrient — so you can eat with confidence.
        </p>
        <div className="flex flex-wrap gap-4 pt-2">
            <button onClick={()=>{router.push("/register")}} className="cursor-pointer px-6 py-3 bg-linear-to-r from-green-600 to-amber-500 text-white font-medium rounded-xl shadow-md hover:opacity-95 transition-opacity flex items-center gap-2">
              Take a Bite <span>→</span>
            </button>

          <a href="#howitworks">
            <button className="cursor-pointer px-6 py-3 bg-white border border-neutral-200 text-neutral-800 font-medium rounded-xl shadow-sm hover:bg-neutral-50 transition-colors">
              See how it works
            </button>
          </a>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-3 gap-6 pt-10 border-t border-neutral-100">
          <div>
            <div className="text-3xl font-black text-neutral-900">101</div>
            <div className="text-xs text-neutral-500 mt-1">food categories</div>
          </div>
          <div>
            <div className="text-3xl font-black text-neutral-900">~2s</div>
            <div className="text-xs text-neutral-500 mt-1">
              average analysis
            </div>
          </div>
          <div>
            <div className="text-3xl font-black text-neutral-900">6+</div>
            <div className="text-xs text-neutral-500 mt-1">
              nutrients tracked
            </div>
          </div>
        </div>
      </motion.div>

      {/* Right Image Feature */}
      <motion.div
        className="relative mt-12 md:mt-0 w-full md:w-1/2 flex justify-center"
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.8, delay: 0.2 }}
      >
        <div className="relative rounded-3xl overflow-hidden shadow-2xl max-w-md w-full aspect-[3/4]">
          <Image
            src="/pizza-hero.jpg" // Add your pizza image to public folder
            alt="Pizza FoodSnapAI Analysis"
            fill
            className="object-cover"
          />
          {/* AI Tag Overlay */}
          <motion.div
            className="absolute top-4 left-4 bg-white/90 backdrop-blur-md px-3 py-1.5 rounded-full shadow-lg flex items-center gap-2 border border-white/20"
            initial={{ y: -20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.8, type: "spring" }}
          >
            <span className="text-sm">🧠</span>
            <span className="text-xs font-semibold text-neutral-800">
              Pizza - 98%
            </span>
          </motion.div>
        </div>
      </motion.div>
    </section>
  );
}
