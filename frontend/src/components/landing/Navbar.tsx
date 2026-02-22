"use client";

import Link from "next/link";
import { Button } from "@/components/ui/button";
import { motion } from "framer-motion";
import MagneticButton from "@/components/ui/MagneticButton";

export default function Navbar() {
    return (
        <motion.header
            className="fixed top-0 z-50 w-full border-b border-white/10 bg-black/50 backdrop-blur-md supports-[backdrop-filter]:bg-black/20"
            initial={{ y: -100 }}
            animate={{ y: 0 }}
            transition={{ duration: 0.5 }}
        >
            <div className="container flex h-14 max-w-screen-2xl items-center">
                <div className="mr-4 hidden md:flex">
                    <Link href="/" className="mr-6 flex items-center space-x-2">
                        <span className="hidden font-bold sm:inline-block">
                            SellSenseAI
                        </span>
                    </Link>
                    <nav className="flex items-center space-x-6 text-sm font-medium">
                        <Link href="#features" className="transition-colors hover:text-foreground/80 text-foreground/60">Features</Link>
                        <Link href="#solutions" className="transition-colors hover:text-foreground/80 text-foreground/60">Solutions</Link>
                        <Link href="#pricing" className="transition-colors hover:text-foreground/80 text-foreground/60">Pricing</Link>
                    </nav>
                </div>

                <div className="flex flex-1 items-center justify-end space-x-2">
                    <nav className="flex items-center space-x-2">
                        <MagneticButton>
                            <Button variant="ghost" size="sm" asChild className="hover:bg-transparent">
                                <Link href="/login">Login</Link>
                            </Button>
                        </MagneticButton>
                        <MagneticButton>
                            <Button size="sm" asChild className="rounded-full bg-white text-black hover:bg-cyan-50">
                                <Link href="/signup">Get Started</Link>
                            </Button>
                        </MagneticButton>
                    </nav>
                </div>
            </div>
        </motion.header>
    );
}
