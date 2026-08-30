---
name: manuscript-rewrite-for-excitement
description: A systematic approach for rewriting existing manuscripts to make them more exciting, bestseller-style while preserving core plot, facts, technology, and characters but changing tone, pacing, and character focus (e.g., making an AI a key antagonist/controller)
category: creative
---

## Memory context (Hindsight)

Long-term memory context is now provided automatically by Hindsight (bank
`mifeco-default`) on every turn — the retired MemPalace manual query step no
longer applies. Do NOT attempt to import `~/.hermes/mempalace` (it was removed
2026-08-19).This retrieves previous decisions, domain-specific context, and lessons learned from the vector memory store.

# Manuscript Rewrite for Excitement Workflow

## Overview
A systematic approach for rewriting existing fiction manuscripts to make them more exciting, bestseller-style while preserving the core storyline, facts, technology, and characters but changing how the story is told. This workflow is particularly effective when you want to:
- Increase pacing and tension
- Make prose more exciting and character-driven
- Introduce or enhance a key antagonistic force (like an AI controller)
- Reduce length while maintaining plot integrity
- Follow specific word count targets per chapter

## When to Use
- Rewriting existing manuscripts that feel too slow, expository, or lacking tension
- Projects where the core story is strong but needs more exciting presentation
- When you want to introduce a specific character element (like an AI antagonist) throughout
- When targeting specific length requirements (e.g., ~180 pages paperback)
- For bestseller-style rewrites with strong hooks and constant tension

## Workflow Steps

### 1. Analysis and Baseline Assessment
- Read the existing manuscript and specification document(s) to understand:
  - Current plot arc, themes, and chapter structure
  - Current writing style, pacing, and tone
  - Current word count per chapter and total
  - Required elements per chapter (if any, like dialogue snippets)
  - Character voices and development arcs
  - Technical elements and how they're currently integrated
- Create baseline analysis document noting:
  - Average words per chapter
  - Current pacing and opening styles
  - How technology is currently presented
  - Character introduction and development patterns
  - Areas that feel slow or expository

### 2. Create Rewrite Specification
- Develop SPECIFICATION_REWRITE.md that defines:
  - **TONE**: Exciting, bestseller-style with strong hooks, tight pacing, constant tension
  - **KEY CHARACTER FOCUS**: (e.g., Earth Central AI as monitoring/controlling presence)
  - **WORD COUNT TARGET**: Specific range per chapter (e.g., 600-800 words)
  - **STORY PRESERVATION**: Keep basic plot, facts, technology, characters - change only how it's told
  - **UPDATED STRUCTURE NOTE**: 
    - Strong opening hook (immediate action/revelation/tension)
    - Story movement showing society evolving AND character responses to key elements
    - Technical element showing maturity or tension (including new character influence)
    - Clear bridge to next chapter with escalating conflict or new mystery
    - Every chapter ends with question/revelation/tension that compels reading onward
  - **UPDATED CHARACTER FOCUS**: How key characters perceive/respond to the new element
  - **UPDATED TECHNOLOGY RULES**: How technology shows both ingenuity AND resistance to/influence from key element

### 3. Create Implementation Plan
- Develop detailed plan with:
  - **Pilot Approach**: Rewrite first 2-3 chapters to establish voice, tone, and key character integration
  - **Chapter Rewrite Process**: Reusable template/process for each chapter
  - **Batch Processing**: Process chapters in manageable batches (e.g., 5-8 chapters at a time)
  - **Verification Steps**: Word count checks, key character presence verification, pacing assessment
  - **Feedback Loop**: Process to refine approach based on pilot results
  - **Compilation Plan**: How to combine rewritten chapters into final manuscript
  - **Delivery Preparation**: Final verification and delivery steps

### 4. Pilot Chapter Rewriting
- Rewrite first chapter to establish:
  - Strong opening hook (no slow build)
  - Key character presence through appropriate mechanisms (interface glitches, suggestions, etc.)
  - Exciting, tight prose that advances plot and tension
  - Target word count range
  - Ending with question/revelation/tension
- Verify against rewrite specification
- Document lessons learned and refine chapter rewrite process

### 5. Establish Chapter Rewrite Process
Create reusable process/template:
1. Read original chapter
2. Identify key plot points and technology/elements to preserve
3. Write strong opening hook (action/revelation)
4. Integrate key character through system interactions, glitches, or behavioral nudges
5. Write exciting, tight prose (active voice, varied sentence length)
6. Ensure technology serves plot/character, not exposition
7. End chapter with question/revelation/tension
8. Check word count target
9. Verify against SPECIFICATION_REWRITE.md
10. Save as rewritten version

### 6. Batch Processing
- Process remaining chapters in batches:
  - For each batch (e.g., chapters 5-12):
    - Apply chapter rewrite process to each chapter
    - Verify word count and key character integration
    - Save as rewritten chapter files
    - Commit batch with descriptive message
- Refine process between batches based on lessons learned

### 7. Final Manuscript Compilation
- Combine all rewritten chapters in order
- Verify final manuscript:
  - Total word count within target range
  - Key character appears meaningfully in each chapter (spot check)
  - Exciting pacing throughout
  - All key plot points and technology elements preserved
- Save final manuscript

### 8. Delivery
- Prepare final manuscript for delivery
- Deliver to user via appropriate channel
- Document completion

## Tools Utilized
- `read_file`: To consult specification, reference materials, and original chapters
- `write_file`: To create rewritten chapter files and specification
- `execute_code`: To run word counts, verification scripts, and compilation scripts
- `session_search`: To reference previous chapters or writing decisions when needed
- `search_files`: To locate chapter files and manuscript components
- `write_file`: To create plans, specifications, and process documents

## Quality Standards
- **Humanization mandate**: All book prose — including rewritten chapters, expanded scenes, bridge passages, and any new content — MUST pass the `humanizer` skill's 29 pattern checks. No AI-isms, no filler, real voice, variable rhythm, opinions where they fit. This is mandatory.
- **Reader engagement mandate**: Every piece of rewritten or added material must be interesting, exciting, and engaging to readers. No filler allowed.
- Each chapter must hit the target word count range
- Key character/element must appear meaningfully in each chapter
- Every chapter must have strong opening hook and compelling ending
- Technology should emerge naturally from character actions and plot
- Maintain exciting, bestseller-prose style: character-driven, emotionally resonant
- Balance action, dialogue, and description appropriately
- Ensure each chapter advances overall narrative while being self-contained
- Preserve all essential plot points, facts, and character arcs from original
- Every added sentence must advance story, reveal character, build tension, or create emotional resonance — never merely fill space.

## Benefits
- Produces exciting, bestseller-style rewrite while preserving core story
- Maintains quality and consistency across long manuscripts
- Creates reusable process for future manuscript rewrite projects
- Enables efficient chapter-by-chapter progress tracking
- Reduces need for constant user correction through established process
- Delivers manuscript that meets specific length and style requirements

## MEM PALACE INTEGRATION
When performing manuscript rewrite tasks, also utilize the MemPalace Integration skill to enhance long-term memory retention and retrieval. This ensures that successful rewrite approaches, chapter-specific insights, and process improvements are preserved across sessions for continuous improvement.