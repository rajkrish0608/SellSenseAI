"use client";

import { motion } from "framer-motion";
import { UserCheck, Sparkles, ShieldCheck, Heart, UserPlus } from "lucide-react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";

const ambassadors = [
    {
        id: "persona_1",
        name: "Sarah",
        vibe: "Professional & Polished",
        description: "Authoritative but friendly. Perfect for luxury or B2B.",
        avatar: "https://api.dicebear.com/7.x/avataaars/svg?seed=sarah",
        selected: true
    },
    {
        id: "persona_2",
        name: "Leo",
        vibe: "High Energy & Gen Z",
        description: "Vibrant and enthusiastic. Perfect for cafes or fashion.",
        avatar: "https://api.dicebear.com/7.x/avataaars/svg?seed=leo",
        selected: false
    }
];

export default function AmbassadorGallery() {
    return (
        <Card className="border-primary/20 bg-primary/5">
            <CardHeader className="flex flex-row items-center justify-between pb-4 border-b border-primary/10">
                <CardTitle className="text-sm font-bold flex items-center gap-2 uppercase tracking-wider">
                    <UserCheck className="h-4 w-4 text-primary" />
                    AI Brand Ambassador
                </CardTitle>
                <Badge variant="outline" className="text-[10px] border-primary/50 text-primary">God Mode Phase 2</Badge>
            </CardHeader>
            <CardContent className="pt-6 space-y-4">
                <p className="text-xs text-muted-foreground leading-relaxed italic">
                    "Every video generated will now feature your selected ambassador to build 10x higher brand recall."
                </p>
                <div className="grid gap-4">
                    {ambassadors.map((amb, idx) => (
                        <motion.div
                            key={amb.id}
                            initial={{ opacity: 0, x: -10 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ delay: idx * 0.1 }}
                            className={`relative rounded-xl border border-white/10 p-4 transition-all hover:border-primary/30 cursor-pointer ${amb.selected ? 'bg-primary/10 border-primary/40 ring-1 ring-primary/20' : 'bg-black/20'}`}
                        >
                            <div className="flex items-center gap-4">
                                <div className="h-12 w-12 rounded-full border-2 border-primary/30 overflow-hidden bg-muted">
                                    <img src={amb.avatar} alt={amb.name} className="h-full w-full object-cover" />
                                </div>
                                <div className="flex-1">
                                    <div className="flex items-center justify-between">
                                        <h4 className="text-sm font-bold">{amb.name}</h4>
                                        {amb.selected && <Badge className="text-[8px] bg-primary text-black font-bold h-4">Active</Badge>}
                                    </div>
                                    <p className="text-[10px] font-medium text-primary mt-0.5">{amb.vibe}</p>
                                    <p className="text-[9px] text-muted-foreground mt-1">{amb.description}</p>
                                </div>
                            </div>
                            {amb.selected && (
                                <div className="absolute -top-2 -right-2 p-1 rounded-full bg-primary text-black">
                                    <ShieldCheck className="h-3 w-3" />
                                </div>
                            )}
                        </motion.div>
                    ))}
                    <Button variant="outline" className="w-full border-dashed border-white/20 text-[10px] gap-2 h-9 text-muted-foreground hover:text-white">
                        <UserPlus className="h-3 w-3" />
                        Train Your Digital Twin (Custom LoRA)
                    </Button>
                </div>
            </CardContent>
        </Card>
    );
}
