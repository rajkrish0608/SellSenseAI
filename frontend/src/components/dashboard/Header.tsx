"use client";

import { Bell, Search } from "lucide-react";
import { Button } from "@/components/ui/button";

export default function Header() {
    return (
        <header className="sticky top-0 z-10 flex h-16 w-full items-center justify-between border-b border-border bg-background/50 backdrop-blur px-6">
            <div className="flex items-center gap-4">
                <h1 className="text-lg font-semibold">Dashboard</h1>
            </div>

            <div className="flex items-center gap-4">
                <div className="hidden md:flex relative">
                    <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
                    <input
                        type="text"
                        placeholder="Search..."
                        className="h-9 w-64 rounded-md border border-input bg-transparent pl-9 text-sm outline-none focus:border-primary focus:ring-1 focus:ring-primary"
                    />
                </div>
                <Button variant="ghost" size="icon">
                    <Bell className="h-5 w-5 text-muted-foreground hover:text-foreground" />
                </Button>
            </div>
        </header>
    );
}
