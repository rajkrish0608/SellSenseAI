"use client";

import { motion } from "framer-motion";
import { useEffect, useState } from "react";

export default function Problem() {
    const [count, setCount] = useState(0);

    useEffect(() => {
        // Simple counter animation when in view could be added here
        // For now, static or css animation
        const interval = setInterval(() => {
            setCount(prev => (prev < 87 ? prev + 1 : 87));
        }, 20);
        return () => clearInterval(interval);
    }, []);

    return (
        <section className="bg-black py-24 md:py-32 text-foreground">
            <div className="container px-4 md:px-6">
                <div className="grid gap-12 lg:grid-cols-2 lg:gap-16 items-center">
                    <motion.div
                        initial={{ opacity: 0, x: -50 }}
                        whileInView={{ opacity: 1, x: 0 }}
                        viewport={{ once: true }}
                        transition={{ duration: 0.8 }}
                    >
                        <h2 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl lg:text-6xl text-foreground">
                            Stop Guessing. <br />
                            <span className="text-destructive">Start Knowing.</span>
                        </h2>
                        <p className="mt-4 max-w-[600px] text-muted-foreground md:text-xl">
                            Marketing without data is just gambling.
                            The average small business wastes thousands on campaigns that never convert.
                            SellSenseAI eliminates the guesswork.
                        </p>
                    </motion.div>

                    <motion.div
                        className="flex flex-col gap-8 rounded-xl border border-white/10 bg-white/5 backdrop-blur-sm p-8 shadow-2xl hover:shadow-[0_0_30px_rgba(6,182,212,0.15)] hover:border-cyan-500/30 transition-all duration-500"
                        initial={{ opacity: 0, scale: 0.9 }}
                        whileInView={{ opacity: 1, scale: 1 }}
                        viewport={{ once: true }}
                        transition={{ duration: 0.8, delay: 0.2 }}
                    >
                        <div className="space-y-2">
                            <div className="flex items-center justify-between text-sm">
                                <span className="text-muted-foreground">Competitors (Manual)</span>
                                <span className="font-mono text-destructive">12% Success</span>
                            </div>
                            <div className="h-4 w-full overflow-hidden rounded-full bg-muted">
                                <motion.div
                                    className="h-full bg-destructive"
                                    initial={{ width: 0 }}
                                    whileInView={{ width: "12%" }}
                                    transition={{ duration: 1.5, ease: "easeOut" }}
                                />
                            </div>
                        </div>

                        <div className="space-y-2">
                            <div className="flex items-center justify-between text-sm">
                                <span className="text-muted-foreground">SellSenseAI (Data-Driven)</span>
                                <span className="font-mono text-success">87% Success</span>
                            </div>
                            <div className="h-4 w-full overflow-hidden rounded-full bg-muted">
                                <motion.div
                                    className="h-full bg-success"
                                    initial={{ width: 0 }}
                                    whileInView={{ width: "87%" }}
                                    transition={{ duration: 1.5, ease: "easeOut", delay: 0.2 }}
                                />
                            </div>
                        </div>

                        <div className="mt-4 rounded bg-background/50 p-4">
                            <p className="text-sm font-mono text-muted-foreground">
                                "87% of businesses using AI-driven insights report significant ROI improvement within the first 30 days."
                            </p>
                        </div>
                    </motion.div>
                </div>
            </div>
        </section>
    );
}
