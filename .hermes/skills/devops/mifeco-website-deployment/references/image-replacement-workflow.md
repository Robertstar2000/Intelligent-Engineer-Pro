# Image Replacement Workflow — mifeco.com/books

## Server Paths
- Images: `/home/dh_mwpxuu/mifeco.com/books/images/`
- Router: `/home/dh_mwpxuu/mifeco.com/books/router.php`
- HTML: `/home/dh_mwpxuu/mifeco.com/books/index.html` (and series subdirs)
- Local: `/mnt/usb_4tb/books/Cindy_Lou_Legal_Capers/books-mifeco-website/images/`

## What HTML References (verify before each deployment)

```bash
cd /home/dh_mwpxuu/mifeco.com/books
grep -ohE 'images/[^\"]*\.(png|jpg|jpeg|gif|svg|ico)' index.html cindy-lou/index.html age-of-lightships/index.html lunar-foundation/index.html no-blue-sky/index.html | sort -u
```

## Image Naming Convention

Local files use NEW naming: `series-name-infographic.png`
Server HTML references OLD naming: `infographic-series-name.png`

**Symlink mapping (create on server):**
```
infographic-age-of-lightships.png → age-of-lightships-infographic.png
infographic-business.png → business-infographic.png
infographic-cindy-lou.png → cindy-lou-infographic.png
infographic-lunar-foundation.png → lunar-foundation-infographic.png
infographic-no-blue-sky.png → no-blue-sky-infographic.png
infographic-all-series.png → copy of business-infographic.png
```

## Resize Specifications
- Book covers: 400x600 (2:3 ratio, JPEG quality 85)
- Infographics: 600px wide (PNG optimized)
- Favicon: 32x32 (keep as-is)
- Author photo: 150x150 (placeholder)

## Step-by-Step Process

1. **Identify what HTML references**: `grep -ohE 'images/...'` across all HTML files
2. **Remove old files**: `rm -f old-file1 old-file2 ...` — delete ALL unreferenced files
3. **Resize new files locally**: Use PIL to resize to web dimensions
4. **Upload via SCP**: Write file locally → SCP to server (NOT heredoc through pexpect)
5. **Create symlinks**: For old naming conventions that HTML still references
6. **Verify**: `for f in ...; do test -f $f && echo "OK" || echo "MISSING"; done`

## Common Pitfalls
- pexpect strips `$` from PHP variables — always SCP PHP files, never write through pexpect heredoc
- `execute_code` sandbox writes to `/tmp` (root partition, 117GB) — write large files to USB drive
- `books.mifeco.com` ≠ `mifeco.com/books` — always verify the actual web path
- Old files not removed before uploading new ones → bloated directory with stale files
- Forgetting to convert RGBA→RGB before saving as JPEG → PIL throws KeyError
