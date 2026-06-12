# Embedding Cover Images into Novella PDFs

Novella/reader-magnet PDFs served from mifeco.com/books/magnets/ need cover images embedded as the first page. The original HTML→PDF conversion produces a text title page, not a graphical cover.

## Workflow

### 1. Prepare the Cover Image

Use the magnet-style cover images (portrait, ~992x1586 pixels) from:
```
/mnt/usb_4tb/books/books-section/images/magnet-*.png
```

Resize to 6x9" book dimensions at 150 DPI (900x1350 pixels) with letterboxing:

```python
from PIL import Image

img = Image.open(cover_img_path)
target_w, target_h = 900, 1350
img_w, img_h = img.size
scale = min(target_w/img_w, target_h/img_h)
new_w, new_h = int(img_w*scale), int(img_h*scale)
img = img.resize((new_w, new_h), Image.LANCZOS)

canvas = Image.new("RGB", (target_w, target_h), (255, 255, 255))
x = (target_w - new_w) // 2
y = (target_h - new_h) // 2
canvas.paste(img, (x, y))
canvas.save("/tmp/cover.pdf", "PDF", resolution=150)
```

### 2. Merge Cover with Content PDF

```python
from PyPDF2 import PdfReader, PdfWriter

writer = PdfWriter()
writer.append("/tmp/cover.pdf")  # cover as page 1

content_reader = PdfReader(content_pdf_path)
for page in content_reader.pages:
    writer.add_page(page)

with open(output_path, "wb") as f:
    writer.write(f)
```

### 3. Upload to DreamHost

Use pexpect-based SCP with DreamHost password from `~/.hermes/.env` (`DREAMHOST_PASSWORD`):

```python
import pexpect, os

env_path = os.path.expanduser("~/.hermes/.env")
password = None
with open(env_path) as f:
    for line in f:
        if "DREAMHOST_PASSWORD" in line and "=" in line:
            password = line.split("=", 1)[1].strip().strip('"').strip("'")
            break

child = pexpect.spawn(
    f"scp -o StrictHostKeyChecking=no '{local_path}' dh_mwpxuu@iad1-shared-b8-42.dreamhost.com:{remote_path}",
    timeout=120
)
child.expect("password:", timeout=15)
child.sendline(password)
child.expect(pexpect.EOF, timeout=120)
```

### 4. Verify

```bash
curl -sI "https://www.mifeco.com/books/magnets/[pdf-name].pdf" | grep -i content-length
# Size should now be ~1.5-2.7MB (with cover) instead of ~76-98KB (without)
```

## Magnet Cover Image Map

| Novella PDF | Cover Image | Content Source |
|---|---|---|
| `lightships-last-transmission.pdf` | `images/magnet-age-of-lightships.png` | `magnets/Age of Lightships Novella/..._Magnet.pdf` |
| `lunar-foundation-first-light.pdf` | `images/magnet-lunar-foundation.png` | `magnets/lunar foundation Novella/..._Magnet.pdf` |
| `no-blue-sky-before-the-dust.pdf` | `images/magnet-no-blue-sky.png` | `magnets/No Blue Sky Novella/..._Magnet.pdf` |
| `cindy-lou-magnet.pdf` | `images/magnet-cindy-lou.png` | `magnets/Cindy Lou Novella/..._Magnet.pdf` |
| `ai-for-small-business.pdf` | `images/magnet-business.png` | `magnets/Business Series Magnet/..._Magnet.pdf` |

## Pitfalls

- PyPDF2 may not be installed: `pip3 install PyPDF2`
- The original magnet PDFs in subdirectories (~1.4-2.5MB) already have text title pages — the web-serving compressed PDFs (~76-98KB) do not
- Don't modify the original PDFs in subdirectories — replace the flat PDFs in `magnets/` root
- The content PDF (original with text title page) is used as the body after the cover
- Always verify the deployed file size matches the local output