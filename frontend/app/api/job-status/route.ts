import { NextRequest, NextResponse } from "next/server";

import { auth } from "@/lib/auth";
import { sql } from "@/lib/db";

export async function GET(req: NextRequest) {
  const session = await auth();

  if (!session?.user?.id) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const jobId = req.nextUrl.searchParams.get("id");

  if (!jobId) {
    return NextResponse.json({ error: "Job ID required" }, { status: 400 });
  }

  const job = await sql`
    SELECT id, status, progress, total, latest_message, error_message,
           started_at, completed_at
    FROM jobs
    WHERE id = ${jobId} AND user_id = ${session.user.id}
  `;

  if (job.length === 0) {
    return NextResponse.json({ error: "Job not found" }, { status: 404 });
  }

  return NextResponse.json(job[0]);
}
