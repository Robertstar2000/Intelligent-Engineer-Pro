# Last Page Back Matter — Quick Reference
# Full spec: creative/publishing-workflow/references/last-page-back-matter.md

## Required on EVERY book's last page (in order):
1. **Thank You Blurb** — 4-5 sentences, unique per book, in Bob's voice
2. **More From Bob** — 2-3 sentences about cross-genre writing
3. **QR Codes** — `qr_mifeco.png` (books.mifeco.com) + `qr_amazon.png` (Amazon author page), 300x300px min
4. **Also by Bob J Mills** — Complete bibliography, ALL books, organized by series
5. **AI Disclosure** — Standard AI disclosure line
6. **Fan Club Blurb** (Added 2026-06-01) — Final section after AI disclosure:

```
---

### Join My Fan Club!

**Join my Fan Club's Mailing List** to get access to free, exclusive content and to receive periodic updates on my various works in progress!

🌐 www.books.mifeco.com
```

## QR Code Generation:
```python
import qrcode
from PIL import Image
def save_qr(url, path, size=300):
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=2)
    qr.add_data(url); qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
    img.resize((size, size), Image.NEAREST).save(path)
save_qr("https://www.books.mifeco.com", "qr_mifeco.png")
save_qr("https://www.amazon.com/stores/Bob-J-Mills/author/", "qr_amazon.png")
```

## Bibliography (20 books as of 2026-06-01):
- Business: AI That Works, The Crisis Ready Company, Owner's Manual for AI Agents
- Lightships: Sunward Exodus, The Mercury Accord, Ghosts Beyond Neptune, The Last Photon Fleet
- Lunar Foundation: Moon Rock, Mooncoming, Waters End, Waters Horizon
- No Blue Sky: Built from Dust, The Oxygen Gamble, Rivers Under Mars, The Red Charter, The First Martian Nation
- Memoir: Tomorrow Remembered
- Cindy Lou Legal Capers: Retainer to Trouble, Clause for Alarm, Affidavits and Alibis
