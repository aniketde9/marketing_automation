import { NextRequest, NextResponse } from 'next/server';
import { auth } from '@/lib/auth';
import { parseUploadedExcel } from '@/lib/excel';

export async function POST(req: NextRequest) {
  const session = await auth();

  if (!session?.user?.id) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  const formData = await req.formData();
  const file = formData.get('file') as File | null;

  if (!file) {
    return NextResponse.json({ error: 'No file uploaded' }, { status: 400 });
  }

  try {
    const arrayBuffer = await file.arrayBuffer();
    const buffer = Buffer.from(arrayBuffer);

    const { topics, count } = await parseUploadedExcel(buffer);

    console.log(`User uploaded ${count} topics`);

    // Return topic details for user confirmation
    return NextResponse.json({
      success: true,
      topics: topics.map(t => ({
        row: t.row,
        topic: t.topic,
        contentType: t.contentType
      })),
      count,
      message: `Ready to generate ${count} piece${count === 1 ? '' : 's'} of content`
    });

  } catch (error: any) {
    console.error('Excel parsing error:', error);
    return NextResponse.json(
      { error: error.message || 'Failed to parse Excel file' },
      { status: 400 }
    );
  }
}

