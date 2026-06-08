#!/usr/bin/env python3
"""Generate KDP-compliant EPUB3 files for a book series. 3 variants per book."""
import os, re, glob
from datetime import datetime
from ebooklib import epub

AUTHOR = "Author Name"
SERIES_NAME = "Series Name"
BASE_DIR = "/path/to/series"

BOOKS = {
    "Book_Dir": {"title": "Title", "subtitle": "Series - Book 1", "book_num": 1,
                 "manuscript_dir": "manuscript_src", "has_manuscript": True,
                 "description": "Description.", "keywords": ["fiction"]},
}
PLACEHOLDERS = {"Book_Dir": ["Chapter 1", "Chapter 2"]}
AUTHOR_BIO = "Author bio paragraph 1.\n\nAuthor bio paragraph 2."
AI_DISCLOSURE = "This book was created with AI assistance."

def get_cover(bd):
    gd = os.path.join(bd, "generated_images")
    if os.path.exists(gd):
        for f in sorted(os.listdir(gd)):
            if 'cover' in f.lower() and f.endswith(('.png','.jpg','.jpeg')):
                return os.path.join(gd, f)
    return None

def md_to_html(md):
    html = re.sub(r'^#\s+.+?\n+', '', md, count=1, flags=re.MULTILINE)
    html = re.sub(r'^---\s*$', '<hr/>', html, flags=re.MULTILINE)
    lines = html.split('\n'); result, inp = [], False
    for line in lines:
        s = line.strip()
        if s == '<hr/>':
            if inp: result.append('</p>'); inp = False
            result.append(s)
        elif s:
            if not inp: result.append('<p>'); inp = True
            result.append(s)
        else:
            if inp: result.append('</p>'); inp = False
    if inp: result.append('</p>')
    html = '\n'.join(result)
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    return html

def read_chapters(bd, md):
    ch = []
    if not md: return ch
    d = os.path.join(bd, md)
    if not os.path.exists(d): return ch
    for fp in sorted(glob.glob(os.path.join(d, "ch*.md"))):
        with open(fp) as f: c = f.read()
        t = os.path.basename(fp).replace('.md','')
        m = re.search(r'^#\s+(.+)$', c, re.MULTILINE)
        if m: t = m.group(1)
        ch.append((t, md_to_html(c)))
    return ch

def placeholder_chapters(bk):
    return [(t, f'<p>Placeholder for {t}.</p>') for t in PLACEHOLDERS.get(bk, [])]

CSS = "body{margin:0;padding:0;}h1{text-align:center;font-size:1.5em;margin:1em 0;font-weight:bold;}h2{text-align:center;font-size:1.2em;margin:.8em 0;}p{text-indent:1.5em;margin:.3em 0;line-height:1.5;}.title-page{text-align:center;padding-top:30%;page-break-after:always;}.toc-table{width:100%;table-layout:auto;border-collapse:collapse;}.toc-table td{padding:.15em 0;border:none;vertical-align:baseline;}.toc-ch{white-space:nowrap;padding-right:.5em;}.toc-dots{width:100%;border-bottom:1px dotted #888;}.toc-pge{width:2em;white-space:nowrap;text-align:right;}.cover{text-align:center;margin-top:1em;}.cover img{max-width:100%;height:auto;}.about-author{page-break-before:always;text-align:center;margin-top:2em;}.about-author p{text-indent:0;text-align:center;margin:.5em 0;}"

def create_epub(bk, bi, variant):
    bd = os.path.join(BASE_DIR, bk)
    od = os.path.join(bd, "output")
    os.makedirs(od, exist_ok=True)
    book = epub.EpubBook()
    book.set_identifier(f"series-{bi['book_num']}-{variant}")
    book.set_title(f"{bi['title']}: {bi['subtitle']}")
    book.set_language('en')
    book.add_author(AUTHOR)
    book.add_metadata('DC', 'series', SERIES_NAME)
    book.add_metadata('DC', 'position', str(bi['book_num']))
    book.add_metadata('DC', 'description', bi['description'])
    for kw in bi.get('keywords', []):
        book.add_metadata('DC', 'subject', kw)
    year = datetime.now().year
    book.add_metadata('DC', 'date', datetime.now().strftime('%Y-%m-%d'))
    book.add_metadata('DC', 'publisher', 'MIFECO Publishing')
    book.add_metadata('DC', 'rights', f'Copyright &copy; {year} {AUTHOR}. All rights reserved.')
    cp = get_cover(bd)
    if cp and os.path.exists(cp):
        with open(cp, 'rb') as f: cd = f.read()
        ext = os.path.splitext(cp)[1].lower()
        mime = 'image/jpeg' if ext in ('.jpg','.jpeg') else 'image/png'
        book.add_item(epub.EpubItem(uid='cover-image', file_name='images/cover'+ext, media_type=mime, content=cd))
    book.add_item(epub.EpubItem(uid="style", file_name="style/nav.css", media_type="text/css", content=CSS))
    def page(title, body, fname):
        p = epub.EpubHtml(title=title, file_name=fname, lang='en')
        p.content = body
        p.add_link(href='style/nav.css', rel='stylesheet', type='text/css')
        book.add_item(p)
        return p
    spine, te = [], []
    cb = '<div class="cover">' + (f'<img src="images/cover{os.path.splitext(cp)[1]}" alt="Cover"/>' if cp else f'<h1>{bi["title"]}</h1>') + '</div>'
    spine.append(page('Cover', cb, 'cover.xhtml'))
    spine.append(page('Title', f'<div class="title-page"><h1>{bi["title"]}</h1><p>{bi["subtitle"]}</p><p><strong>{AUTHOR}</strong></p></div>', 'title.xhtml'))
    spine.append(page('Copyright', f'<div style="text-align:center;margin-top:15%;"><p>Copyright &copy; {year} {AUTHOR}. All rights reserved.</p><p>{AI_DISCLOSURE}</p></div>', 'copyright.xhtml'))
    chs = read_chapters(bd, bi.get('manuscript_dir')) if bi.get('has_manuscript') else placeholder_chapters(bk)
    tb = '<div style="page-break-before:always;"><h1>Contents</h1><table class="toc-table">'
    for i, (ct, _) in enumerate(chs, 1):
        fn = f'chap_{i:02d}.xhtml'
        tb += f'<tr><td class="toc-ch"><a href="{fn}">Chapter {i} &mdash; {ct}</a></td><td class="toc-dots"></td><td class="toc-pge"></td></tr>'
        te.append(epub.Link(fn, f'Chapter {i}: {ct}', f'chap_{i:02d}'))
    tb += '</table></div>'
    spine.append(page('Contents', tb, 'toc.xhtml'))
    for i, (ct, cc) in enumerate(chs, 1):
        spine.append(page(f'Chapter {i}', f'<div><h2>Chapter {i}</h2><h3>{ct}</h3>{cc}</div>', f'chap_{i:02d}.xhtml'))
    ab = '<div class="about-author"><h2>About the Author</h2>' + ''.join(f'<p>{l}</p>' for l in AUTHOR_BIO.split('\n\n')) + '</div>'
    spine.append(page('About Author', ab, 'about.xhtml'))
    book.toc = te
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    book.spine = spine
    fn = f"{bk}_{variant}.epub"
    fp = os.path.join(od, fn)
    epub.write_epub(fp, book, {})
    print(f"  {fn} ({os.path.getsize(fp)/1024:.0f} KB)")
    return fp

if __name__ == "__main__":
    for bk, bi in BOOKS.items():
        print(f"{bk}:")
        for v in ["digital","paperback","hardcover"]:
            create_epub(bk, bi, v)
    print("Done!")
