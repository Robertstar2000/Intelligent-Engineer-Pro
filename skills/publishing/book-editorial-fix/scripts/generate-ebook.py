"""Generate EPUB and PDF from MANUSCRIPT.md using ebooklib and WeasyPrint.

Usage:
    python3 generate_ebook.py /path/to/book/dir

This regenerates both .epub and .pdf in the book's root directory.
Handles multiple chapter header formats (## Chapter N:, # Chapter N —, worded numbers).
"""

import os, sys, re, html as html_lib
from ebooklib import epub
from weasyprint import HTML
from PyPDF2 import PdfReader

def slugify(text):
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')

def md_to_html(text):
    """Convert markdown to HTML body for EPUB/PDF embedding."""
    # Escape HTML entities first, then apply markdown formatting
    text = html_lib.escape(text)
    
    # Headers
    text = re.sub(r'^### (.*?)$', r'</p><h3>\1</h3><p>', text, flags=re.MULTILINE)
    text = re.sub(r'^## (.*?)$', r'</p><h2>\1</h2><p>', text, flags=re.MULTILINE)
    text = re.sub(r'^# (.*?)$', r'</p><h1>\1</h1><p>', text, flags=re.MULTILINE)
    
    # Inline formatting
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)
    
    # Images
    text = re.sub(r'!\[\]\(([^)]+)\)', r'<img src="\1" style="max-width:100%;max-height:4in;" alt="illustration"/>', text)
    
    # Paragraphs and horizontal rules
    text = re.sub(r'\n\n', r'</p><p>', text)
    text = re.sub(r'---', r'</p><hr/><p>', text)
    
    return f'<p>{text}</p>'

def build_epub(ms_path, title, author, slug):
    """Build EPUB3 using ebooklib."""
    with open(ms_path, 'r') as f:
        md = f.read()
    
    html_body = md_to_html(md)
    
    book = epub.EpubBook()
    book.set_identifier(slug)
    book.set_title(title)
    book.set_language('en')
    book.add_author(author)
    
    css = '''@page { margin: 1em; }
body { font-family: Georgia, serif; font-size: 11pt; line-height: 1.5; }
h1 { font-size: 18pt; margin-top: 2em; text-align: center; }
h2 { font-size: 14pt; margin-top: 1.5em; }
h3 { font-size: 12pt; margin-top: 1em; }
p { text-align: justify; text-indent: 1em; margin: 0.3em 0; }
img { max-width: 100%; height: auto; }'''
    
    style = epub.EpubItem(uid="style", file_name="style/epub.css", media_type="text/css", content=css)
    book.add_item(style)
    
    ch = epub.EpubHtml(title=title, file_name='ch01.xhtml', lang='en')
    ch.content = f'<html><head><link rel="stylesheet" type="text/css" href="style/epub.css"/></head><body>{html_body}</body></html>'
    ch.add_item(style)
    book.add_item(ch)
    book.toc = [epub.Link('ch01.xhtml', title, 'ch01')]
    book.spine = ['nav', ch]
    
    epub_path = os.path.join(os.path.dirname(ms_path), f"{slug}.epub")
    epub.write_epub(epub_path, book)
    return epub_path

def build_pdf(ms_path, title, slug):
    """Build 6x9 PDF using WeasyPrint with tight formatting for target page count."""
    with open(ms_path, 'r') as f:
        md = f.read()
    
    html_body = md_to_html(md)
    
    # Tighter formatting: 10pt font, 0.7in margins, tighter line height
    # Adjust font-size up/down to hit 160-190 page target
    full_html = f'''<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
@page {{ size: 6in 9in; margin: 0.7in; }}
body {{ font-family: Georgia, serif; font-size: 10pt; line-height: 1.35; }}
h1 {{ font-size: 15pt; margin-top: 1.5em; page-break-before: always; text-align: center; }}
h1:first-of-type {{ page-break-before: avoid; }}
h2 {{ font-size: 12pt; margin-top: 1.2em; }}
h3 {{ font-size: 11pt; margin-top: 0.8em; }}
p {{ text-align: justify; text-indent: 1em; margin: 0.15em 0; }}
img {{ max-width: 100%; max-height: 4in; }}
</style></head><body>{html_body}</body></html>'''
    
    pdf_path = os.path.join(os.path.dirname(ms_path), f"{slug}.pdf")
    HTML(string=full_html).write_pdf(pdf_path)
    return pdf_path

def estimate_pages(word_count):
    """Estimate 6x9 PDF pages from word count.
    
    At 10pt font with 0.7in margins: ~370 words per page
    At 11pt font with 1in margins: ~300 words per page
    Target: 160-190 pages → ~52K-70K words"""
    return word_count // 370

if __name__ == '__main__':
    book_dir = sys.argv[1] if len(sys.argv) > 1 else '.'
    ms_path = os.path.join(book_dir, 'MANUSCRIPT.md')
    
    # Try alternative manuscript names if MANUSCRIPT.md is a stub
    for alt in ['retainer-to-trouble_MANUSCRIPT.md', 'clause-for-alarm_MANUSCRIPT.md', 
                'affidavits-and-alibis_MANUSCRIPT.md']:
        alt_path = os.path.join(book_dir, alt)
        alt_size = os.path.getsize(alt_path) if os.path.exists(alt_path) else 0
        ms_size = os.path.getsize(ms_path) if os.path.exists(ms_path) else 0
        if alt_size > ms_size:
            ms_path = alt_path
    
    if not os.path.exists(ms_path):
        print(f"ERROR: No manuscript found at {ms_path}")
        sys.exit(1)
    
    with open(ms_path) as f:
        content = f.read()
    words = len(content.split())
    
    # Derive title from first heading
    title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else os.path.basename(book_dir)
    slug = slugify(title)
    
    print(f"Building: {title}")
    print(f"  Words: {words:,}")
    print(f"  Est. pages (10pt): {estimate_pages(words)}")
    
    epub_path = build_epub(ms_path, title, "Bob J Mills", slug)
    pdf_path = build_pdf(ms_path, title, slug)
    
    reader = PdfReader(pdf_path)
    print(f"  EPUB: {os.path.getsize(epub_path)//1024}KB")
    print(f"  PDF: {os.path.getsize(pdf_path)//1024}KB, {len(reader.pages)} pages")
    print(f"  Target: 160-190 pages. {'✅ ON TARGET' if 160 <= len(reader.pages) <= 190 else f'⚠️ {len(reader.pages)}p — needs {\"expansion\" if len(reader.pages) < 160 else \"trimming\"}'}")