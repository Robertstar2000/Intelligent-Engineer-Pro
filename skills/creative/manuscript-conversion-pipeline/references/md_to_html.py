#!/usr/bin/env python3
"""
Simple Markdown to HTML Converter
Converts Markdown to HTML which can then be converted to PDF.
"""

import markdown
import sys
from pathlib import Path

def markdown_to_html(md_path, html_path=None):
    """Convert Markdown to HTML."""
    with open(md_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    html = markdown.markdown(text)
    
    if html_path is None:
        html_path = md_path.with_suffix('.html')
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{Path(md_path).stem}</title>
    <style>
        body {{ font-family: 'DejaVu Serif', serif; max-width: 800px; margin: 0 auto; padding: 20px; }}
        h1, h2, h3 {{ font-family: 'Garamond', serif; }}
        .chapter {{ margin-bottom: 2em; }}
        .mission-ai {{ background-color: #f5f5f5; padding: 10px; border-left: 4px solid #ddd; margin: 10px 0; }}
        .bridge {{ font-style: italic; color: #666; margin: 20px 0; }}
    </style>
</head>
<body>
{html}
</body>
</html>""")
    
    print(f"✅ HTML saved to {html_path}")

def main():
    if len(sys.argv) < 2:
        print("Usage: md_to_html.py <markdown_file>")
        sys.exit(1)
    
    md_path = Path(sys.argv[1])
    if not md_path.exists():
        print(f"Error: File {md_path} not found")
        sys.exit(1)
    
    html_path = md_path.with_suffix('.html')
    markdown_to_html(md_path, html_path)
    print(f"
📄 HTML file created: {html_path}")
    print("
You can now convert this HTML to PDF using a browser's print function or a tool like wkhtmltopdf.")

if __name__ == "__main__":
    main()
