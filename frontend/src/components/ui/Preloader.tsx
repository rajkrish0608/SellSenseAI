"use client";

import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";

const terminalLines = [
    "Initializing SellSenseAI Core...",
    "Loading Neural Architectures...",
    "Optimizing Predictive Models...",
    "Establishing Secure Connection...",
    "Access Granted."
];

export default function Preloader() {
    const [index, setIndex] = useState(0);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // Step through the lines
        if (index < terminalLines.length - 1) {
            const timeout = setTimeout(() => {
                setIndex((prev) => prev + 1);
            }, 500);
            return () => clearTimeout(timeout);
        } else {
            // Finished text, wait then dismiss
            const timeout = setTimeout(() => {
                setLoading(false);
            }, 1000);
            return () => clearTimeout(timeout);
        }
    }, [index]);

    // Failsafe: Force dismiss after 5 seconds no matter what
    useEffect(() => {
        const failsafe = setTimeout(() => {
            setLoading(false);
        }, 5000);
        return () => clearTimeout(failsafe);
    }, []);

    return (
        <AnimatePresence>
            {loading && (
                <motion.div
                    className="fixed inset-0 z-50 flex items-center justify-center bg-black text-cyan-500 font-mono text-sm"
                    exit={{ opacity: 0, y: -20 }}
                    transition={{ duration: 0.5, ease: "easeInOut" }}
                >
                    <div className="w-80 space-y-2">
                        {terminalLines.map((line, i) => (
                            <motion.div
                                key={i}
                                initial={{ opacity: 0, x: -10 }}
                                animate={{ opacity: i <= index ? 1 : 0, x: i <= index ? 0 : -10 }}
                                className="flex items-center gap-2"
                            >
                                <span className="text-blue-600">➜</span> {line}
                            </motion.div>
                        ))}

                        <motion.div
                            className="h-1 bg-cyan-900 mt-4 rounded-full overflow-hidden"
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                        >
                            <motion.div
                                className="h-full bg-cyan-400"
                                initial={{ width: "0%" }}
                                animate={{ width: `${((index + 1) / terminalLines.length) * 100}%` }}
                            />
                        </motion.div>
                    </div>
                </motion.div>
            )}
        </AnimatePresence>
    );
}
