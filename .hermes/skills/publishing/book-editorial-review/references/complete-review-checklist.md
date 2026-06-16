# Complete Editorial Review Checklist (13 Points)

Every review must evaluate ALL 13 points. Flag failures as P0 or P1 depending on severity.

## Structural Checks (1-6)

### 1. Chapter Images
- [ ] Each chapter has `![](chapter_images/chNN.png)` AFTER the chapter header, BEFORE the content
- [ ] Image files actually exist in `chapter_images/`
- [ ] NO cover images in MANUSCRIPT.md

### 2. Copyright & Acknowledgments
- [ ] Copyright © 2026 Bob J Mills
- [ ] All rights reserved, ISBN placeholder, fiction disclaimer
- [ ] Acknowledgments section present
- [ ] Must appear as front matter BEFORE Chapter 1

### 3. Table of Contents (cross-check with chapter images)
- [ ] All chapter titles listed and synced with actual headers
- [ ] No numbering gaps, no wrong titles
- [ ] Front matter (copyright, dedication) included if present
- [ ] Handles worded numbers (`Chapter One`) and non-sequential numbering
- [ ] **TOC chapter count matches image reference count**: Run `grep -cP '^- Chapter|^## Chapter' MANUSCRIPT.md` vs `grep -c 'chapter_images' MANUSCRIPT.md`. Any mismatch is a P0 defect — image placeholders must be added for every chapter.
- [ ] **Covers excluded**: The cover image belongs in the EPUB/PDF build pipeline, NOT in the MANUSCRIPT.md. `grep "cover" MANUSCRIPT.md` should return NO matches for book-cover images.
- [ ] **No duplicate chapter titles**: `grep -oP '^#+ Chapter.*— \K.*' MANUSCRIPT.md | sort | uniq -d` should be empty.

### 4. Back Matter — Complete Book List
- [ ] All 6 series listed in reading order
- [ ] Amazon links (or `[LINK]` placeholder)
- [ ] Reader magnet novella mention
- [ ] Author website: mifeco.com
- [ ] Cross-promotion — list all series even if book is in only one

### 5. No Cover Images in Manuscript
- [ ] `grep "cover" MANUSCRIPT.md` returns NO book-cover matches
- [ ] Covers go in EPUB/PDF build pipeline only

### 6. Page Count Target
- [ ] 6×9" PDF yields 160-190 pages (~50K-70K words)
- [ ] Below 160p → P0: Expand. Above 190p → P1: Trim or tighten

## Series-Level & Readability Checks (7-13)

### 7. Consistent Character Identity (Names & Personas) — WITH CHARACTER MAP REQUIREMENT
- [ ] Names stable across every chapter (no Tom/Thomas/Tommy switching)
- [ ] Personas coherent — brave in Ch3 not cowardly in Ch12 without arc
- [ ] Cross-book: same name, baseline personality, relationships (Bk1→Bk4)
- [ ] **MANDATORY: Character Map per Book** — Book review includes a Character Map table (canonical name, aliases, role, first appearance, key relationships, voice/persona notes, books appearing in)
- [ ] **MANDATORY: Series Character Map** — Series review includes cross-book Character Map showing every recurring character with canonical name and any deliberate changes explained
- **Method:** Track 3 recurring characters across first/middle/final thirds
- **Penalty:** Name inconsistency = -1 grade. Persona drift = -0.5

### 8. Series Flow (Transition Between Books)
- [ ] Previous events acknowledged with consequences that carry forward
- [ ] Recap level is right — enough for forgetful readers, not boring for binge-readers
- [ ] Ending hook pulls toward next book (mystery, choice, new threat)
- [ ] Tone continuity with previous book
- **Method:** Read last 3 chapters of previous book + first 3 of this book
- **Penalty:** Tone break = -1. Missing/excessive recap = -0.5. Continuity error = -1

### 9. Engagement & Bestseller Readability
- [ ] Is this a page-turner? Review must answer directly
- [ ] Pacing: does the story drag in the middle? Tension curve?
- [ ] Emotional resonance — does the reader CARE about the outcome?
- [ ] Sentence-level rhythm — read 3 paragraphs aloud
- [ ] "Read one more chapter" test — each chapter ends with a reason to continue
- **Penalty:** Technically correct but boring = capped at B. Pacing problems = -0.5. Page-turner quality = +0.5

