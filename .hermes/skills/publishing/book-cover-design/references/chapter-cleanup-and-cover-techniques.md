# Chapter Cleanup and Cover Techniques

## Gemini via OpenRouter

Correct model: `google/gemini-2.5-flash-image` (NOT `...-preview` which 404s).

Default output is 1024x1024. For KDP covers, request 1.6:1 aspect ratio and upscale/crop with PIL LANCZOS.

## Bulk Chapter Cleanup

1. Double scene breaks: replace consecutive `<p class="scene">* * *</p>` pairs with single
2. Normalize `&mdash;` to unicode `—`
3. Remove duplicate paragraphs (>30 chars, keep first occurrence)
4. Fix p-tag mismatch after dedup (open count must equal close count)

## TOC pre to Table Conversion

Parse lines with `re.match(r'Chapter\s+(\d+)\s+(.+?)\s+(\d+)\s*$')` and convert to `<table>` with `toc-ch`, `toc-dots`, `toc-pge` cells. Replace `<pre>` block entirely.

## Cover Assembly (Two-Pass)

Pass 1: Generate background with Gemini. Pass 2: Add typography with PIL.
- Title: iterative font sizing for ~80% page width, VERY BOLD
- Author: iterative font sizing for ~50% page width, near bottom
- Shadow: 4px offset black behind white text
- Overlays: dark gradient top 35% for title, bottom 10% for author
