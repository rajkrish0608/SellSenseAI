"use client";

import { useEffect, useState, use } from "react";
import api from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Loader2, ArrowLeft, Play, MessageSquare, Image as ImageIcon, Video, Music, Settings, Zap } from "lucide-react";
import Link from "next/link";
import PageContainer from "@/components/ui/PageContainer";
import { Switch } from "@/components/ui/switch";
import AdPerformanceWidget from "@/components/dashboard/AdPerformanceWidget";

interface CampaignContentPiece {
    day: number;
    theme: string;
    instagram_caption: string;
    whatsapp_message: string;
    poster_text: string;
    video_script?: string;
    video_url?: string;
    audio_url?: string;
}

interface Campaign {
    id: number;
    name: string;
    status: string;
    type: string;
    created_at: string;
    strategy_data?: any;
}

export default function CampaignDetailPage({ params }: { params: Promise<{ id: string }> }) {
    const { id } = use(params);
    const [campaign, setCampaign] = useState<Campaign | null>(null);
    const [content, setContent] = useState<CampaignContentPiece[]>([]);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const [campRes, contRes] = await Promise.all([
                    api.get(`/campaigns/${id}`),
                    api.get(`/campaigns/${id}/content`) // Assumed endpoint for content pieces
                ]);
                setCampaign(campRes.data);
                setContent(contRes.data || []);
            } catch (error) {
                console.error("Failed to fetch campaign details", error);
            } finally {
                setIsLoading(false);
            }
        };
        fetchData();
    }, [id]);

    if (isLoading) {
        return (
            <div className="flex h-screen items-center justify-center">
                <Loader2 className="h-8 w-8 animate-spin text-primary" />
            </div>
        );
    }

    if (!campaign) return <div>Campaign not found</div>;

    return (
        <PageContainer
            title={campaign.name}
            description={`Manage the AI-generated assets for your ${campaign.type} campaign.`}
        >
            <div className="mb-6">
                <Link href="/dashboard/campaigns">
                    <Button variant="ghost" size="sm">
                        <ArrowLeft className="mr-2 h-4 w-4" />
                        Back to Campaigns
                    </Button>
                </Link>
            </div>

            <div className="grid gap-8 lg:grid-cols-12">
                {/* Left Side: Campaign Info */}
                <div className="lg:col-span-4 space-y-6">
                    <Card>
                        <CardHeader>
                            <CardTitle className="text-lg">Campaign Info</CardTitle>
                        </CardHeader>
                        <CardContent className="space-y-4 text-sm">
                            <div className="flex justify-between">
                                <span className="text-muted-foreground">Status</span>
                                <Badge variant={campaign.status === "completed" ? "default" : "secondary"}>
                                    {campaign.status}
                                </Badge>
                            </div>
                            <div className="flex justify-between">
                                <span className="text-muted-foreground">Created</span>
                                <span>{new Date(campaign.created_at).toLocaleDateString()}</span>
                            </div>

                            <hr className="my-4" />

                            <div className="space-y-3">
                                <div className="flex items-center justify-between">
                                    <div className="flex items-center gap-2">
                                        <Zap className="h-4 w-4 text-amber-500" />
                                        <span className="font-semibold">Auto-Pilot</span>
                                    </div>
                                    <Switch />
                                </div>
                                <p className="text-[10px] text-muted-foreground">
                                    AI Agent will automatically manage ad budget and scaling based on trend relevance.
                                </p>
                            </div>
                        </CardContent>
                    </Card>

                    <AdPerformanceWidget />
                </div>

                {/* Right Side: Generated Content */}
                <div className="lg:col-span-8 space-y-6">
                    <h2 className="text-xl font-bold">Daily Content Mix</h2>
                    {content.length === 0 ? (
                        <div className="rounded-xl border border-dashed p-12 text-center text-muted-foreground">
                            No content generated yet. The AI agents are working or the campaign is pending.
                        </div>
                    ) : (
                        content.map((item) => (
                            <Card key={item.day} className="overflow-hidden">
                                <CardHeader className="bg-muted/30 border-b">
                                    <div className="flex items-center justify-between">
                                        <CardTitle className="text-base flex items-center gap-2">
                                            <div className="bg-primary text-primary-foreground h-6 w-6 rounded-full flex items-center justify-center text-xs">
                                                {item.day}
                                            </div>
                                            {item.theme}
                                        </CardTitle>
                                    </div>
                                </CardHeader>
                                <CardContent className="p-0">
                                    <Tabs defaultValue="social" className="w-full">
                                        <TabsList className="w-full justify-start rounded-none border-b bg-transparent h-auto p-0">
                                            <TabsTrigger value="social" className="rounded-none border-b-2 border-transparent data-[state=active]:border-primary py-3 px-6">
                                                <MessageSquare className="h-4 w-4 mr-2" />
                                                Text
                                            </TabsTrigger>
                                            <TabsTrigger value="video" className="rounded-none border-b-2 border-transparent data-[state=active]:border-primary py-3 px-6">
                                                <Video className="h-4 w-4 mr-2" />
                                                AI Video
                                            </TabsTrigger>
                                        </TabsList>

                                        <TabsContent value="social" className="p-6 space-y-4 m-0">
                                            <div>
                                                <h4 className="text-xs font-bold uppercase text-muted-foreground mb-2">Instagram Caption</h4>
                                                <p className="text-sm border rounded-lg p-3 bg-muted/20">{item.instagram_caption}</p>
                                            </div>
                                            <div>
                                                <h4 className="text-xs font-bold uppercase text-muted-foreground mb-2">WhatsApp Message</h4>
                                                <p className="text-sm border rounded-lg p-3 bg-muted/20 italic">"{item.whatsapp_message}"</p>
                                            </div>
                                        </TabsContent>

                                        <TabsContent value="video" className="p-6 m-0">
                                            {item.video_url ? (
                                                <div className="space-y-4">
                                                    <div className="aspect-video bg-black rounded-lg overflow-hidden flex items-center justify-center border group relative">
                                                        <video
                                                            src={item.video_url}
                                                            controls
                                                            className="w-full h-full object-cover"
                                                        />
                                                    </div>
                                                    <div className="flex gap-4 p-4 bg-primary/5 rounded-lg border border-primary/10">
                                                        <Music className="h-5 w-5 text-primary flex-shrink-0" />
                                                        <div>
                                                            <h4 className="text-xs font-bold text-primary uppercase">AI Audio Script</h4>
                                                            <p className="text-sm text-muted-foreground mt-1">{item.video_script || "Narrator: " + item.whatsapp_message}</p>
                                                        </div>
                                                    </div>
                                                </div>
                                            ) : (
                                                <div className="py-12 text-center text-muted-foreground">
                                                    <div className="bg-muted h-12 w-12 rounded-full flex items-center justify-center mx-auto mb-3">
                                                        <Video className="h-6 w-6" />
                                                    </div>
                                                    <p>AI Video not generated for this piece yet.</p>
                                                </div>
                                            )}
                                        </TabsContent>
                                    </Tabs>
                                </CardContent>
                            </Card>
                        ))
                    )}
                </div>
            </div>
        </PageContainer>
    );
}
