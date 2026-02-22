"use client";

import { useRef } from "react";
import { motion, useScroll, useTransform } from "framer-motion";

const storySteps = [
    {
        title: "Data Fragmentation",
        desc: "Your marketing data is scattered across 12 different platforms. You are flying blind.",
        color: "from-red-500 to-orange-600",
    },
    {
        title: "The Neural Link",
        desc: "SellSenseAI connects every touchpoint. One brain. One truth.",
        color: "from-blue-500 to-cyan-400",
    },
    {
        title: "Predictive Future",
        desc: "Don't just analyze the past. Predict the future with 94% accuracy.",
        color: "from-purple-500 to-pink-500",
    }
];

export default function ScrollStory() {
    const containerRef = useRef<HTMLDivElement>(null);
    const { scrollYProgress } = useScroll({
        target: containerRef,
        offset: ["start start", "end end"],
    });

    return (
        <section ref={containerRef} className="relative h-[300vh] bg-black">
            <div className="sticky top-0 h-screen flex items-center justify-center overflow-hidden">
                {storySteps.map((step, index) => {
                    const rangeStart = index / storySteps.length;
                    const rangeEnd = (index + 1) / storySteps.length;

                    const opacity = useTransform(
                        scrollYProgress,
                        [rangeStart, rangeStart + 0.1, rangeEnd - 0.1, rangeEnd],
                        [0, 1, 1, 0]
                    );

                    const scale = useTransform(
                        scrollYProgress,
                        [rangeStart, rangeEnd],
                        [0.8, 1.2]
                    );

                    const blur = useTransform(
                        scrollYProgress,
                        [rangeStart, rangeStart + 0.1, rangeEnd - 0.1, rangeEnd],
                        [10, 0, 0, 10]
                    );

                    return (
                        <motion.div
                            key={index}
                            style={{ opacity, scale, filter: useTransform(blur, (v) => `blur(${v}px)`) }}
                            className="absolute inset-0 flex flex-col items-center justify-center text-center p-8"
                        >
                            <h2 className={`text-6xl md:text-9xl font-bold bg-clip-text text-transparent bg-gradient-to-br ${step.color} mb-8`}>
                                {step.title}
                            </h2>
                            <p className="text-xl md:text-3xl text-gray-400 max-w-3xl">
                                {step.desc}
                            </p>
                        </motion.div>
                    );
                })}
            </div>
        </section>
    );
}
