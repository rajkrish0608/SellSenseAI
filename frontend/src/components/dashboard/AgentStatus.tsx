import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { BrainCircuit, LineChart, Sparkles } from "lucide-react";
import api from "@/lib/api";

export default function AgentStatus() {
    const [status, setStatus] = useState<string>("idle");
    const [currentActivity, setCurrentActivity] = useState<string>("Ready to generate");

    useEffect(() => {
        const fetchStatus = async () => {
            try {
                const response = await api.get("/campaigns/active");
                if (response.data) {
                    const campaign = response.data;
                    setStatus(campaign.status);

                    // Derive activity from status
                    if (campaign.status === "processing") {
                        setCurrentActivity(`Analyzing market data for "${campaign.name}"...`);
                    } else if (campaign.status === "completed") {
                        setCurrentActivity("Campaign generation complete!");
                    } else {
                        setCurrentActivity("Ready to generate");
                    }
                }
            } catch (error) {
                console.error("Failed to fetch agent status", error);
            }
        };

        // Initial fetch
        fetchStatus();

        // Poll every 5 seconds
        const interval = setInterval(fetchStatus, 5000);
        return () => clearInterval(interval);
    }, []);

    // Map global campaign status to individual agent statuses
    const getAgentStatus = (agentName: string) => {
        if (status === "processing") return "processing";
        if (status === "completed") return "idle"; // Or 'success' if we had that visual
        return "idle";
    };

    const agents = [
        { name: "Analyst Bot", status: getAgentStatus("Analyst Bot"), icon: LineChart, color: "text-blue-500", activity: status === "processing" ? "Analyzing trends..." : "Waiting for data" },
        { name: "Strategy Bot", status: getAgentStatus("Strategy Bot"), icon: BrainCircuit, color: "text-purple-500", activity: status === "processing" ? "Developing strategy..." : "Standby" },
        { name: "Content Bot", status: getAgentStatus("Content Bot"), icon: Sparkles, color: "text-emerald-500", activity: status === "processing" ? "Drafting content..." : "Standby" },
    ];

    return (
        <div className="grid gap-4 md:grid-cols-3">
            {agents.map((agent) => (
                <motion.div
                    key={agent.name}
                    className="relative overflow-hidden rounded-xl border border-border bg-card p-4 shadow-sm"
                    whileHover={{ scale: 1.02 }}
                    transition={{ type: "spring", stiffness: 300 }}
                >
                    <div className="flex items-center gap-3">
                        <div className={`rounded-full bg-background p-2 ring-1 ring-border ${agent.color}`}>
                            <agent.icon className="h-5 w-5" />
                        </div>
                        <div>
                            <h3 className="font-medium leading-none">{agent.name}</h3>
                            <p className="text-xs text-muted-foreground mt-1 flex items-center gap-1">
                                <span className={`inline-block h-1.5 w-1.5 rounded-full ${agent.status === 'processing' ? 'bg-amber-500 animate-pulse' : 'bg-slate-500'}`} />
                                {agent.status === 'processing' ? 'Processing' : 'Standby'}
                            </p>
                        </div>
                    </div>

                    {agent.status === 'processing' && (
                        <motion.div
                            className="absolute bottom-0 left-0 h-1 bg-amber-500"
                            initial={{ width: "0%" }}
                            animate={{ width: "100%" }}
                            transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
                        />
                    )}

                    <div className="mt-3 text-xs text-muted-foreground/80 font-mono">
                        {">"} {agent.activity}
                    </div>
                </motion.div>
            ))}
        </div>
    );
}
