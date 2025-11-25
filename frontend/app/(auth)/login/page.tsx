import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { SignInButton } from "@/components/auth/sign-in-button";
import { redirect } from "next/navigation";
import { auth } from "@/lib/auth";
import { Suspense } from "react";

export const dynamic = 'force-dynamic';

export default async function LoginPage() {
  const session = await auth();

  if (session) {
    // Redirect to generate if they have API key, otherwise to API key setup
    if (session.user.hasApiKey) {
      redirect("/generate");
    } else {
      redirect("/api-key");
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-muted/50 px-4 py-16">
      <Suspense fallback={<div className="text-center">Loading...</div>}>
        <Card className="w-full max-w-lg">
          <CardHeader>
            <CardTitle className="text-3xl font-bold">Marketing Automation Hub</CardTitle>
            <CardDescription>
              Securely sign in with Google to access your prompts, upload templates, and launch
              200-post Gemini jobs in a single click.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <p className="text-sm text-muted-foreground">
                You will be asked to connect your Google Workspace account. Once inside, head to the
                &quot;Setup API Key&quot; tab to store your Gemini key securely.
              </p>
              <SignInButton />
            </div>
          </CardContent>
        </Card>
      </Suspense>
    </div>
  );
}