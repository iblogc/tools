const fs = require('fs');
const { PDFDocument, rgb } = require('pdf-lib');

async function mergePagesToSinglePage(inputPath, outputPath) {
  // Load the existing PDF
  const pdfBytes = fs.readFileSync(inputPath);
  const pdfDoc = await PDFDocument.load(pdfBytes);
  
  const pages = pdfDoc.getPages();
  const numPages = pages.length;

  // Get the width and height of the first page to assume all pages have the same size
  const { width, height } = pages[0].getSize();

  // Create a new PDF document
  const mergedPdf = await PDFDocument.create();

  // Create a single page with height = height of all pages combined
  const singlePage = mergedPdf.addPage([width, height * numPages]);

  // Draw each page on the new single page
  for (let i = 0; i < numPages; i++) {
    const page = pages[i];
    const [x, y, w, h] = [0, height * (numPages - i - 1), width, height];

    const pageContent = await mergedPdf.embedPage(page);
    singlePage.drawPage(pageContent, { x, y, width: w, height: h });
  }

  // Serialize the PDFDocument to bytes
  const mergedPdfBytes = await mergedPdf.save();

  // Write the merged PDF to a file
  fs.writeFileSync(outputPath, mergedPdfBytes);
}

// Example usage
const inputPath = 'input.pdf';
const outputPath = 'output.pdf';

mergePagesToSinglePage(inputPath, outputPath)
  .then(() => console.log('PDF pages merged to single page successfully!'))
  .catch(err => console.error('Error merging PDF pages:', err));
