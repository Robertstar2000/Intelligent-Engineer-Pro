# Website Image Updates — No-Crop Replacement Pattern

When replacing images on the mifeco.com/books website (or books.mifeco.com), use this workflow to ensure images display without cropping.

## Image Source Location

User's source images live at `/home/bob/Pictures/` — scene art, book illustrations, author photos.

## File Naming Convention

Copy to `/mnt/usb_4tb/books/books-section/images/` with clean web-friendly names:
- Scene images: `scene-<series-key>.png` (e.g. `scene-no-blue-sky.png`, `scene-lunar-foundation.png`)
- Author photo: `author-photo.jpg`

## CSS: No-Crop Fitting

Always use `object-fit: contain` instead of `object-fit: cover` to prevent cropping. Add dark background and padding so smaller images look intentional:

```css
/* Feature series images (large showcase) */
.feature-series-img {
  background: var(--bg-card);
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 300px;
}
.feature-series-img img {
  width: 100%;
  height: auto;
  max-height: 400px;
  object-fit: contain;
  padding: 1rem;
}

/* Business card images */
.series-card-img {
  object-fit: contain;
  background: var(--bg-deep);
  padding: 1rem;
}

/* Author photo — rounded rectangle, not circle */
.author-photo {
  width: 300px;
  height: 360px;
  border-radius: var(--radius);   /* was border-radius: 50% */
  object-fit: contain;
  background: var(--bg-deep);
  padding: 0.5rem;
}
```

## HTML Changes

Replace `onerror="this.src='data:image/svg+xml,...'"` fallbacks with clean `src` attributes. 
Add inline style `style="background:var(--bg-deep);padding:0.5rem;"` on img tags for containers that don't have CSS background.

## Deployment

```python
import paramiko
host = "IAD1-SHARED-B8-42.DREAMHOST.COM"
user = "dh_mwpxuu"
password = "Rm2214ri####"  # from ~/.hermes/secrets/

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(host, username=user, password=password, timeout=20)
sftp = client.open_sftp()

local_base = "/mnt/usb_4tb/books/books-section"
remote_base = "/home/dh_mwpxuu/mifeco.com/books"

for rel_path, local_path in files_to_upload.items():
    sftp.put(local_path, f"{remote_base}/{rel_path}")

sftp.close()
client.close()
```

## Verification

```python
import requests
for name, url in checks:
    r = requests.get(url, timeout=15)
    assert r.status_code == 200
```

Key checks:
- All new images return HTTP 200
- HTML contains new image references (grep for `scene-` in index.html)
- CSS file contains `object-fit: contain`
