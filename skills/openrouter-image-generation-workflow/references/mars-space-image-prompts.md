# Mars & Space Colonization Image Prompt Guide

## When to Use

Use these prompt additions when generating chapter images for hard science fiction series involving Mars colonization, space exploration, or astronaut narratives (e.g., No Blue Sky series by Bob J Mills).

## Specificity Requirements

### Mars Landscape
- Real Mars appearance: reddish-brown iron oxide regolith, NOT grey moonscape
- Impact craters visible where appropriate
- Thin pale pink/orange sky — NOT blue Earth sky, NOT black space void
- Rust-colored horizon, basaltic rock features
- Fine iron oxide dust texture on all surfaces

### Astronauts — Modern SpaceX-Style ONLY
- Sleek, form-fitting suit profile
- Angular 3D-printed helmet design with wide panoramic visors
- Minimal visible bulk — no puffy Apollo-era suits
- Integrated life support (no boxy PLSS backpacks)
- Modern commercial spaceflight aesthetic

### Equipment — Modern/Near-Future
- Clean, efficient solar panel arrays (not chunky 1970s designs)
- Contemporary habitat modules with clean architectural lines
- Modern rovers with advanced wheel/suspension design
- Current-era ISRU (In-Situ Resource Utilization) equipment
- Avoid: retro-futuristic, steampunk, mid-century aesthetics

## Prompt Template

```
Black and white pencil sketch illustration for a science fiction novel. [Scene description]. Mars must look like the real planet Mars: reddish-brown dusty regolith, impact craters, thin pale pink sky, distant rust-colored horizon, fine iron oxide dust. Any astronauts must wear modern SpaceX-style suits: sleek form-fitting design, angular 3D-printed helmets with wide visors, minimal bulk, modern commercial spaceflight aesthetic. Any equipment must be modern/near-future: sleek solar arrays, contemporary habitat modules, advanced rovers with clean lines. Style: detailed pencil sketch, cross-hatching, no color, book illustration, dramatic lighting, cinematic composition. This must be completely original.
```

## Folder Structure (No Blue Sky Series)

Images go into a flat `images/` folder per book. The `output/` and `images_bw/` folders contain duplicates for different output formats:
- `Book_N_Title/images/chXX.png` — **source of truth** (replace these)
- `Book_N_Title/images_bw/chXX.png` — greyscale variant (copy from images/)
- `Book_N_Title/output/chXX.png` — used by HTML output

## Known Chapter Header Formats

| Series | Header Format | Regex for Parsing |
|--------|---------------|-------------------|
| No Blue Sky Books 1-2 | `## Chapter N — Title` (double hash) | `^## Chapter \d+ — (.+)$` |
| No Blue Sky Books 3-5 | `# Chapter N — Title` (single hash) | `^# Chapter \d[\.\d]* — (.+)$` |

## Script Guidelines

Save batch scripts to the books root directory (not the script directory) so relative paths work. The script should:
1. Always **remove existing images before regenerating** (force regeneration, no skip logic)
2. Generate to `images/` folder
3. Copy to `images_bw/` and `output/` folders after generation
4. Maintain 6-second delay between API calls
5. Log all failed generations for retry
