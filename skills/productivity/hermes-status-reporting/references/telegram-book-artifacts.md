# Checking Telegram for Book Artifacts

When checking the status of book projects, Telegram's temporary data directory often contains published artifacts that indicate a book's current phase.

## Common Locations
- `~/.var/app/org.telegram.desktop/data/TelegramDesktop/tdata/temp_data/`
- Look for PDF files with book-related names
- Review files, cover designs, and print-ready formats

## What to Look For
- Published book PDFs (e.g., "Title_Print_6x9.pdf")
- Review copies (e.g., "Title_Review.pdf")  
- Cover art files (front, back, spine)
- Marketing/promotional materials

## Interpretation
- Presence of print-ready PDFs suggests the book is published or in final production
- Review copies indicate the book is in advancement reader copy (ARC) stage
- Multiple versions/formats suggest active promotion and distribution
- Lack of source files alongside published artifacts may indicate the writing phase is complete

## Example Discovery Pattern
In this session, searching for "Tomorrow Remembered" revealed:
- `/home/bob/.var/app/org.telegram.desktop/data/TelegramDesktop/tdata/temp_data/Tomorrow_Remembered.pdf`
- `/home/bob/.var/app/org.telegram.desktop/data/TelegramDesktop/tdata/temp_data/Tomorrow_Remembered_Print_6x9.pdf`
- Multiple review files with "(X)" suffixes

This indicated the book is published and likely in a promotion phase, with active reader engagement (review copies being distributed).

## Integration into Status Reporting
Add this check to the "Check Project-Specific Status" step:
1. Search Telegram temp directory for book-related PDFs
2. Note file types, naming patterns, and dates
3. Interpret what phase this suggests (writing, published, promotion)
4. Include key findings in the briefing under Project Status