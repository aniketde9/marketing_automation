import ExcelJS from 'exceljs';

export const CONTENT_DISTRIBUTION = [
  { start: 2, end: 31, count: 30, type: 'Carousel (LinkedIn/Instagram)' },
  { start: 32, end: 51, count: 20, type: 'X Threads' },
  { start: 52, end: 71, count: 20, type: 'Carousel (LinkedIn/Instagram)' },
  { start: 72, end: 91, count: 20, type: 'LinkedIn Posts' },
  { start: 92, end: 111, count: 20, type: 'X Posts' },
  { start: 112, end: 151, count: 40, type: 'Instagram Captions' },
  { start: 152, end: 161, count: 10, type: 'Mixed (All Formats)' },
  { start: 162, end: 201, count: 40, type: 'Short Posts' },
];

export async function generateTemplateExcel(): Promise<Buffer> {
  const workbook = new ExcelJS.Workbook();

  const topicsSheet = workbook.addWorksheet('Topics');
  topicsSheet.columns = [
    { header: 'Topic', key: 'topic', width: 50 },
    { header: 'Content Type', key: 'type', width: 30 },
    { header: 'Row Range', key: 'range', width: 15 },
  ];

  topicsSheet.getRow(1).font = { bold: true, size: 12 };
  topicsSheet.getRow(1).fill = {
    type: 'pattern',
    pattern: 'solid',
    fgColor: { argb: 'FF4472C4' },
  };

  CONTENT_DISTRIBUTION.forEach((dist) => {
    for (let row = dist.start; row <= dist.end; row += 1) {
      topicsSheet.addRow({
        topic: '',
        type: dist.type,
        range: `Row ${row}`,
      });
    }
  });

  const instructionsSheet = workbook.addWorksheet('Instructions');
  instructionsSheet.columns = [{ header: 'Instructions', key: 'text', width: 100 }];

  const instructions = [
    '📖 HOW TO USE THIS TEMPLATE',
    '',
    '1. Fill the "Topic" column in the Topics sheet',
    '2. You can fill anywhere from 1 to 200 topics',
    '3. Leave rows empty if you want fewer topics',
    '4. Each row is pre-assigned to a content type',
    '',
    '📊 CONTENT DISTRIBUTION:',
    '',
    ...CONTENT_DISTRIBUTION.map(
      (d) => `Rows ${d.start}-${d.end}: ${d.type} (${d.count} topics max)`,
    ),
    '',
    '⚠️ IMPORTANT:',
    '- Fill as many or as few topics as you need (1-200)',
    '- Keep topics clear and specific',
    '- Empty rows will be skipped',
    '- You can generate up to 1000 posts per day',
    '',
    '✅ Upload when ready to generate your content!',
  ];

  instructions.forEach((text) => {
    instructionsSheet.addRow({ text });
  });

  const contentSheet = workbook.addWorksheet('Generated_Content');
  contentSheet.columns = [
    { header: 'Row', key: 'row', width: 8 },
    { header: 'Topic', key: 'topic', width: 40 },
    { header: 'Content Type', key: 'type', width: 30 },
    { header: 'Generated Content', key: 'content', width: 80 },
  ];

  contentSheet.getRow(1).font = { bold: true };

  const buffer = await workbook.xlsx.writeBuffer();
  return Buffer.from(buffer);
}

export async function parseUploadedExcel(buffer: Buffer): Promise<{
  topics: Array<{ row: number; topic: string; contentType: string }>;
  count: number;
}> {
  const workbook = new ExcelJS.Workbook();
  await workbook.xlsx.load(buffer);

  const topicsSheet = workbook.getWorksheet('Topics');
  if (!topicsSheet) {
    throw new Error('Invalid template: "Topics" sheet not found');
  }

  const topics: Array<{ row: number; topic: string; contentType: string }> = [];

  // Read rows 2-201 but ONLY collect non-empty topics
  for (let i = 2; i <= 201; i += 1) {
    const row = topicsSheet.getRow(i);
    const topicValue = row.getCell(1).value;

    // Handle various cell value types
    let topic = '';
    if (topicValue) {
      topic = topicValue.toString().trim();
    }

    // Skip empty rows
    if (!topic) {
      continue; // This is the key change - we SKIP empty rows instead of erroring
    }

    // Find the content type for this row number
    const dist = CONTENT_DISTRIBUTION.find(
      (d) => i >= d.start && i <= d.end
    );

    if (!dist) {
      console.warn(`Row ${i} is outside defined ranges, using 'Mixed (All Formats)' as default`);
    }

    topics.push({
      row: i,
      topic,
      contentType: dist?.type || 'Mixed (All Formats)',
    });
  }

  // Validate we have at least 1 topic
  if (topics.length === 0) {
    throw new Error('No topics found. Please fill at least one topic in the Topics sheet.');
  }

  console.log(`✅ Parsed ${topics.length} topics from Excel`);

  return {
    topics,
    count: topics.length,
  };
}

export async function generateResultExcel(
  topics: Array<{ row: number; topic: string; contentType: string }>,
  generatedContent: Array<{
    row_number: number;
    topic: string;
    content_type: string;
    generated_text: string;
  }>,
): Promise<Buffer> {
  const workbook = new ExcelJS.Workbook();

  // Topics Sheet (original)
  const topicsSheet = workbook.addWorksheet('Topics');
  topicsSheet.columns = [
    { header: 'Row', key: 'row', width: 10 },
    { header: 'Topic', key: 'topic', width: 50 },
    { header: 'Content Type', key: 'type', width: 30 },
  ];

  topics.forEach((item) => {
    topicsSheet.addRow({
      row: item.row,
      topic: item.topic,
      type: item.contentType,
    });
  });

  // Generated Content Sheet
  const contentSheet = workbook.addWorksheet('Generated_Content');
  contentSheet.columns = [
    { header: 'Row', key: 'row', width: 8 },
    { header: 'Topic', key: 'topic', width: 40 },
    { header: 'Content Type', key: 'type', width: 30 },
    { header: 'Generated Content', key: 'content', width: 80 },
  ];

  contentSheet.getRow(1).font = { bold: true };

  generatedContent.forEach((item) => {
    contentSheet.addRow({
      row: item.row_number,
      topic: item.topic,
      type: item.content_type,
      content: item.generated_text,
    });
  });

  // Summary Sheet
  const summarySheet = workbook.addWorksheet('Summary');
  summarySheet.columns = [
    { header: 'Metric', key: 'metric', width: 30 },
    { header: 'Value', key: 'value', width: 20 },
  ];

  summarySheet.addRow({ metric: 'Total Topics Processed', value: topics.length });
  summarySheet.addRow({ metric: 'Successfully Generated', value: generatedContent.length });
  summarySheet.addRow({ metric: 'Generation Date', value: new Date().toISOString().split('T')[0] });

  const buffer = await workbook.xlsx.writeBuffer();
  return Buffer.from(buffer);
}

export function getContentType(row: number): string {
  if (row >= 2 && row <= 31) return 'carousel';
  if (row >= 32 && row <= 51) return 'thread_x';
  if (row >= 52 && row <= 71) return 'carousel';
  if (row >= 72 && row <= 91) return 'short_linkedin';
  if (row >= 92 && row <= 111) return 'short_x';
  if (row >= 112 && row <= 151) return 'short_instagram';
  if (row >= 152 && row <= 161) return 'mixed';
  if (row >= 162 && row <= 201) return 'short_posts';
  return 'unknown';
}

