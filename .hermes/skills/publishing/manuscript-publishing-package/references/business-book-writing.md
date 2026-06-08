# Business Book Writing Pipeline

A complete pipeline for ideating, outlining, writing, and packaging a non-fiction business book — from concept to KDP-ready EPUB.

## When to Use

Use this pipeline when the user asks to:
- "Write a business book about [topic]"
- "Develop my book idea into a full manuscript"
- "Give me business book concepts"
- "Write a 40-chapter non-fiction book"
- Any request to create a practical/guide-type book based on the author's real expertise

Do NOT use this for fiction, memoir, or creative writing — use `manuscript-creation` or `novel-writing-workflow` for those.

## Pipeline Overview

```
Ideation → Market Research → Concept Selection → Outline → 
Parallel Chapter Writing (4 batches × 10 ch) → Humanize QA → 
Compile → EPUB → Publishing Package
```

## Phase 1: Ideation (Concept Generation)

Given the user's profile, current work, and expertise, generate 3-5 book concepts. Each concept should:
- Be grounded in the AUTHOR'S actual expertise (not research they'd need to do)
- Address a specific market gap (use web_search to check competitors)
- Have a clear target audience
- Be unique enough to stand out from existing books on the topic

**Output:** A ranked list of 3 concepts with:
- Title and subtitle
- The gap it fills in the market
- Why THIS author is uniquely positioned to write it
- Target audience
- Selling point / differentiator

**Example format:**
```markdown
### Concept Title
**The gap:** ...
**Why [author]:** ...
**Target:** ...
**Selling point:** ...
```

## Phase 2: Market Research (Competitive Landscape)

For the selected concept, research existing books in the space:
- Search Amazon and Google for similar titles
- Identify the top 5-10 direct competitors
- Note what each competitor covers and where they fall short
- Find the white space — what no existing book addresses

**The white space for practitioner-authors:** No competitor is written by someone who *owns and operates* the system they describe. Consultants write about what they've advised. Researchers write about what they've studied. An author who built and runs the system daily has a unique advantage — emphasize this.

## Phase 3: Outline (40 Chapters, 4 Parts)

Divide the book into 4 parts of 10 chapters each, following a classic non-fiction arc:

| Part | Theme | % of Book | Narrative Function |
|------|-------|-----------|--------------------|
| I | **The Problem** | 25% | Establish the pain, why existing solutions fail |
| II | **The Solution** | 25% | Build the first working example step by step |
| III | **Scale** | 25% | Move from one to many; handle complexity |
| IV | **The Future** | 25% | Broader vision, roadmap, objections, call to action |

