#!/usr/bin/env python3
"""
PDF to Markdown Converter using pdfplumber
Converts all PDFs in data/source/pdfs/ to markdown files in data/source/markdowns/
"""

import os
import sys
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
import pdfplumber
import re

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('pdf_conversion.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class PDFToMarkdownConverter:
    """Converts PDF files to markdown using pdfplumber"""
    
    def __init__(self, pdf_dir="data/source/pdfs", markdown_dir="data/source/markdowns"):
        self.pdf_dir = Path(pdf_dir)
        self.markdown_dir = Path(markdown_dir)
        self.markdown_dir.mkdir(exist_ok=True)
        
        logger.info(f"PDF directory: {self.pdf_dir}")
        logger.info(f"Markdown directory: {self.markdown_dir}")
    
    def clean_text(self, text):
        """Clean and format text for markdown"""
        if not text:
            return ""
        
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Handle common PDF artifacts
        text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)  # Add space between camelCase
        text = re.sub(r'([.!?])([A-Z])', r'\1 \2', text)  # Add space after punctuation
        
        return text
    
    def extract_tables_to_markdown(self, page):
        """Extract tables from page and convert to markdown format"""
        tables = page.extract_tables()
        markdown_tables = []
        
        for table in tables:
            if not table or not table[0]:
                continue
                
            # Create markdown table
            markdown_table = []
            
            # Add headers
            headers = [str(cell).strip() if cell else '' for cell in table[0]]
            markdown_table.append('| ' + ' | '.join(headers) + ' |')
            markdown_table.append('|' + '|'.join(['---'] * len(headers)) + '|')
            
            # Add data rows
            for row in table[1:]:
                if row:
                    cells = [str(cell).strip() if cell else '' for cell in row]
                    markdown_table.append('| ' + ' | '.join(cells) + ' |')
            
            markdown_tables.append('\n'.join(markdown_table))
        
        return '\n\n'.join(markdown_tables)
    
    def convert_single_pdf(self, pdf_path):
        """Convert a single PDF to markdown"""
        try:
            pdf_name = pdf_path.stem
            markdown_path = self.markdown_dir / f"{pdf_name}.md"
            
            # Skip if markdown already exists
            if markdown_path.exists():
                logger.info(f"Skipping {pdf_name} - markdown already exists")
                return f"SKIPPED: {pdf_name}"
            
            logger.info(f"Converting {pdf_name}...")
            
            # Open PDF and extract content
            with pdfplumber.open(pdf_path) as pdf:
                markdown_content = []
                
                # Add title
                markdown_content.append(f"# {pdf_name.replace('_', ' ').title()}")
                markdown_content.append("")
                
                # Process each page
                for page_num, page in enumerate(pdf.pages, 1):
                    markdown_content.append(f"## Page {page_num}")
                    markdown_content.append("")
                    
                    # Extract text
                    text = page.extract_text()
                    if text:
                        cleaned_text = self.clean_text(text)
                        if cleaned_text:
                            markdown_content.append(cleaned_text)
                            markdown_content.append("")
                    
                    # Extract tables
                    tables_markdown = self.extract_tables_to_markdown(page)
                    if tables_markdown:
                        markdown_content.append("### Tables")
                        markdown_content.append("")
                        markdown_content.append(tables_markdown)
                        markdown_content.append("")
                    
                    # Add page separator
                    markdown_content.append("---")
                    markdown_content.append("")
                
                # Write markdown file
                with open(markdown_path, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(markdown_content))
                
                logger.info(f"✅ Successfully converted {pdf_name}")
                return f"SUCCESS: {pdf_name}"
                
        except Exception as e:
            logger.error(f"❌ Error converting {pdf_name}: {str(e)}")
            return f"ERROR: {pdf_name}"
    
    def convert_all_pdfs(self, max_workers=4):
        """Convert all PDFs in parallel"""
        pdf_files = list(self.pdf_dir.glob("*.pdf"))
        
        if not pdf_files:
            logger.warning(f"No PDF files found in {self.pdf_dir}")
            return
        
        logger.info(f"Found {len(pdf_files)} PDF files to convert")
        logger.info(f"Using {max_workers} parallel workers")
        
        # Track progress
        total_files = len(pdf_files)
        completed = 0
        successful = 0
        failed = 0
        
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all conversion tasks
            future_to_pdf = {
                executor.submit(self.convert_single_pdf, pdf_path): pdf_path 
                for pdf_path in pdf_files
            }
            
            # Process completed tasks
            for future in as_completed(future_to_pdf):
                pdf_path = future_to_pdf[future]
                result = future.result()
                completed += 1
                
                if result.startswith("SUCCESS"):
                    successful += 1
                elif result.startswith("SKIPPED"):
                    # Count as successful since it already exists
                    successful += 1
                else:
                    failed += 1
                
                # Log progress
                progress = (completed / total_files) * 100
                elapsed = time.time() - start_time
                eta = (elapsed / completed) * (total_files - completed) if completed > 0 else 0
                
                logger.info(f"Progress: {completed}/{total_files} ({progress:.1f}%) - "
                          f"Success: {successful}, Failed: {failed} - "
                          f"ETA: {eta/60:.1f} minutes")
        
        # Final summary
        total_time = time.time() - start_time
        logger.info(f"\n🎉 Conversion Complete!")
        logger.info(f"Total time: {total_time/60:.1f} minutes")
        logger.info(f"Total files: {total_files}")
        logger.info(f"Successful: {successful}")
        logger.info(f"Failed: {failed}")
        logger.info(f"Success rate: {(successful/total_files)*100:.1f}%")
        
        return {
            'total': total_files,
            'successful': successful,
            'failed': failed,
            'time_taken': total_time
        }
    
    def list_converted_files(self):
        """List all converted markdown files"""
        markdown_files = list(self.markdown_dir.glob("*.md"))
        logger.info(f"Found {len(markdown_files)} markdown files:")
        
        for md_file in sorted(markdown_files):
            size = md_file.stat().st_size
            logger.info(f"  - {md_file.name} ({size} bytes)")
        
        return markdown_files

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Convert PDFs to Markdown using pdfplumber")
    parser.add_argument("--pdf-dir", default="data/source/pdfs", 
                       help="Directory containing PDF files")
    parser.add_argument("--markdown-dir", default="data/source/markdowns",
                       help="Directory to save markdown files")
    parser.add_argument("--workers", type=int, default=4,
                       help="Number of parallel workers")
    parser.add_argument("--list", action="store_true",
                       help="List converted files and exit")
    
    args = parser.parse_args()
    
    converter = PDFToMarkdownConverter(args.pdf_dir, args.markdown_dir)
    
    if args.list:
        converter.list_converted_files()
        return
    
    # Convert all PDFs
    results = converter.convert_all_pdfs(args.workers)
    
    if results:
        # List converted files
        converter.list_converted_files()

if __name__ == "__main__":
    main()
