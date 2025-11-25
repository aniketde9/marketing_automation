import { NextRequest, NextResponse } from 'next/server';
import { auth } from '@/lib/auth';
import { sql } from '@/lib/db';
import type { PromptTemplates } from '@/lib/db';

// Simplified prompts - just one carousel template
const DEFAULT_PROMPTS: PromptTemplates = {
  carousel: `Create a professional carousel post about: {topic}

Requirements:
- 6-8 slides total
- Each slide: Title + Content
- Professional yet engaging tone
- Value-driven content
- Clear progression
- Works for both LinkedIn and Instagram

Format each slide as:
Slide N: [Title]
[Content]`,
  thread_x: `Create a Twitter/X thread about: {topic}

Requirements:
- 5-8 tweets
- First tweet: hook (under 280 chars)
- Each tweet: one key point
- Conversational tone
- End with CTA + relevant hashtags`,
  short_linkedin: `Create a LinkedIn post about: {topic}

Requirements:
- 100-150 words
- Professional tone
- Include 1-2 relevant hashtags
- End with engagement question`,
  short_x: `Create a Twitter/X post about: {topic}

Requirements:
- Maximum 280 characters
- Punchy and engaging
- Use 1-2 relevant hashtags`,
  short_instagram: `Create an Instagram caption about: {topic}

Requirements:
- 80-120 words
- Engaging and visual
- 5-8 relevant hashtags
- Include emoji
- Call to action`,
  mixed: `Create engaging social media content about: {topic}

Choose the best format and create compelling content that works across platforms.`,
  short_posts: `Create a short, punchy social media post about: {topic}

Requirements:
- 50-100 words
- Platform-agnostic
- Engaging hook
- 2-3 hashtags`,
};

export async function GET() {
  const session = await auth();

  if (!session?.user?.id) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  const result = await sql`
    SELECT templates
    FROM prompts
    WHERE user_id = ${session.user.id}
  `;

  if (result.length === 0) {
    return NextResponse.json({ templates: DEFAULT_PROMPTS });
  }

  // Clean up old carousel_linkedin/carousel_instagram keys if they exist
  let templates = result[0].templates;
  if (templates.carousel_linkedin || templates.carousel_instagram) {
    // Use carousel_linkedin as the base if carousel doesn't exist
    if (!templates.carousel && templates.carousel_linkedin) {
      templates.carousel = templates.carousel_linkedin;
    }
    // Remove old keys
    delete templates.carousel_linkedin;
    delete templates.carousel_instagram;

    // Update in database
    await sql`
      UPDATE prompts
      SET templates = ${JSON.stringify(templates)}
      WHERE user_id = ${session.user.id}
    `;
  }

  return NextResponse.json({ templates });
}

export async function POST(req: NextRequest) {
  const session = await auth();

  if (!session?.user?.id) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  const { templates } = await req.json();

  await sql`
    INSERT INTO prompts (user_id, templates, updated_at)
    VALUES (${session.user.id}, ${JSON.stringify(templates)}, NOW())
    ON CONFLICT (user_id)
    DO UPDATE SET
      templates = EXCLUDED.templates,
      updated_at = NOW()
  `;

  return NextResponse.json({ success: true });
}

export async function DELETE() {
  const session = await auth();

  if (!session?.user?.id) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  await sql`
    INSERT INTO prompts (user_id, templates, updated_at)
    VALUES (${session.user.id}, ${JSON.stringify(DEFAULT_PROMPTS)}, NOW())
    ON CONFLICT (user_id)
    DO UPDATE SET
      templates = EXCLUDED.templates,
      updated_at = NOW()
  `;

  return NextResponse.json({ success: true });
}

