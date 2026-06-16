# Genre Benchmarks for Editorial Review

## Space Opera (Age of Lightships)

### Bestselling Comparisons

| Dimension | The Expanse (Corey) | Revelation Space (Reynolds) | Children of Time (Tchaikovsky) |
|-----------|-------------------|----------------------------|-------------------------------|
| Opening hook | Canterbury disaster in first scene | Ship graveyard, protagonist out of time | First page: failed terraforming experiment |
| POV count | 3-4 per book, distinct voices | 2-3 per book | Dual narrative (spiders + humans) |
| Pacing | Quiet/setpiece alternating every 3-4 ch | Slow burn with explosive climaxes | Generational pacing with acceleration |
| Dialogue | Subtext-heavy, characters deflect | Cold, precise, withholding | Philosophical, revelatory |
| Stakes | Personal + civilizational BOTH present | Existential mystery | Evolutionary survival |

### Key Metrics for A-Level
- Opening hook within first 500 words
- 3-4 POVs maximum, each with distinct sentence rhythm and vocabulary
- Setpiece every 3-4 chapters
- Dialogue where characters rarely say what they mean
- Personal stakes connected to civilizational stakes
- Scientific rigor: technology has consequences

## Hard Sci-Fi Colonization (Lunar Foundation)

### Bestselling Comparisons

| Dimension | The Martian (Weir) | Red Mars (Robinson) | Seveneves (Stephenson) |
|-----------|------------------|-------------------|----------------------|
| Tone | Humor under pressure, first-person voice | Philosophical, political | Technical, urgent |
| Problem structure | Problem → solve → failure → new solution | Escalating ideological conflict | Single disaster → cascading complications |
| Character | Engineer as problem-solver | Generational cast with irreconcilable worldviews | Technical experts under existential pressure |
| Science | Accurate, drives plot | Ecological realism, terraforming as character | Hard physics based on real proposals |

### Key Metrics for A-Level
- Problem→solution→failure→new solution cycle (at least 3 iterations)
- Opening disaster or irreversible choice within first page
- Characters with irreconcilable worldviews/ideologies
- The science carries emotional weight, not just technical detail

## Martian Colonization Epic (No Blue Sky)

### Key Metrics for A-Level
- Protagonist with PERSONAL motivation (not abstract "for humanity")
- Ideological opponent arguing the opposite position
- The planet itself as a character with personality (danger, beauty, scale)
- Multiple factions with different goals
- Generational scope — consequences of decisions ripple across decades

## Cozy Mystery (Cindy Lou Legal Capers)

### Bestselling Comparisons

| Dimension | Precious Ramotswe (McCall Smith) | Thursday Murder Club (Osman) | Stephanie Plum (Evanovich) |
|-----------|--------------------------------|----------------------------|--------------------------|
| Voice | Warm, gentle, philosophical | Witty, ensemble banter | First-person, self-deprecating |
| Mystery role | Framework for character | Clever puzzle within relationships | Excuse for chaos/humor |
| Romantic tension | Background | Absent (married) | Central (Morelli vs Ranger) |
| Word count | 55-65K | 70-80K | 60-70K |

### Key Cozy Mystery Conventions (NON-NEGOTIABLE)

1. **Amateur sleuth** — protagonist is NOT a professional detective or licensed attorney actively practicing
   - Cindy Lou is a working lawyer → this breaks cozy convention
   - Fix: She practices "unusual" law (barter, favors, helping friends) rather than active criminal defense
