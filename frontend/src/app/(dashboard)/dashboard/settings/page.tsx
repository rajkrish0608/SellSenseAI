"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Switch } from "@/components/ui/switch";
import { Badge } from "@/components/ui/badge";
import { MessageCircle, Mic, Zap, Bot, BellRing, CheckCircle2 } from "lucide-react";
import PageContainer from "@/components/ui/PageContainer";

export default function SettingsPage() {
    const [ownerModeActive, setOwnerModeActive] = useState(true);
    const [voiceEnabled, setVoiceEnabled] = useState(true);
    const [briefingEnabled, setBriefingEnabled] = useState(true);

    return (
        <PageContainer title="Settings" description="Manage your account and preferences.">
            <Tabs defaultValue="profile" className="space-y-4">
                <TabsList>
                    <TabsTrigger value="profile">Profile</TabsTrigger>
                    <TabsTrigger value="whatsapp">
                        WhatsApp Mode
                        <Badge className="ml-2 text-[8px] bg-green-500/20 text-green-400 border-green-500/30 h-4 px-1">GOD MODE</Badge>
                    </TabsTrigger>
                    <TabsTrigger value="billing">Billing</TabsTrigger>
                    <TabsTrigger value="notifications">Notifications</TabsTrigger>
                </TabsList>


                <TabsContent value="profile" className="space-y-4">
                    <Card>
                        <CardHeader>
                            <CardTitle>Profile Information</CardTitle>
                            <CardDescription>Update your public profile and account details.</CardDescription>
                        </CardHeader>
                        <CardContent className="space-y-4">
                            <div className="grid gap-2">
                                <Label htmlFor="name">Full Name</Label>
                                <Input id="name" defaultValue="Demo User" />
                            </div>
                            <div className="grid gap-2">
                                <Label htmlFor="email">Email</Label>
                                <Input id="email" defaultValue="demo@sellsense.ai" />
                            </div>
                            <div className="grid gap-2">
                                <Label htmlFor="bio">Bio</Label>
                                <Input id="bio" placeholder="Tell us about yourself" />
                            </div>
                        </CardContent>
                        <CardFooter>
                            <Button>Save Changes</Button>
                        </CardFooter>
                    </Card>

                    <Card>
                        <CardHeader>
                            <CardTitle>Password</CardTitle>
                            <CardDescription>Change your password using the form below.</CardDescription>
                        </CardHeader>
                        <CardContent className="space-y-4">
                            <div className="grid gap-2">
                                <Label htmlFor="current">Current Password</Label>
                                <Input id="current" type="password" />
                            </div>
                            <div className="grid gap-2">
                                <Label htmlFor="new">New Password</Label>
                                <Input id="new" type="password" />
                            </div>
                        </CardContent>
                        <CardFooter>
                            <Button variant="secondary">Update Password</Button>
                        </CardFooter>
                    </Card>
                </TabsContent>

                <TabsContent value="whatsapp" className="space-y-4">
                    {/* Master Switch */}
                    <Card className="border-green-500/20 bg-green-500/5">
                        <CardHeader className="flex flex-row items-center justify-between">
                            <div className="flex items-center gap-3">
                                <div className="p-2 rounded-lg bg-green-500/10">
                                    <MessageCircle className="h-5 w-5 text-green-400" />
                                </div>
                                <div>
                                    <CardTitle>WhatsApp Owner Mode</CardTitle>
                                    <CardDescription>Run your entire business from WhatsApp. Zero-click AI marketing.</CardDescription>
                                </div>
                            </div>
                            <Switch checked={ownerModeActive} onCheckedChange={setOwnerModeActive} />
                        </CardHeader>
                        {ownerModeActive && (
                            <CardContent className="space-y-3 pt-0">
                                <div className="flex items-center gap-2 text-[11px] text-green-400">
                                    <CheckCircle2 className="h-3 w-3" />
                                    <span>Owner Mode is ACTIVE — Your AI is listening on WhatsApp</span>
                                </div>
                            </CardContent>
                        )}
                    </Card>

                    {/* Phone Number */}
                    <Card>
                        <CardHeader>
                            <CardTitle className="text-sm">Your Command Number</CardTitle>
                            <CardDescription>WhatsApp number that sends commands to SellSenseAI.</CardDescription>
                        </CardHeader>
                        <CardContent className="space-y-3">
                            <div className="grid gap-2">
                                <Label htmlFor="wa-phone">WhatsApp Phone Number</Label>
                                <Input id="wa-phone" placeholder="+91 98765 43210" defaultValue="+91 98765 43210" />
                            </div>
                            <div className="grid gap-2">
                                <Label htmlFor="wa-token">WhatsApp API Token</Label>
                                <Input id="wa-token" type="password" placeholder="••••••••••••••••" />
                            </div>
                        </CardContent>
                        <CardFooter><Button>Save Connection</Button></CardFooter>
                    </Card>

                    {/* Capabilities */}
                    <Card>
                        <CardHeader>
                            <CardTitle className="text-sm">God Mode Capabilities</CardTitle>
                            <CardDescription>What your AI will do autonomously when activated.</CardDescription>
                        </CardHeader>
                        <CardContent className="space-y-4">
                            {[
                                { icon: Bot, label: "Business Intelligence Queries", desc: "Ask 'What were my sales today?' and get a real-time report.", active: true },
                                { icon: Mic, label: "Voice-to-Action", desc: "Send a voice note to trigger full campaign creation hands-free.", active: voiceEnabled, toggle: setVoiceEnabled },
                                { icon: BellRing, label: "Daily Morning Briefing", desc: "Receive an automated performance summary every morning at 8am.", active: briefingEnabled, toggle: setBriefingEnabled },
                                { icon: Zap, label: "Competitor Retaliation Alerts", desc: "Reply 'RETALIATE' when a rival trigger is detected to launch a counter-strike.", active: true },
                            ].map((cap) => (
                                <div key={cap.label} className="flex items-center justify-between py-2 border-b border-white/5 last:border-0">
                                    <div className="flex items-center gap-3">
                                        <cap.icon className="h-4 w-4 text-primary" />
                                        <div>
                                            <p className="text-sm font-medium">{cap.label}</p>
                                            <p className="text-xs text-muted-foreground">{cap.desc}</p>
                                        </div>
                                    </div>
                                    {cap.toggle ? (
                                        <Switch checked={cap.active} onCheckedChange={cap.toggle} />
                                    ) : (
                                        <Badge className="text-[9px] bg-primary/20 text-primary">Always On</Badge>
                                    )}
                                </div>
                            ))}
                        </CardContent>
                    </Card>

                    {/* Test Command */}
                    <Card className="border-primary/20 bg-primary/5">
                        <CardHeader>
                            <CardTitle className="text-sm">Test a WhatsApp Command</CardTitle>
                            <CardDescription>Simulate what happens when you text SellSenseAI</CardDescription>
                        </CardHeader>
                        <CardContent className="space-y-3">
                            <div className="grid gap-2">
                                <Label>Simulated Message</Label>
                                <Input defaultValue="How much did I sell today?" />
                            </div>
                            <Button className="w-full gap-2">
                                <MessageCircle className="h-4 w-4" />
                                Simulate WhatsApp Command
                            </Button>
                        </CardContent>
                    </Card>
                </TabsContent>

                <TabsContent value="billing">
                    <Card>
                        <CardHeader>
                            <CardTitle>Subscription Plan</CardTitle>
                            <CardDescription>You are currently on the Pro Plan.</CardDescription>
                        </CardHeader>
                        <CardContent>
                            <div className="text-sm text-muted-foreground">
                                Next billing date: March 1, 2026
                            </div>
                        </CardContent>
                        <CardFooter>
                            <Button variant="outline">Manage Subscription</Button>
                        </CardFooter>
                    </Card>
                </TabsContent>

                <TabsContent value="notifications">
                    <Card>
                        <CardHeader>
                            <CardTitle>Notifications</CardTitle>
                            <CardDescription>Configure how you receive alerts.</CardDescription>
                        </CardHeader>
                        <CardContent>
                            <div className="flex items-center space-x-2">
                                {/* Future: Add Switch component */}
                                <span className="text-sm">Email Notifications Enabled</span>
                            </div>
                        </CardContent>
                    </Card>
                </TabsContent>
            </Tabs>
        </PageContainer>
    );
}