Each chapter outline needs:
- **Chapter number and title**
- **Core argument** (2-3 sentences on what this chapter teaches)
- **Opening story concept** (a specific moment or problem to start with)
- **Key example** (from the author's own work — real numbers, real failures)
- **Bridge to next chapter** (one line, optional)

Chapter titles should be benefit-driven or curiosity-driven — NOT descriptive/academic. Compare:
- "An Overview of AI Agent Architectures" (bad)
- "Why Your CRM Can't Save You" (good)

## Phase 4: Author Voice Guide (MANDATORY)

Every subagent MUST receive this voice guide. It defines the book's entire tone.

### Core Voice Rules

1. **First person, real experience** — "I built this. I broke this. I fixed this." Never "one might consider" or "businesses can benefit from."

2. **Honest about failures** — share what went wrong, not just the wins. A chapter about what broke at 3am is more valuable than five chapters about what worked perfectly.

3. **Short sentences mixed with longer ones** — varied rhythm. Punchy one-liners for key insights, longer sentences for explanations.

4. **Specific > vague** — real numbers, real names, real costs. "The MIFECO pipeline handles 47 leads a week with one human review" not "many businesses see improvement with automated systems."

5. **Opinionated** — say what you actually think. "I hate CRM software" is more honest and engaging than "CRM software presents certain challenges that organizations should consider."

6. **Engineer's eye** — explain WHY things work the way they do, not just WHAT they do. The reader wants to understand the system, not just follow steps.

### Humanizer Mandate (Apply to Every Chapter)

Before delivering any chapter, scan for these patterns and REMOVE them:

| Pattern | Example | Replace With |
|---------|---------|-------------|
| Overused AI vocab | "crucial", "delve", "intricate", "pivotal" | "important", "look at", "complex", "key" |
| Promotional language | "groundbreaking", "game-changing", "vibrant" | Leave it out entirely |
| Vague attributions | "experts say", "industry reports" | Specific source or drop the claim |
| Negative parallelisms | "It's not just X, it's Y" | Direct statement |
| Em dash overuse | More than 2 per 1000 words | Periods and commas |
| Rule of three | Forcing ideas into groups of three | Natural grouping |
| Copula avoidance | "serves as" instead of "is" | Direct "is" statements |
| Filler phrases | "in order to", "due to the fact that" | "to", "because" |
| Hedging | "could potentially", "might arguably" | Direct statement |
| Generic conclusions | Vague upbeat endings about "the future" | Specific next step |
| Persuasive tropes | "The real question is", "at its core" | Just state the point |
| Signposting | "Let's dive in", "let's explore" | Start the content |

### Chapter Structure (Repeatable Pattern)

Each chapter should follow this rhythm:

1. **Opening hook** — Start in the middle of something specific. A moment, a problem, a question. Not "in this chapter we will explore" but "The email arrived at 3:47 AM."

2. **The framework** — What this chapter is actually about. Brief context — one paragraph max.

3. **Real example** — How this works in practice. The author's own experience, with real numbers, real names, real outcomes. This is the longest section.

4. **The lesson** — What the reader should take away. Direct, actionable. One sentence.

5. **Bridge** — One line that sets up the next chapter (optional, don't force it).

### Target Length

- 1,000-1,200 words per chapter
- 40 chapters = ~44,000-48,000 words
- ~180-200 pages at 6x9" with standard typography

## Phase 5: Parallel Batch Writing (via delegate_task)

Split the 40 chapters into 4 batches of 10 chapters each. Use `delegate_task` with up to 3 concurrent tasks:

```python
delegate_task(tasks=[
    {"context": "...Chapters 1-10...", "goal": "...", "toolsets": [...]},
    {"context": "...Chapters 11-20...", "goal": "...", "toolsets": [...]},
    {"context": "...Chapters 21-30...", "goal": "...", "toolsets": [...]},
])
```

### What Each Subagent Receives

Each subagent task must include:
1. **The full voice guide** (Phase 4 above) — don't abbreviate
2. **Their specific 10 chapters** with full outlines (not just numbers — summarize the argument, example, and hook per chapter)
3. **The humanizer patterns list** — verbatim
4. **The project's key examples** — a few real stories/failures the subagent can reference
5. **Target: 1,000-1,200 words per chapter**
6. **Output files: ch01.md through ch10.md** (or appropriate range)

### After All Subagents Return

1. **Compile** into a single manuscript.md with front matter (title, copyright, author's note, TOC) and back matter (about the author, also by, closing thought)
2. **Add part dividers** between Parts I/II/III/IV
3. **Run humanizer scan** on the compiled manuscript (search for banned patterns)
4. **Normalize heading levels** — subagents may use different heading levels (`#` vs `##`) for chapter titles
5. **Check chapter count** — verify all 40 chapters are present
6. **Build EPUB** — see `scripts/build-epub-kdp.py` or the EPUB section in main SKILL.md

### Pitfalls

- **Heading level mismatch**: Different subagents may use `# Chapter N: Title` (level 1) vs `## Chapter N -- Title` (level 2). Normalize to a consistent pattern during compilation.
- **Em dash overuse**: Aggregating 40 chapters from 4 subagents can produce 150+ em dashes. Do a reduction pass targeting 1-2 per 1000 words.
- **Missing front/back matter**: Subagents only write chapters. Add title page, copyright, TOC, about the author, and closing thought during compilation.
- **Inconsistent voice**: Spot-check chapters from different subagents for voice drift. The first-person "I" voice should sound like the same person across all 4 batches.
- **AI-isms from subagents**: Each subagent writes independently and may produce AI-isms that the humanizer didn't catch individually. After compilation, run a second broader scan.

## Phase 6: Title Validation

Before finalizing the book title:
1. **Search web** for similar titles
2. **If taken**, propose 10 alternatives that are unique, capture the angle, and differentiate
3. **Get user confirmation** before proceeding

## Phase 7: Post-Write Deep QA

After compiling all chapters, run a comprehensive QA pass before generating the final EPUB.

### Automated Checks

| Check | What to Look For | Fix |
|-------|-----------------|-----|
| All chapters present | 40 chapter headings found | Insert missing |
| Sequential numbering | No gaps 1-40 | Renumber |
| Title consistency | No old title references | Replace with current |
| Part dividers | Parts I-IV all present | Add missing |
| Front matter | Title, copyright, TOC, note | Add missing sections |
| Back matter | About author, series, closing | Add missing sections |
| Word count per chapter | Each 800-1,500 words | Expand/trim |
| Double spaces | More than 20 | Replace with single |
| AI vocabulary | "delve", "crucial", "pivotal" | Replace naturally |
| Em dashes | >2 per 1,000 words | Replace with . or , |
| Placeholder text | "TODO", "TBD", "FIXME" | Fill or remove |

### Spot-Check (5+ Chapters)

Read chapters 1, 10/11, 20/21, 30/31, and 40. Verify:
- Opens with a specific moment/problem (not "in this chapter...")
- First person with real examples
- Free of AI-isms
- Naturally bridges to next chapter

### Common Fixes Before Final Build

1. **Missing part dividers** — compilation regex may fail if heading levels are inconsistent
2. **Old title in chapter/part names** — update if named after old concept
3. **Em dash overuse from aggregated batches** — 4 subagents × 40 chapters can produce 150+ dashes
4. **Voice drift between subagents** — check that "I" sounds like the same person across chapters

## Related Skills

- `openrouter-image-generation-workflow` — for generating the book cover artwork
- `book-deliverable-kdp` — for EPUB validation and KDP upload
- `manuscript-publishing-package` — for the full publishing package workflow
- `humanizer` — for the 29-pattern AI-ism detection checklist
