"use client";

import { useState, useEffect } from "react";
import GlassHero from "@/components/landing/GlassHero";
import Navbar from "@/components/landing/Navbar";
import Problem from "@/components/landing/Problem";
import ScrollStory from "@/components/landing/ScrollStory";
import Automation from "@/components/landing/Automation";
import Preloader3D from "@/components/ui/Preloader3D";

export default function Home() {
  const [showPreloader, setShowPreloader] = useState(true);

  useEffect(() => {
    // Guaranteed cleanup of preloader after 3.5 seconds
    const timer = setTimeout(() => {
      setShowPreloader(false);
      // NUCLEAR OPTION: Force remove from DOM if React fails
      const el = document.getElementById('preloader-root');
      if (el) el.remove();
    }, 3500);
    return () => clearTimeout(timer);
  }, []);

  return (
    <main className="flex min-h-screen flex-col bg-black">
      {showPreloader && <Preloader3D />}
      <Navbar />
      <GlassHero />
      <Problem />
      <ScrollStory />
      <Automation />

      {/* Footer Placeholder */}
      <footer className="w-full py-6 md:px-8 md:py-0 border-t border-border bg-background">
        <div className="container flex flex-col items-center justify-between gap-4 md:h-24 md:flex-row">
          <p className="text-center text-sm leading-loose text-muted-foreground md:text-left">
            Built by SellSenseAI. The Future of Marketing.
          </p>
        </div>
      </footer>
    </main>
  );
}
