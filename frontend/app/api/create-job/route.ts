import { NextRequest, NextResponse } from 'next/server';
import { auth } from '@/lib/auth';
import { sql } from '@/lib/db';

export async function POST(req: NextRequest) {
  const session = await auth();

  if (!session?.user?.id) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  const { topics } = await req.json();

  if (!topics || !Array.isArray(topics) || topics.length === 0) {
    return NextResponse.json({ error: 'No topics provided' }, { status: 400 });
  }

  // Check daily limit based on actual count, not fixed 200
  const today = new Date().toISOString().split('T')[0];

  const generationLog = await sql`
    SELECT COALESCE(SUM(posts_generated), 0) as total_generated
    FROM user_generation_log 
    WHERE user_id = ${session.user.id} 
      AND generation_date = ${today}
  `;

  const alreadyGenerated = parseInt(generationLog[0]?.total_generated || '0', 10) || 0;
  const remainingQuota = 1000 - alreadyGenerated;

  if (topics.length > remainingQuota) {
    return NextResponse.json(
      {
        error: `Daily limit exceeded. You've generated ${alreadyGenerated}/1000 posts today. You can generate ${remainingQuota} more.`,
        limitReached: true,
        alreadyGenerated,
        remainingQuota
      },
      { status: 429 }
    );
  }

  // Check if user has API key
  const user = await sql`
    SELECT gemini_api_key_encrypted 
    FROM users 
    WHERE id = ${session.user.id}
  `;

  if (!user[0]?.gemini_api_key_encrypted) {
    return NextResponse.json(
      { error: 'Please setup your Gemini API key first' },
      { status: 400 }
    );
  }

  // Create job with actual topic count
  const job = await sql`
    INSERT INTO jobs (user_id, status, progress, total, latest_message)
    VALUES (${session.user.id}, 'pending', 0, ${topics.length}, ${'Queued for generation...'})
    RETURNING id
  `;

  const jobId = job[0].id;

  // Store each topic with its metadata
  for (const topic of topics) {
    await sql`
      INSERT INTO generated_content (job_id, row_number, content_type, topic, generated_text)
      VALUES (${jobId}, ${topic.row}, ${topic.contentType}, ${topic.topic}, '')
    `;
  }

  // Log generation attempt with actual count
  await sql`
    INSERT INTO user_generation_log (user_id, job_id, generation_date, posts_generated)
    VALUES (${session.user.id}, ${jobId}, ${today}, ${topics.length})
    ON CONFLICT (user_id, generation_date)
    DO UPDATE SET 
      posts_generated = user_generation_log.posts_generated + EXCLUDED.posts_generated,
      job_id = EXCLUDED.job_id
  `;

  console.log(`Job ${jobId} created with ${topics.length} topics`);

  return NextResponse.json({
    jobId,
    topicCount: topics.length,
    estimatedTime: Math.ceil(topics.length * 7.5 / 60), // minutes at ~8 seconds per post
    message: `Processing ${topics.length} topic${topics.length === 1 ? '' : 's'}...`
  });
}

