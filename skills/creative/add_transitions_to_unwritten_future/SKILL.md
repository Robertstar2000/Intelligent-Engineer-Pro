---
name: add_transitions_to_unwritten_future
description: Adds historical and psychological transitions between sections/chapters/stories in The Unwritten Future manuscript.
category: creative
---


## 🔍 MemPalace Query (MANDATORY FIRST STEP)
Before proceeding, query MemPalace for existing context:
```python
import sys, os; sys.path.insert(0, os.path.expanduser('~/.hermes/mempalace'))
import embed; embed.init_embedding(os.path.expanduser('~/.hermes/mempalace'))
results = embed.search_embeddings("MIFECO business process", k=5)
```
This retrieves previous decisions, domain-specific context, and lessons learned from the vector memory store.

# Add Transitions to The Unwritten Future

This skill processes the manuscript file `/home/bob/books/The_Unwritten_Future/THE_UNWRITTEN_FUTURE_FINAL.md` and inserts a ~900-word historical/psychological transition after each major heading (lines starting with `# ` or `## `). The transitions are crafted to maintain narrative flow, tying the preceding and following content with relevant historical context and psychological insight, and include detailed descriptions of historical events and deeper psychological explanations.

## When to Use
- When the manuscript feels disjointed between chapters or sections.
- To enrich the reading experience with contextual depth that mirrors Bob’s introspective voice.
- To prepare the text for publishing or further editing.

## Workflow Steps

### 1. Backup the Original
- The skill first creates a timestamped backup of the original file in the same directory.

### 2. Read the Entire File
- The file is read in its entirety using a sufficiently large limit to avoid chunking issues with line-number-prefixed output from read_file.

### 3. Strip Line Number Prefixes
- Each line from read_file includes a prefix like "     1|". This prefix is stripped to get the actual content.

### 4. Detect Headings
- A line is considered a heading if it begins with `# ` (Chapter) or `## ` (Section/Subsection) after stripping leading whitespace.

### 5. Generate Transition Text
- For each heading, a transition is generated that:
  - Summarizes the historical period or psychological theme implied by the heading.
  - Connects the prior narrative’s emotional tone to the upcoming one.
  - Uses Bob’s voice: reflective, futurist, grounded in science and personal experience.
  - Includes detailed descriptions of historical events and deeper psychological explanations.
  - Targets approximately 900 words to provide substantial contextual bridging.

### 6. Insert Transition
- The transition is inserted on a new line directly after the heading line, followed by a blank line before the original content continues.

### 7. Write the Updated File
- The processed lines are written back to the original location, overwriting the manuscript.
- The backup remains available for recovery if needed.

### 8. Verification
- The skill reports the number of headings processed and the approximate added word count.
- A quick sanity check ensures the file still opens and that no heading was duplicated.

## Tools Utilized
- `read_file` and `write_file`: Used for initial testing and verification, but note that in some execution contexts (like execute_code or terminal), the hermes_tools module may not be available.
- `terminal`: For running standalone Python scripts that handle file operations using standard Python open/read/write functions when hermes_tools is unavailable.
- `execute_code`: To run the Python script that performs the chunked reading, heading detection, transition generation, and writing (when hermes_tools is available).
- `memory`: To store the backup file path and processing stats for potential future reference.

## Important Notes on Tool Availability
- In certain execution contexts (particularly when using the execute_code tool directly), the hermes_tools module may not be importable, resulting in ModuleNotFoundError.
- When this occurs, a reliable alternative is to create a standalone Python script that uses standard Python file operations (open, read, write) and execute it via the terminal tool.
- The read_file tool returns content with line number prefixes (e.g., "     1|content") that must be stripped to get the actual line content before processing.

## Quality Standards\n- Transitions must not alter the original story content; they only add contextual bridging.\n- Language should match the memoir’s tone: candid, slightly nostalgic, intellectually curious.\n- Historical facts should be accurate to the era referenced in the adjacent sections.\n- Psychological concepts should be drawn from reputable sources (e.g., Cognitive Behavioral Theory, memory reconsolidation, flashbulb memory, etc.) and explained in layperson’s terms.
- **Physiological effects** should be integrated to describe the body's stress responses (adrenaline, cortisol, oxytocin) and their impact on memory and emotion.
- No markdown syntax errors are introduced; heading levels remain unchanged.
- The original manuscript content must be verifiably preserved in the output (check via diff or content sampling).\n- No markdown syntax errors are introduced; heading levels remain unchanged.\n- The original manuscript content must be verifiably preserved in the output (check via diff or content sampling).\n\n## Customization Points\n- Adjust the target word count per transition by editing the `TRANSITION_WORD_COUNT` constant in the script.\n- Change the backup directory or naming scheme via the `BACKUP_DIR` variable.\n- To focus only on certain parts (e.g., only Part One), modify the heading detection regex.\n- Adapt heading detection patterns if source uses different heading formats (e.g., ###, or different spacing).\n\n## Example Transition (Illustrative)\nAfter the heading `# Chapter One: The Shock`, a transition might read:\n\n> The summer of 1958 was more than a seasonal shift; it marked the cusp of a postwar America poised on the edge of rapid technological optimism and simmering social unrest. As the nation absorbed the launch of Sputnik the previous year, a six‑year‑old Bob’s encounter with a live electrical outlet became a personal flashbulb moment—a vivid, emotionally charged snapshot that, according to cognitive psychologists, is encoded with extra detail due to the surge of adrenaline and fear. This biological imprint set the stage for a lifelong fascination with invisible forces, linking the intimate jolt of childhood curiosity to the broader societal current of seeking understanding in an age where the universe suddenly felt both larger and more accessible.\n\n## Workflow Enhancements Based on Experience\n\n### Preserving Original Content\n- Always work from a verified backup of the original manuscript\n- After processing, verify that original story segments remain intact by spot-checking known content\n- Use diff tools to confirm only transitional content was added\n\n### Table of Contents Generation\n- Ensure TOC is formatted as a proper hierarchical list (not just copied headings)\n- Include proper indentation to show chapter/section relationships\n- Verify all major sections appear in the TOC\n\n### Cover Generation Approach\n- When local font packages (pyfiglet, figlet) are unavailable, use remote ASCII art APIs as fallback\n- Validate ASCII art output fits within reasonable width constraints\n- Consider providing both ASCII and graphical cover options when possible\n\n### Heading Detection Robustness\n- Test heading detection on sample content before full processing\n- Allow configuration of heading patterns (e.g., '# ', '## ', '### ') \n- Log number of headings detected for verification\n\n## Notes\n- Because the manuscript exceeds typical token limits, the skill relies on chunked reading and writing to avoid truncation.\n- The backup file follows the pattern `THE_UNWRITTEN_FUTURE_FINAL.md.backup_YYYYMMDD_HHMMSS`.\n- If the process is interrupted, the original file remains intact via the backup, allowing a safe retry.\n- Heading detection should be validated against the actual manuscript format to ensure proper transition placement.\n\n## MEM PALACE INTEGRATION\nWhen performing manuscript transition tasks, also utilize the MemPalace Integration skill to enhance long-term memory retention and retrieval. This ensures that successful transition generation approaches and insights about the manuscript's structure are preserved across sessions for continuous improvement.