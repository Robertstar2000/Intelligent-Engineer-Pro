# EPUB Generation Pitfalls

## EpubHtml.content is Body-Only
Set `.content` to body HTML ONLY. NEVER include DOCTYPE/head tags. Full documents crash with "Document is empty".

## set_cover() Creates Duplicate Empty cover.xhtml
Don't mix `set_cover()` with manual cover xhtml pages. Use one approach only.

## Gemini Image Model
Use `google/gemini-2.5-flash-image` (NOT `-preview` which 404s).

## KDP Sign-In Requires OTP
Always stops for user-provided OTP code.

## Long-Running Tasks
Use `terminal(background=True)` with log file. Check `tail` not `process(poll)`.

## Bulk Manuscript Writing
Write each chapter to disk immediately. ~10-15s per chapter.

## Chapter Cleanup (4 Fixes)
1. Duplicate paragraphs — remove second occurrences
2. Double scene breaks — collapse to single
3. Mixed em-dashes — normalize to unicode
4. P-tag mismatch — verify counts after dedup

## Cover Image Sizing
Gemini defaults to 1024x1024. Request 1.6:1 aspect ratio for KDP covers, then upscale/crop with PIL LANCZOS.