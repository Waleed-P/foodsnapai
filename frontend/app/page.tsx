import React from "react";
import Navbar from "@/components/landing/Navbar";
import Hero from "@/components/landing/Hero";
import HowItWorks from "@/components/landing/HowitWorks";
import Benefits from "@/components/landing/Benefits";
import Coverage from "@/components/landing/Coverage";
import CTA from "@/components/landing/CTA";

export default function Home() {
  return (
    <main className="min-h-screen bg-white text-neutral-900 antialiased selection:bg-green-100 selection:text-green-800">
      <Navbar />
      <Hero />
      <HowItWorks />
      <Benefits />
      <Coverage />
      <CTA />
      
      {/* Footer minimal footprint line */}
      <footer className="w-full py-8 text-center text-xs text-neutral-400 bg-white border-t border-neutral-100">
        © 2026 FoodSnapAI. Eat smart.
      </footer>
    </main>
  );
}