# Last Page Back Matter — Full Specification
# Reference for publishing-workflow skill section 2C

## Overview
The last page of EVERY manuscript MUST include these four elements, in order:

## A. Thank You Blurb (Expanded)
A warm, genuine, expanded thank-you paragraph (4-6 sentences) thanking the reader for reading the book. Write in Bob J Mills' voice — direct, no-nonsense, sincere. Acknowledge the reader's time and trust. Mention that every hour spent reading is an hour you don't get back, and the fact that they spent it on this book means something. End with a forward-looking line about hoping the story stayed with them after the last page.

**Tone:** Sincere, grounded, slightly personal. NOT flowery or over-the-top. Bob speaks like a real person, not a marketing brochure.

**Per-book customization:** The thank-you should reference the specific journey the reader just completed in THIS book. For a Lightship book, reference the fleet and the voyage. For a Lunar Foundation book, reference the Moon and survival. For a business book, reference the practical tools they now have.

## B. More From Bob Statement (Expanded)
A 2-3 sentence expanded statement about the breadth of Bob J Mills' writing career. Mention that he writes across genres — hard science fiction about humanity's future in space, practical business books about AI and crisis management, and personal memoir. Reference that this single book is part of a larger body of work spanning space colonization, lunar settlements, Martian independence, AI for small businesses, and one man's journey from the first computers to the first AI agents.

**Tone:** Brief but substantive. Not a sales pitch — more like a fellow traveler saying "if you liked this, there's a lot more where it came from."

## C. QR Codes — Two Required
Two QR codes displayed side-by-side:

1. **MIFECO QR Code** — Links to `https://www.mifeco.com`
   - Label: "Scan for more from Bob J Mills — books, updates, and more"
2. **Amazon QR Code** — Links to Bob's Amazon author page
   - Label: "Scan to find all Bob J Mills books on Amazon"

### QR Code Generation
```python
import qrcode
from PIL import Image

def save_qr(url, output_path, size_px=300):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=2
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
    img = img.resize((size_px, size_px), Image.NEAREST)
    img.save(output_path)
    return output_path

save_qr("https://www.mifeco.com", "qr_mifeco.png", 300)
save_qr("https://www.amazon.com/stores/Bob-J-Mills/author/", "qr_amazon.png", 300)
```

**Requirements:**
- Each QR code must be at least 200x200 pixels (300x300 recommended)
- Use `ERROR_CORRECT_H` (high error correction)
- Display as PNG images embedded in HTML/PDF output
- For HTML: embed as `<img>` tags with alt text
- For PDF via WeasyPrint: reference PNG files or use base64 data URIs
- Save QR codes in each book's directory

## D. Complete Book List — ALL Bob J Mills Books Published To-Date

A comprehensive, formatted list of ALL Bob J Mills books, organized by series. MUST be current and complete. Update whenever a new book is published.

### Current Complete List (17 books as of 2026-05-31):

```
Also by Bob J Mills

BUSINESS BOOKS:
  1. AI That Works
  2. The Crisis Ready Company
  3. Owner's Manual for AI Agents

THE AGE OF LIGHTSHIPS SERIES:
  1. Sunward Exodus
  2. The Mercury Accord
  3. Ghosts Beyond Neptune
  4. The Last Photon Fleet

THE LUNAR FOUNDATION SERIES:
  1. Moon Rock
  2. Mooncoming
  3. Waters End
  4. Waters Horizon

THE NO BLUE SKY SERIES:
  I.   Built from Dust
  II.  The Oxygen Gamble
  III. Rivers Under Mars
  IV.  The Red Charter
  V.   The First Martian Nation

MEMOIR:
  • Tomorrow Remembered
```

**IMPORTANT:** Check `/mnt/usb_4tb/books/` for the current inventory before finalizing any book. This list grows with each new publication.

## HTML Template

