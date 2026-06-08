# Two-Pass Cover Generation Pattern

Confirmed working pattern for high-quality book covers (Age of Lightships, May 2026).

## Why Two-Pass?

Single-pass (text in prompt baked into AI image) produces uncontrollable typography. Two-pass separates art quality from typography quality.

## Pass 1: Base Art (NO text in prompt)

Include "NO TEXT NO WORDS NO LETTERS NO WRITING" at end of prompt. Output: 1024×1024 clean art.

## Pass 2: Typography Overlay (PIL)

Crop/resize to 1024×1536, apply gradient + series label + title + author. Export: cover_final.png + cover_KDP.jpg (1600×2560).

## Pass 3: EPUB Integration

Batch-replace `EPUB/images/cover.jpg` in all EPUBs. Copy `cover_KDP.jpg` to `KDP_PACKAGE/images/cover.jpg`.

## Working Parameters (confirmed)

| Parameter | Value |
|-----------|-------|
| Working canvas | 1024×1536 (3:4) |
| KDP export | 1600×2560 JPEG, quality 95 |
| Font | LiberationSans-Bold.ttf |
| Series label | 14pt, y=15, light gray |
| Title start | y=54, iterative sizing to 80% width |
| Line spacing | 8px |
| Shadow | 4-layer (4,3,2,1px), RGBA(0,0,0,200) |
| Author | 28pt, bottom 55px bar |
| Gradient | Top 35% fade alpha 200→0, bottom bar alpha 180 |
