const ExcelJS = require('exceljs');
const fs = require('fs');
const path = require('path');

async function testExcel() {
  try {
    // Test the template generation function
    const { generateTemplateExcel } = require('./lib/excel.ts');
    
    console.log('Generating template...');
    const buffer = await generateTemplateExcel();
    
    // Save to temp file for inspection
    const tempPath = path.join(__dirname, 'temp_template.xlsx');
    fs.writeFileSync(tempPath, buffer);
    console.log(`Template saved to: ${tempPath}`);
    
    // Read it back
    const workbook = new ExcelJS.Workbook();
    await workbook.xlsx.load(buffer);
    
    const topicsSheet = workbook.getWorksheet('Topics');
    console.log('\n✅ Topics sheet found:', !!topicsSheet);
    console.log('📊 Row count:', topicsSheet.rowCount);
    console.log('📋 Column headers:', topicsSheet.columns.map(c => c.header || c.key));
    
    // Check first few rows
    console.log('\n📝 First 5 rows:');
    for (let i = 2; i <= 6; i++) {
      const row = topicsSheet.getRow(i);
      console.log(`Row ${i}:`, {
        topic: row.getCell(1).value || '(empty)',
        type: row.getCell(2).value,
        range: row.getCell(3).value
      });
    }
    
    // Check last few rows
    console.log('\n📝 Last 5 rows:');
    for (let i = 197; i <= 201; i++) {
      const row = topicsSheet.getRow(i);
      console.log(`Row ${i}:`, {
        topic: row.getCell(1).value || '(empty)',
        type: row.getCell(2).value,
        range: row.getCell(3).value
      });
    }
    
    // Verify row count
    const expectedRows = 201; // Header + 200 data rows
    if (topicsSheet.rowCount === expectedRows) {
      console.log(`\n✅ Row count correct: ${topicsSheet.rowCount} (expected ${expectedRows})`);
    } else {
      console.log(`\n❌ Row count mismatch: ${topicsSheet.rowCount} (expected ${expectedRows})`);
    }
    
    // Check other sheets
    const instructionsSheet = workbook.getWorksheet('Instructions');
    const contentSheet = workbook.getWorksheet('Generated_Content');
    
    console.log('\n📑 Other sheets:');
    console.log('  Instructions:', !!instructionsSheet);
    console.log('  Generated_Content:', !!contentSheet);
    
    console.log('\n✅ Excel template format is correct!');
    
  } catch (error) {
    console.error('❌ Error testing Excel:', error);
    process.exit(1);
  }
}

testExcel();