```html
<div class="last-page" style="page-break-before: always; text-align: center; padding: 40px 20px;">
  <h2 style="font-size: 1.6em; margin-bottom: 20px;">Thank You for Reading</h2>
  <p style="font-size: 1.05em; line-height: 1.7; max-width: 600px; margin: 0 auto 15px;">
    [Book-specific 4-5 sentence thank-you blurb in Bob's voice]
  </p>
  <p style="font-size: 1.05em; line-height: 1.7; max-width: 600px; margin: 0 auto 30px;">
    [2-3 sentence "More From Bob" statement]
  </p>
  <hr style="width: 60%; margin: 30px auto; border: 1px solid #ccc;" />
  <h3 style="font-size: 1.2em; margin-bottom: 20px;">For More From Bob J Mills</h3>
  <div style="display: flex; justify-content: center; gap: 40px; flex-wrap: wrap; margin-bottom: 30px;">
    <div>
      <img src="qr_mifeco.png" alt="MIFECO QR Code" style="width: 150px; height: 150px;" />
      <p style="font-size: 0.85em; color: #666; margin-top: 8px;">
        Scan for books, updates & more<br/>www.mifeco.com
      </p>
    </div>
    <div>
      <img src="qr_amazon.png" alt="Amazon QR Code" style="width: 150px; height: 150px;" />
      <p style="font-size: 0.85em; color: #666; margin-top: 8px;">
        Scan to find all Bob J Mills<br/>books on Amazon
      </p>
    </div>
  </div>
  <hr style="width: 60%; margin: 30px auto; border: 1px solid #ccc;" />
  <h3 style="font-size: 1.2em; margin-bottom: 15px;">Also by Bob J Mills</h3>
  <div style="text-align: left; display: inline-block; font-size: 0.95em; line-height: 1.6;">
    <!-- Complete book list here, updated per current inventory -->
  </div>
  <p style="margin-top: 30px; font-size: 0.9em; color: #888;">
    Available on Amazon Kindle and Paperback
  </p>
</div>
```

## Markdown Template (for .md manuscripts)

```markdown
---

## Thank You for Reading

[Book-specific 4-5 sentence thank-you blurb in Bob's voice]

[2-3 sentence "More From Bob" statement]

---

**For More From Bob J Mills:**

- **MIFECO:** www.mifeco.com — Scan the QR code below for books, updates, and more
- **Amazon:** Scan the QR code below to find all Bob J Mills books on Amazon

[QR Code: MIFECO] [QR Code: Amazon]

---

## Also by Bob J Mills

**BUSINESS BOOKS:**
1. AI That Works
2. The Crisis Ready Company
3. Owner's Manual for AI Agents

**THE AGE OF LIGHTSHIPS:**
1. Sunward Exodus
2. The Mercury Accord
3. Ghosts Beyond Neptune
4. The Last Photon Fleet

**THE LUNAR FOUNDATION:**
1. Moon Rock
2. Mooncoming
3. Waters End
4. Waters Horizon

**THE NO BLUE SKY:**
I. Built from Dust
II. The Oxygen Gamble
III. Rivers Under Mars
IV. The Red Charter
V. The First Martian Nation

**MEMOIR:**
Tomorrow Remembered

---

*Available on Amazon Kindle and Paperback*
```

## Pre-Upload Checklist Additions
- [ ] Last page includes expanded thank-you blurb
- [ ] Last page includes MIFECO QR code
- [ ] Last page includes Amazon QR code
- [ ] Last page includes expanded "more from Bob" statement
- [ ] Last page includes complete "Also by Bob J Mills" book list (updated)
- [ ] QR codes are scannable (test with phone camera)

## Series-Specific Structural Notes (learned 2026-05-31)

When applying last-page back matter across a series, be aware of structural variations:

- **Lightship (Age of Lightships)**: Arabic numeral dirs (Book_1_, Book_2_). 40 chapters each. Some books may lack compiled .md manuscripts — must assemble from `manuscript_src/` chapters first.
- **Lunar Foundation**: Arabic numeral dirs (Book_1_, Book_2_). Has HTML output files (.html). QR codes go in book root AND `_resources/` subdirectory for HTML references.
- **No Blue Sky**: **Roman numeral dirs** (Book_I_, Book_II_, Book_III_, Book_IV_, Book_V_). Chapter counts vary: Book I has 29, Book II has 22, Book III has 38, Books IV and V have only 5 each. Check actual `manuscript_src/` contents — don't assume 40 chapters.
- **Business**: Arabic numeral dirs (AI_That_Works, The_Crisis_Ready_Company, Owners_Manual_AI_Agents). No standard chapter structure — some have Compiled.md, some have chapter files, some have HTML output.
- **Memoir**: Single directory (Tomorrow_Remembered). Has Enhanced.md file.

**Always verify the actual filesystem structure before processing a series.** Use `ls` and `search_files` to find what exists rather than assuming a uniform structure.
