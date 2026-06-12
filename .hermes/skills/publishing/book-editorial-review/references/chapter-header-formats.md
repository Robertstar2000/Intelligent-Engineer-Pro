# Chapter Header Formats on this USB Drive

Every book on `/mnt/usb_4tb/books/` uses a slightly different chapter header format. Tools that expect a single pattern (image generators, compilers, editorial reviewers) will silently fail on books with non-standard formats. This reference documents what each book actually uses.

## Age of Lightships (4 books)

| Book | MANUSCRIPT file | Header format | Regex pattern |
|------|----------------|---------------|---------------|
| Bk 1 Sunward Exodus | MANUSCRIPT.md | `# Chapter N — Title` | `r"^# Chapter \d+[\.\d]* — "` |
| Bk 2 Mercury Accord | MANUSCRIPT.md | `# Chapter N: Title` | `r"^# Chapter \d+[\.\d]*[: ]"` |
| Bk 3 Ghosts Beyond Neptune | MANUSCRIPT.md | `# Chapter N: Title` | Same as Bk 2 |
| Bk 4 Last Photon Fleet | MANUSCRIPT.md | `# Chapter N: Title` | Same as Bk 2 |

## Lunar Foundation (4 books)

| Book | MANUSCRIPT file | Header format | Notes |
|------|----------------|---------------|-------|
| Bk 1 Moon Rock | MANUSCRIPT.md | `# Chapter N — Title` | Standard H1 |
| Bk 2 Mooncoming | MANUSCRIPT.md | `# Chapter N — Title` | 39 chapters, sequential |
| Bk 3 Waters End | MANUSCRIPT.md | `# Chapter N — Title` | Standard |
| Bk 4 Waters Horizon | MANUSCRIPT.md | `# Chapter N — Title` | Standard |

## No Blue Sky (5 books)

| Book | MANUSCRIPT file | Header format | Notes |
|------|----------------|---------------|-------|
| Bk I Built from Dust | MANUSCRIPT.md | `# Chapter N: Title` | Standard H1, 8 chapters |
| Bk II Oxygen Gamble | MANUSCRIPT.md | `# Chapter N: Title` | 41 chapters |
| Bk III Rivers Under Mars | MANUSCRIPT.md | `# Chapter N: Title` | 70 chapters |
| Bk IV Red Charter | MANUSCRIPT.md | `# Chapter N: Title` | 12 chapters |
| Bk V First Martian Nation | MANUSCRIPT.md | `# Chapter N: Title` | 25 chapters |

## Cindy Lou Legal Capers (3 books) ⚠️ NON-STANDARD

| Book | MANUSCRIPT file | Header format | Notes |
|------|----------------|---------------|-------|
| Bk 1 Retainer to Trouble | **Retainer_to_Trouble_MANUSCRIPT.md** | `## Chapter N: Title` | **Double hash!** Chapters are **non-sequential** (1,2,3,4,5,7,10,11,12,13,16,18,21,25,26,27,28,29). The `MANUSCRIPT.md` file is a ~8K stub — the real book is in `Retainer_to_Trouble_MANUSCRIPT.md` at 88K. |
| Bk 2 Clause for Alarm | MANUSCRIPT.md | `-- Chapter N -- Title` | Has inline style. 28 chapters. |
| Bk 3 Affidavits and Alibis | **affidavits-and-alibis_MANUSCRIPT.md** | `## Chapter N: Title` | **Double hash!** 29 chapters. The `MANUSCRIPT.md` file is a stub. |

## Business Series (3 books)

| Book | MANUSCRIPT file | Header format | Notes |
|------|----------------|---------------|-------|
| Crisis Ready Company | MANUSCRIPT.md | `# Chapter N: Title` | 15 chapters + 4 Part dividers |
| AI That Works | MANUSCRIPT.md | `# Chapter N: Title` | 12 chapters |
| Owner's Manual for AI Agents | MANUSCRIPT.md | `# Chapter N: Title` | 40 chapters |

## Tomorrow Remembered (memoir) ⚠️ NON-STANDARD

| File | Header format | Notes |
|------|---------------|-------|
| MANUSCRIPT.md | `## Chapter (worded_number): Title` | **Worded numbers** (One through Sixteen). **Inline headers** — many chapter headers are merged into the previous paragraph without a newline (e.g., `...could only imagine.## Chapter Two: The Echoes`). Only 3 of 16 headers start at the beginning of a line. |

## Critical: The `MANUSCRIPT.md` vs `*_MANUSCRIPT.md` Trap

Several books have a **stub** `MANUSCRIPT.md` and the **real** manuscript in a book-specific file:

| Book | Real file | Stub file size |
|------|-----------|---------------|
| CLLC Bk 1 Retainer to Trouble | `Retainer_to_Trouble_MANUSCRIPT.md` (88K) | `MANUSCRIPT.md` (~8K) |
| CLLC Bk 3 Affidavits and Alibis | `affidavits-and-alibis_MANUSCRIPT.md` (50K+) | `MANUSCRIPT.md` (few lines) |

Automated tools that hardcode `MANUSCRIPT.md` will silently fail on these books — they'll find 0 chapters, 0 images, and report success with 0 work done. Always check:
```bash
ls -la /path/to/book/*MANUSCRIPT*.md | grep -v backup
# The largest file is the real manuscript
```