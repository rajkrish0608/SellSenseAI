"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { ResponsiveContainer, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, BarChart, Bar } from "recharts";
import { DollarSign, MousePointer2, Eye, BarChart3, TrendingUp, Zap, Bot } from "lucide-react";
import PageContainer from "@/components/ui/PageContainer";

const trafficData = [
    { name: "Mon", visits: 4000 },
    { name: "Tue", visits: 3000 },
    { name: "Wed", visits: 2000 },
    { name: "Thu", visits: 2780 },
    { name: "Fri", visits: 1890 },
    { name: "Sat", visits: 2390 },
    { name: "Sun", visits: 3490 },
];

const conversionData = [
    { name: "Instagram", value: 45 },
    { name: "LinkedIn", value: 30 },
    { name: "Twitter", value: 15 },
    { name: "Direct", value: 10 },
];

const adStats = [
    { label: "Ad Spend", value: "₹12,450", icon: DollarSign, color: "text-blue-500" },
    { label: "CTR", value: "2.9%", icon: BarChart3, color: "text-emerald-500", trend: "+0.4%" },
    { label: "Clicks", value: "1,420", icon: MousePointer2, color: "text-purple-500" },
    { label: "Impressions", value: "48,500", icon: Eye, color: "text-orange-500" },
];

export default function AnalyticsPage() {
    return (
        <PageContainer title="Analytics" description="Deep dive into your marketing performance.">
            <div className="flex flex-col gap-6">
                <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
                    <Card>
                        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                            <CardTitle className="text-sm font-medium">Total Revenue</CardTitle>
                        </CardHeader>
                        <CardContent>
                            <div className="text-2xl font-bold">₹45,231</div>
                            <p className="text-xs text-muted-foreground">+20.1% from last month</p>
                        </CardContent>
                    </Card>
                    <Card>
                        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                            <CardTitle className="text-sm font-medium">Subscriptions</CardTitle>
                        </CardHeader>
                        <CardContent>
                            <div className="text-2xl font-bold">+2350</div>
                            <p className="text-xs text-muted-foreground">+180.1% from last month</p>
                        </CardContent>
                    </Card>
                    <Card>
                        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                            <CardTitle className="text-sm font-medium">Active Users</CardTitle>
                        </CardHeader>
                        <CardContent>
                            <div className="text-2xl font-bold">+12,234</div>
                            <p className="text-xs text-muted-foreground">+19% from last month</p>
                        </CardContent>
                    </Card>
                    <Card>
                        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                            <CardTitle className="text-sm font-medium">Bounce Rate</CardTitle>
                        </CardHeader>
                        <CardContent>
                            <div className="text-2xl font-bold">42.3%</div>
                            <p className="text-xs text-muted-foreground">-4% from last month</p>
                        </CardContent>
                    </Card>
                </div>

                <div className="grid gap-6 md:grid-cols-2">
                    <Card>
                        <CardHeader>
                            <CardTitle>Traffic Overview</CardTitle>
                        </CardHeader>
                        <CardContent className="h-[300px]">
                            <ResponsiveContainer width="100%" height="100%">
                                <AreaChart data={trafficData}>
                                    <defs>
                                        <linearGradient id="colorVisits" x1="0" y1="0" x2="0" y2="1">
                                            <stop offset="5%" stopColor="#2563eb" stopOpacity={0.8} />
                                            <stop offset="95%" stopColor="#2563eb" stopOpacity={0} />
                                        </linearGradient>
                                    </defs>
                                    <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
                                    <XAxis dataKey="name" className="text-xs text-muted-foreground" />
                                    <YAxis className="text-xs text-muted-foreground" />
                                    <Tooltip contentStyle={{ backgroundColor: "hsl(var(--card))", borderColor: "hsl(var(--border))" }} itemStyle={{ color: "hsl(var(--foreground))" }} />
                                    <Area type="monotone" dataKey="visits" stroke="#2563eb" fillOpacity={1} fill="url(#colorVisits)" />
                                </AreaChart>
                            </ResponsiveContainer>
                        </CardContent>
                    </Card>

                    <Card>
                        <CardHeader>
                            <CardTitle>Conversion by Channel</CardTitle>
                        </CardHeader>
                        <CardContent className="h-[300px]">
                            <ResponsiveContainer width="100%" height="100%">
                                <BarChart data={conversionData}>
                                    <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
                                    <XAxis dataKey="name" className="text-xs text-muted-foreground" />
                                    <YAxis className="text-xs text-muted-foreground" />
                                    <Tooltip cursor={{ fill: 'transparent' }} contentStyle={{ backgroundColor: "hsl(var(--card))", borderColor: "hsl(var(--border))" }} itemStyle={{ color: "hsl(var(--foreground))" }} />
                                    <Bar dataKey="value" fill="#adfa1d" radius={[4, 4, 0, 0]} />
                                </BarChart>
                            </ResponsiveContainer>
                        </CardContent>
                    </Card>
                </div>

                {/* === GOD MODE: AUTONOMOUS AD BUYING === */}
                <div className="space-y-2">
                    <div className="flex items-center gap-2">
                        <Zap className="h-4 w-4 text-primary" />
                        <h3 className="text-sm font-bold uppercase tracking-widest text-primary">Autonomous Ad Buying & Optimization</h3>
                        <Badge className="text-[9px] bg-primary/20 text-primary">God Mode Feature 4</Badge>
                    </div>
                </div>

                <Card className="border-primary/20 overflow-hidden">
                    <CardHeader className="bg-primary/5 pb-4 flex flex-row items-center justify-between">
                        <CardTitle className="text-sm font-bold uppercase tracking-wider text-muted-foreground flex items-center gap-2">
                            <Bot className="h-4 w-4 text-primary" />
                            Live Ad Performance
                        </CardTitle>
                        <span className="text-[10px] font-mono text-emerald-500 bg-emerald-500/10 px-2 py-0.5 rounded">AI Optimizing</span>
                    </CardHeader>
                    <CardContent className="p-6">
                        <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mb-6">
                            {adStats.map((stat) => (
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

                        <div className="space-y-2">
                            <div className="flex justify-between text-xs font-medium">
                                <span>A/B Test Progress (Variation B)</span>
                                <span className="text-primary">82%</span>
                            </div>
                            <Progress value={82} className="h-1.5" />
                            <p className="text-[10px] text-muted-foreground italic">
                                🤖 AI Agent: &quot;Variation B is outperforming on CTR. Reallocating budget in 4h automatically.&quot;
                            </p>
                        </div>
                    </CardContent>
                </Card>
            </div>
        </PageContainer>
    );
}

