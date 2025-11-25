"use client";

import { Button } from "@/components/ui/button";
import { signIn } from "next-auth/react";
import { useState } from "react";

export function SignInButton() {
  const [loading, setLoading] = useState(false);

  const handleSignIn = async () => {
    try {
      setLoading(true);
      await signIn("google", { callbackUrl: "/generate" });
    } finally {
      setLoading(false);
    }
  };

  return (
    <Button onClick={handleSignIn} size="lg" disabled={loading} className="gap-2">
      <span>{loading ? "Redirecting..." : "Continue with Google"}</span>
    </Button>
  );
}

