"use client";

import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { TrendingUp, Hash, Music, Zap, ArrowUpRight } from "lucide-react";
import api from "@/lib/api";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

interface Trend {
    name: string;
    type: string;
    source: string;
    growth: string;
}

export default function MarketTrends() {
    const [trends, setTrends] = useState<Trend[]>([]);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        const fetchTrends = async () => {
            try {
                const response = await api.get("/trends");
                setTrends(response.data);
            } catch (error) {
                console.error("Failed to fetch trends", error);
            } finally {
                setIsLoading(false);
            }
        };
        fetchTrends();
    }, []);

    const getTypeIcon = (type: string) => {
        switch (type) {
            case "audio": return <Music className="h-4 w-4" />;
            case "hashtag": return <Hash className="h-4 w-4" />;
            default: return <Zap className="h-4 w-4" />;
        }
    };

    return (
        <Card className="col-span-1 overflow-hidden">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
                <CardTitle className="text-lg font-bold flex items-center gap-2">
                    <TrendingUp className="h-5 w-5 text-primary" />
                    Market Pulse
                </CardTitle>
                <Badge variant="outline" className="font-mono text-[10px] uppercase">Live</Badge>
            </CardHeader>
            <CardContent className="space-y-4">
                {isLoading ? (
                    <div className="flex justify-center py-8">
                        <div className="h-6 w-6 animate-spin rounded-full border-2 border-primary border-t-transparent" />
                    </div>
                ) : (
                    trends.map((trend, idx) => (
                        <motion.div
                            key={trend.name}
                            initial={{ opacity: 0, x: -10 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ delay: idx * 0.1 }}
                            className="flex items-center justify-between p-3 rounded-lg bg-muted/30 hover:bg-muted/50 transition-colors group cursor-pointer"
                        >
                            <div className="flex items-center gap-3">
                                <div className="p-2 rounded-full bg-background ring-1 ring-border group-hover:ring-primary/30 transition-all text-muted-foreground group-hover:text-primary">
                                    {getTypeIcon(trend.type)}
                                </div>
                                <div>
                                    <p className="text-sm font-medium leading-none">{trend.name}</p>
                                    <p className="text-[10px] text-muted-foreground mt-1 uppercase tracking-wider">{trend.source}</p>
                                </div>
                            </div>
                            <div className="text-right">
                                <p className="text-xs font-bold text-emerald-500 flex items-center justify-end">
                                    {trend.growth}
                                    <ArrowUpRight className="h-3 w-3" />
                                </p>
                            </div>
                        </motion.div>
                    ))
                )}
            </CardContent>
        </Card>
    );
}
