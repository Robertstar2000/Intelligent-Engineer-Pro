# Page Count Target Reference

## The 160-190 Page Rule

The user's standard: **Every full-length book must fit 160-190 pages at 6x9" trim.**

This is a hard requirement, not a guideline. Books below 160 pages need expansion. Books above 190 pages need trimming or tighter formatting.

## Word Count to Page Count Conversion

At 6x9" with WeasyPrint default formatting (11pt, 1in margins):
- ~300 words per page → 160 pages = ~48K words, 190 pages = ~57K words

At 6x9" with tighter formatting (10pt, 0.7in margins, 1.35 line-height):
- ~370 words per page → 160 pages = ~59K words, 190 pages = ~70K words

**Practical target:** Aim for 50K-70K words depending on formatting density.

## Page Count Estimation

```bash
# Quick check: word count
wc -w MANUSCRIPT.md

# Estimate pages at default 6x9" formatting
python3 -c "print(f'{len(open(\"MANUSCRIPT.md\").read().split()) // 300} pages at default format')"

# Estimate pages at tight 6x9" formatting
python3 -c "print(f'{len(open(\"MANUSCRIPT.md\").read().split()) // 370} pages at tight format')"
```

## PDF Generation Settings for Page Count Control

| Setting | Value | WPP | Effect |
|---------|-------|-----|--------|
| Default | 11pt, 1in margins, 1.5 line-height | ~300 | Standard readability |
| Tight | 10pt, 0.7in margins, 1.35 line-height | ~370 | +23% more content per page |
| Compact | 9.5pt, 0.6in margins, 1.25 line-height | ~430 | +43% more content per page |

Use tighter settings for books that are slightly over 190 pages (no content changes needed).
Use expansion for books under 160 pages (content must grow).

## Check During Editorial Review

Every review MUST include the page count estimate. Add this to the review:

```markdown
### Page Count Check

| Metric | Value | Target |
|--------|-------|--------|
| Word count | N | 50K-70K |
| Est. pages (default) | N | 160-190 |
| Est. pages (tight) | N | 160-190 |
| Status | ✅/⚠️ | — |
```

If below 160 pages at tight formatting → P0 issue: "Book is N pages short. Expand by adding [genre-appropriate content: case studies for business, scenes for fiction, vignettes for memoir]"

If above 190 pages at default formatting → P1 issue: "Book is N pages over. Use tighter PDF formatting (10pt, 0.7in margins) OR trim content."

## What NOT to Do

- Do NOT pad with filler paragraphs, repeated scenes, or AI-generated content
- Do NOT add new characters or subplots unless they serve the existing story
- Expansion content must be A-quality, genre-appropriate, and consistent with existing characters/voice
- Cutting content must preserve the narrative arc, voice, and emotional beats