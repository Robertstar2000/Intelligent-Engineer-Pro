---
name: manuscript-creation
description: >-
  A pipeline for generating new books in any genre (sci-fi, fantasy, business, etc.)
  from a concept. Phase 0 researches best-selling comparable books to extract plot,
  style, and character templates, then generates original versions. Phases 1-5
  develop the concept, characters, chapter outline, write in parallel batches, and
  polish into a final .md manuscript.
version: 2.0.0
author: Hermes Agent
category: creative
tags: [manuscript, writing, sci-fi, fantasy, business, pipeline, creation, research]
related_skills: [novel-writing-workflow, manuscript-preparation-and-delivery, writing-plans]
---

## Memory context (Hindsight)

Long-term memory context is now provided automatically by Hindsight (bank
`mifeco-default`) on every turn — the retired MemPalace manual query step no
longer applies. Do NOT attempt to import `~/.hermes/mempalace` (it was removed
2026-08-19).This retrieves previous decisions, domain-specific context, and lessons learned from the vector memory store.

# Manuscript Creation Skill

## Purpose
This skill provides an end-to-end pipeline to generate an original manuscript
in any genre, from market research to polished Markdown file. It uses a
research-first approach: study best-selling comparable books, extract what
works, then create an original work informed by those patterns.

## When to Use
- When given a genre (sci-fi, business, fantasy, other) and a concept, to
  produce a complete book from scratch.
- When the user wants market-informed writing — books that fit proven demand.
- To produce a draft manuscript that can be further refined or delivered.
- As a starting point for a novel-writing project.

## Prerequisites
- Access to writing-related skills (e.g., `novel-writing-workflow`,
  `writing-plans`, `manuscript-preparation-and-delivery`).
- Ability to call other skills via `skill_view` or delegate tasks if needed.
- Ability to search the web for best-selling books and extract data.
- Basic familiarity with Markdown formatting.

## Implementation

This skill provides an executable pipeline that generates a complete manuscript.
It starts with **Phase 0: Market Research** when given a genre + concept, then
proceeds through concept development, character creation, chapter outlining,
parallel writing, and editing.

---

## Phase 0: Market Research (Genre + Concept → Informed Foundation)

**Trigger:** The user provides a genre (e.g., "sci-fi", "business", "fantasy",
"thriller", "memoir", "self-help", etc.) and a concept or premise.

This phase grounds the book in proven market patterns before any creative work
begins. Skip only if the user provides a fully-formed concept + characters +
outline already.

### Step 0.1: Find Best-Selling Comparable Books

Search for best-selling books that match the given genre and are a similar fit
to the concept. Use web_search to find them:

```
Search queries to run:
1. "best selling [genre] books 2024 2025"
2. "top [genre] books on Amazon Kindle"
3. "best-selling books similar to [concept关键词]"
4. "most popular [genre] books this year"
```

For each query, collect the top 5-10 results. Aim for a pool of **8-12 unique
best-selling books** total across all queries.

Extract for each book:
- **Title & author**
- **Sub-genre / niche** (e.g., "space opera" within sci-fi, "AI business" within business)
- **Amazon ranking / bestseller status** if visible
- **Publication recency** (prefer books from last 3-5 years)

Save the raw list to `{book_dir}/research/01_bestseller_list.md`.

### Step 0.2: Extract Plot, Style, and Characters

For each of the 8-12 best-selling books identified, gather detailed information.
Use `web_search` and `web_extract` to find reviews, summaries, and author
interviews.

For each book, extract and document:

#### A. Plot Structure
- **Core premise**: One-sentence hook (what is this book about?)
- **Central conflict**: What drives the story/problem?
- **Narrative arc**: Setup → escalation → climax → resolution (2-3 sentences)
- **Key plot turns**: 3-5 major events or revelations
- **Ending type**: Triumphant, bittersweet, cliffhanger, open-ended, etc.
- **For non-fiction only**: Core thesis, framework/model presented, key takeaways

#### B. Writing Style
- **Voice/tone**: (e.g., "technical and precise", "warm conversational",
  "gritty noir", "inspirational")
