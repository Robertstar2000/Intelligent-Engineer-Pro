---
name: novel-writing-workflow
description: A systematic approach for writing long-form fiction using Hermes agent with detailed specifications
category: creative
---

## 🔍 MemPalace Query (MANDATORY FIRST STEP)
Before proceeding, query MemPalace for existing context:
```python
import sys, os; sys.path.insert(0, os.path.expanduser('~/.hermes/mempalace'))
import embed; embed.init_embedding(os.path.expanduser('~/.hermes/mempalace'))
results = embed.search_embeddings("novel writing workflow specification chapters fiction series", k=5)
```
This retrieves previous decisions, domain-specific context, and lessons learned from the vector memory store.

# Novel Writing Workflow for Hermes Agent

> Updated via skill patch test
A systematic approach for writing long-form fiction (novels, book series) using the Hermes agent, specifically designed for projects with detailed specifications and consistent formatting requirements.
See `references/observed-file-structures.md` for observed file structure patterns from actual book projects.

## When to Use
- Writing novels or book series with chapter-by-chapter specifications
- Projects requiring consistent formatting (specific headers, dialogue snippets, etc.)
- Long-form creative writing where maintaining voice and continuity is crucial
- Collaborative writing projects where the AI follows a human-defined outline

## Workflow Steps

### 1. Specification Review
- Read the project specification document (e.g., SPECIFICATION.md) to understand:
  - Overall plot arc and themes
  - Chapter-specific requirements and outlines
  - Character voices and development arcs
  - Required elements per chapter (e.g., Mission AI dialogue, character quotes)
  - Technical elements to weave into action
- Extract chapter-by-chapter breakdown for reference

### 2. Chapter Preparation
For each chapter:
- Read the specific chapter outline from the specification
- Identify required elements:
  - Mission AI dialogue snippet (opening)
  - Character quote (typically from main cast)
  - Technical transition/bridge (closing)
  - Key plot points to cover
  - Theme to explore
- Determine appropriate tone and pacing based on chapter position in arc

### 3. Writing Process\n- Open chapter file in book-sources directory\n- Write chapter following specification requirements:\n  - Start with Mission AI dialogue in italics\n  - Include character quote in italics after Mission AI\n  - Write main narrative in third-person limited or specified POV\n  - Weave technical elements into action (show, don't tell)\n  - End with technical transition/bridge that connects to next chapter\n- Maintain consistent voice for recurring characters\n- Ensure chapter advances overall plot while being self-contained\n\n## Large-Scale Project Management\nFor novels with 50+ chapters:\n- Create a chapter tracking system to monitor progress\n- Schedule regular consistency checks every 10-15 chapters\n- Use session_search to review earlier chapters when maintaining long arcs\n- Consider breaking work into thematic blocks (parts) for better organization\n- Keep a running list of unresolved plot points or character arcs to address\n- Periodically consolidate completed chapters to review overall flow and pacing\n- When stuck on a chapter, skip ahead and return later with fresh perspective\n- Maintain a master document with all completed chapters for periodic review\n\n### 4. Consistency Checks
- Verify character voices remain consistent
- Check that technical elements are accurate and integrated naturally
- Confirm chapter hits all specification points
- Ensure proper length and pacing
- Review for continuity with previous chapters

