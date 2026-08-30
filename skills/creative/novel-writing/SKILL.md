---
name: novel-writing
description: >
  Write full novel-length works using parallel subag
triggers:
  - writing a novel
  - writing chapters
  - multi-chapter fiction
  - book writing
  - creative writing large project
---

## Memory context (Hindsight)

Long-term memory context is now provided automatically by Hindsight (bank
`mifeco-default`) on every turn — the retired MemPalace manual query step no
longer applies. Do NOT attempt to import `~/.hermes/mempalace` (it was removed
2026-08-19).This retrieves previous decisions, domain-specific context, and lessons learned from the vector memory store.

## Novel-Length Creative Writing via Parallel or Sequential Subagents

## Overview

Write complete novels using either parallel subagents (for new works) or sequential writing (for continuing existing works). Each approach involves subagents writing chapters from a detailed specification, reading prior chapters for style/continuity, and saving independently. The orchestrator verifies completeness and corrects failures.

**Core principle:** Don't write the novel yourself. Write the spec, spawn agents or write sequentially, verify outputs, repeat.

**Key insight from Second Generation project:** When creating a sequel that builds on an established universe, invest extra time in:
1. Reading multiple existing chapters to calibrate to the established voice and style
2. Creating detailed character evolution guides showing how characters change from previous books
3. Developing a clear narrative arc for the AI/narrator character that shows growth across books
4. Ensuring technological elements show progression and maturity from the previous book

**Sequential Writing Approach (Used for Second Generation):** 
When continuing an existing work where chapters must build on each other with tight narrative control, write chapters one at a time using this pattern:
1. Read the last 2-3 completed chapters to calibrate to current voice and ongoing plot threads
2. Load the specification for the next chapter
3. Write the chapter with explicit instructions to:
   - Include Mission AI dialogue in the specified format
   - Include a character quote in the specified format  
   - Follow the scene-by-scene outline exactly
   - End with the exact bridge text from spec
   - Target 4000-6000 words
4. Verify the saved file exists and check its actual word count
5. If too short (<2000 words), rewrite with explicit expansion instructions
6. If acceptable, move to next chapter
7. Every 5 chapters, run consolidation script to update the full manuscript

---

## 1. Preparation

### Gather Style Context
Read 3-4 fully-written existing chapters to understand:
- Prose style and pacing
- Character voices and relationships
- Formatting patterns (chapter headers, dialogue style, scene breaks, bridge lines)
- Technical depth (how technology is explained through action vs exposition)
- Recurring motifs and narrative devices

### Extract Chapter Specifications
Parse the book's specification document to get scene-by-scene outlines for each chapter. Each chapter spec should include:
- Scene descriptions (1-5 sentences each)
- Bridge text to next chapter
- Key characters needed
- Technical elements to include
- Mission AI / narrator voice guidance

### Build Character and Voice Guides
Ensure the subagent has access to:
- Character roster with personality summaries
- Narrator/voice guide (e.g., Mission AI dialogue format, evolution across the book)
- Style rules (e.g., "technical elements through dialogue, never exposition dumps")

---

## 2. Parallel Writing Architecture

### Dispatch Mode
Spawn 3 subagents in parallel, each writing 2-3 chapters:

```
delegate_task(goal="Write Chapter X and Y...", context=full_spec, toolsets=["terminal", "file"])
delegate_task(goal="Write Chapter Z...", context=full_spec, toolsets=["terminal", "file"])
delegate_task(goal="Write Chapter W...", context=full_spec, toolsets=["terminal", "file"])
```

### Per-Chapter Context Must Include
```
## Chapter N SPEC:
[Exact scene-by-scene outline from specification]

## Key Characters: [who appears]

## Mission AI / Narrator Voice: [opening dialogue format, monitoring style]

## Style: BESTSELLER prose, 4000-6000 words. Technical through action/dialogue.

## Context: [what precedes this chapter, continuity notes]

## Bridge: "[exact text from spec]"

## Format: # Chapter N -- Title
*Mission AI: "..."*
*Character: "..."*
[5 prose scenes]
*End of Chapter N -- Bridge: [exact bridge text].*
```

