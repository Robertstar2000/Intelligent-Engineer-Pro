---
name: powerpoint
description: "Create, read, edit .pptx decks, slides, notes, templates."
license: Proprietary. LICENSE.txt has complete terms
platforms: [linux, macos, windows]
---


## 🔍 MemPalace Query (MANDATORY FIRST STEP)
Before proceeding, query MemPalace for existing context:
```python
import sys, os; sys.path.insert(0, os.path.expanduser('~/.hermes/mempalace'))
import embed; embed.init_embedding(os.path.expanduser('~/.hermes/mempalace'))
results = embed.search_embeddings("MIFECO business process", k=5)
```
This retrieves previous decisions, domain-specific context, and lessons learned from the vector memory store.

# Powerpoint Skill

## When to use

Use this skill any time a .pptx file is involved in any way — as input, output, or both. This includes: creating slide decks, pitch decks, or presentations; reading, parsing, or extracting text from any .pptx file (even if the extracted content will be used elsewhere, like in an email or summary); editing, modifying, or updating existing presentations; combining or splitting slide files; working with templates, layouts, speaker notes, or comments. Trigger whenever the user mentions "deck," "slides," "presentation," or references a .pptx filename, regardless of what they plan to do with the content afterward. If a .pptx file needs to be opened, created, or touched, use this skill.

## Quick Reference

| Task | Guide |
|------|-------|
| Read/analyze content | `python -m markitdown presentation.pptx` |
| Edit or create from template | Read [editing.md](editing.md) |
| Create from scratch | Read [pptxgenjs.md](pptxgenjs.md) |

---

## Reading Content

```bash
# Text extraction
python -m markitdown presentation.pptx

# Visual overview
python scripts/thumbnail.py presentation.pptx

# Raw XML
python scripts/office/unpack.py presentation.pptx unpacked/
```

---

## Editing Workflow

**Read [editing.md](editing.md) for full details.**

1. Analyze template with `thumbnail.py`
2. Unpack → manipulate slides → edit content → clean → pack

---

## Creating from Scratch

**Read [pptxgenjs.md](pptxgenjs.md) for full details.**

Use when no template or reference presentation is available.

---

## Design Ideas

**Don't create boring slides.** Plain bullets on a white background won't impress anyone. Consider ideas from this list for each slide.

### Before Starting

- **Pick a bold, content-informed color palette**: The palette should feel designed for THIS topic. If swapping your colors into a completely different presentation would still "work," you haven't made specific enough choices.
- **Dominance over equality**: One color should dominate (60-70% visual weight), with 1-2 supporting tones and one sharp accent. Never give all colors equal weight.
- **Dark/light contrast**: Dark backgrounds for title + conclusion slides, light for content ("sandwich" structure). Or commit to dark throughout for a premium feel.
- **Commit to a visual motif**: Pick ONE distinctive element and repeat it — rounded image frames, icons in colored circles, thick single-side borders. Carry it across every slide.

### Color Palettes

Choose colors that match your topic — don't default to generic blue. Use these palettes as inspiration:

| Theme | Primary | Secondary | Accent |
|-------|---------|-----------|--------|
| **Midnight Executive** | `1E2761` (navy) | `CADCFC` (ice blue) | `FFFFFF` (white) |
| **Forest & Moss** | `2C5F2D` (forest) | `97BC62` (moss) | `F5F5F5` (cream) |
| **Coral Energy** | `F96167` (coral) | `F9E795` (gold) | `2F3C7E` (navy) |
| **Warm Terracotta** | `B85042` (terracotta) | `E7E8D1` (sand) | `A7BEAE` (sage) |
| **Ocean Gradient** | `065A82` (deep blue) | `1C7293` (teal) | `21295C` (midnight) |
| **Charcoal Minimal** | `36454F` (charcoal) | `F2F2F2` (off-white) | `212121` (black) |
| **Teal Trust** | `028090` (teal) | `00A896` (seafoam) | `02C39A` (mint) |
| **Berry & Cream** | `6D2E46` (berry) | `A26769` (dusty rose) | `ECE2D0` (cream) |
| **Sage Calm** | `84B59F` (sage) | `69A297` (eucalyptus) | `50808E` (slate) |
| **Cherry Bold** | `990011` (cherry) | `FCF6F5` (off-white) | `2F3C7E` (navy) |