### 10. Plot Coherence (Follow-Through)
- [ ] Every setup has payoff — no loose threads
- [ ] Cause and effect visible — decisions ripple through later chapters
- [ ] No deus ex machina — problems solved by character actions, not coincidence
- [ ] Subplots have closure (even if resolution is "character accepts mystery")
- **Method:** Track 3 biggest mysteries/conflicts from first third → middle third → final third
- **Penalty:** Dropped thread = -1 per thread. Deus ex machina climax = -1.5. Perfect follow-through = +0.5

### 11. Genre-Appropriate Formatting
- [ ] Chapter header format consistent (same style, punctuation, spacing EVERY chapter)
- [ ] Scene break convention uniform (all `---` or all `***`, never mixed)
- [ ] Paragraph style fits genre (business: headers + boxes. Fiction: prose only, no bullet lists)
- [ ] Dialogue formatting correct (consistent quotes, new speaker = new paragraph)
- [ ] White space adequate — fiction chapters not dense legal documents

### 12. Plot Flow & Bestseller Quality — WITH PLOT MAP REQUIREMENT
- [ ] Plot flows consistently — each scene causes the next, not "and then this happened"
- [ ] Plot is interesting — stakes escalate, complications multiply, tension curves upward
- [ ] Plot is of bestseller quality — fresh twists, emotional stakes, genre-savvy execution
- [ ] No "idiot plot" — characters don't act stupidly just to advance the plot
- [ ] No deus ex machina — resolutions earned through character agency
- [ ] Subplots interweave with main plot, not run parallel without intersection
- [ ] The middle does not sag — Act II has rising complications, not filler
- [ ] Ending is both surprising and inevitable — the only way it could have gone
- [ ] **MANDATORY: Plot Map per Book** — Book review includes a Plot Map table showing:
    | Chapter Range | Core Conflict | Stakes | Key Twist/Revelation | Cause→Effect Link to Next | Resolution Status |
    |---|---|---|---|---|---|
    | Ch1-5 | [setup conflict] | [what's at risk] | [hook] | [how this causes Ch6-10] | [open/partial/closed] |
    | Ch6-10 | [escalation] | [higher stakes] | [complication] | [how this causes Ch11-15] | [open/partial/closed] |
    | Ch11-15 | [midpoint reversal] | [personal + public stakes] | [major revelation] | [how this causes Ch16-20] | [open/partial/closed] |
    | Ch16-20 | [dark night] | [all seems lost] | [false defeat] | [how this causes Ch21-25] | [open/partial/closed] |
    | Ch21-25 | [climax approach] | [final stakes] | [final preparation] | [how this causes Ch26-30] | [open/partial/closed] |
    | Ch26-30 | [climax] | [everything on the line] | [final confrontation] | [how this causes resolution] | [open/partial/closed] |
    | Ch31-35 | [fallout] | [consequences] | [new status quo] | [how this sets up next book] | [closed] |
    | Ch36-40 | [resolution] | [new normal] | [ending hook] | [series continuity] | [closed] |
- [ ] **MANDATORY: Series Plot Map** — Series review includes cross-book Plot Map showing:
    | Book | Core Conflict | Stakes Arc | Key Twists | How It Sets Up Next Book | Resolution |
    |---|---|---|---|---|---|---|
    | Book 1 | [conflict] | [low→high] | [twists] | [hook for Book 2] | [status] |
    | Book 2 | [conflict] | [higher] | [twists] | [hook for Book 3] | [status] |
    | Book 3 | [conflict] | [peak] | [twists] | [hook for Book 4] | [status] |
    | Book 4 | [conflict] | [resolution] | [twists] | [series conclusion] | [closed] |
- **Method:** Trace 3 main plot threads from setup through climax to resolution. Verify cause→effect chain is unbroken.
- **Penalty:** Broken cause→effect = -1 grade per break. Sagging middle = -0.5. Deus ex machina = -1.5. Dull/derivative plot = capped at B. Fresh, earned, page-turning plot = +0.5 over other metrics.

### 12B. Non-Fiction / Business Book Framework Map — WITH FRAMEWORK MAP REQUIREMENT

For business, self-help, and non-fiction books, the "Plot Map" is replaced by a **Framework Map** that tracks the book's argument architecture, not narrative arcs:

**MANDATORY: Framework Map per Book** — Book review includes a Framework Map table showing:

| Chapter Range | Core Thesis/Claim | Framework Element | Key Case Study | Actionable Takeaway ("The One Thing") | Reader Exercise/Tool | Cross-Chapter Link |
|---|---|---|---|---|---|---|
| Ch1-3 (Assess) | [Foundational claim] | [Assessment tool] | [Case study] | [Takeaway] | [Exercise] | [Sets up Ch4-6] |
| Ch4-7 (Choose) | [Selection criteria] | [Decision framework] | [Case study] | [Takeaway] | [Worksheet] | [Builds on Ch1-3] |
| Ch8-10 (Implement) | [Execution method] | [Rollout framework] | [Case study] | [Takeaway] | [Checklist] | [Leads to Ch11-12] |
| Ch11-12 (Optimize) | [Refinement principle] | [Optimization loop] | [Case study] | [Takeaway] | [Sprint template] | [Closes the loop] |

**MANDATORY: Series Framework Map** — Series review includes cross-book Framework Map:

| Book | Core Thesis | Framework Contribution | Key Frameworks Introduced | How It Builds on Previous | Reader Journey Position |
|---|---|---|---|---|---|
| Book 1 | [Thesis] | [Foundation] | [Frameworks] | [N/A or builds on] | [Entry point] |
| Book 2 | [Thesis] | [Deepening] | [Frameworks] | [Extends Book 1] | [Practitioner] |
| Book 3 | [Thesis] | [Mastery] | [Frameworks] | [Synthesizes 1-2] | [Expert] |

**Non-Fiction Quality Checks (replace fiction Plot Flow checks):**

- [ ] **Thesis clarity** — Core argument stated in Ch 1, reinforced every chapter
- [ ] **Framework utility** — Each chapter introduces/applies a reusable framework (not just advice)
- [ ] **Case study density** — ≥1 concrete case study per chapter (real, specific, with numbers)
- [ ] **Personal storytelling** — Author's own failures/successes woven throughout (vulnerability builds trust)
- [ ] **Provocative chapter headers** — Every chapter title makes a CLAIM reader wants to verify ("The $8M Mistake" not "Why Most Strategies Fail")
- [ ] **Implementation apparatus** — Every chapter ends with "The One Thing" + exercise/checklist/template
- [ ] **No filler** — Every paragraph advances argument or illustrates framework; zero consultant-speak padding
- [ ] **Cross-chapter coherence** — Frameworks build cumulatively; Ch 7's tool requires Ch 3's concept
- [ ] **Reader journey clarity** — Book positions reader at specific competency level (novice→practitioner→expert)
- [ ] **Companion resources** — Downloadable tools/templates referenced and actually exist

**Method:** Trace the core thesis through all 4 parts. Verify each chapter's framework element is distinct, reusable, and builds on prior. Check case studies for specificity (names, numbers, outcomes).
**Penalty:** Missing framework element = -0.5 grade per chapter. Descriptive (not provocative) headers = -0.5 per 4+ cluster. No personal stories = -1 grade. No implementation tools = -1 grade. Filler/consultant-speak = -0.5 per cluster. Broken framework chain = -1 grade per break.


### 13. Series-Level Failure Patterns (Multi-Book Reviews)
- **Method:** Check 5 chapters across the book for format consistency. For business NF, also check all chapter headers pass the "provocative claim" test.
- **Penalty:** Inconsistent = -0.5. Genre-mismatched = -1 (e.g., bullet lists in novel prose). Descriptive business NF headers = -0.5 per chapter cluster (4+ consecutive descriptive headers).

## Rating Quick Reference

| Rating | Quick | Meaning | Target |
|--------|-------|---------|--------|
| A | Published bestseller quality | Final target |
| A- | Near-bestseller, one rewrite needed | Acceptable |
| B+ | Strong manuscript, solid foundation | Above-B threshold |
| B | Competent, needs significant revision | Below threshold |
| C+ | Has potential, major structural problems | Needs major work |
| C/D | Repetitive, templated, or broken | Needs full rewrite |

## Iteration Convention

| Field | Iteration 1 (Fresh) | Iteration 2+ (Re-review) |
|-------|--------------------|------------------------|
| Heading label | `**Fresh Rating:** A-` | `**Rating:** B+` |
| Iteration | `**Iteration:** 1` | `**Iteration:** 2` (increment) |
| Changes Applied | `Initial review — fresh assessment. No changes applied.` | Describe what was fixed since last review |

The "Fresh" label signals the first review of an iteration cycle — the book has not been reviewed before or is starting a new editorial loop.