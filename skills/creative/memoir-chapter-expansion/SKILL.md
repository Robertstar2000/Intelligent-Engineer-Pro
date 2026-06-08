---
name: memoir-chapter-expansion
displayName: Memoir Chapter Expansion
description: Expand an underdeveloped memoir chapter from skeletal summary prose into a fully-realized scene with sensory detail, emotional depth, and first-person voice — while preserving the true story and hitting a target word count.
---

## 🔍 MemPalace Query (MANDATORY FIRST STEP)
Before proceeding, query MemPalace for existing context:
```python
import sys, os; sys.path.insert(0, os.path.expanduser('~/.hermes/mempalace'))
import embed; embed.init_embedding(os.path.expanduser('~/.hermes/mempalace'))
results = embed.search_embeddings("memoir chapter expansion first-person voice sensory detail scene work", k=5)
```
This retrieves previous decisions, domain-specific context, and lessons learned from the vector memory store.

# Memoir Chapter Expansion

## When to Use This Skill

Use this skill when:

- A chapter in a memoir manuscript is **too short and reads like a summary** (100-300 words) and needs expanding to a fuller length (500-1000+ words)
- The existing text is **skeletal**: tells what happened but doesn't show it — no scenes, no sensory detail, no emotional presence
- The chapter is currently in **third-person summary** ("Bob did X, Bob felt Y") and needs converting to **first-person memoir voice** ("I did X, I felt Y")
- The true story must be preserved — all facts, sequence of events, and key characters stay intact
- You need to add **scene work**: specific moments with setting, sensory details, dialogue/touch, and an emotional arc
- The user provides a **target word count range**

**Do NOT use for:**
- Fiction novels (significant plot changes may be needed — use `manuscript-rewrite-for-excitement`)
- Compressing bloated chapters (use the compression subsection in `manuscript-restructuring`)
- Structural reorganization or bulk text transforms (use `manuscript-restructuring`)
- Assembling fragments with transitional content (use `memoir-assembly-with-transitions`)

## Core Technique: Summary → Scene Conversion

The fundamental operation is converting *telling* into *showing*. Every sentence of summary prose should be unpacked into one or more of these elements:

| Summary (tell) | Scene (show) |
|---------------|--------------|
| "They got a dog" | The screen door slaps shut. Nails click on linoleum. A whimper. First touch. The weight of a dog's head on a child's knee. |
| "They played together for four years" | A specific memory: throwing sticks in the woods, the dog crashing through ferns, mud-caked paws, morning rituals, the warm lump at the foot of the bed. |
| "The dog died" | The search through the woods. Voices going hoarse calling a name. The discovery on the roadside. The stillness. The cold. The wind moving fur. Sitting there alone. |
| "He was sad" | The space at the foot of the bed left open. The dog's spot kept waiting. The car that passes without stopping. |

## Workflow Steps

### 1. Locate and Read the Chapter

- Search for the manuscript file using `search_files` by title or chapter name
- Read the chapter in full using `read_file` with offset/limit
- Note: The chapter may be numbered differently across manuscript versions — check all recent versions

### 2. Baseline Assessment

Assess what you're working with:

