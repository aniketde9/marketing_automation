import { NextRequest, NextResponse } from 'next/server';
import { auth } from '@/lib/auth';
import { sql } from '@/lib/db';

export async function GET() {
  const session = await auth();

  if (!session?.user?.id) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  const jobs = await sql`
    SELECT j.id, j.status, j.progress, j.total, j.completed_at, j.created_at,
           f.file_size, f.file_name
    FROM jobs j
    LEFT JOIN files f ON f.job_id = j.id
    WHERE j.user_id = ${session.user.id}
      AND j.status = 'completed'
      AND j.created_at > NOW() - INTERVAL '15 days'
    ORDER BY j.created_at DESC
  `;

  return NextResponse.json({ jobs });
}

export async function DELETE(req: NextRequest) {
  const session = await auth();

  if (!session?.user?.id) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  const jobId = req.nextUrl.searchParams.get('id');

  if (!jobId) {
    return NextResponse.json({ error: 'Job ID required' }, { status: 400 });
  }

  await sql`
    DELETE FROM jobs
    WHERE id = ${jobId} AND user_id = ${session.user.id}
  `;

  return NextResponse.json({ success: true });
}

