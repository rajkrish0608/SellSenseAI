"use client";

import { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { motion } from "framer-motion";
import {
    LayoutDashboard,
    Megaphone,
    BarChart3,
    Settings,
    ChevronLeft,
    Menu,
    BrainCircuit
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

const sidebarItems = [
    { icon: LayoutDashboard, label: "Dashboard", href: "/dashboard" },
    { icon: Megaphone, label: "Campaigns", href: "/dashboard/campaigns" },
    { icon: BarChart3, label: "Analytics", href: "/dashboard/analytics" },
    { icon: Settings, label: "Settings", href: "/dashboard/settings" },
];

export default function Sidebar() {
    const [collapsed, setCollapsed] = useState(false);
    const pathname = usePathname();

    return (
        <motion.aside
            className="sticky top-0 z-20 flex h-screen flex-col border-r border-border bg-card/50 backdrop-blur-xl"
            initial={{ width: 240 }}
            animate={{ width: collapsed ? 80 : 240 }}
            transition={{ duration: 0.3, ease: "easeInOut" }}
        >
            <div className="flex h-16 items-center justify-between px-4 py-4">
                {!collapsed && (
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        className="flex items-center gap-2 font-bold text-xl tracking-tight"
                    >
                        <BrainCircuit className="h-6 w-6 text-primary" />
                        <span>SellSenseAI</span>
                    </motion.div>
                )}
                {collapsed && (
                    <div className="mx-auto">
                        <BrainCircuit className="h-6 w-6 text-primary" />
                    </div>
                )}

                <Button
                    variant="ghost"
                    size="icon"
                    onClick={() => setCollapsed(!collapsed)}
                    className={cn("hidden md:flex", collapsed && "absolute -right-4 top-6 z-50 h-8 w-8 rounded-full border bg-background shadow-md")}
                >
                    {collapsed ? <Menu className="h-4 w-4" /> : <ChevronLeft className="h-4 w-4" />}
                </Button>
            </div>

            <nav className="flex-1 space-y-2 p-2">
                {sidebarItems.map((item) => {
                    const isActive = pathname === item.href;
                    return (
                        <Link key={item.href} href={item.href}>
                            <div
                                className={cn(
                                    "flex items-center gap-3 rounded-lg px-3 py-2.5 transition-all hover:bg-accent hover:text-accent-foreground",
                                    isActive && "bg-primary/10 text-primary shadow-[0_0_20px_rgba(37,99,235,0.15)]"
                                )}
                            >
                                <item.icon className={cn("h-5 w-5", isActive && "text-primary")} />
                                {!collapsed && (
                                    <motion.span
                                        initial={{ opacity: 0 }}
                                        animate={{ opacity: 1 }}
                                        transition={{ delay: 0.1 }}
                                    >
                                        {item.label}
                                    </motion.span>
                                )}
                            </div>
                        </Link>
                    );
                })}
            </nav>

            <div className="border-t border-border p-4">
                <div className={cn("flex items-center gap-3", collapsed && "justify-center")}>
                    <div className="h-8 w-8 rounded-full bg-gradient-to-tr from-primary to-secondary" />
                    {!collapsed && (
                        <div className="flex flex-col">
                            <span className="text-sm font-medium">Demo User</span>
                            <span className="text-xs text-muted-foreground">Pro Plan</span>
                        </div>
                    )}
                </div>
            </div>
        </motion.aside>
    );
}
