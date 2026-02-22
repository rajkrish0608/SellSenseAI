"use client";

import { motion } from "framer-motion";
import { Cpu, Handshake, ShoppingCart, Activity, RefreshCw, Layers } from "lucide-react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";

const recentDeals = [
    { agent: "Google Gemini (Custom)", product: "Premium Blend", price: "₹850", status: "Closed", savings: "15%" },
    { agent: "Siri Pro Assistant", product: "Organic Beans", price: "₹1,200", status: "Negotiating", savings: "5%" },
];

export default function CommercePortal() {
    return (
        <Card className="border-cyan-500/20 bg-cyan-500/5 backdrop-blur-md">
            <CardHeader className="flex flex-row items-center justify-between pb-3 border-b border-cyan-500/10">
                <CardTitle className="text-sm font-bold flex items-center gap-2 text-cyan-400 uppercase tracking-widest">
                    <Cpu className="h-4 w-4 animate-spin-slow" />
                    Agentic Commerce: AI-to-AI Hub
                </CardTitle>
                <div className="flex gap-2">
                    <Badge variant="outline" className="text-[9px] border-cyan-500/40 text-cyan-300">RFC-822 Ready</Badge>
                </div>
            </CardHeader>
            <CardContent className="pt-5 space-y-5">
                {/* Live Negotiation Monitor */}
                <div className="space-y-3">
                    <div className="flex justify-between items-center text-[10px] text-cyan-300 font-mono">
                        <span className="flex items-center gap-1"><Activity className="h-3 w-3" /> Live Protocol Traffic</span>
                        <span className="text-cyan-500">v2.4.1 Connected</span>
                    </div>
                    <div className="h-10 w-full bg-black/40 rounded-lg flex items-center px-4 overflow-hidden border border-cyan-500/10">
                        <motion.div
                            animate={{ x: [0, -100, 0] }}
                            transition={{ duration: 10, repeat: Infinity, ease: "linear" }}
                            className="text-[9px] font-mono text-cyan-600 whitespace-nowrap"
                        >
                            GET /api/agentic/offer?q=coffee HTTP/1.1 · NEGOTIATING_DISCOUNT_15% · PROPOSAL_READY · TRANSACTION_SIGN_PENDING
                        </motion.div>
                    </div>
                </div>

                {/* Recent Deals Table */}
                <div className="space-y-3">
                    <h4 className="text-[11px] font-bold text-white flex items-center gap-2">
                        <Handshake className="h-3 w-3 text-cyan-400" /> Recent AI Closings
                    </h4>
                    <div className="space-y-2">
                        {recentDeals.map((deal, idx) => (
                            <motion.div
                                key={deal.agent}
                                initial={{ opacity: 0, scale: 0.95 }}
                                animate={{ opacity: 1, scale: 1 }}
                                transition={{ delay: idx * 0.1 }}
                                className="flex items-center justify-between p-3 rounded-xl bg-black/30 border border-white/5 group hover:border-cyan-500/30 transition-all"
                            >
                                <div className="space-y-1">
                                    <p className="text-[10px] font-bold text-white group-hover:text-cyan-300">{deal.agent}</p>
                                    <p className="text-[9px] text-muted-foreground">{deal.product} • {deal.price}</p>
                                </div>
                                <div className="text-right">
                                    <Badge className={`text-[8px] tracking-tight ${deal.status === 'Closed' ? 'bg-cyan-500/20 text-cyan-400' : 'bg-amber-500/20 text-amber-400'}`}>
                                        {deal.status}
                                    </Badge>
                                    <p className="text-[9px] text-cyan-600 mt-1">Saved User: {deal.savings}</p>
                                </div>
                            </motion.div>
                        ))}
                    </div>
                </div>

                <div className="pt-2">
                    <div className="flex justify-between text-[10px] items-end mb-1">
                        <span className="text-muted-foreground font-medium">Agent Discovery Rate</span>
                        <span className="text-cyan-400 font-bold">92%</span>
                    </div>
                    <Progress value={92} className="h-1 bg-white/5" />
                </div>
            </CardContent>
        </Card>
    );
}