### 5. File Management\n- Save each chapter as individual markdown file:\n  ```\n  /home/bob/books/[Book_Title]/book-sources/[Book_Title]/Chapter_XX_[Title].md\n  ```\n- Use clear, descriptive chapter titles\n- Maintain consistent header formatting (## Chapter XX — Title)\n- Periodically consolidate chapters into master document for review\n- For publishing preparation, compile all chapters into a single manuscript\n\n### 6. Tools Utilized\n- `read_file`: To consult specification and reference materials\n- `write_file`: To create individual chapter files\n- `execute_code`: To run consolidation scripts (optional)\n- `session_search`: To reference previous chapters or writing decisions when needed\n\n### 7. Manuscript Compilation for Publishing\nWhen preparing a completed novel for publishing:\n- Verify all chapter files exist and are properly named (Chapter_01_Title.md through Chapter_NN_Title.md)\n- If multiple manuscript candidates exist (for example a clean full manuscript, an assembled intro/TOC file, and a partially rewritten variant), audit them before choosing a base. Prefer the cleanest continuous source file over a noisier “complete” file that may contain duplicate slug headings, packaging artifacts, or mixed rewrite styles.\n- Do **not** blindly merge partial rewrites into a full novel unless the whole book will be brought to the same voice. Mixing only a few rewritten chapters into an otherwise older draft creates tonal inconsistency that hurts publish readiness.\n- Create a compilation script that:\n  - Reads chapters in numerical order\n  - Adds a title page with book title and subtitle\n  - Inserts horizontal rules (---) between chapters for readability\n  - Formats chapter headings consistently (## Chapter XX)\n  - Preserves all original content exactly as written unless you are intentionally doing an editorial pass\n- Execute the script to produce a single manuscript file\n- Verify the compiled manuscript:\n  - Check file size and line count\n  - Confirm all chapters are present in correct order\n  - Validate formatting is consistent\n  - Confirm there are no duplicate chapter headings or filename-slug headings (for example `## Chapter 01 — The_Title`) left in the assembled book\n- Use the compiled manuscript for:\n  - Human review and approval\n  - Publishing platform uploads (Kindle, etc.)\n  - Creating backups and distribution files\n\n## Example Compilation Script\n```python\nimport os\n\nbase_dir = \"/path/to/book/sources\"\nchapters = [\n    (1, \"Chapter_Title_1\"),\n    (2, \"Chapter_Title_2\"),\n    # ... continue for all chapters\n    (64, \"Final_Chapter_Title\")\n]\n\nchapter_files = [f\"Chapter_{num:02d}_{name}.md\" for num, name in chapters]\n\n# Verify files exist\nmissing = []\nfor filename in chapter_files:\n    if not os.path.exists(os.path.join(base_dir, filename)):\n        missing.append(filename)\n\nif missing:\n    print(f\"Missing files: {missing}\")\nelse:\n    output_path = \"/path/to/output/COMPILED_MANUSCRIPT.md\"\n    with open(output_path, 'w', encoding='utf-8') as outfile:\n        outfile.write(\"# Book Title\\n\\n\")\n        outfile.write(\"*Subtitle or tagline*\\n\\n\")\n        outfile.write(\"---\\n\\n\")\n        \n        for i, (num, name) in enumerate(chapters, 1):\n            filepath = os.path.join(base_dir, f\"Chapter_{num:02d}_{name}.md\")\n            with open(filepath, 'r', encoding='utf-8') as infile:\n                content = infile.read().strip()\n                outfile.write(f\"## Chapter {num}\\n\\n\")\n                outfile.write(content)\n                outfile.write(\"\\n\\n---\\n\\n\")\n    \n    print(f\"Compiled manuscript saved to: {output_path}\")\n```

## Novel Rewrite and Production Strategy
For large-scale rewrites (50+ chapters) or projects with high structural complexity:
- **Deconstruction (Shattering):** If the original project exists as a single "Complete" manuscript but lacks individual source files, use `execute_code` with Regex to "shatter" the manuscript back into individual source files (`book-sources/`) first.
- **Tone-of-Voice Anchors:** Establish specific formatting rules early (e.g., italicized Mission AI dialogue snippets at headers) to ground the AI in the new tone for every chapter.
- **Batch Processing:** Process thematic blocks (e.g., 8-chapter parts) or segments to maintain stylistic continuity and stay within context window limits.
- **Custom PDF Generation:** If professional "bestseller" formatting (Times New Roman, A4, justified text, page breaks) is needed and standard tools like Pandoc fail, use `reportlab` in `execute_code` to generate a high-quality PDF.
- **Persistent Progress Tracking:** Use the `todo` tool to monitor progress. In the event of turn-interruption or timeouts, the task list allows for immediate resumption without re-auditing.

