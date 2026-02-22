"use client";

import { motion } from "framer-motion";
import { STAGGER } from "@/lib/motion";
import { cn } from "@/lib/utils";

interface PageContainerProps {
    children: React.ReactNode;
    className?: string;
    title?: string;
    description?: string;
}

export default function PageContainer({ children, className, title, description }: PageContainerProps) {
    return (
        <motion.div
            variants={STAGGER.container}
            initial="hidden"
            animate="show"
            className={cn("flex-1 space-y-4 p-8 pt-6", className)}
        >
            {(title || description) && (
                <motion.div variants={STAGGER.item} className="flex items-center justify-between space-y-2 mb-6">
                    <div>
                        {title && <h2 className="text-3xl font-bold tracking-tight text-white">{title}</h2>}
                        {description && <p className="text-muted-foreground">{description}</p>}
                    </div>
                </motion.div>
            )}

            {/* We assume children are wrapped in motion components or we wrap them here if needed. 
            For granular control, children should use variants={STAGGER.item} 
        */}
            {children}
        </motion.div>
    );
}