### Word Count Enforcement
- State the word count target explicitly (4000-6000 words)
- If the first attempt is too short (<2000 words), rewrite with instruction to expand — this is COMMON, subagents frequently produce scene outlines instead of full prose
- If too long (>8000 words), trim to target range. Chapters frequently overshot to 8,000-12,000 words without enforcement
- CRITICAL: Always verify the actual word count of the saved file, not what the subagent reports. Subagents frequently lie about word count

---

## 3. Verification and Course Correction

### After Each Batch
```bash
# Check all chapter files exist with reasonable size
for n in $(seq 1 64); do
    f=$(ls Chapter_$(printf '%02d' $n)_*.md 2>/dev/null)
    words=$(cat "$f" | wc -w)
    [ $words -gt 2000 ] && echo "OK: Ch $n ($words words)" || echo "SHORT: Ch $n ($words words)"
done
```

### Fix Truncated Outputs
Common issues:
- **File not saved** → subagent's write call failed silently; rewrite from scratch
- **Too short** → subagent ran out of token budget; rewrite with explicit expansion instruction
- **Wrong path** → agent saved to unexpected location; move the file

### Retry Pattern
```
delegate_task(goal="FULLY WRITE Chapter N. Previous attempt was truncated at X words. Must be 4000-6000 words.", context=...spec...)
```

---

## 4. Quality Principles

### Humanization Mandate
ALL book writing across every series and every project MUST apply the **humanizer** skill's process. Before writing, editing, or rewriting any manuscript content, load the `humanizer` skill and apply its 29 pattern checks and PERSONALITY AND SOUL section. No AI-isms, no filler, real voice, variable rhythm, opinions where they fit, first-person when honest. Call out any LLM-sounding language and fix it before delivering. This is mandatory.

### Reader Engagement & Excitement Mandate
Every piece of content added to a fiction manuscript — whether a new chapter, a bridge passage, an expanded section, a transition, or any other added material — MUST be crafted to be **interesting, exciting, and engaging to readers**. This is a non-negotiable quality bar, not a suggestion.

- **Every added paragraph must earn its place**: If a section, sentence, or phrase doesn't advance the story, reveal character, build tension, or create emotional resonance, it doesn't belong.
- **Strong hooks**: Every new chapter and every section within a chapter must open with a compelling hook — action, revelation, tension, or intrigue.
- **Compelling endings**: Every chapter and transition must end with a question, revelation, or escalation that compels the reader to continue.
- **Sensory richness**: Added material must include concrete sensory details (sight, sound, smell, touch, emotion) rather than abstract exposition.
- **No filler**: Transitions, bridges, and connective tissue must serve the story — not just move the reader from point A to point B. They should reveal something new, deepen understanding, or build anticipation.
- **Voice consistency**: All added material must match the established narrative voice and style of the surrounding content, never feeling like an insert or afterthought.

### Technical Integration
- Technology appears through use, failure, maintenance, and social meaning -- never as exposition
- Plain-language explanations delivered through character dialogue in context
- Technical accuracy grounded in real-world logic (Mars settlement physics, etc.)

### Character Consistency
- Each character has a distinct voice and perspective
- Characters evolve across the arc (track their development)
- The AI/narrator character evolves from functional to emotionally attached

### Chapter Bridges
- Every chapter ends with a bridge sentence that opens the next chapter's problem
- The bridge is always included verbatim from the spec

---

## 5. What to Track Across Chapters

### Continuity Threads
- Timeline progression (sols, days, years)
- Resource status (water, food, power, oxygen levels)
- Population changes (deaths, births, arrivals)
- Infrastructure additions (new halls, systems, buildings)
- Character arc positions