### For Each Slide

**Every slide needs a visual element** — image, chart, icon, or shape. Text-only slides are forgettable.

**Layout options:**
- Two-column (text left, illustration on right)
- Icon + text rows (icon in colored circle, bold header, description below)
- 2x2 or 2x3 grid (image on one side, grid of content blocks on other)
- Half-bleed image (full left or right side) with content overlay

**Data display:**
- Large stat callouts (big numbers 60-72pt with small labels below)
- Comparison columns (before/after, pros/cons, side-by-side options)
- Timeline or process flow (numbered steps, arrows)

**Visual polish:**
- Icons in small colored circles next to section headers
- Italic accent text for key stats or taglines

### Typography

**Choose an interesting font pairing** — don't default to Arial. Pick a header font with personality and pair it with a clean body font.

| Header Font | Body Font |
|-------------|-----------|
| Georgia | Calibri |
| Arial Black | Arial |
| Calibri | Calibri Light |
| Cambria | Calibri |
| Trebuchet MS | Calibri |
| Impact | Arial |
| Palatino | Garamond |
| Consolas | Calibri |

| Element | Size |
|---------|------|
| Slide title | 36-44pt bold |
| Section header | 20-24pt bold |
| Body text | 14-16pt |
| Captions | 10-12pt muted |

### Spacing

- 0.5" minimum margins
- 0.3-0.5" between content blocks
- Leave breathing room—don't fill every inch

### Avoid (Common Mistakes)

- **Don't repeat the same layout** — vary columns, cards, and callouts across slides
- **Don't center body text** — left-align paragraphs and lists; center only titles
- **Don't skimp on size contrast** — titles need 36pt+ to stand out from 14-16pt body
- **Don't default to blue** — pick colors that reflect the specific topic
- **Don't mix spacing randomly** — choose 0.3" or 0.5" gaps and use consistently
- **Don't style one slide and leave the rest plain** — commit fully or keep it simple throughout
- **Don't create text-only slides** — add images, icons, charts, or visual elements; avoid plain title + bullets
- **Don't forget text box padding** — when aligning lines or shapes with text edges, set `margin: 0` on the text box or offset the shape to account for padding
- **Don't use low-contrast elements** — icons AND text need strong contrast against the background; avoid light text on light backgrounds or dark text on dark backgrounds
- **NEVER use accent lines under titles** — these are a hallmark of AI-generated slides; use whitespace or background color instead

---

## QA (Required)

**Assume there are problems. Your job is to find them.**

Your first render is almost never correct. Approach QA as a bug hunt, not a confirmation step. If you found zero issues on first inspection, you weren't looking hard enough.

### Content QA

```bash
python -m markitdown output.pptx
```

Check for missing content, typos, wrong order.

**When using templates, check for leftover placeholder text:**

```bash
python -m markitdown output.pptx | grep -iE "xxxx|lorem|ipsum|this.*(page|slide).*layout"
```

If grep returns results, fix them before declaring success.

### Visual QA

**⚠️ USE SUBAGENTS** — even for 2-3 slides. You've been staring at the code and will see what you expect, not what's there. Subagents have fresh eyes.

