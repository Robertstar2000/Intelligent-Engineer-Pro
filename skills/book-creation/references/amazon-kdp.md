# Amazon KDP Reference — ASINs, Links, Monitor

## Known ASINs (update when new books publish)

| Book | ASIN | Price |
|------|------|-------|
| Tomorrow Remembered | B0GX2XC5YF | $3.99 |
| AI That Works for Small Business | B0H15NLBW8 | $2.99 |
| Built from Dust (NBS 1) | B0GX2YJ92K | $2.99 |
| The Owner's Manual for AI Agents | B0H1KSCRYC | $3.99 |

## ASIN Lookup

Search Amazon for "Bob J Mills":
```
https://www.amazon.com/s?k=%22Bob+J+Mills%22&i=digital-text
```

Extract ASINs via DevTools console:
```javascript
Array.from(document.querySelectorAll('[data-asin]')).map(e => e.getAttribute('data-asin')).filter(a => a.length > 5)
```

## Amazon Link Format

- Use ASIN-based: `https://www.amazon.com/dp/[ASIN]`
- Always use ASIN (not author page) for direct book links
- In JS: `<a href="https://www.amazon.com/dp/${asin}">Buy on Kindle</a>`

## Weekly Amazon Book Monitor

Cron job runs every Monday at 9 AM:
- Job ID: `b111a8678866`
- Script: `~/.hermes/scripts/amazon-book-monitor.py`
- Schedule: `0 9 * * 1`
- Toolset: terminal, browser, file

Run manually: `python3 ~/.hermes/scripts/amazon-book-monitor.py`
Check status: `hermes cron list`

## Pipeline Dashboard Updates

When adding/updating books:
1. Add `asin` field to book entry in `pipeline-books.json`
2. Add `asin` field to `booksCatalog` array in `pipeline-dashboard.html`
3. Render function generates Amazon link using `b.asin`
4. Sync: `bash ~/.hermes/scripts/dashboard-sync.sh`

## Series Description Format (MANDATORY for every series)

Save as `SERIES_DESCRIPTION.txt` in series root directory.

**HARD LIMIT: 4,000 characters max.** First draft: ~3,000-3,200 chars.

**Must include:**
1. Series tagline — one sentence
2. Series hook — 2-3 paragraphs (marketing prose)
3. Book-by-book breakdown — 2-3 sentences per book
4. Themes — 3-5 bullets
5. Market position — comp titles
6. Series stats — books, chapters, word count
7. Call to action — "Available on Amazon Kindle and Paperback" + website

**Format example:**
```
[Series Title]
[Tagline]

[Hook paragraph]

[Book 1 — 2-3 sentences]
[Book 2 — 2-3 sentences]
[Book 3 — 2-3 sentences]
[Book 4 — 2-3 sentences]

THEMES:
• [Theme 1]
• [Theme 2]
• [Theme 3]

Perfect for fans of [comp] and [comp].

[N books. N chapters. One journey.]

Available on Amazon Kindle and Paperback.
www.mifeco.com
```

**Each book's `Book_Description.txt` MUST reference the series:**
- First line: "THE SERIES NAME — Book N of X"
- End with "Also in series: Book 1... Book 2..."

## Books NOT on Amazon Yet (Coming Soon)

- No Blue Sky 2-5 (The Oxygen Gamble, Rivers Under Mars, The Red Charter, The First Martian Nation)
- Lunar Foundation 1-4 (Moon Rock, Mooncoming, Waters End, Waters Horizon)
- Age of Lightships 1-4 (Sunward Exodus, The Mercury Accord, Ghosts Beyond Neptune, The Last Photon Fleet)
- Cindy Lou Legal Capers 1-3 (Retainer to Trouble, Clause for Alarm, Affidavits and Alibis)
- The Crisis Ready Company

## Cover Generation — Image Generation LLM Only

ALL book covers MUST use image generation LLM — NOT Python/matplotlib/generate_cover.py.

**Business book reference style:**
- Dark navy/black background (#0a0a1a)
- White bold sans-serif title stacked 3-4 lines
- Title width = 80% cover width
- Amber/gold accent, "A Business Book" tagline
- Author name at bottom

**Science fiction reference style:**
- Dramatic space imagery, deep blacks/blues with warm amber accents
- Series label at top: "Series Name • Book N"
- 4-layer shadow for title depth
- Top 40% dark for title overlay

**KDP export:** 1600×2560 px JPEG (1.6:1), RGB, ≤50MB

Source covers:
- Business: `/home/bob/books/Business_Series/AI_That_Works/MIFECO_AI_Playbook_Cover.png`
- Sci-fi: `/home/bob/books/Lunar_Foundation_Series/Book_1_Moon_Rock/LF_1_Moon_Rock_Cover.png`
