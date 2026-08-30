---
name: add-book-to-pipeline
description: Add a new book title to the MIFECO book pipeline — updates all data files, sequences, dashboards, reader magnet, and books.mifeco.com website
trigger: User provides a new book title, author, price, and optionally series/standalone/box-set designation
---

## 🔍 MemPalace Query (MANDATORY FIRST STEP)
Before proceeding, query MemPalace for existing context:
```python
import sys, os; sys.path.insert(0, os.path.expanduser('~/.hermes/mempalace'))
import embed; embed.init_embedding(os.path.expanduser('~/.hermes/mempalace'))
results = embed.search_embeddings("add book pipeline MIFECO dashboard nurture sequence website", k=5)
```
This retrieves previous decisions, domain-specific context, and lessons learned from the vector memory store.

# Add a New Book to the MIFECO Book Pipeline

When Bob writes a new book, add it to every layer of the pipeline. Update all 5 files below PLUS the reader magnet and website.

## 1. Pipeline Data — `pipeline-books.json`
**Path:** `~/.hermes/.openclaw/workspace/pipeline-engine/data/pipeline-books.json`

Add to the correct products array:
- **NBS series** → `products.titles[]` with `volume`, `title`, `price`
- **Moon book** → `products.moon_books.titles[]` with `volume`, `title`, `price`
- **Standalone** → `products.standalone[]` with `title`, `price`
- **Box set** → `products.box_sets[]` with `title`, `price`

Update `metadata.last_updated`.

## 2. Nurture Sequence — `books-nurture.json`
**Path:** `~/.hermes/.openclaw/workspace/pipeline-engine/sequences/books-nurture.json`

Add to `series.books[]` or `moon_books.books[]`. Update the **Day 1 welcome email** body — this is the catalog listing. Add the book and price.

## 3. Dashboard — `pipeline-dashboard.html`
**Path:** `~/.hermes/.openclaw/workspace/pipeline-engine/dashboard/pipeline-dashboard.html`

Update `booksPipeline.books[]` JS array (around line 916). Format:
```javascript
{ title:'Full Title', price:XX.XX, tags:['moon'] }
```
Tags: `'moon'` for moon books, `'box-set'` for bundles.

## 4. Command Center — `content-command-center.html`
**Path:** `~/.hermes/.openclaw/workspace/pipeline-engine/dashboard/content-command-center.html`

Update **em13** body (Books welcome email) — add title+price to catalog listing section.

## 5. Social Content — `data/social-content-books.json`
**Path:** `~/.hermes/.openclaw/workspace/pipeline-engine/data/social-content-books.json`

Add X post + LinkedIn post entries for the new book.

## 6. Reader Magnet — NEW
**Path:** `/home/bob/Desktop/hermesfiles/cindy-lou-series/books-mifeco-website/magnets/`

Every new series gets a reader magnet: a free novella (2,500-3,500 words) that appeals to the same audience, provides a complete experience, and hooks into Book 1.

Create:
- Markdown: `magnets/SERIES-NAME-TITLE.md`
- EPUB: via build-epub-python.py
- PDF: via pandoc

Update series landing page at `books-mifeco-website/SERIES-NAME/index.html`.

## 7. books.mifeco.com Website — NEW
**Path:** `/home/bob/Desktop/hermesfiles/cindy-lou-series/books-mifeco-website/`

Update for every new book/series:
1. Homepage `index.html` — add/update series card
2. Series landing page — add book card with cover, description, Amazon link
3. Reader magnet — add to series page
4. Email template — update email-3.html (book showcase)
5. **Deploy to DreamHost**: Use SFTP to upload to books.mifeco.com
6. **Cron job**: Weekly auto-deploy via `cronjob` tool (Mondays 9 AM). Script: `/home/bob/Desktop/hermesfiles/cindy-lou-scripts/sync-books-site.py`
7. **Subagent delegation**: Single-file tasks only per subagent. Multi-file batches (4+ pages, 3+ novellas) timeout at 600s. Delegate one file per subagent. See `references/session-patterns.md`.

## Deploy Main Site
```python
import paramiko, os
host="IAD1-SHARED-B8-42.DREAMHOST.COM"; user="dh_mwpxuu"; pw="Rm2214ri####"
ssh=paramiko.SSHClient(); ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(host, username=user, password=pw, look_for_keys=False); sftp=ssh.open_sftp()
base=os.path.expanduser("~/.hermes/.openclaw/workspace/pipeline-engine")
dst="/home/dh_mwpxuu/mifeco.com/admin"
for l,r in [("dashboard/pipeline-dashboard.html","pipeline-dashboard.html"),("dashboard/content-command-center.html","content-command-center.html"),("data/pipeline-books.json","data/pipeline-books.json"),("sequences/books-nurture.json","sequences/books-nurture.json"),("data/social-content-books.json","data/social-content-books.json")]:
    f=os.path.join(base,l); sftp.put(f,os.path.join(dst,r)) if os.path.exists(f) else None
sftp.close(); ssh.close()
```

## Cron Job — Weekly Auto-Update
The `books.mifeco.com` site is auto-updated weekly via cron:
```
0 9 * * 1 /home/bob/.hermes/hermes-agent/venv/bin/python3 /home/bob/Desktop/hermesfiles/cindy-lou-scripts/sync-books-site.py
```
This script scans for new book materials (chapters, covers, magnets) and deploys to DreamHost.
## Verify

1. Login at `https://www.mifeco.com/admin/`
2. Pipeline Dashboard → Books → check catalog
3. Content Command Center → Books emails → check listing
4. Check `https://books.mifeco.com` loads correctly
5. Test email signup at series landing page

## Bulk Status Updates (Marking Books Published)
## Rules
- **No bulk pricing** — all books sold individually
- **Store**: Amazon Kindle (placeholder URL until live)
- **AI Playbook is retired** — do not add
- **Author**: Bob Mills
- **Every series gets a reader magnet** — no exceptions
- **books.mifeco.com must be updated** for every new book/series
- **Weekly cron job** auto-deploys new materials to books.mifeco.com
- **Fan Club blurb** — Every book MUST end with the fan club mailing list blurb after the AI disclosure (see `book-deliverable-kdp` skill for exact text). The blurb directs readers to www.books.mifeco.com.
- **QR code URL** — All `qr_mifeco.png` files MUST encode `https://www.books.mifeco.com` (NOT `www.mifeco.com`). The books subdomain is the reader-facing site with series pages, magnets, and email capture.