2. **Small contained community** — the series needs a neighborhood, village, or workplace ecosystem
3. **No explicit violence, gore, or sex**
4. **Humor and warmth throughout** — even the villain isn't purely evil
5. **Found family** — quirky supporting cast that appears in every book
6. **Romantic subplot** — tension without resolution (will-they-won't-they)
7. **Word count**: 50-70K (strict) — NOT 100K+

### Key Metrics for A-Level
- Chapter length: 1,500-2,000 words (fast, punchy)
- Dialogue-driven, not description-driven
- Every chapter ends with a mini-cliffhanger or revelation
- 30 maximum chapters for a 60K book

## Business Non-Fiction

### Bestselling Comparisons

| Dimension | Zero to One (Thiel) | Atomic Habits (Clear) | Lean Startup (Ries) |
|-----------|-------------------|---------------------|--------------------|
| Structure | One provocative thesis per chapter | One idea + one story + one application | Case-study driven |
| Chapter length | 2,000-3,000 words | 2,000-3,000 words | 3,000-5,000 words |
| Voice | Contrarian, opinionated | Clear, humble, evidence-based | Technical, narrative |
| Takeaway | Implicit — reader connects dots | Explicit "The One Thing" box | Implicit in case study |

### Key Metrics for A-Level
- Every chapter has ONE idea, argued with evidence
- Chapter headers are PROVOCATIVE claims, not descriptive labels
- Personal stories from the author in every section
- "The One Thing" takeaway at end of each chapter
- No filler sentences — every paragraph advances the argument

## Memoir

### Bestselling Comparisons

| Dimension | Educated (Westover) | When Breath Becomes Air (Kalanithi) | Wild (Strayed) |
|-----------|-------------------|------------------------------------|-----------------|
| Voice | First-person, specific, unflinching | First-person, philosophical, earned | First-person, raw, vulnerable |
| Opening | A single vivid childhood memory | Doctor-patient scene | The trail, alone, broken |
| Structure | Chronological with thematic threading | Chronological with philosophical interludes | Journey mirroring interior arc |
| Contract | The author's specific experience | The author's specific experience | The author's specific experience |
| Word count | ~85K | ~80K | ~90K |
| Scene/summary ratio | Heavy scene, minimal summary | Heavy scene | Heavy scene |
| Reflection style | Earned through narrative, never explains | Trusts reader to find meaning | Trusts reader to find meaning |

### 11-Point Memoir Checklist

Every memoir review MUST evaluate ALL 11 items. Flag failures as P0 or P1.

| # | Check | Fail Marker | Detection Method |
|---|-------|-------------|------------------|
| 1 | First person throughout (not third) | P0: POV slippage into "he" | grep -n -e '\bhe would\b' -e '\bhe had\b' -e '\bhe learned\b' MANUSCRIPT.md |
| 2 | Opens with a vivid single scene, not a life summary | P0: First 500 words are biography | Read first 500 words — one specific time+place+incident? |
| 3 | Reflection earned through narrative (not explained) | P1: "This taught me…" / explicit philosophy | Count instances of explicit lesson-stating |
| 4 | Key events rendered as scenes, not summaries | P1: Death/relationship mentioned but not shown | Every death/illness/wedding must have sensory setting + dialogue |
| 5 | Front/back matter present | P1: Missing copyright, TOC, back matter | grep for ©, Table of Contents, Also by |
| 6 | Word count at genre target (70-90K) | P1: Under 70K or over 90K | wc -w |
| 7 | NO speculative futurology | P0: AGI, quantum, space, climate predictions | grep for 'will be' / 'may' / 'could' in final chapters |
| 8 | NO identity-summary opening ("I was born in…") | P0: Opener is biography, not narrative | Check first paragraph structure |
| 9 | Dialogue and sensory detail carry weight | P1: Flat prose, no physical grounding | Minimum 2 sensory details per scene |
| 10 | Consistent POV — no narrator pronoun switching | P1: Mixed "I" and "he" for narrator | grep narrative sections for third-person pronouns |
| 11 | Unique chapter titles — no duplicate names | P2: Two chapters share the same title | grep -oP '^#+ Chapter.*— \K.*' | sort | uniq -d |

### Critical Memoir Rules
1. **MUST be first person** — "I remembered..." not "Bob remembered..."
2. **Opens with a single vivid scene** — NOT a life summary, NOT "I was born in..."
3. **Reflection is earned through narrative** — don't explain meaning, let the reader feel it. Flag "This taught me..." / "The lesson was..." / "What I learned is..." as over-explanation.
4. **Dialogue and sensory detail carry weight** — show, don't tell
5. **NO speculative futurology** — if the last chapters pivot to AGI prediction, quantum computing, space settlement, or climate projections, the memoir contract is broken. These sections must be removed or relocated to a separate companion work.
6. **Every death/relationship/event MUST be rendered as a scene** — not referenced, not summarized, actually shown with sensory detail
7. **Word count**: 70-90K — NOT 52K (too short), NOT 116K (too long for debut memoir)
8. **POV consistency across ALL chapters** — use grep to detect third-person slippage: search for '\bhe\b', '\bhis\b', and '\bhim\b' in first-person narrative sections. Common error: engineering chapters accidentally written in third person.
9. **No duplicate chapter content** — check for the same story told in multiple chapters (e.g., Y2K appearing 3 times, hangar fire appearing 2-3 times, same romance story retold). grep for unique key phrases from repeated stories.
10. **"I wa" typo detection** — search for ' wa ' (missing 's' in "was"). This is a common copy-paste artifact in first-person manuscripts.
11. **Unique chapter titles** — ensure no two chapters share the same title (common when chapters are assembled from separate documents). grep for duplicate titles.

### POV Slip Detection Technique (Essential for Memoir Reviews)

Memoirs written in first person sometimes have sections that were drafted in third person and not fully converted. Run this detection in every memoir review:

```bash
# Check for "he" referring to the narrator in narrative sections
grep -n -e '\bhe would\b' -e '\bhe had\b' -e '\bhe was\b' -e '\bhe learned\b' -e '\bhe worked\b' MANUSCRIPT.md | grep -i -v 'father\|dog\|grandf\|teacher\|Mr\.\|Hendricks\|Kovacs\|Richardson\|son\|friend\|colleague\|pilot\|doctor\|Chen\|said he\|he said\|he asked\|he replied\|he told'

# Check for "I wa" typo (should be "I was")
grep -n ' wa ' MANUSCRIPT.md

# Check for pronoun confusion in dialogue tags
grep -n 'sI said' MANUSCRIPT.md  # should be "she said"
grep -n 'I looked at me' MANUSCRIPT.md  # likely should be "He looked at me"
```

### Memoir Review Format Requirements

Every memoir book-review.md must use this exact section ordering:

```markdown
# Editorial Review: [Book Title]

**Title:** [title]
**Author:** [author]
**Review Date:** YYYY-MM-DD
**Iteration:** 1
**Fresh Rating:** A/A-/B+/B/C+/C/D/F
**Word Count:** [N words]
**Chapter Count:** [N]
**Target Range:** 70,000-90,000 words
**Shortfall:** [N words]

## Executive Summary

[2-3 paragraphs. MUST state findings as facts, no hedging.]

## [N]-Point Checklist Evaluation

[Explicit enumeration of the 11 checklist items with PASS/FAIL/MARGINAL per item]

## Strengths (With Evidence)

[Numbered, with specific chapter evidence — line numbers, quoted passages]

## Critical Weaknesses — MUST FIX

[Organized as P0/P1/P2, with concrete chapter numbers and evidence]

## Bestseller Benchmark Comparison

[Table comparing against Educated, When Breath Becomes Air, Wild across 6-8 dimensions]

## Changes Applied

Iteration 1: "Initial review — fresh assessment. No prior changes applied."

## Remaining Issues (P0/P1/P2)

[Sequenced by severity]

## Single Highest-Impact Revision

[One paragraph describing the single change that would most improve the book]

## Next Step Decision

[One paragraph describing what should happen next]

## Rating

**Rating: X** — [explicit "above B+" or "below B+" statement]

Examples:
- **Rating: A-** — Above B+. Near-bestseller quality.
- **Rating: B+** — Below A range, above B. Strong foundation with structural gaps.
- **Rating: B** — Below A and B+ ranges. Competent but needs significant revision.
- **Rating: C+** — Well below B+. Major structural problems.
```