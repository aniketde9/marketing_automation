"use client";

import { useEffect, useState } from "react";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Textarea } from "@/components/ui/textarea";
import { useToast } from "@/hooks/use-toast";

type Templates = Record<string, string>;

const promptFields: Array<{ key: keyof Templates; label: string; description: string }> = [
  {
    key: "carousel",
    label: "📱 Carousel (LinkedIn & Instagram)",
    description: "Single carousel format that works for both LinkedIn and Instagram.",
  },
  {
    key: "thread_x",
    label: "🧵 X/Twitter Thread",
    description: "Multi-tweet threads for X/Twitter.",
  },
  {
    key: "short_linkedin",
    label: "💼 LinkedIn Post",
    description: "Professional LinkedIn posts.",
  },
  {
    key: "short_x",
    label: "🐦 X/Twitter Post",
    description: "Short tweets for X/Twitter (280 chars).",
  },
  {
    key: "short_instagram",
    label: "📷 Instagram Caption",
    description: "Instagram captions with hashtags.",
  },
  {
    key: "mixed",
    label: "🔄 Mixed Format",
    description: "Flexible format for any platform.",
  },
  {
    key: "short_posts",
    label: "📝 Short Posts",
    description: "Quick, short-form content.",
  },
];

export function PromptManager() {
  const [templates, setTemplates] = useState<Templates>({});
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const { toast } = useToast();

  useEffect(() => {
    const fetchPrompts = async () => {
      setLoading(true);
      try {
        const res = await fetch("/api/prompts", { cache: "no-store" });
        const data = await res.json();
        const templates = data.templates || {};
        
        // Migrate old carousel keys to new single carousel key
        if (templates.carousel_linkedin || templates.carousel_instagram) {
          if (!templates.carousel && templates.carousel_linkedin) {
            templates.carousel = templates.carousel_linkedin;
          }
          delete templates.carousel_linkedin;
          delete templates.carousel_instagram;
          setTemplates(templates);
        } else {
          setTemplates(templates);
        }
      } catch {
        toast({
          variant: "destructive",
          title: "Unable to load prompts",
          description: "Please refresh and try again.",
        });
      } finally {
        setLoading(false);
      }
    };

    fetchPrompts();
  }, [toast]);

  const updateField = (key: string, value: string) => {
    setTemplates((prev) => ({ ...prev, [key]: value }));
  };

  const handleSave = async () => {
    setSaving(true);
    try {
      const res = await fetch("/api/prompts", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ templates }),
      });
      if (!res.ok) {
        throw new Error("Failed to save prompts");
      }
      toast({ title: "Prompts updated", description: "New defaults will be used immediately." });
    } catch (error) {
      toast({
        variant: "destructive",
        title: "Save failed",
        description: error instanceof Error ? error.message : "Unknown error",
      });
    } finally {
      setSaving(false);
    }
  };

  const handleReset = async () => {
    setSaving(true);
    try {
      const res = await fetch("/api/prompts", { method: "DELETE" });
      if (!res.ok) {
        throw new Error("Failed to reset prompts");
      }
      const fresh = await fetch("/api/prompts", { cache: "no-store" }).then((r) => r.json());
      setTemplates(fresh.templates || {});
      toast({ title: "Prompts reset", description: "Default templates restored." });
    } catch (error) {
      toast({
        variant: "destructive",
        title: "Reset failed",
        description: error instanceof Error ? error.message : "Unknown error",
      });
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Custom prompt templates</h1>
        <p className="text-muted-foreground">
          Tweak the instructions Gemini receives for each content block. The worker will merge the topic
          and content type with these templates.
        </p>
      </div>

      <div className="flex flex-wrap gap-3">
        <Button onClick={handleSave} disabled={saving || loading}>
          {saving ? "Saving…" : "Save prompts"}
        </Button>
        <Button variant="outline" onClick={handleReset} disabled={saving || loading}>
          Reset to defaults
        </Button>
      </div>

      <div className="grid gap-6">
        {promptFields.map((field) => (
          <Card key={field.key}>
            <CardHeader>
              <CardTitle>{field.label}</CardTitle>
              <CardDescription>{field.description}</CardDescription>
            </CardHeader>
            <CardContent>
              <Textarea
                rows={6}
                value={templates[field.key] || ""}
                onChange={(event) => updateField(field.key, event.target.value)}
                placeholder="Enter the instructions Gemini should follow..."
                disabled={loading}
              />
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}

