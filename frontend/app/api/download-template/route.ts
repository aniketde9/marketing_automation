import { NextResponse } from 'next/server';
import { generateTemplateExcel } from '@/lib/excel';

export async function GET() {
  const buffer = await generateTemplateExcel();
  const uint8Array = new Uint8Array(buffer);

  return new NextResponse(uint8Array, {
    headers: {
      'Content-Type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
      'Content-Disposition': 'attachment; filename="marketing_template.xlsx"',
    },
  });
}

