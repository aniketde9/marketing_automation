import { ApiKeyForm } from "@/components/auth/api-key-form";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { auth } from "@/lib/auth";
import { redirect } from "next/navigation";

export default async function ApiKeyPage() {
  const session = await auth();

  if (!session) {
    redirect("/login");
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">API Key Settings</h1>
        <p className="text-muted-foreground">
          Manage your Gemini API key. You can update it anytime to use a different key.
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Gemini API Key</CardTitle>
          <CardDescription>
            Your API key is encrypted with AES-256 before being stored securely in NeonDB.
            Update your key anytime if you need to use a different one.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <ApiKeyForm initialHasKey={session.user.hasApiKey} />
        </CardContent>
      </Card>
    </div>
  );
}

