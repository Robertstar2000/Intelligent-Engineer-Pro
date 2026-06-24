# Page Count Expansion Strategy

## Pattern That Works

When a book is below 160 pages (P0 blocker), use this expansion pattern:

### Step 1: Identify Shortest Chapters
Run word count per chapter, sort ascending. Target chapters under 2,500 words.

### Step 2: Target and Expand
- Target chapters under 2,500 words
- Add 800-1,500 words per chapter
- Use delegate_task with 2-3 chapters per subagent
- Each subagent reads the manuscript, expands assigned chapters, writes back via patch

### Step 3: Expansion Techniques
1. Deepen character interiority (thoughts, memories, sensory details)
2. Add dialogue exchanges that reveal character and advance themes
3. Expand scenes with specific concrete details (not vague filler)
4. Add subplots/character moments that enrich narrative
5. Apply humanizer skill (remove AI-isms, vary rhythm, add personality)
6. Maintain existing prose style

### Step 4: Rebuild and Verify
- Rebuild PDF after each round
- Check page count: words / 275 + 6 = total pages
- Target: 44,000+ words for 160+ pages

### Multiple Rounds Are Normal
Books often need 2-3 expansion rounds. Each round adds 5,000-10,000 words.

## Gemini Image Generation Notes

- Model: google/gemini-2.5-flash-image via OpenRouter
- Response format: choices[0].message.images[0].image_url.url (nested dict, not flat string)
- 1.5-2 second delay between requests to avoid rate limits
- Resize to 440x439px at 150 DPI for print

## TOC Sync After Expansion

After each expansion round, rebuild PDF (2-pass TOC build handles page number updates). Verify TOC page numbers match actual chapter locations. The _extract_toc_pages() function in step_pdf.py handles this automatically.
