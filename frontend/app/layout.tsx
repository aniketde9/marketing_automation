import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

import { SessionProvider } from "@/components/providers/session-provider";
import { Toaster } from "@/components/ui/toaster";
import { cn } from "@/lib/utils";

const inter = Inter({ subsets: ["latin"], variable: "--font-sans" });

export const metadata: Metadata = {
  title: "Marketing Automation",
  description: "Generate 200-piece social content batches powered by Gemini.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body
        className={cn("bg-background font-sans antialiased", inter.variable)}
        suppressHydrationWarning
      >
        <SessionProvider>{children}</SessionProvider>
        <Toaster />
      </body>
    </html>
  );
}
