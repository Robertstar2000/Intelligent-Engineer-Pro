# MIFECO Book Publishing - Process Quick Reference

## Complete Book Lifecycle
1. **Concept** → Phase 0 research (8-12 bestsellers, extract patterns)
2. **Outline** → 40 chapters × 3-5 beats each
3. **Write** → Parallel batches (4 batches × 10 chapters via delegate_task)
4. **Edit** → Flow edit → Humanizer → Grammar → Consistency → Fabricated-claim integrity
5. **Compile** → Single .md manuscript
6. **Cover** → AI image gen (Gemini/Flux) + typography overlay (PIL)
7. **Build** → PDF (WeasyPrint) + EPUB3 (pure Python)
8. **Package** → KDP zip (EPUB + PDF + cover + metadata)
9. **Publish** → Upload to KDP
10. **Deploy** → Books website (mifeco.com/books/)

## Key Paths
| Purpose | Path |
|---------|------|
| Main books dir | `/mnt/usb_4tb/books/` |
| Book series | `/home/bob/books/{Series_Name}/` |
| Pipeline runner | `/mnt/usb_4tb/books/hermes_publish.py` |
| Books website (local) | `/mnt/usb_4tb/books/books-section/` |
| Books website (live) | `/home/dh_mwpxuu/mifeco.com/books/` |
| Subscriber DB (live) | `/home/dh_mwpxuu/mifeco.com/books/api/subscribers.json` |
| Subscriber DB (backup) | `/mnt/usb_4tb/books/books-section/api/subscribers.json` |
| Author photo source | `/home/bob/books/Business_Series/AI_That_Works/Author_Photo.jpg` |
| Reports dir | `~/.hermes/consulting-reports/` |

## Published Books (ASINs)
| Book | ASIN | Price |
|------|------|-------|
| Tomorrow Remembered | B0GX2XC5YF | $3.99 |
| AI That Works for Small Business | B0H15NLBW8 | $2.99 |
| Built from Dust (NBS 1) | B0GX2YJ92K | $2.99 |
| Owner's Manual for AI Agents | B0H1KSCRYC | $3.99 |

## Key Rules
- **Humanizer mandate**: ALL book prose must pass humanizer check (29 patterns, 7 categories)
- **Image gen LLM only**: Covers MUST use AI image generation — NEVER Python/matplotlib
- **Reader engagement**: Every paragraph must earn its place
- **RGBA→RGB**: Convert all images before EPUB build
- **TOC mandatory**: Every book must have TOC with synchronized page numbers (2-pass rendering)
- **Author photo**: Must exist in every book directory
- **No <a> tags in print PDF TOC**: Causes WeasyPrint text corruption

## Deployment Credentials
| System | Host | User | Password |
|--------|------|------|----------|
| DreamHost SSH/SFTP | ssh.mifeco.com | dh_mwpxuu | Rm2214ri#### |
| MySQL | mysql.mifeco.com | ak48bme | 7jpetxEL |
| Stripe (placeholder) | — | — | pk_live_CHANGEME |

## Common Pitfalls
1. **Subagent word count lies**: Always verify actual word count after subagent writes chapters
2. **TOC duplicate injection**: Verify `grep -c 'class="toc"' manuscript.html` = 1 after injection
3. **EPUB RGBA failure**: Convert images to RGB BEFORE building EPUB
4. **Cover style mismatch**: Business = dark navy + white title; Sci-fi = space imagery + amber accents
5. **Published book immutability**: Never rebuild/regenerate for books with existing ASINs
