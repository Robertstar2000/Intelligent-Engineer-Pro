---
name: memoir-assembly-with-transitions
description: Workflow for assembling memoirs where core user content must be preserved exactly while inserting substantial transitional content between sections
version: 1.0
author: Hermes Agent
---

## Memory context (Hindsight)

Long-term memory context is now provided automatically by Hindsight (bank
`mifeco-default`) on every turn — the retired MemPalace manual query step no
longer applies. Do NOT attempt to import `~/.hermes/mempalace` (it was removed
2026-08-19).This retrieves previous decisions, domain-specific context, and lessons learned from the vector memory store.

# Memoir Assembly with Transitions Skill

## Trigger Conditions\nUse this skill when:\n- Assembling a memoir or document where core user-provided content must be preserved exactly\n- Need to insert transitional content between sections (length can vary based on requirements)\n- Transitional content requires specific thematic elements (historical, psychological, technical, etc.)\n- Source content may be in various formats (markdown, DOCX, etc.) that need extraction and cleaning\n- Document is large enough to require chunked processing to avoid context window limits\n- Final output needs proper sequencing, table of contents, and component assembly (cover, intro, chapters)

## Workflow Steps

### 1. Source Content Preservation
- Identify the definitive source file containing the user's "edited stories" or core content
- Never modify this source file directly - treat it as immutable truth
- Extract all structural elements (headings, chapters, sections) from this source
- Verify no core content is altered during processing

### 2. Transition Point Identification
- Use regex to identify all insertion points (typically `^#` and `^##` for markdown headings)
- For each heading, plan to insert transition content immediately after the heading line
- Count total insertion points to estimate processing requirements
- If >50 insertion points, prepare for chunked processing

### 3. Transition Generation (Chunked Approach)
- Process in batches of 10-20 headings per LLM call to stay within context limits
- For each batch:
  * Provide the heading and surrounding context (previous/next content snippets)
  * Specify exact transition requirements (word count, thematic elements, tone)
  * Generate transitions that bridge preceding and following content
  * Include specific historical events, psychological concepts, or technical details as required
  * Maintain consistent voice matching the memoir's overall tone
- Store generated transitions with clear mapping to their insertion points

### 4. Component Assembly
- Create cover element (ASCII art, image reference, or placeholder)
- Include user-provided introduction/preface
- Generate proper table of contents as a hierarchical list of parts/chapters
- Interleave content in this order:
  * Cover
  * Introduction
  * For each section:
    - Heading line
    - Generated transition content (if applicable)
    - Preserved core content from source (until next heading)
- Ensure no core content is omitted or duplicated

### 5. Quality Verification
- **Reader engagement mandate**: All generated transitions and inserted content MUST be interesting, exciting, and engaging to readers. Every transition must do more than bridge sections — it must reveal character, build tension, deepen understanding, or create emotional resonance. No mechanical filler transitions.
- Compare source document against final manuscript to verify:
  * All original sentences/paragraphs appear exactly once
  * No core content is missing or altered
  * Transitions are inserted at correct locations
  * Transition content meets specified requirements (word count, themes)
- Check TOC accuracy against actual headings in final document
- Verify file size expectations (large increase due to transitions is expected)
- Verify each transition opens with a hook, includes sensory detail, and ends with narrative momentum.

## Pitfalls to Avoid
- **Content Overwriting**: Never let transition generation consume or replace source text
- **Context Loss**: When chunking, preserve enough context for coherent transitions
- **Voice Inconsistency**: Ensure transitions match the memoir's established tone
- **TOC Errors**: Generate TOC from actual final document headings, not source
- **Sequence Mistakes**: Maintain exact chapter/section ordering from source
- **Format Drift**: Preserve original markdown formatting in source content

## DOX Integration

When working in a project that uses the [DOX (Self-documenting AGENTS.md)](https://github.com/agent0ai/dox) framework:

- **Read Before Editing:** Walk the DOX tree from root to the target path. Read every AGENTS.md along the route before making any changes.
- **Update After Editing:** If the change affects purpose, scope, ownership, structure, workflows, or operating rules, update the closest owning AGENTS.md and refresh the Child DOX Index.
- **Reference:** [agent0ai/dox](https://github.com/agent0ai/dox) — copy `AGENTS.md` from the repo root into your project to initialize.

## Verification Checklist
- [ ] Source content appears intact and unaltered in final manuscript
- [ ] All transitions present at correct locations (after each heading)
- [ ] Transitions meet specified word count (±10%)
- [ ] Transitions contain required thematic elements (historical/psychological/etc.)
- [ ] TOC matches actual document structure exactly
- [ ] Cover and introduction properly positioned
- [ ] No duplicate or missing content blocks
- [ ] Consistent voice throughout transitions
- [ ] When using Hermes read_file tool, account for line number prefix format "     LINE|CONTENT" when processing content

## Example Commands
```bash
# For processing for memoir assembly:
python3 process_memoir.py \
  --source THE_UNWRITTEN_FUTURE_BACKUP.md \
  --output THE_UNWRITTEN_FUTURE_FINAL.md \
  --transitions-per-call 15 \
  --min-transition-words 800 \
  --max-transition-words 1000 \
  --transition-themes "historical events, psychological concepts" \
  --voice "reflective, matching author's persona"
```

## When to Use Alternative Approaches
- For small documents (<20 headings): Process in single LLM call
- For highly technical transitions: Consider using domain-specific APIs or data sources
- When cover image generation is needed: Integrate with image generation tools
- For collaborative workflows: Use version control to track changes to assembly script
- When working with Hermes agent's read_file tool: Remember it returns content with line number prefixes (e.g., "     1|actual content") that must be stripped before processing and potentially re-added for verification

## Pitfalls to Avoid (Updated)
- **Content Overwriting**: Never let transition generation consume or replace source text
- **Context Loss**: When chunking, preserve enough context for coherent transitions
- **Voice Inconsistency**: Ensure transitions match the memoir's established tone
- **TOC Errors**: Generate TOC from actual final document headings, not source
- **Sequence Mistakes**: Maintain exact chapter/section ordering from source
- **Format Drift**: Preserve original markdown formatting in source content
- **Line Number Prefix Confusion**: When using Hermes tools, remember that read_file returns lines with numeric prefixes that must be stripped for content analysis

## Maintenance Notes
- Update transition generation prompts if thematic requirements change
- Adjust chunk size based on LLM context window and transition complexity
- Verify script handles various markdown heading styles (atx, setext)
- Consider adding progress reporting for large documents