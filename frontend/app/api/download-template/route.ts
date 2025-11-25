import { NextResponse } from 'next/server';
import { generateTemplateExcel } from '@/lib/excel';

export async function GET() {
  const buffer = await generateTemplateExcel();
  return new NextResponse(buffer, {
    headers: {
      'Content-Type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
      'Content-Disposition': 'attachment; filename="marketing_template.xlsx"',
    },
  });
}

