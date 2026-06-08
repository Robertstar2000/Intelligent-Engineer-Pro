# Manuscript Heading Patterns

Reference of heading formats found across Bob Mills' book manuscripts.
Use `grep -n '^#' manuscript.md | head -30` to detect before writing any parser.

## No Blue Sky Series (5 Mars books)

| Book | File | Heading Format | Example |
|------|------|---------------|---------|
| I — First Generation | `First_Generation_Manuscript.md` | `## Chapter N — Title` | `## Chapter One — Built From Dust` |
| II — Second Generation | `SECOND_GENERATION_FULL_MANUSCRIPT.md` | `# Chapter N — Title` (mostly), mix of `## Chapter N — Title` in parts | `# Chapter 1 — The Welcome Fleet` |
| III — Third Generation | `Third_Generation_Manuscript.md` | `## Chapter N — Title` (ch1-16), `# Chapter N: Title` (ch17-24), then back to `##` | `## Chapter 1 — The First Resonance` |
| IV — Moon Base: The Beginning | `Moon_Base_The_Beginning/manuscript.md` | `## Chapter N — Title` (Mission AI voice pattern) | `## Chapter 1 — The Artemis Accord` |
| V — Moon Base: Homecoming | `Moon_Base_Homecoming/manuscript.md` | `## Chapter N — Title` | `## Chapter 1 — The Observatory Rising` |

## Other Books

| Book | File | Heading Format | Example |
|------|------|---------------|---------|
| Tomorrow Remembered | `Tomorrow_Remembered_Manuscript.md` | `# Chapter N: Title` (Part One structured) | `# Chapter One: The Shock` |

## Key Insight

**The majority use `## Chapter N` (level-2 headings), not `# Chapter N` (level-1).**
This is the opposite of what a naive parser expects. Always detect first.
