# Page Count Target Reference

## 6x9" Trade Paperback

Formula: total_pages = (word_count / 275) + 6

## Target Ranges

| Pages | Words | Status |
|-------|-------|--------|
| < 160 | < 44,000 | P0 -- Too short, must expand |
| 160-190 | 44,000-52,000 | OK In range |
| 190-220 | 52,000-60,000 | P1 -- Slightly over |
| > 220 | > 60,000 | P1 -- Significantly over |

## User Directive

The actual target is 180 pages at 6x9" format = ~50,000 words. This is the universal target for all full-length books. Word counts above 52K are OVER target, not under.

## Critical Pitfall: Drifting from 50K Target

During long sessions, the todo list may drift to inflated targets (80K, 100K, 110K). Always verify against the 180-page / 50K-word standard. If the todo list says 80K+, correct it to 50K immediately.

## Pitfall: write_file Token Limits

When expanding large manuscripts, write_file() has an ~8K token limit. For large expansions: (1) Write expansion content to an external .txt file first, (2) Use a Python script to read and apply, (3) Use cat >> for small appends, (4) Verify word count after each expansion.