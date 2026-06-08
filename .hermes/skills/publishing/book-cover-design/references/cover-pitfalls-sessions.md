# Cover Pitfalls — Session Learnings

Granular learnings from real cover corrections, too specific for the main SKILL.md but invaluable for reproducing the same class of work without repeating mistakes.

## "Inspired by" Trap (May 2026 — Waters End)

**Context:** User asked for a Waters End cover "inspired by a best-selling book." The generated cover accidentally had the other book's author name ("Aurora Novak") and subtitle ("Celestial Tears") on it instead of the correct ones. The artwork itself was also too dark and contained recognizable elements from the inspiration book.

**Fix — Two distinct problems:**
1. **Visual elements** — The art contained recognizable composition/scene elements from the reference book. Fix: ground the prompt in actual story elements from the user's book.
2. **Text elements** — The typography picked up the wrong author name AND an extra subtitle from the reference book. Fix: hardcode `author_text = "Bob J Mills"` and NEVER add subtitles or extra text without explicit user request.

**Action when user says "inspired by [Book X]":**
1. Extract the **genre/style cues** only: lighting approach, composition philosophy, color temperature direction
2. NEVER copy: named objects, specific color palettes, recognizable compositions, character poses, setting elements
3. Ground the prompt in actual story elements from the user's book instead
4. If uncertain, generate art based purely on the user's book content and apply the *lighting/style* approach from the reference

**Example bad vs good:**
- ❌ "Inspired by The Martian — orange desert landscape, lone figure in spacesuit, minimal composition"
- ✅ "Inspired by The Martian — high contrast, photorealistic, solitary scale against vast environment. Content: moon base water facility, bright luminous droplet, silver structures"

## Single-Line vs Stacked Title Correction (May 2026 — All Covers)

**Context:** User requested "80% width" for title text on short titles. The script was stacking "WATERS END" vertically instead of putting it on one line at large size.

**Lesson:** For 2-3 word titles where each word is under ~10 characters, ALWAYS test single-line fit first. A single-line title at 145pt scales to 80% width naturally. Stacking short words creates:
- Excessively tall letterforms (looks amateurish)
- Wasted vertical space
- Overcrowded cover composition

**Decision rule:** If the single-line version of the title fits at 58pt on the test canvas, use single line. Simple heuristic: `len(" ".join(words)) < 25` characters → single line.

## Author Name Must Default Correctly (May 2026 — Waters End)

**Context:** Cover showed wrong author name. Root cause was either a stale script variable or an AI-generated image with baked-in text.

**Hard rule:** The typography template must hardcode `author_text = "Bob J Mills"` and never derive, prompt-infer, or parameterize it. This is the ONLY author name used across all books in any series.

## Baked-In AI Text in Cover Art

**Context:** AI models (especially Gemini) sometimes generate text in images — book titles, author names, or random letters. This text is garbled/nonsensical (e.g., different word under the correct title).

**Verification step:** After generating the raw image, overlay the correct typography. If the user reports "wrong text," it could be:
1. Baked-in AI text in the raw image (ignore it — user sees your clean overlay)
2. Mistake in your typography script (check the variable)
3. Both (fix the script and verify the raw image doesn't distract)

**Fix:** Always overlay clean, correct typography via PIL. The overlay text takes visual priority over any baked-in AI muddle.
