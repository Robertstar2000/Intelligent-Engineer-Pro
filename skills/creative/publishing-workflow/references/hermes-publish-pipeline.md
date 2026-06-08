# hermes-publish: Unified Pipeline Runner

**Created**: 2026-06-02
**Location**: `/mnt/usb_4tb/books/hermes_publish.py`
**Package**: `/mnt/usb_4tb/books/hermes_publish/`

## What It Is

Single entry point for the entire book product line (20 books, 6 series). Replaces all ad-hoc per-series pipeline scripts.

## CLI Usage

```bash
python3 hermes_publish.py --list                        # list all books
python3 hermes_publish.py --book moon-rock               # build one book
python3 hermes_publish.py --series "No Blue Sky" --steps compile epub
python3 hermes_publish.py --all                          # build everything
python3 hermes_publish.py --status                       # show build state
python3 hermes_publish.py --watch                        # file-watcher CI/CD
```

## Steps

| Step | Module | What It Does |
|------|--------|-------------|
| `compile` | `step_compile.py` | Collects chapters, adds front/back matter |
| `cover` | `step_cover.py` | PIL-based cover + text overlay |
| `cover-ai` | `step_images.py` | AI cover via Gemini + Codex OAuth |
| `pdf` | `step_pdf.py` | WeasyPrint PDF |
| `epub` | `step_epub.py` | Unified ZIP-based EPUB 3 (no external deps) |
| `kdp` | `step_kdp.py` | KDP submission package ZIP |
| `marketing` | `step_marketing.py` | Marketing text files |
| `infographic` | `step_images.py` | Multi-format infographics with QR codes |

## Incremental Builds

File-hash change detection via `.pipeline_state.json`. Use `--force` to override.

## MemPalace Auto-Offload

Checks MEMORY.md size at each run. Offloads to FAISS vector store if > 1800 chars. Graceful degradation if numpy/faiss missing.
