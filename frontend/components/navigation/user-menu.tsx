"use client";

import { Button } from "@/components/ui/button";
import { signOut } from "next-auth/react";

type UserMenuProps = {
  name?: string | null;
  email?: string | null;
};

export function UserMenu({ name, email }: UserMenuProps) {
  const displayName = name || email || "User";

  return (
    <div className="flex items-center gap-4">
      <div className="text-right">
        <p className="text-sm font-medium leading-tight">{displayName}</p>
        {email && (
          <p className="text-xs text-muted-foreground" suppressHydrationWarning>
            {email}
          </p>
        )}
      </div>
      <Button
        variant="outline"
        onClick={() => signOut({ callbackUrl: "/login" })}
        className="whitespace-nowrap"
      >
        Sign out
      </Button>
    </div>
  );
}