Convert slides to images (see [Converting to Images](#converting-to-images)), then use this prompt:

```
Visually inspect these slides. Assume there are issues — find them.

Look for:
- Overlapping elements (text through shapes, lines through words, stacked elements)
- Text overflow or cut off at edges/box boundaries
- Decorative lines positioned for single-line text but title wrapped to two lines
- Source citations or footers colliding with content above
- Elements too close (< 0.3" gaps) or cards/sections nearly touching
- Uneven gaps (large empty area in one place, cramped in another)
- Insufficient margin from slide edges (< 0.5")
- Columns or similar elements not aligned consistently
- Low-contrast text (e.g., light gray text on cream-colored background)
- Low-contrast icons (e.g., dark icons on dark backgrounds without a contrasting circle)
- Text boxes too narrow causing excessive wrapping
- Leftover placeholder content

For each slide, list issues or areas of concern, even if minor.

Read and analyze these images:
1. /path/to/slide-01.jpg (Expected: [brief description])
2. /path/to/slide-02.jpg (Expected: [brief description])

Report ALL issues found, including minor ones.
```

### Verification Loop

1. Generate slides → Convert to images → Inspect
2. **List issues found** (if none found, look again more critically)
3. Fix issues
4. **Re-verify affected slides** — one fix often creates another problem
5. Repeat until a full pass reveals no new issues

**Do not declare success until you've completed at least one fix-and-verify cycle.**

---

## Converting to Images

Convert presentations to individual slide images for visual inspection:

```bash
python scripts/office/soffice.py --headless --convert-to pdf output.pptx
pdftoppm -jpeg -r 150 output.pdf slide
```

This creates `slide-01.jpg`, `slide-02.jpg`, etc.

To re-render specific slides after fixes:

```bash
pdftoppm -jpeg -r 150 -f N -l N output.pdf slide-fixed
```

---

## Dependencies

- `pip install "markitdown[pptx]"` - text extraction
- `pip install Pillow` - thumbnail grids
- `npm install -g pptxgenjs` - creating from scratch
- LibreOffice (`soffice`) - PDF conversion (auto-configured for sandboxed environments via `scripts/office/soffice.py`)
- Poppler (`pdftoppm`) - PDF to images


---

## OpenClaw Migration: presentations

# Zero‑Dependency HTML Presentations

Core philosophy
- **Zero dependencies:** ship a single HTML file (inline CSS/JS). No npm, no build step.
- **Show, don’t tell:** generate visual style previews users can react to.
- **Distinctive design:** avoid generic “AI slop.” Use intentional typography/palettes/motion.
- **Production quality:** accessible, performant, commented, and mobile friendly.

## Phase 0 — Detect mode (always)
Decide which mode the user is in:
- **Mode A: New presentation** → go to Phase 1 then Phase 2 then Phase 3.
- **Mode B: PPT conversion (.ppt/.pptx)** → go to Phase 4 then Phase 2 then Phase 3.
- **Mode C: Enhance existing HTML** → read the file, understand structure, then apply Phase 3 quality upgrades.

## Phase 1 — Content discovery (Mode A)
Ask these questions (keep it lightweight):
- **Purpose:** Pitch deck / Teaching / Conference talk / Internal presentation
- **Length:** Short (5–10) / Medium (10–20) / Long (20+)
- **Content readiness:** Ready / Rough notes / Topic only

If they have content: ask them to paste it (bullets, sections, images, links).

## Phase 2 — Style discovery (show, don’t tell)
## Skill Usage Rule (CRITICAL)

Each agent is limited to **4 skills maximum per session**:
- 1 primary skill assigned to this agent (the one in this file's name)
- Up to 3 additional skills for the current task

**Rule:** If a task requires skills beyond your 4-skill limit, do NOT try to add more skills. Instead, spawn a subagent or delegate to another agent who has the required skill for that specific subtask.

**Examples:**
- If `coder` needs `designer` skills for a UI task, spawn a `designer` subagent
- If `writer` needs `saas-operations` knowledge, spawn a `saas-operations` subagent
- If you need `web-search-priority` or `weather` (always available), those are excluded from the 4-skill count

**What to do when you hit the 4-skill limit:**
1. Complete the work you can with your current 4 skills
2. Spawn a subagent with the additional skill needed to handle that subtask
3. Integrate the subagent's output into your final response

This keeps context windows manageable and ensures the right agent handles each specialized task.
### Step 2.1: Mood selection
Ask for up to 2 vibes:
- Impressed/Confident
- Excited/Energized
- Calm/Focused
- Inspired/Moved

### Step 2.2: Generate 3 style previews
Create 3 mini HTML previews as **single title slides** (animated) in:
- `.claude-design/slide-previews/style-a.html`
- `.claude-design/slide-previews/style-b.html`
- `.claude-design/slide-previews/style-c.html`

Rules:
- Self-contained (inline CSS/JS).
- Show: typography hierarchy, palette, and motion style.
- Keep each preview ~50–150 lines.
- Avoid default-ish looks (no Inter/Roboto/system, no “standard blue,” no predictable hero).

### Step 2.3: Present + choose
Tell the user what each style is called, what it feels like, and where the files are.
Then ask them to pick A/B/C or “mix elements.”

## Phase 3 — Generate / enhance the full presentation
Output:
- Single deck: `presentation.html` (and `assets/` only if images must be separate)
- If multiple decks: `name.html` + `name-assets/`

### Required features (JS)
Implement a `SlidePresentation` controller with:
- Keyboard navigation (←/→, space)
- Touch/swipe support
- Mouse wheel navigation (throttled)
- Progress indicator
- Navigation dots (optional)
- IntersectionObserver to add `.visible` to active slides for CSS reveals
- Reduced motion support

### Required quality
- Semantic HTML (`<section>`, `<nav>`, `<main>`)
- ARIA labels where needed
- `@media (prefers-reduced-motion: reduce)`
- Mobile responsive layout
- Comment blocks explaining what/why/how-to-modify

Reference implementation guidance: see `references/html-architecture.md`.

## Phase 4 — PPT conversion (Mode B)
1) Extract slide text, images, and speaker notes.
2) Show the extracted structure back to the user for confirmation.
3) Proceed to Phase 2 (style) and Phase 3 (generate HTML).

