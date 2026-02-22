"use client";

import { motion } from "framer-motion";

export default function Automation() {
    return (
        <section className="relative bg-black py-24 md:py-32 overflow-hidden border-t border-white/5">
            <div className="container px-4 md:px-6 relative">
                <div className="text-center mb-16">
                    <motion.h2
                        className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl text-foreground"
                        initial={{ opacity: 0, y: 20 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        viewport={{ once: true }}
                    >
                        Autonomous Workflow
                    </motion.h2>
                    <p className="mt-4 text-muted-foreground md:text-xl">
                        From raw sales data to published content in seconds.
                    </p>
                </div>

                <div className="relative flex flex-col items-center justify-center gap-8 md:flex-row md:gap-4 lg:gap-8">
                    {/* Step 1 */}
                    <StepCard icon="📊" title="Sales Data" description="Connect your POS/Excel" delay={0} />

                    <ConnectionArrow delay={0.3} />

                    {/* Step 2 */}
                    <StepCard icon="🤖" title="AI Agents" description="Analyst, Strategy, Content" delay={0.6} active />

                    <ConnectionArrow delay={0.9} />

                    {/* Step 3 */}
                    <StepCard icon="🚀" title="Campaign" description="Optimized Ads & Posts" delay={1.2} />

                    <ConnectionArrow delay={1.5} />

                    {/* Step 4 */}
                    <StepCard icon="📱" title="Socials" description="Auto-Publishing" delay={1.8} />
                </div>
            </div>
        </section>
    );
}

function StepCard({ icon, title, description, delay, active = false }: any) {
    return (
        <motion.div
            className={`flex flex-col items-center justify-center rounded-xl border p-6 text-center shadow-lg w-48 h-48 z-10 bg-white/5 backdrop-blur-sm transition-all duration-300 ${active ? 'border-cyan-500 ring-1 ring-cyan-500/50 shadow-[0_0_30px_rgba(6,182,212,0.3)]' : 'border-white/10 hover:border-cyan-500/30 hover:shadow-[0_0_20px_rgba(6,182,212,0.1)]'}`}
            initial={{ opacity: 0, scale: 0.8 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            transition={{ delay, duration: 0.5 }}
        >
            <div className="mb-2 text-4xl">{icon}</div>
            <h3 className="font-bold text-foreground">{title}</h3>
            <p className="text-xs text-muted-foreground mt-1">{description}</p>
        </motion.div>
    )
}

function ConnectionArrow({ delay }: { delay: number }) {
    return (
        <motion.div
            className="hidden md:block text-muted-foreground/30"
            initial={{ opacity: 0, x: -10 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ delay, duration: 0.5 }}
        >
            <svg width="40" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M5 12h14" />
                <path d="M12 5l7 7-7 7" />
            </svg>
        </motion.div>
    )
}