- **POV**: (first person, third limited, third omniscient, second person for guides)
- **Pacing**: (fast/action-driven, slow/contemplative, mixed)
- **Dialogue style**: (snappy, realistic, minimal, expository)
- **Prose complexity**: (accessible, literary, technical)
- **Use of humor**: (dry, slapstick, none, situational)
- **Chapter length tendency**: (short punchy 2-3 pages, medium 5-8, long 10+)
- **Unique stylistic hooks**: (e.g., "Mission AI italic lines", "present-tense
  urgency", "framed as case studies")

#### C. Characters (for fiction/genres that use characters)
- **Main characters** (protagonist, antagonist, key supporting): name, role, one-sentence personality description
- **Character dynamics**: How main characters relate to each other
- **Character arc pattern**: (hero's journey, fall from grace, mentor → leader,
  ensemble growth)
- **Diversity/representation approach**: (varies by genre; note what works)

For **non-fiction / business / self-help** books, instead of characters,
extract:
- **Author persona**: How the author presents themselves (practitioner,
  researcher, coach, storyteller)
- **Use of case studies**: Frequency, format, anonymized vs named
- **Narrative devices**: (anecdotes, frameworks, exercises, frameworks)

Save all extracted data to `{book_dir}/research/02_bestseller_analysis.md`.

### Step 0.3: Summarize Research Findings

Produce a concise market research summary that identifies the **patterns**
across all studied bestsellers. Save to
`{book_dir}/research/03_research_summary.md`:

```
# Market Research Summary: [Genre] — [Concept Title]

## Common Plot Patterns
- [Pattern 1: e.g., "Most books follow a 'discovery → crisis → breakthrough' structure"]
- [Pattern 2]
...

## Style Patterns
- [Pattern 1: e.g., "Third-person limited with technical precision dominates"]
- [Pattern 2]
...

## Character Patterns (if applicable)
- [Pattern 1: e.g., "Ensemble casts of 5-7 with one clear protagonist"]
- [Pattern 2]
...

## Market Gaps & Opportunities
- [What's missing or underserved in current bestsellers — this is the angle for the new book]

## Reference Style (What We're Writing Toward)
- [2-3 sentence description of the target style for this new book, informed by research]
```

### Step 0.4: Generate Original Plot

Using the research analysis (Step 0.2-0.3), generate a **new, original plot**
that is:

1. **Informed by** the common patterns found in bestsellers (the proven structures)
2. **Distinct from** any specific bestseller (not a copy — a fresh take that fits
   the genre)
3. **Specific to** the user's concept/instructions

The output is a plot document with:

```
# Plot Document: [Working Title]
## Core Premise
[One-sentence hook]

## Central Conflict
[What drives the narrative/problem]

## Narrative Arc
### Act I: Setup (Chapters ~1-10)
[3-5 bullet points — key events, character introductions, world establishment]

### Act II: Escalation (Chapters ~11-20)
[3-5 bullet point — complications rising, stakes increasing, midpoint reversal]

### Act III: Climax (Chapters ~21-30)
[3-5 bullet points — everything on the line, major confrontations]

### Act IV: Resolution (Chapters ~31-40)
[3-5 bullet points — aftermath, transformation, new status quo]

## Key Plot Turns
1. [Turn 1]
2. [Turn 2]
...

## Ending Type
[e.g., "Bittersweet triumph — the goal is achieved but at personal cost"]

## What Makes This Original
[2-3 sentences on how this differs from the specific bestsellers studied]
```

For **non-fiction**, the plot document is replaced by a **thesis & framework document**:
```
# Thesis Document: [Working Title]
## Core Thesis
[One-sentence argument]

## The Problem
[What pain point / gap this book addresses]

## The Framework
[The model, method, or system the book teaches — 3-7 key principles]

## Chapter Arc
### Part I: [Theme] (Chapters ~1-10)
### Part II: [Theme] (Chapters ~11-20)
### Part III: [Theme] (Chapters ~21-30)
### Part IV: [Theme] (Chapters ~31-40)

## What Makes This Original
[How this book's angle differs from the specific bestsellers studied]
```

Save to `{book_dir}/research/04_original_plot.md`.

### Step 0.5: Generate Style Specification

Based on the research analysis (Steps 0.2-0.3), write a **style specification**
for the new book. This becomes the authoritative style guide for every
subagent that writes chapters.

```
# Style Specification: [Working Title]

## Target Voice
[2-3 sentence description of the desired narrative voice, referencing research patterns]

## Humanization Requirements
- Start in the middle of action or a specific moment — NO cold opens or weather reports
- Every paragraph must earn its place: advance plot OR deepen character OR build tension
- Sensory details in every scene: sight, sound, smell, touch, taste — not just visual
- Internal character thoughts: what they're feeling, not just what they're doing
- Dialogue that reveals character — distinct voices per character, not interchangeable
- No AI-isms: avoid "delve", "leverage", "tapestry", "intricate", "fostering",
  "vibrant", "pivotal", "testament", "showcase", "additionally", "revolutionary",
  "game-changing", "groundbreaking", "cutting-edge", "synergy", "empower", "paradigm",
  "unlock"
- Em dash usage: max 3 per 1,000 words. Vary sentence structure with periods.
- First person when honest; never hedge or equivocate in the author's voice

## Pacing & Structure
- [Pacing notes from research — e.g., "Alternate high-tension scenes with quieter character moments"]
- [Chapter structure notes — e.g., "Each chapter 1,000-1,400 words, ending with a hook"]

## What to Avoid
- [Specific patterns from research that this book should NOT use, or common genre
  pitfalls to sidestep]

## Reference Authors/Works
- [1-3 specific books/authors the style should echo, with caveats about what NOT to copy]
```

Save to `{book_dir}/research/05_style_spec.md`.

### Step 0.6: Generate Character Roster (Fiction Only)

**Skip for non-fiction** unless the genre regularly uses recurring personas/case studies.

**MANDATORY: Character Naming Rules & Character Map**

Before generating any names, you MUST understand and enforce the Character Naming Rules that have been established to prevent the naming inconsistencies that have plagued prior projects:

**Character Naming Rules (NON-NEGOTIABLE):**
1. **One canonical name per character** — Pick ONE name and use it consistently. No "Tom/Thomas/Tommy" switching.
2. **Surnames are stable** — A character's surname does not change mid-book or across books unless explicitly explained in-story.
3. **No duplicate names for different characters** — "Jane Wilson" cannot be 4 different people across 4 books.
4. **Pronouns are intentional and consistent** — If a character uses they/them, this must be consistent within the book and across the series (or explained).
5. **Title/rank consistency** — "Col. James Kovacs" / "James" / "Director Kovacs" / "Director Reeves" — pick ONE reference style per scene context.

**MANDATORY: Character Map Creation**
Every book project must maintain a **Character Map** — a canonical reference document that tracks all characters:
- **Per Book (stored in book directory as CHARACTER_MAP.md):** Canonical name, aliases/nicknames, role, first appearance (chapter), key relationships, voice/persona notes, books appearing in
- **Per Series (stored at series level as SERIES_CHARACTER_MAP.md):** Cross-book canonical reference for every recurring character, with deliberate changes explained

**Before writing any chapter:**
- Read the Character Map
- Verify character names/pronouns match the map
- Update the map if new characters are introduced

**After completing a book:**
- Audit the manuscript against the Character Map
- Flag any deviations as P0 defects

---

**MANDATORY: Plot Flow Rules & Plot Map**

Before generating any plot structure, you MUST understand and enforce the Plot Flow Rules that have been established to prevent the plot failures that have plagued prior projects:

**Plot Flow Rules (NON-NEGOTIABLE):**
1. **Plot flows consistently** — Each scene causes the next, not "and then this happened." Cause and effect must be visible from chapter to chapter.
2. **Stakes escalate** — Complications multiply, tension curves upward. The middle does not sag; Act II has rising complications, not filler.
3. **No idiot plot** — Characters don't act stupidly just to advance the plot.
4. **No deus ex machina** — Resolutions earned through character agency, not coincidence.
5. **Subplots interweave** with main plot, not run parallel without intersection.
6. **Ending is both surprising and inevitable** — The only way it could have gone.

**MANDATORY: Plot Map Creation**
Every book project must maintain a **Plot Map** — a canonical reference document that tracks plot structure:
- **Per Book (stored in book directory as PLOT_MAP.md):** Chapter-range table showing core conflict, stakes, key twist/revelation, cause→effect link to next section, resolution status for each major structural segment (Ch1-5, Ch6-10, Ch11-15, Ch16-20, Ch21-25, Ch26-30, Ch31-35, Ch36-40)
- **Per Series (stored at series level as SERIES_PLOT_MAP.md):** Cross-book canonical reference showing each book's core conflict, stakes arc, key twists, how it sets up the next book, resolution status

**Before writing any chapter:**
- Read the Plot Map
- Verify the chapter's conflict, stakes, and twist advance the cause→effect chain
- Update the Plot Map if the story takes a new direction

**After completing a book:**
- Audit the manuscript against the Plot Map
- Trace 3 main plot threads from setup through climax to resolution
- Flag any broken cause→effect chains, sagging middle, or unearned resolutions as P0 defects

---

**MANDATORY: Non-Fiction Framework Map (for Business/Self-Help/Non-Fiction Books)**

For non-fiction books, the Plot Map is replaced by a **Framework Map** that tracks the book's argument architecture:

**Framework Map Creation**
Every non-fiction book project must maintain a **Framework Map**:
- **Per Book (stored in book directory as FRAMEWORK_MAP.md):** Part-level table showing core thesis/claim, framework element, key case study, actionable takeaway ("The One Thing"), reader exercise/tool, cross-chapter link for each major part (Assess/Choose/Implement/Optimize or equivalent 4-part structure)
- **Per Series (stored at series level as SERIES_FRAMEWORK_MAP.md):** Cross-book canonical reference showing each book's core thesis, framework contribution, key frameworks introduced, how it builds on previous, reader journey position

**Non-Fiction Quality Rules (NON-NEGOTIABLE):**
1. **Thesis clarity** — Core argument stated in Ch 1, reinforced every chapter
2. **Framework utility** — Each chapter introduces/applies a reusable framework (not just advice)
3. **Case study density** — ≥1 concrete case study per chapter (real, specific, with numbers)
4. **Personal storytelling** — Author's own failures/successes woven throughout (vulnerability builds trust)
5. **Provocative chapter headers** — Every title makes a CLAIM reader wants to verify
6. **Implementation apparatus** — Every chapter ends with "The One Thing" + exercise/checklist/template
7. **No filler** — Every paragraph advances argument or illustrates framework
8. **Cross-chapter coherence** — Frameworks build cumulatively
9. **Reader journey clarity** — Positions reader at competency level (novice→practitioner→expert)
10. **Companion resources** — Downloadable tools/templates referenced and exist

**Before writing any chapter:**
- Read the Framework Map
- Verify the chapter's thesis, framework, case study, and takeaway advance the argument
- Update the Framework Map if the structure evolves

**After completing a book:**
- Audit the manuscript against the Framework Map
- Trace the core thesis through all 4 parts
- Flag any missing framework elements, descriptive headers, missing case studies, or broken framework chains as P0 defects

---

Write a Python script to randomly select names from the top 50 most common US names. This is **MANDATORY** — never invent names or use internationally-diverse name lists.

```python
import random

FIRST_NAMES_MALE = [
    "James", "Robert", "John", "Michael", "David", "William", "Richard",
    "Joseph", "Thomas", "Christopher", "Charles", "Daniel", "Matthew",
    "Anthony", "Mark", "Steven", "Paul", "Andrew", "Joshua", "Kenneth",
    "Kevin", "Brian", "George", "Timothy", "Ronald", "Edward", "Jason",
    "Jeffrey", "Ryan", "Jacob", "Gary", "Nicholas", "Eric", "Jonathan",
    "Stephen", "Larry", "Justin", "Scott", "Brandon", "Benjamin", "Samuel",
    "Raymond", "Gregory", "Frank", "Alexander", "Patrick", "Jack", "Dennis", "Jerry"
]

FIRST_NAMES_FEMALE = [
    "Mary", "Patricia", "Jennifer", "Linda", "Barbara", "Elizabeth", "Susan",
    "Jessica", "Sarah", "Karen", "Lisa", "Nancy", "Betty", "Margaret",
    "Sandra", "Ashley", "Dorothy", "Kimberly", "Emily", "Donna", "Michelle",
    "Carol", "Amanda", "Melissa", "Deborah", "Stephanie", "Rebecca", "Sharon",
    "Laura", "Cynthia", "Kathleen", "Amy", "Angela", "Shirley", "Anna",
    "Brenda", "Pamela", "Emma", "Nicole", "Helen", "Samantha", "Katherine",
    "Christine", "Debra", "Rachel", "Carolyn", "Janet", "Catherine", "Maria",
    "Heather"
]

def pick_names(count, gender_mix=None):
    """Pick `count` unique random names."""
    used = set()
    results = []
    pool = FIRST_NAMES_MALE + FIRST_NAMES_FEMALE
    while len(results) < count:
        name = random.choice(pool)
        if name not in used:
            used.add(name)
            results.append(name)
    return results
```

Create 6-10 characters (depending on genre needs) with:

```
# Character Roster: [Working Title]

## [First Name] — [Role, e.g., "Protagonist", "Mentor", "Antagonist"]
- **Background**: [1-2 sentences — where they come from, what they do]
- **Personality**: [1-2 sentences — key traits, how they come across]
- **Motivation**: [What they want / what drives them]
- **Arc**: [How they change from beginning to end]
- **Voice**: [How they speak — formal, casual, technical, clipped, warm]
- **Key relationship**: [Who they're most connected to and why]

[Repeat for each character]
```

Ensure:
1. Names are drawn randomly from the top 50 US lists above
2. No ethnically-marked or internationally-diverse names unless specifically
   justified by a character's background
3. Characters have **distinct personalities** — no two characters should feel
   interchangeable
4. Characters are informed by patterns found in research (e.g., if bestsellers
   use "reluctant hero + loyal sidekick + brilliant antagonist", create a
   similar dynamic but with original characters)

Save to `{book_dir}/research/06_characters.md`.

### Step 0.7: Generate Chapter Titles with Beats

Using the original plot (Step 0.4), style spec (Step 0.5), and character roster
(Step 0.6), generate a complete chapter outline sized for a **175-225 page book
at 6×9in** (≈40 chapters × 1,000-1,400 words each ≈ 40,000-56,000 words total
at ~250-280 words/page).

```
# Chapter Outline: [Working Title]

## Part I: [Part Title]
### Chapter 1 — [Title]
- [Beat 1: e.g., "Introduce protagonist in the middle of a specific problem — not backstory"]
- [Beat 2: e.g., "Inciting incident disrupts normal life"]
- [Beat 3: [e.g., "End with a hook that forces reader into Chapter 2"]

### Chapter 2 — [Title]
- [Beat 1]
- [Beat 2]
- [Beat 3]

[Continue for all 40 chapters, organized into 4 parts]

## Part II: [Part Title]
...

## Part III: [Part Title]
...

## Part IV: [Part Title]
...
```

Each chapter has **3-5 beats** describing the narrative content. Beats should be
specific, not generic — "Margaret discovers the water tank is cracked and the
crew has 48 hours of reserves" not "Water problem discovered."

The chapter-level beats, combined with the style spec and character roster,
should give a writing subagent everything needed to write a complete chapter
without guessing.

Save to `{book_dir}/research/07_chapter_outline.md`.

---

## Phase 1-5: Manuscript Production

After Phase 0 completes, the research directory contains everything needed
to write the book. The remaining phases follow the established pipeline:

### Phase 1: Create Planning Documents → {book_dir}/research/ (completed by Phase 0)

### Phase 2: Develop Character Roster → {book_dir}/research/06_characters.md (completed by Phase 0)

### Phase 3: Outline Chapter Structure → {book_dir}/research/07_chapter_outline.md (completed by Phase 0)

### Phase 4: Write Manuscript Chapter-by-Chapter (Parallel Batches)

Use **parallel batch writing** for books with 30+ chapters. Each batch subagent writes 10 complete chapters.

Each batch subagent receives (from Phase 0 research):
- `07_chapter_outline.md` — their specific 10-chapter section with all beats
- `06_characters.md` — full character roster (fiction) or author persona notes (non-fiction)
- `05_style_spec.md` — the authoritative style specification
- `03_research_summary.md` — market context and patterns

For each chapter:
- **Follow the style specification** (Phase 0.5) — this is the authoritative voice guide
- **Follow the chapter beats** (Phase 0.7) — hit every beat; these are the narrative requirements
- **Humanize all content** — include personal reflections, emotional beats, sensory details
- **Apply the humanizer skill to all output** — before delivering any chapter, load the `humanizer` skill and run its 29 pattern checks. Strip all AI-isms, filler, and LLM-sounding language. Ensure real voice, variable rhythm, opinions where they fit. This is mandatory for every chapter.
- Target **1,000-1,400 words per chapter** (~40,000-56,000 words total for 40 chapters) to ensure final paperback book of 175-225 pages at 6×9in
- Maintain consistent character voices across parallel batches (fiction) by sharing the character roster and sample chapters
- Verify character voice consistency after all batches return — spot-check one chapter from each batch per major character

### Phase 5: Edit and Polish
- **Sequential flow edit**: Read the manuscript sequentially, ensuring smooth transitions between chapters, consistent pacing, and logical plot progression. Trim or expand sections as needed.
- **Reader engagement check**: Every chapter, every transition, every scene must be interesting, exciting, and engaging to readers. If any section reads as filler or flat exposition, rewrite it. Each added paragraph must earn its place — advancing story, revealing character, building tension, or creating emotional resonance.
- **Grammar & Mechanics**: Check for spelling, punctuation, and grammatical errors. Apply consistent style (e.g., Oxford comma, dialogue formatting).
- **Markdown Formatting**: Verify Markdown syntax (heading levels, list formatting, emphasis) and ensure the document renders correctly.
- **Consistency Check** (fiction): Character names, terminology, world-building details, timeline consistency.
- **Fabricated-claim integrity pass** (non-fiction): Scan for fabricated first-person claims (e.g., "I spent $43k"). Rewrite as anonymized case studies. See `book-deliverable-kdp` skill references.
- **Read-Aloud Edit**: Simulate reading aloud to catch awkward phrasing, repetition, and rhythm issues.
- **Final Proofread**: Line-by-line edit to catch any remaining errors before final output.

### Phase 6: Output Final Manuscript
- Save as polished `.md` file in the book directory
- Ready for handoff to the book publishing pipeline (`book-deliverable-kdp`,
  `manuscript-preparation-and-delivery`, `publishing-workflow`, etc.)

## Cover Art Generation (After Manuscript is Complete)

After the manuscript is finalized and before entering the publishing pipeline, generate the book cover. See `book-cover-design` skill for the full workflow.

### Cover Specs (from phase 0 research document `05_style_spec.md`)

Use the research-generated style specification to inform the cover design:
- **Genre** → determines cover visual language (from research in Phase 0.1-0.2)
- **Tone** → determines color palette (bright/hopeful vs dark/survival)
- **Key imagery** → extract pivotal scenes from the plot/thesis document (Phase 0.4)

### KDP Cover Compliance (mandatory)

See the full spec in `book-deliverable-kdp` skill. Summary:

| Format | Dimensions | Format | Color |
|---|---|---|---|
| **Kindle eBook cover** | **2560×1600 px** (1.6:1) | JPEG | RGB |
| **Paperback wrap** | Calculated per trim+pages | **PDF** | CMYK preferred |
| **Hardcover wrap** | Calculated per trim+pages (includes 0.189" board) | **PDF** | CMYK preferred |

- Title: large white bold with drop-shadow
- Author: Bob J Mills (bottom of cover)
- No front/back cover in manuscript — KDP Cover Creator handles that

## "Best Selling Author Quality" — Concrete Requirements

The style spec (Phase 0.5) is the primary style guide. In addition:

### Universal Quality Standards (All Genres)
- **Show, don't tell**: Concepts emerge through action, failure, and discovery, not exposition
- **Reader engagement**: Every scene advances the story or deepens understanding
- **Sensory detail**: Smell, sound, physical sensation, taste — not just visual
- **Varied sentence length**: Short for tension, longer for reflection
- **Dialogue/monologue that reveals character**: Distinct voices, not interchangeable
- **No AI-isms**: "delve", "leverage", "tapestry", "intricate", "fostering",
  "vibrant", "pivotal", "revolutionary", "game-changing", "synergy", "paradigm"

### Genre-Specific Guidance
- The **style specification** (Phase 0.5) overrides these general guidelines with
  genre-specific voice, pacing, and structural requirements derived from research.

## Production Approach

### Parallel Batch Writing (Preferred for 30+ Chapters)

1. **Phase 0 creates all planning docs**: concept, character roster, 40-chapter outline in `{book_dir}/research/`
2. **Write chapters in parallel batches** via `delegate_task`:
   - Batch 1: Chapters 1-10 (Part I)
   - Batch 2: Chapters 11-20 (Part II)
   - Batch 3: Chapters 21-30 (Part III)
   - Batch 4: Chapters 31-40 (Part IV)
3. **Each batch subagent receives**: the outline for their section, character doc, style spec, and research summary
4. **Each batch subagent writes**: 10 fully complete chapters of 1,000-1,400 words each
5. **After all batches return**: combine into single manuscript, add front/back matter

### 4-Part Narrative Framework

Structure chapters into a 4-part arc. Each part is ~10 chapters. The specific
themes come from the **plot/thesis document** (Phase 0.4):

| Part | Chapters | Narrative Function |
|------|:--------:|--------------------|
| I | 1-10 | **Setup** — introduce problem, characters, stakes |
| II | 11-20 | **Escalation** — complications multiply, stakes rise |
| III | 21-30 | **Climax** — everything on the line, breakthrough |
| IV | 31-40 | **Resolution** — aftermath, transformation, looking forward |

### Character Consistency Across Parallel Batches (Fiction)

- Each batch subagent receives the full character roster (Phase 0.6) with personality notes, speech patterns, and relationship dynamics
- A sample chapter from an already-written batch for tone/voice reference
- After all batches return: **character voice consistency check** — verify each major character sounds the same in all 4 parts

### Front Matter for Manuscript Files

Every compiled manuscript must include:
1. **Title page** — book title, subtitle, series name, author name
2. **Copyright page** — copyright notice, rights reserved, "Review proof — not for distribution"
3. **Table of Contents** — linked list of all chapter titles (no page numbers for eBook; page numbers for print)
   - Use consistent heading levels: `## Chapter N — Title` for all chapters
   - KDP requires TOC for books >20 pages (nav.xhtml for EPUB3 + HTML TOC for clickable navigation)
4. **All chapters** — in order, each starting with `## Chapter N — Title`, with page-break before each chapter
5. **About the Author** — back matter bio
6. **About the Series** — optional, listing other books in the series (for series books)

### Verification Checklist — Including All 11 Editorial Review Rules

Before handing off to the publishing pipeline, verify every item. The 11 editorial review rules (items 1-6 structural, 7-11 quality) determine the book's A-F rating.

**Structural Checks (1-6):**
- [ ] Phase 0 research complete: 01-07 files in `{book_dir}/research/`
- [ ] Core story concept/thesis defined in Phase 0.4
- [ ] Character roster includes 6–8 distinct individuals (fiction) with role, background, arc, and voice notes
- [ ] Style specification written (Phase 0.5) — genre-appropriate, research-informed
- [ ] Chapter outline contains 36–44 entries, each with title AND 3-5 specific beats
- [ ] Writing done in parallel batches of 10 chapters each via delegate_task
- [ ] Each chapter is 1,000-1,400 words
- [ ] Character voices consistent across all batches (spot-check at least one chapter from each batch)
- [ ] Manuscript has undergone flow, grammar, and formatting edits
- [ ] Total word count 40,000-56,000 for a ~175-225 page book at 6×9in
- [ ] Fabricated-claim integrity pass completed (non-fiction)
- [ ] Final output is a valid Markdown `.md` file
- [ ] **1. Chapter Images**: Each chapter has `![](chapter_images/chNN.png)` AFTER header, BEFORE content. Files exist. No cover images in manuscript.
- [ ] **2. Copyright & Acknowledgments**: Copyright © Bob J Mills, all rights reserved, ISBN placeholder, fiction disclaimer, edition info. Acknowledgments present. Front matter BEFORE Chapter 1.
- [ ] **3. Table of Contents**: All chapter titles listed, synced with headers. No gaps, wrong titles, or missing chapters. Handles worded/sequential numbering.
- [ ] **4. Back Matter — Full Book List**: "Also by Bob J Mills" with all 6 series in reading order. Reader magnet mention, author website, cross-promotion.
- [ ] **5. No Cover Images**: `grep "cover" MANUSCRIPT.md` returns 0 matches for cover-type images.
- [ ] **6. Page Count Target**: 6×9" PDF estimated at 160-190 pages (~44K-52K words at 275 w/p). Below 160p = P0 expand. Above 190p = P1 trim.

**Quality Checks (7-11):**
- [ ] **7. Character Consistency**: Names stable across chapters and books. Personas coherent. Cross-book name/relationship consistency.
- [ ] **8. Series Flow**: Previous events acknowledged, consequences carry forward. Ending hook pulls toward next book. Tone continuity.
- [ ] **9. Engagement & Readability**: Chapter-ending hooks (cliffhanger/revelation/question). Pacing has tension curve. Reader cares about outcome.
- [ ] **10. Plot Coherence**: Every setup has payoff. Cause-and-effect visible. No deus ex machina. Subplots resolved.
- [ ] **11. Genre Formatting**: Consistent chapter headers, uniform scene breaks, genre-appropriate paragraph style, proper dialogue formatting.

- [ ] Manuscript handed off to book publishing pipeline

## Pipeline Integration

Once Phase 6 produces the final `.md` manuscript, the book enters the
publishing pipeline:

1. **`book-deliverable-kdp`** — builds KDP package (EPUB, PDF, cover, metadata)
2. **`publishing-workflow`** — HTML generation, WeasyPrint PDF, EPUB building
3. **`manuscript-preparation-and-delivery`** — final formatting, proof generation
4. **`openclaw-hermes`** — compliance review, AI disclosure, multi-retailer readiness
5. **`add-book-to-pipeline`** — add to MIFECO pipeline dashboard
6. **`book-inventory-and-delivery`** — final delivery and organization

## Example Usage

```
User: "Write me a business book about AI for small agents"

Phase 0: Research best-selling AI/business books → extract patterns → generate
         original thesis, style spec, and 40-chapter outline with beats
         (saved to book_dir/research/)

Phase 1-3: Completed by Phase 0

Phase 4: Write 40 chapters in 4 parallel batches of 10, each following the
         style spec and chapter beats

Phase 5: Flow edit, humanize, grammar check, integrity pass

Phase 6: Final .md → publishing pipeline
```

## Notes
- The skill relies on other writing and manuscript skills for the actual
  text generation and editing steps; ensure those are available and
  functional.
- Adjust chapter length targets and number of chapters based on the
  desired final book length. Target is always 175-225 pages at 6×9in.
- For non-fiction: characters are replaced by author persona and case study
  frameworks. Adjust the Phase 0.6 step accordingly.
- **Non-fiction generated content must pass the fabricated-claim integrity
  pass** — see `book-deliverable-kdp` skill for the detection patterns.