## Quality Standards
- **Humanization mandate (ALL books, all projects)**: Before writing, editing, or rewriting any manuscript content, load the `humanizer` skill and apply its 29 pattern checks and PERSONALITY AND SOUL section. No AI-isms, no filler, real voice, variable rhythm, opinions where they fit, first-person when honest. This is mandatory for every piece of book prose without exception.
- **Reader engagement mandate**: Every piece of added material — new chapters, transitions, bridge passages, expanded sections, or connective tissue — MUST be interesting, exciting, and engaging to readers. This is not optional. Every added sentence must earn its place.
- Each chapter must include required Mission AI dialogue and character quote.
- Technical elements should emerge naturally from character actions and plot; follow the "Technology Writing Rules" (showing tech through use, failure, and cultural meaning).
- Maintain "best-seller" prose style: character-driven, emotionally resonant, high-tension.
- Balance action, dialogue, and description appropriately.
- Ensure each chapter contributes to the overall narrative arc (e.g., the escalating tension between Martian Sovereignty and Earth Central AI).
- Keep technical explanations integrated, not expository.
- Added material must open with a hook, end with a reason to keep reading, and include concrete sensory detail — never exposition filler.

## Customization Points
- Adjust character focus based on chapter needs
- Vary pacing (action vs. introspection chapters) as needed
- Modify technical depth based on specification requirements
- Adapt chapter length while maintaining consistency

## Example Chapter Structure
```
## Chapter XX — [Chapter Title]

*Mission AI: "[Relevant dialogue reflecting chapter theme]"*  
*[Character Name]: "[Relevant quote reflecting chapter theme]"*

[Opening scene setting tone and immediate context]

[Character-driven action advancing plot]
[Technical elements woven into character actions and decisions]
[Dialogue revealing character relationships and motivations]
[Building tension or revelation per chapter outline]

[Closing scene with technical transition/bridge that connects to next chapter's setup]
```

## Troubleshooting
- **Voice inconsistency**: Refer to character voice documents (e.g., MISSION_AI_VOICE.md)
- **Plot deviation**: Re-read specification chapter outline
- **Technical accuracy issues**: Research or consult technical references in specification
- **Pacing problems**: Adjust balance of action/dialogue/description
- **Continuity errors**: Use session_search to review previous chapters
- **Partial-rewrite temptation**: Do not blindly merge a handful of rewritten chapters into an otherwise older draft unless the whole novel will be brought to the same voice; hybrid manuscripts usually feel tonally uneven and less publish-ready.
- **Long rewrite reliability**: For full-book editorial rewrites, use a resumable chapter-by-chapter pipeline that saves state after each completed chapter, writes a rolling compiled manuscript, and logs progress. This makes 50+ chapter rewrites recoverable across API failures, timeouts, and resumptions.

### 8. Cover Art Text Overlay (Post-Generation)
When generating covers via AI (Flux, Pollinations), the images are often returned as "clean" plates without readable text. To ensure retailer readiness, use `PIL` (Pillow) to overlay bold, high-contrast titles.
- **Font Selection:** Use bold sans-serif fonts (e.g., `DejaVuSans-Bold.ttf`) at a scale visible at thumbnail size (typically 80px+ for 1024px width).
- **Readability:** Always add a 2px offset drop-shadow (black) behind the white text to ensure readability against complex sci-fi backgrounds (stars, nebulae, dust).
- **Positioning:** Center titles in the upper third or lower third, avoiding the middle band where the main subject usually resides.

```python
from PIL import Image, ImageDraw, ImageFont
img = Image.open(path).convert('RGB')
draw = ImageDraw.Draw(img)
font = ImageFont.truetype(font_path, 80)
draw.text(((w - tw) / 2 + 2, top + 2), title, font=font, fill='black') # Shadow
draw.text(((w - tw) / 2, top), title, font=font, fill='white') # Main
```

## AI Disclosure Compliance (KDP)
When using this workflow, maintain a `KDP_AI_DISCLOSURE.md` file to track:
- **Text:** Disclose as "AI-Assisted" if steered by human specification/theme.
- **Images:** Disclose as "AI-Generated" (specify model: Flux, Stable Diffusion).
- **Formatting:** Disclose as "AI-Generated" (HTML/CSS layout).

## Checking Book Project Status

When checking the status of a book project, if the `book_source` directory appears empty, check the `output` directory for compiled manuscripts (e.g., EPUB, PDF) to confirm the book has been published and is in the promotion phase.

Example structure:
```
/home/bob/books/[Book_Title]/
├── book_source/          # Should contain chapter markdown files
├── output/               # Contains compiled manuscripts (EPUB, PDF, etc.)
└── ...                   # Other resources (covers, marketing materials)

If `book_source` is empty but `output` contains a manuscript, the book is likely published.
