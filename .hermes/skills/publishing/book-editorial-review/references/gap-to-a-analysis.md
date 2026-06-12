# Gap-to-A Analysis Template

A targeted review that identifies ONLY the improvements needed to reach A rating, without re-writing or re-rating the book. Useful when the user asks: "identify only what's needed for an A rating."

## When to Use

- The user asks "do an editorial review on all books under A and identify only improvements needed to reach A"
- You need to prioritize which books to work on next
- You need a roadmap, not another rewrite pass

## Process

### Step 1: Collect Current Ratings

```bash
for f in $(find /mnt/usb_4tb/books -name "book-review.md" -not -path "*/_archived/*" | sort); do
  rating=$(grep -m1 -i "rating:" "$f" | sed 's/.*\*\*Rating:\*\*\s*//' | sed 's/(.*)//' | tr -d '[:space:]')
  echo "  [$rating]  $(dirname "$f" | sed 's|/mnt/usb_4tb/books/||')"
done
```

### Step 2: For Each Book Under A, Read the Existing Review

Extract:
- Current rating and why it's held there
- The "Single Highest-Impact Revision" from the review
- Any P0 issues that are blocking A
- Word count vs genre target

### Step 3: Categorize into Tiers

**Quick wins (30 min — 1 pass to A-):**
- Minor formatting issues (epilogue header artifacts, duplicate chapter numbers)
- Simple chapter cleanup (merge duplicates, renumber)
- Small word count gaps (within 2-5K of target)

**Major work (1-2 weeks — 3-6 passes to A-):**
- Missing central crisis or antagonist action
- Word count 10-30K below target
- Summary chapters need conversion to full scenes
- Missing subplot activation

**Massive work (months — 10+ passes to A):**
- Word count 70K+ below target (e.g., 16K vs 90K)
- Source material nearly exhausted
- Needs complete chapter-by-chapter expansion
- Genre-level issues

### Step 4: Per-Book Gap Documentation

For each book, document the gap-to-A in this format:

```
### Book Title || Current Rating
| Gap | Severity | Fix |
|-----|----------|-----|
| [Specific gap] | P0/P1/P2 | [Concrete fix description] |
→ **To A-:** [One-sentence summary of effort needed]
```

**Severity definitions:**
- **P0:** Must fix — structural blocker
- **P1:** Should fix — quality gap
- **P2:** Nice to have — polish

### Step 5: Genre-Specific Gap Patterns

**Sci-Fi Colonization Thriller (Lunar Foundation) — gaps to A:**
- No central crisis or cascading failure
- No visible antagonist action (sabotage, recall order, blocked supply)
- No irreversible choice tied to the plot
- Word count 50-70% below target
- Summary chapters instead of full scenes
- Placeholder transitions
- Flat secondary characters

**Cozy-Legal Hybrid (Cindy Lou) — gaps to A:**
- No chapter headers (scene breaks only)
- Spoiler placement (flash-forward that reveals ending)
- Word count far below or above genre target
- Thin supporting cast
- AI-template language in narration
- Duplicate chapter numbering from expansions

**Space Opera (Age of Lightships) — gaps to A:**
- Word count 30-50% below 90K target
- Missing flashbacks/backstory chapters
- Thin middle section between setup and climax
- Underused antagonist
- Repetitive ship-loss structure

**Business Non-Fiction (MIFECO) — gaps to A:**
- Consultant-speak instead of first-person founder voice
- Word count below 40K minimum
- Front matter title mismatch
- Missing Part dividers for framework
- No Table of Contents

**Memoir (Tomorrow Remembered) — gaps to A:**
- Source material nearly exhausted
- Word count 50% below 90K target
- Uneven chapter distribution
- Speculative content needing voice conversion

### Step 6: Triage Summary

End with a summary table:

```
### Quick Wins (1-2 passes to A-)
| Book | Current → Target | Fix | Effort |

### Major Work (3-6 passes to A-)
| Book | Current → Target | Fix | Effort |

### Massive Work (10+ passes to A)
| Book | Current → Target | Fix | Effort |
```