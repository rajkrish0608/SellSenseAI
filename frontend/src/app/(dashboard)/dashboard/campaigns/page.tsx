"use client";

import { useEffect, useState } from "react";
import api from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Plus, Play, MoreVertical, Loader2 } from "lucide-react";
import { motion } from "framer-motion";
import PageContainer from "@/components/ui/PageContainer";

interface Campaign {
    id: number;
    name: string;
    status: string;
    type: string;
    created_at: string;
    strategy_data?: string;
}

export default function CampaignsPage() {
    const [campaigns, setCampaigns] = useState<Campaign[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [isCreating, setIsCreating] = useState(false);

    const fetchCampaigns = async () => {
        try {
            const response = await api.get("/campaigns");
            setCampaigns(response.data);
        } catch (error) {
            console.error("Failed to fetch campaigns", error);
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
        fetchCampaigns();
    }, []);

    const handleCreateCampaign = async () => {
        setIsCreating(true);
        try {
            await api.post("/campaigns", {
                name: "New Campaign " + new Date().toLocaleDateString(),
                type: "Social Media"
            });
            await fetchCampaigns(); // Refresh list
        } catch (error) {
            console.error("Failed to create campaign", error);
        } finally {
            setIsCreating(false);
        }
    };

    return (
        <PageContainer title="Campaigns" description="Manage your AI-driven marketing campaigns.">
            <div className="flex flex-col gap-6">
                <div className="flex items-center justify-end">
                    <Button onClick={handleCreateCampaign} disabled={isCreating}>
                        {isCreating ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : <Plus className="mr-2 h-4 w-4" />}
                        New Campaign
                    </Button>
                </div>

                {isLoading ? (
                    <div className="flex h-64 items-center justify-center">
                        <Loader2 className="h-8 w-8 animate-spin text-primary" />
                    </div>
                ) : campaigns.length === 0 ? (
                    <div className="flex h-64 flex-col items-center justify-center rounded-lg border border-dashed p-8 text-center animate-in fade-in-50">
                        <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-primary/10">
                            <Play className="h-6 w-6 text-primary" />
                        </div>
                        <h3 className="mt-4 text-lg font-semibold">No campaigns yet</h3>
                        <p className="mb-4 mt-2 text-sm text-muted-foreground">
                            Start your first AI-powered marketing campaign today.
                        </p>
                        <Button onClick={handleCreateCampaign} variant="outline">
                            Create Campaign
                        </Button>
                    </div>
                ) : (
                    <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
                        {campaigns.map((campaign, index) => (
                            <motion.div
                                key={campaign.id}
                                initial={{ opacity: 0, y: 20 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ delay: index * 0.1 }}
                            >
                                <Card className="overflow-hidden transition-all hover:shadow-md">
                                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                                        <div className="space-y-1">
                                            <CardTitle className="text-base font-medium">
                                                {campaign.name}
                                            </CardTitle>
                                            <p className="text-xs text-muted-foreground">
                                                {new Date(campaign.created_at).toLocaleDateString()}
                                            </p>
                                        </div>
                                        <Badge
                                            variant={campaign.status === "completed" ? "default" : "secondary"}
                                            className={campaign.status === "processing" ? "animate-pulse" : ""}
                                        >
                                            {campaign.status}
                                        </Badge>
                                    </CardHeader>
                                    <CardContent>
                                        <div className="mt-4 flex items-center justify-between text-sm">
                                            <span className="text-muted-foreground">Type</span>
                                            <span className="font-medium">{campaign.type}</span>
                                        </div>
                                        <div className="mt-2 flex items-center justify-between text-sm">
                                            <span className="text-muted-foreground">Strategy</span>
                                            <span className="font-medium">
                                                {campaign.status === "completed" ? "Generated" : "Pending..."}
                                            </span>
                                        </div>
                                    </CardContent>
                                </Card>
                            </motion.div>
                        ))}
                    </div>
                )}
            </div>
        </PageContainer>
    );
}
