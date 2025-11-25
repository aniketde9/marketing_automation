"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { History, Key, MessageSquareText, Sparkles } from "lucide-react";

import { cn } from "@/lib/utils";

const navItems = [
  { label: "Generate", href: "/generate", icon: Sparkles },
  { label: "Prompts", href: "/prompts", icon: MessageSquareText },
  { label: "API Key", href: "/api-key", icon: Key },
  { label: "History", href: "/history", icon: History },
];

type DashboardNavProps = {
  orientation?: "vertical" | "horizontal";
  className?: string;
  onNavigate?: () => void;
};

export function DashboardNav({
  orientation = "vertical",
  className,
  onNavigate,
}: DashboardNavProps) {
  const pathname = usePathname();

  return (
    <nav
      className={cn(
        "flex gap-2",
        orientation === "vertical" && "flex-col",
        className,
      )}
    >
      {navItems.map((item) => {
        const Icon = item.icon;
        const isActive =
          pathname === item.href || pathname?.startsWith(`${item.href}/`);

        return (
          <Link
            onClick={onNavigate}
            key={item.href}
            href={item.href}
            className={cn(
              "flex items-center gap-2 rounded-md px-3 py-2 text-sm font-medium transition-colors",
              isActive
                ? "bg-muted text-foreground"
                : "text-muted-foreground hover:bg-muted/70 hover:text-foreground",
            )}
          >
            <Icon className="h-4 w-4" />
            {item.label}
          </Link>
        );
      })}
    </nav>
  );
}

