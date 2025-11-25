import { redirect } from "next/navigation";

import { HistoryTable, type HistoryJob } from "@/components/history/history-table";
import { auth } from "@/lib/auth";
import { sql } from "@/lib/db";

export const dynamic = "force-dynamic";

export default async function HistoryPage() {
  const session = await auth();

  if (!session?.user?.id) {
    redirect("/login");
  }

  const jobs = (await sql`
    SELECT j.id, j.status, j.progress, j.total, j.completed_at, j.created_at,
           f.file_size, f.file_name
    FROM jobs j
    LEFT JOIN files f ON f.job_id = j.id
    WHERE j.user_id = ${session.user.id}
      AND j.status = 'completed'
      AND j.created_at > NOW() - INTERVAL '15 days'
    ORDER BY j.created_at DESC
  `) as HistoryJob[];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Recent exports</h1>
        <p className="text-muted-foreground">We keep files for 15 days for quick re-downloads.</p>
      </div>
      <HistoryTable initialJobs={jobs} />
    </div>
  );
}