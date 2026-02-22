"use client";

import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { DollarSign, MousePointer2, Eye, BarChart3, TrendingUp, TrendingDown } from "lucide-react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";

interface AdMetrics {
    clicks: number;
    impressions: number;
    ctr: number;
    spend: number;
}

export default function AdPerformanceWidget({ adId }: { adId?: string }) {
    const [metrics, setMetrics] = useState<AdMetrics | null>(null);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        // Mocking metric fetch
        setTimeout(() => {
            setMetrics({
                clicks: 142,
                impressions: 4850,
                ctr: 2.9,
                spend: 12.45
            });
            setIsLoading(false);
        }, 1000);
    }, [adId]);

    if (isLoading) return <div className="h-48 w-full animate-pulse bg-muted rounded-xl" />;
    if (!metrics) return null;

    const stats = [
        { label: "Spend", value: `$${metrics.spend}`, icon: DollarSign, color: "text-blue-500" },
        { label: "CTR", value: `${metrics.ctr}%`, icon: BarChart3, color: "text-emerald-500", trend: "+0.4%" },
        { label: "Clicks", value: metrics.clicks, icon: MousePointer2, color: "text-purple-500" },
        { label: "Impressions", value: metrics.impressions, icon: Eye, color: "text-orange-500" },
    ];

    return (
        <Card className="overflow-hidden border-primary/10">
            <CardHeader className="bg-muted/30 pb-4">
                <CardTitle className="text-sm font-bold uppercase tracking-wider text-muted-foreground flex items-center justify-between">
                    Live Ad Performance
                    <span className="text-[10px] font-mono text-emerald-500 bg-emerald-500/10 px-2 py-0.5 rounded">Optimizing</span>
                </CardTitle>
            </CardHeader>
            <CardContent className="p-6">
                <div className="grid grid-cols-2 gap-4">
                    {stats.map((stat, idx) => (
                        <div key={stat.label} className="space-y-1">
                            <div className="flex items-center gap-2 text-xs text-muted-foreground">
                                <stat.icon className={`h-3 w-3 ${stat.color}`} />
                                {stat.label}
                            </div>
                            <div className="flex items-end gap-2">
                                <span className="text-xl font-bold">{stat.value}</span>
                                {stat.trend && (
                                    <span className="text-[10px] text-emerald-500 font-bold mb-1 flex items-center">
                                        <TrendingUp className="h-2 w-2 mr-0.5" />
                                        {stat.trend}
                                    </span>
                                )}
                            </div>
                        </div>
                    ))}
                </div>

                <div className="mt-6 space-y-2">
                    <div className="flex justify-between text-xs font-medium">
                        <span>A/B Test Progress (Variation B)</span>
                        <span className="text-primary">82%</span>
                    </div>
                    <Progress value={82} className="h-1.5" />
                    <p className="text-[10px] text-muted-foreground italic">
                        AI Agent: "Variation B is outperforming on CTR. Reallocating budget in 4h."
                    </p>
                </div>
            </CardContent>
        </Card>
    );
}
