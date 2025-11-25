import { NextRequest, NextResponse } from 'next/server';
import { auth } from '@/lib/auth';
import { sql } from '@/lib/db';
import { generateResultExcel } from '@/lib/excel';

export async function GET(req: NextRequest) {
  const session = await auth();

  if (!session?.user?.id) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  const jobId = req.nextUrl.searchParams.get('id');

  if (!jobId) {
    return NextResponse.json({ error: 'Job ID required' }, { status: 400 });
  }

  try {
    // Verify job belongs to user and is completed
    const job = await sql`
      SELECT status, created_at FROM jobs 
      WHERE id = ${jobId} AND user_id = ${session.user.id}
    `;

    if (job.length === 0) {
      return NextResponse.json({ error: 'Job not found' }, { status: 404 });
    }

    if (job[0].status !== 'completed') {
      return NextResponse.json(
        { error: `Job status is ${job[0].status}. Download available only for completed jobs.` },
        { status: 400 }
      );
    }

    // Fetch generated content with proper typing
    const contentRaw = await sql`
      SELECT row_number, topic, content_type, generated_text
      FROM generated_content
      WHERE job_id = ${jobId} AND generated_text != ''
      ORDER BY row_number ASC
    `;

    // Type assertion to match generateResultExcel expected type
    const content = contentRaw as Array<{
      row_number: number;
      topic: string;
      content_type: string;
      generated_text: string;
    }>;

    if (content.length === 0) {
      return NextResponse.json(
        { error: 'No generated content found for this job' },
        { status: 404 }
      );
    }

    console.log(`Generating Excel with ${content.length} posts for job ${jobId}`);

    // Prepare data for Excel generation
    const topics = content.map((c) => ({
      row: c.row_number,
      topic: c.topic,
      contentType: c.content_type,
    }));

    // Generate Excel buffer
    const buffer = await generateResultExcel(topics, content);

    // Convert Buffer to Uint8Array for NextResponse
    const uint8Array = new Uint8Array(buffer);

    // Generate filename with date
    const date = new Date(job[0].created_at).toISOString().split('T')[0];
    const filename = `marketing_content_${date}_${content.length}_posts.xlsx`;

    // Return Excel file directly
    return new NextResponse(uint8Array, {
      status: 200,
      headers: {
        'Content-Type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'Content-Disposition': `attachment; filename="${filename}"`,
        'Content-Length': buffer.length.toString(),
      },
    });

  } catch (error: any) {
    console.error('Download generation error:', error);
    return NextResponse.json(
      {
        error: 'Failed to generate Excel file',
        message: error.message
      },
      { status: 500 }
    );
  }
}

