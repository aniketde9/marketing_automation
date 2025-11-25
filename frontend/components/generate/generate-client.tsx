'use client';

import { useEffect, useRef, useState } from 'react';
import { useRouter } from 'next/navigation';
import {
  ArrowRight,
  DownloadCloud,
  FileSpreadsheet,
  Loader2,
  Sparkles,
  Upload,
} from 'lucide-react';

import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Progress } from '@/components/ui/progress';
import { useToast } from '@/hooks/use-toast';

type JobStatusResponse = {
  id: string;
  status: 'pending' | 'processing' | 'completed' | 'failed';
  progress: number;
  total: number;
  latest_message?: string | null;
  error_message?: string | null;
};

export function GenerateClient() {
  const [topics, setTopics] = useState<string[]>([]);
  const [jobId, setJobId] = useState<string | null>(null);
  const [status, setStatus] = useState<'idle' | 'processing' | 'completed' | 'failed'>('idle');
  const [progress, setProgress] = useState(0);
  const [latestMessage, setLatestMessage] = useState<string | null>(null);
  const [hasApiKey, setHasApiKey] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [starting, setStarting] = useState(false);
  const intervalRef = useRef<NodeJS.Timeout | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const { toast } = useToast();
  const router = useRouter();

  useEffect(() => {
    const checkKey = async () => {
      try {
        const res = await fetch('/api/setup-key', { cache: 'no-store' });
        const data = await res.json();
        setHasApiKey(Boolean(data?.hasApiKey));
      } catch {
        setHasApiKey(false);
      }
    };

    checkKey();

    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    };
  }, []);

  const handleDownloadTemplate = () => {
    window.location.href = '/api/download-template';
  };

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    if (!event.target.files?.length) return;
    const file = event.target.files[0];
    const formData = new FormData();
    formData.append('file', file);

    setUploading(true);
    try {
      const res = await fetch('/api/upload-excel', {
        method: 'POST',
        body: formData,
      });
      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.error || 'Failed to parse Excel');
      }

      setTopics(data.topics);
      toast({
        title: 'Template parsed',
        description: `${data.count} topics ready for generation.`,
      });
    } catch (error) {
      toast({
        variant: 'destructive',
        title: 'Upload failed',
        description: error instanceof Error ? error.message : 'Unknown error',
      });
      setTopics([]);
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    } finally {
      setUploading(false);
    }
  };

  const pollJobStatus = (id: string) => {
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
    }

    intervalRef.current = setInterval(async () => {
      try {
        const res = await fetch(`/api/job-status?id=${id}`, { cache: 'no-store' });
        if (!res.ok) return;
        const job: JobStatusResponse = await res.json();

        setProgress(Math.round((job.progress / job.total) * 100));
        setLatestMessage(job.latest_message ?? null);

        if (job.status === 'completed' || job.status === 'failed') {
          clearInterval(intervalRef.current as NodeJS.Timeout);
          intervalRef.current = null;
          setStatus(job.status);
          if (job.status === 'completed') {
            toast({
              title: 'Generation complete',
              description: 'Download the Excel file with your content.',
            });
          } else {
            toast({
              variant: 'destructive',
              title: 'Job failed',
              description: job.error_message || 'Check worker logs for more details.',
            });
          }
        }
      } catch {
        // ignore transient polling errors
      }
    }, 3000);
  };

  const startGeneration = async () => {
    if (!topics.length) {
      toast({
        variant: 'destructive',
        title: 'No topics loaded',
        description: 'Upload the filled template first.',
      });
      return;
    }

    setStarting(true);
    try {
      const res = await fetch('/api/create-job', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ topics }),
      });
      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.error || 'Failed to create job');
      }

      setJobId(data.jobId);
      setStatus('processing');
      setProgress(0);
      pollJobStatus(data.jobId);
      toast({
        title: 'Job queued',
        description: 'The worker will begin processing within a few seconds.',
      });
    } catch (error) {
      toast({
        variant: 'destructive',
        title: 'Unable to start job',
        description: error instanceof Error ? error.message : 'Unknown error',
      });
    } finally {
      setStarting(false);
    }
  };

  const handleDownloadResult = () => {
    if (!jobId) return;
    window.location.href = `/api/download-result?id=${jobId}`;
  };

  return (
    <div className="space-y-8">
      <div>
        <p className="text-sm uppercase tracking-wide text-muted-foreground">Automation</p>
        <h1 className="mt-2 text-3xl font-bold">Generate 200 multi-channel posts</h1>
        <p className="mt-2 text-muted-foreground">
          Upload the filled Excel template, queue a new job, and the worker will populate Gemini
          outputs for every row.
        </p>
      </div>

      {!hasApiKey && (
        <div className="rounded-lg border border-dashed border-yellow-400 bg-yellow-50 p-4 text-sm text-yellow-900">
          <p className="font-medium">Gemini API key missing</p>
          <p className="mt-1">
            Add your Gemini API key before running jobs.{' '}
            <button
              type="button"
              onClick={() => router.push('/api-key')}
              className="font-semibold underline"
            >
              Go to API Key settings →
            </button>
          </p>
        </div>
      )}

      <div className="grid gap-6 lg:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <FileSpreadsheet className="h-5 w-5 text-primary" />
              Excel workflow
            </CardTitle>
            <CardDescription>Download the template, fill all 200 topics, then upload it.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex flex-wrap gap-3">
              <Button variant="secondary" onClick={handleDownloadTemplate} className="gap-2">
                <DownloadCloud className="h-4 w-4" />
                Download template
              </Button>
              <Button
                variant="outline"
                onClick={() => fileInputRef.current?.click()}
                className="gap-2"
              >
                <Upload className="h-4 w-4" />
                Upload filled template
              </Button>
              <Input
                ref={fileInputRef}
                type="file"
                accept=".xlsx"
                className="hidden"
                onChange={handleFileUpload}
              />
            </div>

            <div className="rounded-md border bg-muted/50 p-4 text-sm">
              <p className="font-medium">
                {uploading ? 'Parsing template…' : `${topics.length || 0} topics ready`}
              </p>
              <p className="text-muted-foreground">
                Ensure all 200 rows have a topic. You can re-upload to replace the list.
              </p>
            </div>

            <Button
              className="w-full gap-2"
              disabled={!topics.length || starting || !hasApiKey || status === 'processing'}
              onClick={startGeneration}
            >
              {starting ? (
                <>
                  <Loader2 className="h-4 w-4 animate-spin" />
                  Queuing job…
                </>
              ) : (
                <>
                  <Sparkles className="h-4 w-4" />
                  Start generation
                </>
              )}
            </Button>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Sparkles className="h-5 w-5 text-primary" />
              Worker status
            </CardTitle>
            <CardDescription>We poll the job every 3 seconds to update progress.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <div className="flex items-center justify-between text-sm font-medium">
                <span>Status</span>
                <span className="capitalize">{status}</span>
              </div>
              <Progress value={progress} className="mt-2" />
              {latestMessage && (
                <p className="mt-2 text-sm text-muted-foreground">{latestMessage}</p>
              )}
            </div>

            <div className="rounded-md border bg-muted/50 p-4 text-sm text-muted-foreground">
              <p>
                Jobs typically take 5-10 minutes depending on Gemini rate limits. When finished, you
                can download the Excel output or revisit it later from the history tab.
              </p>
            </div>

            <Button
              variant="outline"
              className="w-full gap-2"
              disabled={status !== 'completed' || !jobId}
              onClick={handleDownloadResult}
            >
              <ArrowRight className="h-4 w-4" />
              Download result
            </Button>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

