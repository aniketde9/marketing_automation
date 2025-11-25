"use client";

import { useState } from "react";
import { format } from "date-fns";
import { Trash2 } from "lucide-react";

import { Button } from "@/components/ui/button";
import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { useToast } from "@/hooks/use-toast";

export type HistoryJob = {
  id: string;
  status: string;
  progress: number;
  total: number;
  completed_at: string | null;
  created_at: string;
  file_size: number | null;
  file_name: string | null;
};

type HistoryTableProps = {
  initialJobs: HistoryJob[];
};

export function HistoryTable({ initialJobs }: HistoryTableProps) {
  const [jobs, setJobs] = useState(initialJobs);
  const [deleting, setDeleting] = useState<string | null>(null);
  const { toast } = useToast();

  const handleDownload = (jobId: string) => {
    window.location.href = `/api/download-result?id=${jobId}`;
  };

  const handleDelete = async (jobId: string) => {
    setDeleting(jobId);
    try {
      const res = await fetch(`/api/history?id=${jobId}`, { method: "DELETE" });
      if (!res.ok) throw new Error("Failed to delete job");
      setJobs((prev) => prev.filter((job) => job.id !== jobId));
      toast({
        title: "Job deleted",
        description: "Related files and generated content were removed.",
      });
    } catch (error) {
      toast({
        title: "Delete failed",
        description: error instanceof Error ? error.message : "Unknown error",
      });
    } finally {
      setDeleting(null);
    }
  };

  if (!jobs.length) {
    return (
      <div className="rounded-lg border border-dashed bg-muted/30 p-8 text-center">
        <p className="text-lg font-semibold">No completed jobs yet</p>
        <p className="mt-2 text-sm text-muted-foreground">
          Your last 15 days of exports will show up here once the worker finishes a batch.
        </p>
      </div>
    );
  }

  return (
    <Table>
      <TableCaption>Your last 15 days of completed generations.</TableCaption>
      <TableHeader>
        <TableRow>
          <TableHead>Job ID</TableHead>
          <TableHead>Status</TableHead>
          <TableHead>Created</TableHead>
          <TableHead>Completed</TableHead>
          <TableHead>File size</TableHead>
          <TableHead className="text-right">Actions</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {jobs.map((job) => (
          <TableRow key={job.id}>
            <TableCell className="font-mono text-xs">{job.id.split("-")[0]}</TableCell>
            <TableCell className="capitalize">{job.status}</TableCell>
            <TableCell>{format(new Date(job.created_at), "PPp")}</TableCell>
            <TableCell>
              {job.completed_at ? format(new Date(job.completed_at), "PPp") : "—"}
            </TableCell>
            <TableCell>
              {job.file_size ? `${(job.file_size / (1024 * 1024)).toFixed(2)} MB` : "—"}
            </TableCell>
            <TableCell className="text-right">
              <div className="flex justify-end gap-2">
                <Button variant="outline" size="sm" onClick={() => handleDownload(job.id)}>
                  Download
                </Button>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => handleDelete(job.id)}
                  disabled={deleting === job.id}
                >
                  <Trash2 className="h-4 w-4" />
                </Button>
              </div>
            </TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
}

