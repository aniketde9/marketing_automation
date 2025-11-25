"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { ChevronDown, ChevronUp, ExternalLink } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { useToast } from "@/hooks/use-toast";

type ApiKeyFormProps = {
  initialHasKey?: boolean;
};

export function ApiKeyForm({ initialHasKey }: ApiKeyFormProps) {
  const [apiKey, setApiKey] = useState("");
  const [hasKey, setHasKey] = useState(initialHasKey ?? false);
  const [checking, setChecking] = useState(initialHasKey === undefined);
  const [saving, setSaving] = useState(false);
  const [showInstructions, setShowInstructions] = useState(!initialHasKey);
  const { toast } = useToast();
  const router = useRouter();

  useEffect(() => {
    if (initialHasKey !== undefined) {
      setChecking(false);
      return;
    }

    const fetchStatus = async () => {
      try {
        const res = await fetch("/api/setup-key");
        const data = await res.json();
        setHasKey(Boolean(data?.hasApiKey));
      } catch {
        toast({
          title: "Unable to load key status",
          description: "Please refresh the page and try again.",
        });
      } finally {
        setChecking(false);
      }
    };

    fetchStatus();
  }, [initialHasKey, toast]);

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    if (!apiKey) return;

    setSaving(true);
    try {
      const res = await fetch("/api/setup-key", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ apiKey }),
      });

      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.error || "Failed to save key");
      }

      toast({
        title: "API key updated",
        description: hasKey 
          ? "Your API key has been successfully updated." 
          : "API key saved! You can now start generating content.",
      });
      setHasKey(true);
      setApiKey("");
      router.refresh();
    } catch (error) {
      toast({
        title: "Failed to validate key",
        description: error instanceof Error ? error.message : "Unknown error",
      });
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Instructions Section */}
      <div className="rounded-lg border bg-muted/50 p-6">
        <button
          type="button"
          onClick={() => setShowInstructions(!showInstructions)}
          className="flex w-full items-center justify-between text-left"
        >
          <h3 className="text-lg font-semibold">How to Get Your Gemini API Key</h3>
          {showInstructions ? (
            <ChevronUp className="h-5 w-5 text-muted-foreground" />
          ) : (
            <ChevronDown className="h-5 w-5 text-muted-foreground" />
          )}
        </button>

        {showInstructions && (
          <div className="mt-4 space-y-4 text-sm">
            <div className="space-y-3">
              <div className="flex gap-3">
                <div className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-primary text-primary-foreground text-xs font-semibold">
                  1
                </div>
                <div className="flex-1">
                  <p className="font-medium">Go to Google AI Studio</p>
                  <p className="text-muted-foreground">
                    Visit{" "}
                    <a
                      href="https://aistudio.google.com"
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-primary hover:underline inline-flex items-center gap-1"
                    >
                      aistudio.google.com
                      <ExternalLink className="h-3 w-3" />
                    </a>
                    , click "Get Started," and sign in with your Google account.
                  </p>
                </div>
              </div>

              <div className="flex gap-3">
                <div className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-primary text-primary-foreground text-xs font-semibold">
                  2
                </div>
                <div className="flex-1">
                  <p className="font-medium">Accept Terms</p>
                  <p className="text-muted-foreground">
                    Review and accept the Google APIs Terms of Service and Gemini API Additional Terms of Service when
                    prompted.
                  </p>
                </div>
              </div>

              <div className="flex gap-3">
                <div className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-primary text-primary-foreground text-xs font-semibold">
                  3
                </div>
                <div className="flex-1">
                  <p className="font-medium">Navigate to API Keys</p>
                  <p className="text-muted-foreground">
                    In the bottom left sidebar, click on "API Keys" to access the key management page.
                  </p>
                </div>
              </div>

              <div className="flex gap-3">
                <div className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-primary text-primary-foreground text-xs font-semibold">
                  4
                </div>
                <div className="flex-1">
                  <p className="font-medium">Create a New Project</p>
                  <p className="text-muted-foreground">
                    Click "+ Create project," enter a project name (e.g., "My Gemini App"), and click "Create project."
                  </p>
                </div>
              </div>

              <div className="flex gap-3">
                <div className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-primary text-primary-foreground text-xs font-semibold">
                  5
                </div>
                <div className="flex-1">
                  <p className="font-medium">Generate Your API Key</p>
                  <p className="text-muted-foreground">
                    Select your newly created project from the dropdown, then click "Create API Key." Your key will be
                    instantly generated as a long alphanumeric string (e.g., AIzaSyB1234567890abcdefghijklmnopqrstuvwxyz).
                  </p>
                </div>
              </div>

              <div className="flex gap-3">
                <div className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-primary text-primary-foreground text-xs font-semibold">
                  6
                </div>
                <div className="flex-1">
                  <p className="font-medium">Copy and Save Securely</p>
                  <p className="text-muted-foreground">
                    Click the "Copy" button next to your API key, then paste it here. Never share your API key with
                    anyone. We encrypt your API key before storing it.
                  </p>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* API Key Form */}
      <div className="rounded-lg border bg-card p-6 shadow-sm">
        <div className="space-y-4">
          <div>
            <p className="text-sm font-medium">Google Gemini API key</p>
            <p className="text-sm text-muted-foreground">
              Keys are encrypted with AES-256 before being stored in NeonDB.
            </p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-3">
            <Input
              type="password"
              placeholder="Paste your Gemini API key (starts with AIza...)"
              value={apiKey}
              onChange={(event) => setApiKey(event.target.value)}
              disabled={saving}
            />
            <Button type="submit" disabled={!apiKey || saving}>
              {saving ? "Validating…" : hasKey ? "Update API key" : "Save API key"}
            </Button>
          </form>

          <div className="rounded-md bg-muted p-3 text-sm text-muted-foreground">
            {checking ? "Checking stored key…" : hasKey ? "✅ Key on file" : "❌ No key found"}
          </div>
        </div>
      </div>

      <div className="flex flex-wrap gap-3">
        <Button variant="outline" onClick={() => window.open("https://aistudio.google.com/apikey", "_blank")}>
          <ExternalLink className="mr-2 h-4 w-4" />
          Open Google AI Studio
        </Button>
        {!hasKey && (
          <Button onClick={() => router.push("/generate")} disabled={!hasKey}>
            Go to generator
          </Button>
        )}
      </div>
    </div>
  );
}