### Recurring Elements
- AI voice evolution (early functional → late warm)
- Technical theme per chapter
- Bridge text to next chapter
- Character ensemble balance
- Plain-language explanation moments

---

## 6. Pitfalls

### DO NOT write chapters sequentially yourself
This wastes your context window. Spawn agents, verify, fix.

### DO NOT skip style calibration
The first 2-3 chapters set the voice. If you write without reading existing chapters, the new ones will clash.

### DO NOT trust first write attempts
Subagents frequently produce:
- Truncated files (write succeeded but content was cut off)
- Overly short chapters — scene outlines instead of full prose (<2000 words when 4000+ required)
- Files saved to wrong paths (e.g., `.hermes/hermes-agent/` instead of the target directory)
- Chapters that are too long (8,000-12,000 words) — require trimming
- Subagents that time out without saving anything (silent failure)
Always verify the actual file exists at the expected path and check its word count independently.

### DO use parallel for speed
Three agents writing different chapters simultaneously is the fastest path. They don't need to wait for each other -- each subagent reads all prior chapters for continuity independently.

**BATCH SIZING UPDATE from Third Generation workflow:**
- Batches of 4 chapters per subagent work reliably (tested successfully across all 40 chapters of Third Generation)
- Batches of 5+ will frequently timeout — keep at 4 max
- Run 3 parallel batches of 4 for optimal throughput (12 chapters per round)

### DO verify the full manuscript at the end
After all 64 chapters exist, run a final check:
```bash
# Count chapters, check word counts, verify no gaps
ls Chapter_*.md | wc -l
for f in Chapter_*.md; do echo "$(wc -w < $f) $f"; done | sort -n
```

---

## 10. Content Discovery Across a Series

When working with a book series or collection, **each book will exist in a completely different state**. Before applying the generation workflow, verify what actually exists:

### Discovery Strategy
Content is typically scattered across multiple locations:
- `~/Downloads/*.zip` — archived exports from previous agent sessions
- `~/.hermes/.openclaw/` — agent state from prior sessions
- `~/Desktop/.openclaw/` — local workspace copies
- Book source directories — `book-sources/*/` or `workspace-writer/book-sources/`
- Consolidated manuscripts — `*_COMPLETE.md`, `*_FULL.md` files

### Typical State Mix (real example from 4-book series):
| Book | What Actually Exists | Action Needed |
|------|---------------------|---------------|
| Book 1 (Fiction) | 0 chapters written, just a spec | Full generation (390K words) |
| Book 2 (Fiction) | 0 chapters, just a spec | Full generation needed |
| Memoir | ~57K words already written | Compile + intro only |
| Business book | ~27K words in individual chapter files | Compile + intro only |

### Extracting Individual Chapters from Consolidated Manuscripts
When standalone chapter files are stubs (e.g., just "Chapter X content"), the full text may be embedded in a consolidated manuscript:

```bash
# Check if full text exists in consolidated manuscript
wc -w manuscript.md
# Extract individual chapters using awk
awk '/^## Chapter N/,/^## Chapter N+1/' manuscript.md | head -n -1 > Chapter_N.md
```

### When to Generate vs. Compile
- **0 prose, spec exists** → run parallel subagent generation
- **Prose exists (>10K words)** → compile, write intro, add TOC
- **Some chapters written, some stubs** → write only missing/short ones
- **Autobiographical/memoir** → compile only (already personal prose)
- **Business/non-fiction chapters** → compile with intro

---

## 11. Consolidated Manuscript Compilation Pattern

After content is verified (whether generated or existing), compile with a proper introduction and table of contents:

### Introduction Template
Match the introduction style to the book type:
- **Fiction**: Describe the creative vision, the AI workflow, and what the author built
- **Memoir**: Personal voice, the origin story, the thread that connects everything
- **Business**: Practical framing, the author's experience, what the reader will get

Always write the introduction in the author's voice using context from their memory.

