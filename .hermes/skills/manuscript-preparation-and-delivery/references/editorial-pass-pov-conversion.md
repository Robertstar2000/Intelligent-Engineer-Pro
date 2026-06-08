# Editorial Pass: POV Conversion Artifacts

## Session Context
May 9, 2026 — Full editorial pass on "Tomorrow Is Still Open" (memoir, ~180K chars, 178 pages).
The manuscript was originally written in first-person ("I") and converted to third-person ("Bob").
The editorial pass found and fixed 14+ POV conversion artifacts that standard grammar checkers miss.

## Full Fix List (Real Examples)

| Issue | Before | After |
|-------|--------|-------|
| "Bob would ordered" | `Bob would ordered from some magazine` | `Bob had ordered from some magazine` |
| "Bob wish Bob could" | `Bob wish Bob could tell you` | `Bob wishes he could tell you` |
| "Bob would said" | `Bob would said something` | `Bob had said something` |
| "Bob would learned" (x3) | `Bob would learned that Bob was capable` | `Bob had learned that Bob was capable` |
| "Bob would gotten" | `what Bob would gotten` | `what Bob had gotten` |
| "Bob would had" | `better than anything Bob would had` | `better than anything Bob had` |
| "Bob discover" | `Each visit, Bob discover something new` | `Each visit, Bob discovered something new` |
| "Bob sometimes wonder" | `Bob sometimes wonder if his father knew` | `Bob sometimes wonders if his father knew` |
| "Bob still carry" | `a moment Bob still carry with him` | `a moment Bob still carries with him` |
| "Bob carry feels" | `The memory Bob carry feels real` | `The memory Bob carries feels real` |
| "Bob have studied" | `Bob have studied the neuroscience` | `Bob has studied the neuroscience` |
| "Bob know about" | `Bob know about synaptic plasticity` | `Bob knows about synaptic plasticity` |
| "Bob have never" | `Death is a part of life Bob have never` | `Death is a part of life Bob has never` |
| "Bob only remember" | `Bob only remember the photograph` | `Bob only remembers the photograph` |
| "only remember his mother" | `or only remember his mother` | `or only remembers his mother` |
| "Did Bob remembered" | `Did Bob remembered these things?` | `Did Bob remember these things?` |
| "remembereded" (x2) | `Bob remembereded his mother's advice` | `Bob remembered his mother's advice` |
| "inches from mine" | `inches from mine` | `inches from his` |
| "curved away from mine" | `curved away from mine` | `curved away from his` |

## Structural Duplicates Found

### Duplicate Transition Sections
A "Transition: From Wood to Stars" section appeared TWICE in the manuscript (lines 306-312 originally). The second instance had a dropped word ("learned to models" vs "learned to build models"). This happens when content from two source files is merged and both had the same transition.

**Fix:** Remove the second occurrence entirely and verify the remaining one is complete.

### Redundant Story Sections
Chapter 9 already covered Bob meeting Cindy on Plenty of Fish. A later section (lines 900-906) titled "### The Singles club – Plenty of Fish" and "### Then He Met Her." told the exact same story again with different wording.

**Fix:** Remove the redundant section and verify the transition into Chapter 10 is clean.

## Front Matter Checklist (Memoir)

For Bob's memoirs, always include these pages in order:

1. **Title page** — Title / Subtitle / Author
2. **Copyright page** — Copyright notice, all-rights-reserved, AI disclosure (if applicable), publisher info
3. **Acknowledgments** — Personal acknowledgments for family (parents, Nancy, Cindy, children, grandchildren)
4. **Table of Contents** — Part + chapter listing
5. **Book body** — Part dividers (w/ images if available) + chapters + transitions
6. **Back matter** — Author note / letter to descendants / life lessons

The copyright page is distinct from the marketing/compliance docs in the KDP package. Include both.