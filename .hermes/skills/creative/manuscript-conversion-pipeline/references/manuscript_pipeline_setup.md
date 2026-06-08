# Manuscript Conversion Pipeline Setup Guide

## Overview
This pipeline converts Markdown manuscripts to PDF, EPUB, and Kindle MOBI formats.

## Prerequisites

### 1. Install Pandoc (for Markdown to PDF/EPUB conversion)
**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install -y pandoc texlive-xetex texlive-fonts-recommended
```

**macOS:**
```bash
brew install pandoc --cask
brew install --cask mactex
```

**Windows:**
Download and install from https://pandoc.org/installing.html

### 2. Install KindleGen (for MOBI generation)
KindleGen is available from Amazon but is now deprecated. You can use:
- The `ebook-convert` tool from Calibre
- Or download KindleGen from Amazon's archives

**Alternative: Install Calibre**
**Ubuntu/Debian:**
```bash
sudo apt-get install calibre
```

**macOS:**
```bash
brew install --cask calibre
```

**Windows:**
Download from https://calibre-ebook.com/

### 3. Install Python Dependencies
```bash
pip install markdown
```

## Pipeline Script

Create a file called `manuscript_pipeline.py` with the following content:

```python
#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path

def convert_to_pdf(md_path, pdf_path):
    """Convert Markdown to PDF using Pandoc."""
    print(f"📄 Converting {md_path} to PDF...")
    subprocess.run([
        "pandoc", str(md_path),
        "-o", str(pdf_path),
        "--pdf-engine=xelatex",
        "--variable=mainfont='DejaVu Serif'",
        "--variable=fontsize=12pt",
        "--variable=geometry:margin=1in",
        "--toc"
    ], check=True)
    print(f"✅ PDF saved to {pdf_path}")

def convert_to_epub(md_path, epub_path):
    """Convert Markdown to EPUB using Pandoc."""
    print(f"📚 Converting {md_path} to EPUB...")
    subprocess.run([
        "pandoc", str(md_path),
        "-o", str(epub_path),
        "--toc"
    ], check=True)
    print(f"✅ EPUB saved to {epub_path}")

def convert_to_kindle(md_path, mobi_path):
    """Convert Markdown to Kindle MOBI using Calibre."""
    print(f"🔥 Converting {md_path} to Kindle MOBI...")
    # Convert to EPUB first, then to MOBI
    temp_epub = Path("temp.epub")
    convert_to_epub(md_path, temp_epub)
    
    subprocess.run([
        "ebook-convert", str(temp_epub), str(mobi_path),
        "--output-format=mobi"
    ], check=True)
    print(f"✅ Kindle MOBI saved to {mobi_path}")
    
    # Clean up temp file
    if temp_epub.exists():
        temp_epub.unlink()

def main():
    if len(sys.argv) < 2:
        print("Usage: pipeline.py <markdown_file> [output_directory]")
        sys.exit(1)
    
    md_path = Path(sys.argv[1])
    if not md_path.exists():
        print(f"Error: File {md_path} not found")
        sys.exit(1)
    
    output_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else md_path.parent
    output_dir.mkdir(exist_ok=True)
    
    base_name = md_path.stem
    pdf_path = output_dir / f"{base_name}.pdf"
    epub_path = output_dir / f"{base_name}.epub"
    mobi_path = output_dir / f"{base_name}.mobi"
    
    print(f"🚀 Starting conversion for: {md_path.name}")
    print(f"📁 Output directory: {output_dir}")
    print(f"📄 PDF: {pdf_path.name}")
    print(f"📚 EPUB: {epub_path.name}")
    print(f"🔥 Kindle MOBI: {mobi_path.name}")
    print("-" * 50)
    
    try:
        convert_to_pdf(md_path, pdf_path)
        print()
        convert_to_epub(md_path, epub_path)
        print()
        convert_to_kindle(md_path, mobi_path)
        print()
        print("✅ All conversions complete!")
        print(f"📄 PDF: {pdf_path}")
        print(f"📚 EPUB: {epub_path}")
        print(f"🔥 Kindle MOBI: {mobi_path}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Conversion failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

## Usage

1. Place your manuscript Markdown file in a directory
2. Run the pipeline:
```bash
python manuscript_pipeline.py your_manuscript.md
```

3. The pipeline will generate:
   - PDF: for print and digital distribution
   - EPUB: for most e-readers
   - MOBI: for Kindle devices
4. After conversion, do a final publication-polish review of the generated artifacts before delivery:
   - reopen the HTML/PDF and spot-check front matter, TOC, mid-book, and ending pages
   - verify TOC ordering and, if used, recompute printed page numbers from the near-final PDF
   - remove placeholders, duplicate headings, editor notes, and leftover scaffolding text
   - fix any last grammar, punctuation, or formatting inconsistencies

## KDP Publishing Specifications

For Amazon KDP, you may want to customize the PDF output:

```bash
pandoc manuscript.md -o output.pdf   --pdf-engine=xelatex   --variable=paper-size=6in×9in   --variable=trim:6in:9in   --variable=mainfont='Garamond'   --variable=fontsize=12pt   --variable=geometry:margin=0.75in   --toc
```

## Notes

- The first run will download and cache the tools (Pandoc, KindleGen) via uvx
- Subsequent runs will use the cached versions
- Make sure your Markdown file includes proper front matter (title, author, etc.)
- For best results, use UTF-8 encoding and standard Markdown syntax

## Troubleshooting

If you encounter issues:
1. Check that Pandoc and Calibre are installed and in your PATH
2. Verify the Markdown file is valid
3. Check file permissions for output directory
4. Look at error messages for specific problems