### TOC Generation
```python
# Standard TOC with word counts per chapter
import os, re
for ch_num in range(1, 65):
    num = f"{ch_num:02d}"
    for fname in sorted(os.listdir(book_dir)):
        if f"Chapter_{num}" in fname and fname.endswith(".md"):
            # read file, count words, extract(clean) title
```

### Final Output Structure
```
Title
Introduction (by author)
---
Table of Contents (with word counts)
---
Part I
  Chapter 1
  Chapter 2
  ...
```

---

## 12. Key Lessons Updated from Full 4-Book Series Run

- **Different books need different workflows** in the same project — don't assume uniformity
- **Introductions should match the book's genre** — fiction gets the AI-workflow story, memoir gets personal voice, business gets practical framing
- **Always read the author's memory** for personal details when writing introductions — makes them authentic
- **The write_file tool can silently fail** with empty results or save to unexpected paths — ALWAYS verify the file exists AND has content afterward
- **Model changes mid-session are not possible** — the session's model is pinned at start; user's model preference is saved for the next session
- **Batch of 3 chapters is the sweet spot** — 5 will frequently timeout, 1 is too slow

---

## 13. Multi-Book Project Discovery

When working with a book series or collection, **each book may exist in a completely different state**. Before applying the generation workflow, verify what actually exists:

```bash
# Check what's in each book's directory or source archive
for book_dir in book-sources/*/; do
    echo "=== $book_dir ==="
    find "$book_dir" -name "*.md" -exec wc -w {} +
    grep -c "^[A-Za-z]" "$book_dir"/*.md  # lines with actual prose
done
```

**Common patterns found:**
- **Complete manuscript exists** → compile with intro/TOC, don't regenerate
- **Only spec/outline exists** → run full parallel subagent generation workflow
- **Some chapters written, some stubs** → write only the missing/short ones
- **Autobiographical/memoir content** → already personal prose — compile only
- **Business/non-fiction chapters** → different writing style, same compilation approach

**Discovery across locations:**
Content may be scattered across:
- `~/Downloads/*.zip` — archived exports from previous sessions
- `~/.hermes/.openclaw/` — agent state from prior sessions
- `~/Desktop/.openclaw/` — local workspace copies
- `/tmp/` — extraction directories from previous work

Always search all locations before assuming content is missing.

### Extraction from Consolidated Manuscripts
When standalone chapter files are stubs (e.g., just "Chapter X content"), the full text may be embedded in a consolidated manuscript:

```bash
# Extract individual chapters from a full manuscript
awk '/^## Chapter N/,/^## Chapter N+1/' manuscript.md | head -n -1 > Chapter_N.md
```

---

## 11. Consolidated Manuscript Generation

After all chapters are complete, compile a single manuscript:

1. **Read all chapter files** in numerical order
2. **Standardize headings** (remove redundant chapter number prefixes, fix ALL CAPS titles)
3. **Write a custom introduction** based on the project context
4. **Generate table of contents** with word counts
5. **Combine into single file** with consistent formatting

```python
# Quick consolidation script
for ch_num in range(1, 65):
    num = f"{ch_num:02d}"
    for fname in os.listdir(book_dir):
        if f"Chapter_{num}" in fname and fname.endswith(".md"):
            # read, clean, append to output
```

---

## 9. Lessons Learned from First Generation (390K words, 64 chapters)

- **Subagents will save files to unexpected directories** — always verify the output path, be ready to copy/move files
- **A single subagent batch of 5 chapters will frequently time out** — keep batches to 3 chapters max
- **The write_file tool can silently fail with errors** — always check the return value, not just that no exception was raised
- **Some chapters are easy** (action, dialogue-heavy), **some are hard** (reflective, emotional) — budget more time for reflective chapters
- **Existing draft stubs from previous work can cause confusion** — subagents found the old outline files and sometimes returned those instead of writing new content
- **Style calibration is everything** — the subagents that read 3-4 existing chapters wrote much better prose than those that read only the spec
