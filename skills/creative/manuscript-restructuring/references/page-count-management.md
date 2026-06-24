# PDF Page Count Management

## Page Count Targets (from user session 2026-06-18)
- **Maximum**: 275 pages for all books (fiction and business)
- **Minimum**: 160 pages for all books
- **Fiction**: 6×9" format, ~250-300 words per page with images
- **Business**: 8.5×11" format, ~350-400 words per page with charts

## Word Count Targets for 160-275 Pages
| Format | Min Words | Max Words | Notes |
|--------|-----------|-----------|-------|
| 6×9" fiction | 40,000 | 70,000 | With B&W chapter images |
| 8.5×11" business | 55,000 | 85,000 | With charts/infographics |
| 6×9" memoir | 35,000 | 60,000 | With B&W images |

## Build Script
The reliable build script is at `/tmp/build_book_pdf.py` (and should be saved to scripts/).
- Uses WeasyPrint with CSS page size configuration
- Converts all images to B&W (grayscale)
- Handles image paths from `chapter_images/`, `images/`, `charts/` directories
- Fiction: 6×9" with 0.65-0.75in margins
- Business: 8.5×11" with 0.7-0.85in margins

## Subagent Timeout Warning
Large manuscript expansion tasks (adding 10k+ words) cause delegate_task subagents to time out after 1200s. For expansions larger than 5k words, either:
1. Do the writing directly in the parent session
2. Break into multiple smaller subagent tasks (each < 3k words)
3. Use a single subagent with a very specific, narrow scope

## Content Expansion Patterns
For business books, effective expansion includes:
- Adding new chapters on related topics
- Expanding existing chapters with more detailed case studies
- Adding reader exercises to each chapter (these add ~200-500 words each)
- Adding appendices (checklists, templates, quick-reference guides)
- Adding a detailed table of contents

For fiction books, effective expansion includes:
- Adding sensory detail and scene-setting
- Expanding dialogue with character-specific voices
- Adding subplots and secondary character arcs
- Adding technical/domain-specific detail
