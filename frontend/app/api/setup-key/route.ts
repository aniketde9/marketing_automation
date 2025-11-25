import { NextRequest, NextResponse } from 'next/server';
import { auth } from '@/lib/auth';
import { sql } from '@/lib/db';
import { encrypt } from '@/lib/encryption';

export async function POST(req: NextRequest) {
  const session = await auth();

  if (!session?.user?.email) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  const { apiKey } = await req.json();

  if (!apiKey || typeof apiKey !== 'string') {
    return NextResponse.json({ error: 'API key is required' }, { status: 400 });
  }

  // Basic format validation only (skip REST API test - it's broken)
  if (!apiKey.startsWith('AIza') || apiKey.length < 35 || apiKey.length > 45) {
    return NextResponse.json(
      { error: 'Invalid API key format. Google AI Studio keys start with "AIza" and are ~39 characters.' },
      { status: 400 }
    );
  }

  // Check for common mistakes
  if (apiKey.includes(' ')) {
    return NextResponse.json(
      { error: 'API key contains spaces. Please remove any spaces.' },
      { status: 400 }
    );
  }

  console.log('✅ API key format valid. Saving key...');
  console.log('Note: Full validation will happen when you start generation.');

  // Encrypt and store
  try {
    const encryptedKey = encrypt(apiKey);

    await sql`
      UPDATE users 
      SET gemini_api_key_encrypted = ${encryptedKey}, updated_at = NOW()
      WHERE email = ${session.user.email}
    `;

    return NextResponse.json({
      success: true,
      message: 'API key saved successfully! It will be validated when you start generating content.'
    });

  } catch (error: any) {
    console.error('Database error:', error);
    return NextResponse.json(
      { error: 'Failed to save API key to database.' },
      { status: 500 }
    );
  }
}

export async function GET(req: NextRequest) {
  const session = await auth();

  if (!session?.user?.email) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  const result = await sql`
    SELECT gemini_api_key_encrypted 
    FROM users 
    WHERE email = ${session.user.email}
  `;

  return NextResponse.json({
    hasApiKey: !!result[0]?.gemini_api_key_encrypted
  });
}