- **Current word count** — run `wc -w` on just the chapter (not the whole file)
- **Target word count** — the user may specify a range; if not, infer from surrounding chapters or default to 500-800
- **Compression/expansion ratio** — how many times larger the final version needs to be
- **Existing elements** — what's already there (facts, names, sequence) that must be preserved
- **Problems to fix** — typos, third-person voice, name inconsistencies (e.g., "Max" used once but the dog's real name is "Chips"), AI lecture-voice, missing emotion

### 3. Identify the Story Beats

Extract the essential true-story sequence from the summary. For example:

1. **Arrival** — how the person/animal came into the story (shelter, purchase, first encounter)
2. **Bonding** — the daily life of the relationship, a specific shared activity
3. **Daily rituals** — sleeping, waking, playing, habits
4. **The loss** — the event (ran away, accident, illness), the search/waiting
5. **Discovery** — finding them, the moment of knowing
6. **Grief** — the immediate response, the aftermath
7. **Reflection** — what this meant then, what it means now, foreshadowing of future losses

**These beats must all be present in the expansion. Do not drop any.**

### 4. Add Scene Work for Each Beat

For each beat, build a scene with these layers:

**Setting:** Where does this moment happen? (kitchen floor, woods, bedroom, side of a road, gravel)
**Sensory detail:** What does it sound like? (screen door, clicking nails, bark, silence between calls, wind in fur) — what does it look like? (midnight-black coat, white-tipped tail, dust on fur, shadows shifting) — what does it feel like? (cold nose on knuckles, warm skull through jeans, cold body, scratched legs from branches) — what does it smell like? (dust, pine, linoleum, something warm and animal)
**Emotional anchor:** What is the character feeling in this exact moment? (uncertainty, joy, security, dread, stillness, numbness)
**Movement:** What are the characters physically doing? (kneeling, sitting, calling, walking, lying still, branches scratching)

### 5. Convert to First-Person Memoir Voice

- Bob/he/him → I/me/my
- Bob's → my
- "Bob felt" → "I felt" or remove the frame and just show the feeling
- Replace clinical/analytical framing with raw sensory experience
- Replace "This is how X works" lecture-voice with "That is how X shaped me" reflection

**Before:** "Bob's grief was palpable and he took a long time to heal."
**After:** "I didn't cry right away. I just sat there on that gravel shoulder, my hand on his fur, staring at the trees across the road."

### 6. Fix All Typos and Inconsistencies

Common issues in summary prose:
- Wrong verb: "laying" → "lying"
- Missing possessive apostrophe: "Bobs" → "Bob's" (or convert to first-person "my")
- Inconsistent names: "Max" used once but dog is "Chips" — pick the correct name and use it throughout
- Run-on sentences: break into shorter, punchier lines for memoir rhythm
- Missing punctuation: fix commas, em-dashes, capitalization after em-dashes
- "every where" → "everywhere", "Mongrel" → "mongrel"

### 7. Write the Expansion

Write in this style:
- **Short paragraphs** — 1-3 sentences each for emotional impact
- **Punchy, varied sentences** — mix short, medium, and long sentences. Fragment sentences for emphasis: "Two days. I barely slept."
- **Restraint in grief** — the most emotional moments should be understated, not overwrought. "He was cold." carries more weight than "He was ice cold and I felt a wave of overwhelming sadness."
- **Specificity over generalization** — not "they were best friends" but "he slept at the foot of my bed every night, a warm, breathing lump that rose and fell in the dark"
- **End with reflection** — tie the chapter's emotional arc to the broader theme of the memoir. Foreshadow future losses without over-explaining.

### 8. Verify Word Count

Check with:
```bash
wc -w <file>
```

If over target: trim redundant adjectives, remove secondary details that don't serve the emotional arc.
If under target: add more sensory detail to thin beats, or expand a scene with more specific memory.

Target within ±50 words of the requested range.

### 9. Update the Manuscript File

Use `patch` to replace the old chapter text with the new version in the manuscript file. The old_string must be unique — include the chapter heading in the match.

## Quality Standards

- [ ] **Reader engagement mandate**: All expanded/added material MUST be interesting, exciting, and engaging to readers. Every added sentence must draw the reader deeper into the story.
- [ ] **All true story beats preserved** — no facts added or removed from the original sequence
- [ ] **First-person voice throughout** — no third-person drift
- [ ] **Sensory detail present** — at least one specific sensory anchor per beat (sound, smell, touch, sight)
- [ ] **Scene work present** — at least 3 distinct scenes (arrival, bonding, loss) with setting and physical action
- [ ] **Emotional restraint** — the biggest moments use the smallest words; no melodrama
- [ ] **Typos all fixed** — no "laying" for "lying", no missing apostrophes
- [ ] **Word count in target range**
- [ ] **Bestseller memoir style** — short paragraphs, varied sentences, specific details, reflective ending
- [ ] **Tone consistent with surrounding chapters** — match the tense, voice, and intimacy level

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Overwriting the emotional climax with too many words | Use short, plain sentences. "He was cold." Let the reader sit in the stillness. |
| Dropping a story beat during expansion | Before writing, checklist every beat from the original. After writing, cross-check. |
| Third-person voice creeping back mid-chapter | Do a final grep for "Bob" or "his" (when referring to the narrator) |
| Chapter heading inconsistency | The chapter may be numbered differently (Chapter 3 vs Chapter 14) across different manuscript versions. Check which version the user is actively working on. |
| Making the grief too analytical | Cut psychological framing. The moment itself carries the weight — you don't need to name the emotion. |
| Using the wrong file | Multiple manuscript versions may exist. Check timestamps and use the latest working version, not archives. |

## Example Output

**Before (196 words, summary):**
*The summer Bob turned seven, the family got a dog. His name was Mr. Chips... On the third day Bob found him laying on the side of a road...*

**After (748 words, scene):**
*The summer I turned seven, my father came home with a dog. I remember the screen door slapping shut, that loose spring never quite catching. And then a sound I'd never heard in our house before. Clicking. Nails on linoleum...*