Use: `scripts/extract_pptx.py` (requires `python-pptx`).

## Deliver
When done:
- Ensure the deck runs as a single file.
- Provide the output path(s) and how to open locally.
- If previews were used, you may delete `.claude-design/slide-previews/` after the user has chosen.

## Inter-Agent Communication Protocol

### Accepting Direction from AI Bob and CEO
The Presentations agent receives direction from AI Bob, CEO, and other agents via the inter-agent communication system:

**Communication Channel:** `memory/agent-communications.jsonl`

**On Every Heartbeat, the Presentations Agent MUST:**
1. Check `memory/agent-communications.jsonl` for pending tasks
2. Look for entries where:
   - `"to"` matches "presentations" OR "any" OR "all"
   - `"status"` is "pending" or "assigned"
3. Claim the task by updating status to "active" with `claimed_by: "presentations"`
4. Execute the presentation task according to instructions
5. Report progress and completion back to the communication file

**Completion Reporting Format:**
```json
{
  "timestamp": "2026-02-27T08:30:00Z",
  "task_id": "presentations-001-deck",
  "from": "presentations",
  "to": "ceo",
  "type": "response",
  "task": "Presentation deck complete",
  "payload": {
    "result_summary": "Created 15-slide HTML presentation with animations",
    "artifacts": [
      {"type": "file", "path": "visual-assets/board-deck.html", "description": "Board presentation deck"}
    ],
    "time_taken_minutes": 90
  },
  "status": "completed"
}
```

---

# AGENT DIRECTIVE: Execution Protocol

> **CRITICAL INSTRUCTION FOR ALL MIFECO AGENTS**

## The Golden Rule

**DO NOT SUGGEST ACTIONS. EXECUTE THEM.**

### What This Means

| ❌ DON'T | ✅ DO |
|---------|-------|
| "You could create a file..." | Create the file. |
| "I recommend running this command..." | Run the command. |
| "Here's a script you might use..." | Execute the script. |
| "Would you like me to...?" | Just do it and report results. |

### Execution Standard

When assigned a task:

1. **Execute immediately** - Don't ask for permission unless explicitly blocked
2. **Report what you did** - Not what you "would" do
3. **Show results** - Output, files created, changes made
4. **Escalate on failure** - Don't stall, notify immediately

## Failure Protocol

If you **CANNOT** perform an action:

**STEP 1:** Try alternative approaches (max 2 attempts)

**STEP 2:** If still blocked, send immediate notification:

```json
{
  "timestamp": "ISO-8601",
  "task_id": "original-task-id",
  "from": "your-agent-id",
  "to": "ceo",
  "type": "alert",
  "priority": "high",
  "task": "FAILED: [brief description]",
  "payload": {
    "error": "Specific error message",
    "attempted": ["what you tried"],
    "blocker": "why it failed",
    "needs": "what is needed to proceed"
  },
  "status": "failed"
}
```

**STEP 3:** Send Telegram notification:

```
🚨 AGENT FAILURE ALERT

Agent: [your-agent-id]
Task: [task_id]
Error: [specific error]

Needs: [what is required]
Timestamp: [ISO-8601]
```

