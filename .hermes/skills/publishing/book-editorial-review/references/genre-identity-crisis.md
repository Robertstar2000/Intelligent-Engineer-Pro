# Genre Identity Crisis: Pattern Detection and Handling

## The Pattern

A "genre identity crisis" occurs when a book in a series is written in a fundamentally different genre from the rest of the series. This renders the book incompatible with reader expectations and makes it unsellable as part of the series.

## Detection

Run these checks when reviewing 2+ books in a series:

```bash
# Check for different AI/setting names
grep -c "Mission AI\|UNIT-7\|Hymenarch\|sub-quantum" Book_*/MANUSCRIPT.md

# Check author name consistency
grep -oP "By (Bob J Mills|Bob Mills|Bob N\.)" Book_*/MANUSCRIPT.md

# Check protagonist name consistency across books
grep -oP "(Elena Varga|Elena Vargas|Elena Chen|Elara Varga)" Book_*/MANUSCRIPT.md | sort | uniq -c

# Check for genre markers (alien contact vs. colony politics)
grep -c "alien\|first contact\|Hymenarch\|quantum\|galactic" Book_*/MANUSCRIPT.md
```

## Real Example: No Blue Sky Book III — Rivers Under Mars

| Signal | Book I (Built from Dust) | Book III (Rivers Under Mars) | Verdict |
|--------|------------------------|---------------------------|---------|
| Genre | Mars colony politics, sovereignty | First-contact alien, sub-quantum | DIFFERENT |
| AI | Mission AI | UNIT-7 | DIFFERENT |
| Protagonist | Elena Varga | Elara Varga (different last name) | INCONSISTENT |
| Author | Bob J Mills | Bob Mills (missing middle initial) | INCONSISTENT |
| Tech base | Martian regolith, ISRU, domes | Sub-quantum skipping, hive logic | INCOMPATIBLE |
| Tone | Hard sci-fi colonization | Pulp SF alien contact | MISMATCHED |

## Handling Options

When you detect a genre identity crisis, present these options to the user:

1. **Regenre the outlier book** — Rewrite it to match the series genre (e.g., rewrite alien contact as a Mars political/engineering crisis)
2. **Spin off as a separate series** — The outlier book is strong in its own genre but doesn't belong here
3. **Accept the mismatch with framing** — Add series-connecting material (bridge chapters, references to prior events) so the genre shift feels like an evolution, not a reboot. This is the weakest option and still leaves the book feeling out of place.

## Rating Impact

A book with a genre identity crisis cannot be rated above C+ within the series context. On its own terms (as a standalone book in its actual genre), it may rate higher, but the series context is the evaluation frame unless the user directs otherwise.

**Always flag the mismatch explicitly in the review** — do not silently evaluate the book within its mismatched genre without calling out the incompatibility.