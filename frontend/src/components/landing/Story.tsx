"use client";

import { motion } from "framer-motion";

export default function Story() {
    return (
        <section className="relative z-10 bg-background py-24 md:py-32">
            <div className="container px-4 md:px-6">
                <div className="mb-16 text-center">
                    <motion.h2
                        className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl text-foreground"
                        initial={{ opacity: 0, y: 20 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        viewport={{ once: true }}
                    >
                        Stop Guessing. Start Knowing.
                    </motion.h2>
                    <p className="mt-4 text-muted-foreground md:text-xl">
                        Turn uncertainty into predictable revenue.
                    </p>
                </div>

                <div className="grid gap-8 md:grid-cols-3">
                    <StoryCard
                        icon="📊"
                        title="Analyst Intelligence"
                        description="Raw data transforms into actionable insights. Our AI identifies patterns invisible to the human eye."
                        delay={0.1}
                    />
                    <StoryCard
                        icon="🧠"
                        title="Strategic Formulation"
                        description="Battle-tested marketing strategies generated in seconds. Target the right audience with precision."
                        delay={0.2}
                    />
                    <StoryCard
                        icon="🎨"
                        title="Content Execution"
                        description="Production-grade creative assets generated instantly. From copy to visuals, your brand voice is preserved."
                        delay={0.3}
                    />
                </div>
            </div>
        </section>
    );
}

function StoryCard({ icon, title, description, delay }: { icon: string, title: string, description: string, delay: number }) {
    return (
        <motion.div
            className="flex flex-col items-center text-center p-6 rounded-2xl border border-border/50 bg-card/50 hover:bg-card hover:border-border transition-colors"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay, duration: 0.5 }}
        >
            <div className="mb-6 text-5xl">{icon}</div>
            <h3 className="mb-3 text-2xl font-bold text-foreground">{title}</h3>
            <p className="text-muted-foreground leading-relaxed">
                {description}
            </p>
        </motion.div>
    );
}