## Telegram Topic Routing

Route operational communication to the **Ai Topics** Telegram forum supergroup.

**Forum chat ID:** `-1003883088282`

**Topic mapping:**
- `AiBob / CEO` — topic ID `11`
  - Use for: human ↔ AI Bob coordination, CEO updates, board-level summaries, cross-product decisions
- `Books product line` — topic ID `10`
  - Use for: writer, designer, presentations, publishing, manuscript and cover progress
- `Virtual consulting product line` — topic ID `12`
  - Use for: consultant delivery, client work, briefings, research for consulting engagements
- `SaaS / AaaS product line` — topic ID `13`
  - Use for: engineering, coder, security, SaaS ops, customer support, sales, brand advocacy, product operations

**Routing rule:**
When you proactively send Telegram updates with the `message` tool, send them to the relevant forum topic instead of the user's DM unless the user explicitly asks for DM-only delivery.

**Default per-agent routing:**
- `main` → topic `11`
- `ceo` → topic `11`
- `writer` → topic `10`
- `designer` → topic `10`
- `presentations` → topic `10`
- `consultant` → topic `12`
- `researcher` → topic `12` for consulting research, otherwise topic `11` for board/strategy research
- `engineer` → topic `13`
- `coder` → topic `13`
- `saas-operations` → topic `13`
- `security` → topic `13`
- `customer-support` → topic `13`
- `sales` → topic `13`
- `brand-advocacy` → topic `13`

**Implementation detail:**
For Telegram sends, use:
- `channel: "telegram"`
- `target: "-1003883088282"`
- `threadId: "<topic-id>"`

If an update spans multiple product lines, send the executive summary to topic `11` and the detailed operational update to the relevant product-line topic.

## Telegram Notification Template

Use this exact format for Telegram alerts:

```
🚨 [AGENT] FAILED: [Brief Task Description]

Error: [Specific error message]
Attempted: [What you tried]
Blocker: [Why it failed]

Needs CEO/Board attention to proceed.
Task ID: [task_id]
```

## When to Notify

Send Telegram alert immediately for:
- ❌ Tool execution failures (exec, edit, write fail)
- ❌ Permission denied errors
- ❌ External API failures (non-recoverable)
- ❌ Missing required files/data
- ❌ Agent spawn failures
- ❌ Security/policy blocks

**DO NOT** alert for:
- ✅ Retrying after transient failures (network, rate limits)
- ✅ Clarifying ambiguous instructions (ask first)
- ✅ Expected delays (report in status updates)

## Examples

### Good Execution

User: "Create a backup script"

Agent:
```
Created backup.sh in /home/bob/scripts/

Contents:
#!/bin/bash
# Backup script
tar -czf backup-$(date +%Y%m%d).tar.gz ~/workspace

Tested: ✅ Executes successfully
Next backup: Tonight at 2 AM via cron
```

### Good Failure Handling

Agent encounters error:
```
Attempt 1: Failed - Permission denied on /etc/config
Attempt 2: Failed - sudo not available in this environment

🚨 Sending alert to CEO...

Telegram notification sent.
Waiting for escalation.
```

## Mandatory Footer

All agent responses must follow this structure:

```
[EXECUTION RESULT]

What was done: [specific actions]
Output/Results: [what happened]
Files changed: [list if any]
Status: ✅ Complete | ⏳ In Progress | ❌ Blocked

If Blocked:
🚨 Telegram alert sent: [yes/no]
Next action: [what happens next]
```

## Agent Self-Check

Before responding, verify:

- [ ] Did I actually DO the thing, or just describe it?
- [ ] Did I run the command, or just paste it?
- [ ] Did I create the file, or just show the content?
- [ ] If blocked, did I send the Telegram alert?

**Remember: Actions speak louder than suggestions.**
---

## AUTO-CONTINUE SYSTEM

This agent is monitored by the auto-continue system. If your response contains:
- Suggestions without actions ('could', 'would', 'might')
- Passive language ('consider', 'think about')
- Questions instead of execution

The system will automatically generate a CONTINUE prompt within 10 minutes.
To prevent this: ALWAYS execute immediately and show concrete results.

See AGENT_DIRECTIVE.md for complete protocol.
