# Gemini Image Generator Argument Reference

Script: `~/.hermes/pipeline-engine/scripts/generate-blog-image.py`
Model: `gemini-2.5-flash-image` (via Google AI Studio `GOOGLE_AI_STUDIO_KEY`)

## Required Arguments

| Arg | Required | Notes |
|-----|----------|-------|
| `--mode` | **Always** | `cover-inspired` or `infographic`. Even with `--prompt`, this is mandatory. |
| `--output` | **Always** | Output PNG path |

## Mode-Specific Structured Args

### cover-inspired mode
| Arg | Purpose |
|-----|---------|
| `--book-title` | Book title (used in prompt template) |
| `--series` | Series name (used in prompt template) |
| `--genre` | Genre (defaults to "Science Fiction") |
| `--description` | Book theme description |

### infographic mode
| Arg | Purpose |
|-----|---------|
| `--post-title` | Blog post title |
| `--content-summary` | What the blog is about |
| `--category` | Post category |

## Custom Prompt Override

Providing `--prompt` overrides the auto-generated prompt entirely. This is **preferred for comparative/fusion images** where two works are being blended, since the structured args generate text like "the book 'X' from series 'Y'" which doesn't suit a two-book comparison.

## Return Format

Prints JSON to stdout:
- Success: `{"success": true, "output_path": "...", "size_bytes": N, "text_response": "..."}`
- Failure: `{"error": "..."}`

## Pitfalls

- `--mode` is required even with `--prompt` — argparse enforces this at the parser level
- API key from `GOOGLE_AI_STUDIO_KEY` env var, with fallback to `~/.hermes/.env`
- 120-second timeout recommended (image generation can be slow)
- Output is always PNG; no format option available