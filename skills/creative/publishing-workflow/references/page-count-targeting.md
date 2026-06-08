# Page Count Targeting for 6x9" Condensed Books

Target range: **150-190 pages** for a 6x9" trade paperback.

## Word Count Targets

| Format | Words per page | Total words for 150 pages | Total words for 190 pages |
|--------|:-------------:|:------------------------:|:------------------------:|
| Dense (small font) | 270 | 40,500 | 51,300 |
| Standard | 250 | 37,500 | 47,500 |
| Loose (large font) | 230 | 34,500 | 43,700 |

**Rule of thumb:** ~1,200-1,600 words per chapter × 30 chapters = ~36,000-48,000 chapter words. Add ~5,000 words for front/back matter (title page, copyright, TOC, back matter, series sales pitch).

## Verifying PDF Page Count

After generating a PDF with WeasyPrint, check page count using pypdf:

```python
from pypdf import PdfReader
reader = PdfReader("/path/to/book.pdf")
print(f"{len(reader.pages)} pages")
```

## Adjusting Page Count

**Too short (< 150 pages):**
- Re-expand condensed chapters by adding back descriptive passages
- Increase font size or line spacing in CSS
- Add front/back matter (series bibliography, author bio, fan club blurb, AI disclosure)

**Too long (> 190 pages):**
- Remove redundant internal monologue
- Tighten dialogue (cut "he said"/"she said" tags)
- Merge short scene breaks
- Reduce chapter-intro atmospheric description
- Target 1,000-1,200 words per chapter instead of 1,300-1,500

## Example: Cindy Lou Legal Capers Condensation

| Book | Original words | Condensed words | PDF pages | Method |
|------|:------------:|:--------------:|:--------:|--------|
| Retainer to Trouble | 103,768 | 36,517 | 174 | Rewrote each chapter from ~3,500 to ~1,200 words |
| Clause for Alarm | 109,869 | 33,781 | 160 | Rewrote each chapter from ~3,500 to ~1,100 words |
| Affidavits and Alibis | 119,732 | 43,274 | 186 | Rewrote chapters ~1-15, lighter pass on 16-30 |

All three books kept every plot beat, the first-person voice, the humor, and the NYC setting while cutting ~65% of the word count.