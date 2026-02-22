"use client";

import { motion } from "framer-motion";
import { ShieldAlert, Crosshair, Zap, Eye, ArrowRight, Target } from "lucide-react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";

const rivals = [
    { name: "Starbucks Local", threat: "High", action: "Flash Sale (30% off)", retaliation: "Launch 'Happy Hour' ad blitz", status: "Detected" },
    { name: "Blue Tokai", threat: "Med", action: "New Monsoon Blend", retaliation: "Highlight 'Arabica Superior' quality", status: "Neutralized" }
];

export default function CompetitorRadar() {
    return (
        <Card className="border-red-500/20 bg-red-500/5 backdrop-blur-sm">
            <CardHeader className="flex flex-row items-center justify-between pb-2 border-b border-red-500/10">
                <CardTitle className="text-sm font-bold flex items-center gap-2 text-red-500 uppercase tracking-tighter">
                    <Crosshair className="h-4 w-4 animate-pulse" />
                    God's Eye: Competitor Radar
                </CardTitle>
                <Badge variant="destructive" className="bg-red-500 text-white animate-pulse text-[10px]">Active Tracking</Badge>
            </CardHeader>
            <CardContent className="pt-4 space-y-4">
                {rivals.map((rival, idx) => (
                    <motion.div
                        key={rival.name}
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: idx * 0.1 }}
                        className="group relative rounded-xl border border-white/10 bg-black/40 p-4 transition-all hover:border-red-500/30"
                    >
                        <div className="flex items-start justify-between">
                            <div className="space-y-1">
                                <h4 className="flex items-center gap-2 text-sm font-bold">
                                    {rival.name}
                                    <Badge variant="outline" className={`text-[8px] h-4 ${rival.threat === 'High' ? 'border-red-500 text-red-400' : 'border-amber-500 text-amber-400'}`}>
                                        {rival.threat} Threat
                                    </Badge>
                                </h4>
                                <p className="text-xs text-muted-foreground flex items-center gap-1 italic">
                                    <Zap className="h-3 w-3 text-amber-500" />
                                    {rival.action}
                                </p>
                            </div>
                            <Badge variant="outline" className="text-[9px] uppercase font-mono tracking-widest bg-red-500/10 border-red-500/20 text-red-400">
                                {rival.status}
                            </Badge>
                        </div>

                        <div className="mt-4 flex items-center justify-between rounded-lg bg-red-500/10 p-2 ring-1 ring-inset ring-red-500/20">
                            <div className="flex items-center gap-2">
                                <Target className="h-3 w-3 text-red-500" />
                                <span className="text-[10px] font-bold text-red-200">Retaliation: {rival.retaliation}</span>
                            </div>
                            <Button size="sm" variant="ghost" className="h-6 gap-1 px-2 text-[8px] font-bold text-red-400 hover:text-red-300 hover:bg-red-500/20">
                                Deploy <ArrowRight className="h-2 w-2" />
                            </Button>
                        </div>
                    </motion.div>
                ))}
            </CardContent>
        </Card>
    );
}
