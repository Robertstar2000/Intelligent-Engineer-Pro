---
name: manuscript-preparation-and-delivery
description: Workflow for preparing completed manuscripts for review and delivery, including file consolidation, front matter creation, and messaging platform delivery
category: creative
---


## Memory context (Hindsight)

Long-term memory context is now provided automatically by Hindsight (bank
`mifeco-default`) on every turn — the retired MemPalace manual query step no
longer applies. Do NOT attempt to import `~/.hermes/mempalace` (it was removed
2026-08-19).This retrieves previous decisions, domain-specific context, and lessons learned from the vector memory store.

# Manuscript Preparation and Delivery

## Workflow

1. **Character name check** — Before any editorial work, check character names against the avoid list in `references/character-name-avoid-list.md`. All first names must come from the SSA top 50. If AI-typical names are found, use the replacement procedure in `references/character-name-standardization.md`.

2. **Manuscript modification** — When adding chapters, appendices, or modifying front matter:
   - Use Python scripts for bulk text manipulation (find-and-replace, section insertion)
   - Always fix title pages to ONE title page per book (not duplicate blocks)
   - Update the TOC to reflect all current chapters
   - Update chapter counts in the preface if chapters are added/removed

3. **Pipeline build** — Use `hermes_publish/step_pdf.py` and `hermes_publish/step_epub.py` to regenerate output files. See `references/hermes-publish-pipeline.md` for known issues with the `manuscript_md` type and the `collect_chapters()` function.

4. **Page count verification** — For 6"×9" books, target 160-275 pages. For 8.5"×11" business books, target 160-275 pages. Word count ÷ 350 ≈ body pages, plus ~10 for front/back matter.

## Key References

- `references/character-name-avoid-list.md` — Names that must not be used
- `references/character-name-standardization.md` — Full find-and-replace procedure for renaming
- `references/hermes-publish-pipeline.md` — Pipeline bugs, front matter structure, chapter numbering