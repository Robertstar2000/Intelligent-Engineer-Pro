# Chapter Writing Patterns for Bulk Manuscript Generation

## Approach
For large manuscripts (30-90 chapters), write each chapter individually via `delegate_task` subagents rather than batching multiple chapters per subagent.

### Why Individual Chapter Delegation?
- Batching 5+ chapters per subagent hits the 600s timeout limit
- Individual chapter delegation (~3-7 min each) allows each chapter to save to disk immediately
- Each subagent fully reads previous chapters for voice continuity — quality is dramatically higher
- If a subagent times out, only one chapter is lost
- Running 3 concurrent subagents (one per book) creates an efficient pipeline

### The Proven Pipeline Pattern
```
# 3 concurrent subagents, each writing ONE chapter:
delegate_task(chapter_N_of_book_1)  ← includes context from ch(N-1)
delegate_task(chapter_M_of_book_2)  ← includes context from ch(M-1)  
delegate_task(chapter_K_of_book_3)  ← includes context from ch(K-1)
# Each subagent reads existing chapters, writes one, saves to disk
# Result: ~3 chapters every 5-8 minutes of wall-clock time
```

### Context to Include Per Subagent
Each chapter subagent receives:
- Writing style rules (first person past tense, no AI-isms, em-dash limit)
- Character roster with correct names (Cindy Lou, not just Cindy)
- Specific chapter beats (3-5 plot points that MUST be hit)
- Continuity notes from prior chapters
- Exact file path to save to (e.g., `chapters/ch07.md`)

### Continuity Technique
Each subagent should READ the most recent chapter(s) before writing. Include this instruction explicitly: "Read ch01.md through ch(N-1).md for voice consistency."

### File Naming Convention
Use `ch01.md`, `ch02.md` ... `ch30.md` — NOT `Chapter_01_Title.md`. Shorter names, sequential, zero-padded.

### Output Format Per Chapter
```
[First person prose — indented paragraphs via writing style]

* * *

[Scene break]

* * *

[Cliffhanger ending — specific hook for next chapter]
```

NO markdown heading (`## Chapter XX — Title`) in the prose — the chapter file is body text only.

### Image Generation (Covers + Chapter Illustrations)
- Generate B&W chapter images separately using Gemini 2.5 Flash Image
- One image per chapter, grayscale, high contrast (1.5x)
- Prompt: "Black and white illustration for Chapter [N]: [title]. [theme]. No text. Grayscale."
- Post-process: convert to grayscale mode 'L', enhance contrast 1.5x, sharpen
