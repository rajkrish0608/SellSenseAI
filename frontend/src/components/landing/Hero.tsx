"use client";

import { Canvas } from "@react-three/fiber";
import { Suspense } from "react";
import NeuralCore from "./3d/NeuralCore";
import { Button } from "@/components/ui/button";
import { motion } from "framer-motion";

export default function Hero() {
    return (
        <section className="relative min-h-screen w-full bg-black text-foreground flex items-center pt-24 pb-12 overflow-hidden">
            {/* Ambient Glow */}
            <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-cyan-500/10 rounded-full blur-[120px] pointer-events-none" />
            {/* 3D Background */}
            <div className="absolute inset-0 z-0">
                <Canvas camera={{ position: [0, 0, 2] }} dpr={[1, 1.5]}>
                    <Suspense fallback={null}>
                        <NeuralCore />
                    </Suspense>
                </Canvas>
            </div>

            {/* Content Overlay */}
            <div className="container relative z-10 mx-auto px-4 md:px-6 flex flex-col justify-center h-full">
                <div className="max-w-5xl space-y-4">
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.8, ease: "easeOut" }}
                    >
                        <h1 className="text-4xl font-extrabold tracking-tighter leading-[1.1] sm:text-5xl md:text-6xl lg:text-7xl pb-4">
                            The Intelligent <br />
                            <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary to-secondary">
                                Command Center
                            </span>
                        </h1>
                    </motion.div>

                    <motion.p
                        className="max-w-[700px] text-muted-foreground md:text-xl lg:text-lg"
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        transition={{ delay: 0.5, duration: 0.8 }}
                    >
                        SellSenseAI orchestrates your entire marketing strategy with autonomous agents.
                        Analyze, plan, and execute with Apple-level precision.
                    </motion.p>

                    <motion.div
                        className="flex flex-col gap-2 min-[400px]:flex-row"
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.8, duration: 0.5 }}
                    >
                        <Button size="lg" className="bg-primary hover:bg-primary/90 text-white">
                            Start Free Trial
                        </Button>
                        <Button variant="outline" size="lg" className="border-muted hover:bg-muted/50">
                            Watch Demo
                        </Button>
                    </motion.div>
                </div>
            </div>
        </section>
    );
}
