# Cover Generation Session Examples

## Waters Horizon (The Lunar Foundation, Book 4)

**Scenario:** Book 4 of a 4-book series had no cover image and no publishing package zip. Covers existed for books 1-3 (Moon Rock, Mooncoming, Waters End).

### Step 1: Study Existing Series Covers

Existing covers (from `publishing_output/covers/`):
- `LF_1_Moon_Rock_Cover.png` — 1.7M, 1024×1536
- `LF_2_Mooncoming_Cover.png` — 1.8M, 1024×1536
- `LF_3_Waters_End_Cover.png` — 2.2M, 1024×1536

Used the cover generation scripts in `/home/bob/books/generate_trilogy_covers.py` and `/home/bob/books/redo_trilogy_covers.py` to identify the design parameters:
- Full-bleed crop from Gemini's square (1024×1024) to portrait (1024×1536) — scale height to 1536, center-crop width to 1024
- Gradient overlay: 28% top gradient (max alpha 70), 10% bottom gradient (max alpha 60)
- Typography: DejaVuSans-Bold or LiberationSans-Bold, thick shadow (3-2-1 layer)
- Title stacked: 58pt, centered, with line spacing at 1.4× font size
- Series line: "The Lunar Foundation  •  Book N" at y=8, 16pt, with shadow
- Author: "Bob J Mills" at y=H-120, 26pt, with shadow
- Art brightened +15% / contrast +10% via PIL

### Step 2: Read the Manuscript

Extracted from the epub contents:
- 10 chapters (numbered 31-40, continuing from Book 3)
- Key themes: audit, recovery, proposal for the future, legacy, memorial, base upgrade, expansion, looking toward the horizon
- "Six months later, the base was transformed" — from survival to growth
- New elements: expanded hydroponic garden, second borehole, lava tube extraction system, 60 inhabitants
- Emotional tone: hopeful, forward-looking, closure

### Step 3: Design the Prompt

```python
prompt = """Create a cinematic book cover image for a sci-fi novel called 'Waters Horizon'.
The scene: An expanded, thriving lunar base on the Moon — six months after a water crisis, now transformed. The image shows:
- A panoramic view of a lunar base at the horizon with multiple interconnected habitat modules, glowing with warm amber light
- A large hydroponic dome with a visible green glow (the expanded garden producing strawberries and crops)
- A water extraction plant in the foreground with pipes and storage tanks (12 liters per minute flowing)
- A drilling rig for a second borehole on the right side
- The lunar surface in the foreground with rover tracks leading between structures
- Earth hanging in the dark sky above the horizon — about 25-30% above the horizon line
- Distant mountains/craters on the lunar horizon under the black sky
- Stars visible in the upper sky
Style requirements:
- Leave generous negative space at the top (upper 40%) for stacked book title text
- Leave clean negative space at the bottom (lower 15%) for the author name
- No text, logos, symbols, or watermarks anywhere
- Minimal visual clutter in the title zone
- Cinematic, photorealistic quality
- Aspect ratio: 2:3 portrait (approximately 1024x1536 pixels)
- Color palette: warm amber/gold, green hydroponics, dark grey lunar, deep black space sky with Earth's blue-white glow
- Sense of hope, growth, transformation, and looking toward the future
- This must be completely original — do not reference or copy elements from any existing book covers"""
```

### Step 4: Generate and Process

1. Called Google Gemini Flash Image via OpenRouter — got 1024×1024 square (typical)
2. Full-bleed crop: scale height to 1536 → 1536×1536 → center-crop width to 1024 → 1024×1536
3. Brightened +15%, contrast +10%
4. Applied gradient overlays matching series (28% top, 10% bottom)
5. Added series label, stacked title "WATERS / HORIZON", author
6. QA via GPT-4o-mini vision confirmed: clear title area, no baked-in text, appropriate scene with biodomes and Earth

### Step 5: Deliver

- Saved to `publishing_output/covers/LF_4_Waters_Horizon_Cover.png` (2.0M)
- Copied to `The_Lunar_Foundation/Book_4_Waters_Horizon/LF_4_Waters_Horizon_Cover.png`
- Cover file size (2.0M) consistent with LF 1-3 covers (1.7M-2.2M)

### Key Lessons

- Gemini Flash Image always returns square (1024×1024). Always plan for full-bleed crop to 1024×1536.
- The series' own generation scripts are the best source of truth for typography parameters — read them before guessing.
- For a missing series cover, the most time-efficient approach is: find existing generation script → extract parameters → read manuscript for story → write prompt → generate → apply same typography → deliver.
- QA with a vision model catches baked-in text, wrong author name, or AI artifacts before showing the user.
