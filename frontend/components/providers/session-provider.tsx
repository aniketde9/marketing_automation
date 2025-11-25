"use client";

import { SessionProvider as NextAuthProvider } from "next-auth/react";
import type { Session } from "next-auth";
import type { ReactNode } from "react";

type SessionProviderProps = {
  children: ReactNode;
  session?: Session | null;
};

export function SessionProvider({ children, session }: SessionProviderProps) {
  return <NextAuthProvider session={session}>{children}</NextAuthProvider>;
}

