"use client";

import { motion } from "framer-motion";
import { TrendingUp, Users, ShoppingBag, Activity, Plus } from "lucide-react";
import AgentStatus from "@/components/dashboard/AgentStatus";
import MarketTrends from "@/components/dashboard/MarketTrends";
import CompetitorRadar from "@/components/dashboard/CompetitorRadar";
import AmbassadorGallery from "@/components/dashboard/AmbassadorGallery";
import CommercePortal from "@/components/dashboard/CommercePortal";
import { Button } from "@/components/ui/button";
import { useState } from "react";
import api from "@/lib/api";
import PageContainer from "@/components/ui/PageContainer";
import { STAGGER } from "@/lib/motion";

const stats = [
    { label: "Total Revenue", value: "₹1,24,500", change: "+12.5%", icon: TrendingUp, color: "text-emerald-500" },
    { label: "Active Campaigns", value: "3", change: "2 Pending", icon: Activity, color: "text-blue-500" },
    { label: "Engagement", value: "8.4%", change: "+2.1%", icon: Users, color: "text-purple-500" },
    { label: "Products Sold", value: "145", change: "+18", icon: ShoppingBag, color: "text-orange-500" },
];

export default function DashboardPage() {
    const [isLoading, setIsLoading] = useState(false);

    const handleStartCampaign = async () => {
        setIsLoading(true);
        try {
            await api.post("/campaigns/", {
                name: "New Campaign " + new Date().toLocaleDateString(),
                type: "Social Media"
            });
            // We don't need to manually update state as AgentStatus components polls for changes
        } catch (error) {
            console.error(error);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <PageContainer title="Overview" description="Welcome back to your intelligent command center.">
            <div className="space-y-8">
                {/* Welcome Section */}
                <div className="flex items-center justify-end">
                    <Button onClick={handleStartCampaign} disabled={isLoading}>
                        <Plus className="mr-2 h-4 w-4" />
                        {isLoading ? "Starting..." : "New Campaign"}
                    </Button>
                </div>

                {/* KPI Cards */}
                <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
                    {stats.map((stat, index) => (
                        <motion.div
                            key={stat.label}
                            className="rounded-xl border border-border bg-card p-6 shadow-sm transition-all hover:shadow-md hover:border-primary/20"
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: index * 0.1 }}
                        >
                            <div className="flex items-center justify-between space-y-0 pb-2">
                                <span className="text-sm font-medium text-muted-foreground">
                                    {stat.label}
                                </span>
                                <stat.icon className={`h-4 w-4 ${stat.color}`} />
                            </div>
                            <div className="mt-2 text-2xl font-bold">{stat.value}</div>
                            <p className="mt-1 text-xs text-muted-foreground">
                                <span className="text-emerald-500 font-medium">{stat.change}</span> from last month
                            </p>
                        </motion.div>
                    ))}
                </div>

                {/* Main Content Area */}
                <div className="grid gap-6 lg:grid-cols-3">
                    <div className="lg:col-span-2 space-y-6">
                        <AgentStatus />
                        <AmbassadorGallery />
                    </div>
                    <div className="lg:col-span-1 space-y-6">
                        <CommercePortal />
                        <CompetitorRadar />
                        <MarketTrends />
                    </div>
                </div>
            </div>
        </PageContainer>
    );
}
