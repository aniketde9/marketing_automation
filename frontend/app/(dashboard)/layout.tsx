import { ReactNode } from "react";
import { redirect } from "next/navigation";

import { DashboardNav } from "@/components/navigation/dashboard-nav";
import { UserMenu } from "@/components/navigation/user-menu";
import { auth } from "@/lib/auth";

export default async function DashboardLayout({ children }: { children: ReactNode }) {
  const session = await auth();

  if (!session) {
    redirect("/login");
  }

  return (
    <div className="flex min-h-screen flex-col bg-background lg:flex-row">
      <aside className="hidden w-64 border-r lg:flex lg:flex-col">
        <div className="flex-1 space-y-6 p-6">
          <div>
            <p className="text-xl font-semibold">Marketing Automation</p>
            <p className="text-sm text-muted-foreground">200-post daily Gemini workflow</p>
          </div>
          <DashboardNav />
        </div>
        <div className="border-t p-6 text-xs text-muted-foreground">Need help? hello@example.com</div>
      </aside>

      <div className="flex flex-1 flex-col">
        <header className="flex flex-col gap-4 border-b px-6 py-4 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <p className="text-xs uppercase text-muted-foreground">Workspace</p>
            <p className="text-lg font-semibold">Content Engine</p>
          </div>

          <div className="flex flex-1 flex-col gap-4 sm:flex-row sm:items-center sm:justify-end">
            <div className="lg:hidden">
              <DashboardNav orientation="horizontal" />
            </div>
            <UserMenu name={session.user?.name} email={session.user?.email} />
          </div>
        </header>

        <main className="flex-1 bg-muted/30 px-4 py-6 sm:px-6 lg:px-10">
          <div className="mx-auto w-full max-w-5xl space-y-8">{children}</div>
        </main>
      </div>
    </div>
  );
}