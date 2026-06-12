# Complete Editorial Review Checklist (11 Points)

Every review must evaluate ALL 11 points. Flag failures as P0 or P1 depending on severity.

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

### 3. Table of Contents
- [ ] All chapter titles listed and synced with actual headers
- [ ] No numbering gaps, no wrong titles
- [ ] Front matter (copyright, dedication) included if present
- [ ] Handles worded numbers (`Chapter One`) and non-sequential numbering

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

## Series-Level & Readability Checks (7-11)

### 7. Consistent Character Identity
- [ ] Names stable across every chapter (no Tom/Thomas/Tommy switching)
- [ ] Personas coherent — brave in Ch3 not cowardly in Ch12 without arc
- [ ] Cross-book: same name, baseline personality, relationships (Bk1→Bk4)
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
- **Method:** Check 5 chapters across the book for format consistency
- **Penalty:** Inconsistent = -0.5. Genre-mismatched = -1 (e.g., bullet lists in novel prose)

## Rating Quick Reference

| Rating | Meaning | Target |
|--------|---------|--------|
| A | Published bestseller quality | Final target |
| A- | Near-bestseller, one rewrite needed | Acceptable |
| B+ | Strong manuscript, solid foundation | Above-B threshold |
| B | Competent, needs significant revision | Below threshold |
| C+ | Has potential, major structural problems | Needs major work |
| C/D | Repetitive, templated, or broken | Needs full rewrite |