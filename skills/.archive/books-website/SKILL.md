---
name: books-website
description: Architecture and deployment info for the Bob J Mills author books section at mifeco.com/books/. Load when modifying, deploying, or troubleshooting the books website.
version: 2.1.0
author: OWL
tags: [books, website, mifeco, deployment, newsletter, gated-downloads]
---

## 🔍 MemPalace Query (MANDATORY FIRST STEP)
Before proceeding, query MemPalace for existing context:
```python
import sys, os; sys.path.insert(0, os.path.expanduser('~/.hermes/mempalace'))
import embed; embed.init_embedding(os.path.expanduser('~/.hermes/mempalace'))
results = embed.search_embeddings("books website mifeco deployment DreamHost newsletter subscribe", k=5)
```
This retrieves previous decisions, domain-specific context, and lessons learned from the vector memory store.

# Books Section Website — mifeco.com/books/

> **MemPalace Query (MANDATORY):** Before deploying or modifying the books website, query MemPalace for relevant context:
> `mempalace_integration.semantic_recall("mifeco website deployment books")`
> This retrieves previous deployment history, image issues, and router fixes.

## File Structure

Built at `/mnt/usb_4tb/books/books-section/`, deployed to `mifeco.com/books/`.

```
books-section/
├── index.html              # Main author page (hero, series, magnets, signup)
├── css/style.css           # Complete stylesheet (~24KB, dark theme + gold accents)
├── js/main.js              # Mobile nav, scroll animations, subscribe AJAX handler
├── api/
│   ├── subscribe.php       # Subscribe handler (JSON db, AJAX response with download links)
│   └── subscribers.json    # Auto-created JSON database of all subscribers
├── privacy.html            # Privacy policy
├── images/                 # 27+ files: covers + infographics + scene images
│   ├── scene-*.png         # Series scene images (no-crop, object-fit:contain)
│   ├── author-photo.jpg    # Bob's photo (rounded rectangle, object-fit:contain)
│   ├── infographic-*.png   # Series infographics
│   └── *-cover.jpg         # Book covers
├── magnets/                # Free reader magnet downloads (PDF + EPUB + markdown)
├── no-blue-sky/            # Series detail page (5 books)
├── lunar-foundation/       # Series detail page (4 books)
├── age-of-lightships/      # Series detail page (4 books)
├── cindy-lou/              # Series detail page (3 books)
```

## Gated Free Book Downloads (Added 2026-06-05)

The Free Reader Magnets section (#magnets) is NOW GATED behind newsletter signup:

### UX Flow
1. User sees 5 magnet cards in #magnets section — each with "Subscribe to Download →" button
2. Clicking any button smooth-scrolls to #newsletter signup form
3. User fills: first name (required), email (required), interests (checkboxes, optional), comments/ideas (optional)
4. AJAX POST to `/books/api/subscribe.php` returns JSON with download links
5. On success: form hides, download grid appears with 5 PDF cards
6. Returning subscribers get instant access (no form) — API detects duplicate email

### The Subscribe Form Fields
| Field | Name | Type | Required |
|-------|------|------|----------|
| First Name | `first_name` | text | ✅ |
| Email | `email` | email | ✅ |
| Interests | `interests[]` | checkbox array (Business, SciFi, Fun Beach Reads, Serious Thought Provoking) | ❌ |
| Comments | `comments` | textarea (up to 2000 chars) | ❌ |

### API Endpoint: POST /books/api/subscribe.php
**Success Response (200):**
```json
{
  "success": true,
  "is_new": true,
  "message": "Welcome, Bob! Your free book downloads are ready.",
  "downloads": [
    {"title": "Cindy Lou and the Case of the Missing Retainer", "url": "/books/magnets/cindy-lou-missing-retainer.pdf", "series": "Cindy Lou Legal Capers"},
    ...
  ]
}
```
**Duplicate Email Response (200, is_new=false):**
Same shape with `is_new: false` — instant access without re-registering.
**Validation Error (400):** `{"success": false, "message": "Please enter your first name."}`

### Download Cards (AJAX-rendered)
After signup, the download grid creates `<a class="download-card">` per file:
- Title, series name, and "📥 Download Free PDF" button
- Each card links directly to the PDF in `/books/magnets/`

### Subscriber Database
- **Location:** `api/subscribers.json` on DreamHost + synced locally
- **Format:** JSON array of subscriber objects:
```json
[
  {
    "first_name": "Bob",
    "email": "bob@example.com",
    "interests": ["SciFi", "Business"],
    "comments": "Would love a Mars colony series",
    "source": "books-page",
    "subscribed_at": "2026-06-05T14:30:00-04:00",
    "ip": "192.168.1.1",
    "downloads_accessed": true
  }
]
```
- **Local backup:** Daily cron job (`sync-subscriber-db` at 2AM) copies the file to `/mnt/usb_4tb/books/books-section/api/subscribers.json` via paramiko SSH. This ensures it's included in the nightly Hermes backup (which covers `/mnt/usb_4tb/books/`).

## Image Management

### Source Directories
Four sources for images used on the books website:

1. **Book covers & infographics:** `/mnt/usb_4tb/books/Cindy_Lou_Legal_Capers/books-mifeco-website/images/`
2. **Series scene images:** `/home/bob/Pictures/` — contains thematic scene art for each series (Dust_Image.png, Moon_Image.png, lightship_image.png, Condy_Lou_image.png, Ai_that_works_image.png, Crisis_image.png, Manual_for_ai_Agents_image.png)
3. **Author photo:** `/home/bob/Pictures/Bobs pic 2 - Copy (2).jpg`
4. **Book cover art from generated_images:** `/mnt/usb_4tb/books/[Series]/[Book]/generated_images/` — contains `cover_final.png`, `Cover.jpg`, `cover_KDP.jpg` per book. Also fallback cover files at `[Book]/Cover.png` or `[Book]/KDP_PACKAGE/images/cover.jpg`.

### Cover Art Sources by Series

| Series | Image Source Path | File Used |
|--------|------------------|-----------|
| Age of Lightships | `.../Book_1_Sunward_Exodus/generated_images/cover_final.png` | cover-sunward-exodus.png |
| Age of Lightships | `.../Book_2_Mercury_Accord/generated_images/cover_final.png` | cover-mercury-accord.png |
| Age of Lightships | `.../Book_3_Ghosts_Beyond_Neptune/generated_images/cover_final.png` | cover-ghosts-neptune.png |
| Age of Lightships | `.../Book_4_Last_Photon_Fleet/generated_images/cover_final.png` | cover-last-photon.png |
| No Blue Sky | `.../Book_I_Built_from_Dust/Cover.jpg` | cover-built-from-dust.jpg |
| No Blue Sky | `.../Book_II_The_Oxygen_Gamble/Cover.png` | cover-oxygen-gamble.png |
| No Blue Sky | `.../Book_III_Rivers_Under_Mars/Cover.png` | cover-rivers-under-mars.png |
| No Blue Sky | `.../Book_IV_The_Red_Charter/Cover.png` | cover-red-charter.png |
| No Blue Sky | `.../Book_V_The_First_Martian_Nation/Cover.png` | cover-first-martian-nation.png |
| Lunar Foundation | `.../Book_1_Moon_Rock/cover.png` | cover-moon-rock.png |
| Lunar Foundation | `.../Book_2_Mooncoming/cover.png` | cover-mooncoming.png |
| Lunar Foundation | `.../Book_3_Waters_End/cover.png` | cover-waters-end.png |
| Lunar Foundation | `.../Book_4_Waters_Horizon/cover.png` | cover-waters-horizon.png |
| Cindy Lou | `.../book-1-retainer-to-trouble/Cover.png` | cover-retainer-to-trouble.jpg |
| Cindy Lou | `.../book-2-clause-for-alarm/Cover.png` | cover-clause-for-alarm.jpg |
| Cindy Lou | `.../book-3-affidavits-and-alibis/Cover.png` | cover-affidavits-alibis.jpg |
| Business | `.../AI_That_Works/KDP_PACKAGE/images/cover.jpg` | cover-ai-that-works.jpg |
| Business | `.../Owners_Manual_AI_Agents/Cover.png` | cover-ai-agents.jpg |
| Business | `.../The_Crisis_Ready_Company/generated_images/cover_KDP.jpg` | cover-crisis-ready.jpg |
| Memoir | `.../Tomorrow_Remembered/_resources/generated_images/Tomorrow_is_Still_Open_KDP_Cover.png` | cover-tomorrow-remembered.png |

### Magnet Art (replaces old infographics)
The old `infographic-*.png` images were replaced with reader magnet cover art from the magnets directory (`/mnt/usb_4tb/books/books-section/magnets/`):

| Source File | Web Name |
|-------------|----------|
| `magnets/No Blue Sky Novella/Dust.png` | `magnet-no-blue-sky.png` |
| `magnets/lunar foundation Novella/Moon.png` | `magnet-lunar-foundation.png` |
| `magnets/Age of Lightships Novella/Lightships.png` | `magnet-age-of-lightships.png` |
| `magnets/Cindy Lou Novella/CindyLou.png` | `magnet-cindy-lou.png` |
| `magnets/Business Series Magnet/Business.png` | `magnet-business.png` |

These are displayed in the `#infographics` section grid (5 cards, 2-column layout).

### Scene Images (Added 2026-06-05)
These replacement images go in place of book cover images in the feature series cards and business series cards:

| Source File | Web Name | Used In |
|-------------|----------|---------|
| `Dust_Image.png` | `scene-no-blue-sky.png` | No Blue Sky feature card |
| `Moon_Image.png` | `scene-lunar-foundation.png` | Lunar Foundation feature card |
| `lightship_image.png` | `scene-age-of-lightships.png` | Age of Lightships feature card |
| `Condy_Lou_image.png` | `scene-cindy-lou.png` | Cindy Lou feature card |
| `Ai_that_works_image.png` | `scene-ai-that-works.png` | AI That Works business card |
| `Crisis_image.png` | `scene-crisis-ready.png` | Crisis Ready business card |
| `Manual_for_ai_Agents_image.png` | `scene-ai-agents.png` | AI Agents business card |

### No-Crop CSS Rule (Added 2026-06-05)
ALL images use `object-fit: contain` to scale without cropping:
```css
/* Feature series images — dark background, contain, padding */
.feature-series-img {
  background: var(--bg-card);
  display: flex; align-items: center; justify-content: center;
  min-height: 300px;
}
.feature-series-img img {
  width: 100%; height: auto; max-height: 400px;
  object-fit: contain; padding: 1rem;
}

/* Business card images */
.series-card-img {
  object-fit: contain; background: var(--bg-deep); padding: 1rem;
}

/* Author photo — rounded rectangle, NOT circular crop */
.author-photo {
  border-radius: var(--radius);
  object-fit: contain; background: var(--bg-deep); padding: 0.5rem;
  width: 300px; height: 360px;
}
```

### Deployment Procedure
1. Copy from source to `books-section/images/` with clean web-friendly names
2. Do NOT resize — images are served at native resolution and scaled via CSS
3. Upload via paramiko SFTP batch (see Deployment section)
4. Verify all HTML-referenced files return HTTP 200

## Deployment

### SSH Access (Verified June 2026)
SSH is accessible via password authentication. **Paramiko is preferred over pexpect** — more reliable for multi-file transfer:
```python
import paramiko
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('IAD1-SHARED-B8-42.DREAMHOST.COM', username='dh_mwpxuu', password='Rm2214ri####', timeout=20)
sftp = client.open_sftp()
sftp.put(local_path, remote_path)
sftp.close()
client.close()
```

**Web root:** `/home/dh_mwpxuu/mifeco.com/books/` (NOT `books.mifeco.com` subdomain — that's a different config requiring separate DNS setup)

### Server Details
- Host: iad1-shared-b8-42.dreamhost.com
- Username: dh_mwpxuu
- Password: Rm2214ri####
- Web root: /home/dh_mwpxuu/mifeco.com/books/
- PHP validation: `php -l subscribe.php` before deploy
- Filesystem: Linux (case-sensitive — `Author-photo.jpg` ≠ `author-photo.jpg`)

### Method 1: Paramiko SFTP (Preferred — Fast & Reliable)
Upload individual files or batch with Python:
```python
def upload_files(files_dict):  # {remote_name: local_path}
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, username=user, password=pw, timeout=20)
    sftp = client.open_sftp()
    for remote_name, local_path in files_dict.items():
        sftp.put(local_path, f"{remote_base}/{remote_name}")
    sftp.close(); client.close()
```

### Method 2: Panel File Manager
1. `panel.dreamhost.com` → log in with MIFECOinc@gmail.com / Rm2214ri####
2. Websites → Manage → mifeco.com → File Manager
3. Navigate to the target directory, upload ZIP, extract in-place
4. **Panel React SPA navigation tip:** Direct URL navigation fails in headless browser. Use sidebar navigation buttons with native click events (not synthetic). The Websites button is a `<button>`, not an `<a>` tag.

### Method 3: Create ZIP locally (for Panel upload)
```bash
cd /mnt/usb_4tb/books/books-section && \
zip -r /tmp/books-deploy.zip . \
  --exclude "*.git*" --exclude "*__pycache__*" --exclude "*/.*" -x "*.pyc"
```
**NEVER use `--delete`** on the DreamHost web root — SPA, WordPress, and static site coexist.

## Design System
- Background: #06060f (deep navy-black)
- Accent: #d4a554 (gold)
- Card bg: #12122a
- Text: #f0f0f5 (primary), #9898b8 (secondary)
- Feature images: dark card background, object-fit:contain, padding, no cropping
- Author photo: rounded rectangle (not circle), object-fit:contain
- Scroll animation: IntersectionObserver with fade-up class (threshold 0.1)
- Responsive breakpoint: 768px (mobile nav, stacked cards, single-column checkboxes)

## HTML Sections (in page order)

1. **#top** — Hero section (worlds built from words, stats, CTA buttons)
2. **#scifi** — Sci-Fi section (No Blue Sky, Lunar Foundation, Age of Lightships — 3 feature-series cards with scene images)
3. **#cozy** — Mystery section (Cindy Lou — 1 feature-series card with scene image)
4. **#business** — Business section (3 series-grid cards with scene images)
5. **#memoir** — Memoir section (Tomorrow Remembered feature card)
6. **#magnets** — Gated free downloads (5 magnet cards pointing to #newsletter)
7. **#infographics** — Series art gallery (un-gated, free to browse — shows magnet cover art)
8. **#covers** — Book Cover Gallery (shows all 20 book covers from generated_images, organized by series with series headers)
9. **#author** — About the author (photo + bio)
10. **#reviews** — Testimonials
11. **#newsletter** — Subscribe form + hidden download success section
12. **#cta** — Final CTA banner

### Cover Art Gallery (#covers)

Displayed below the magnet art section. Shows book covers organized by series:

- **Layout:** CSS grid (`.cover-grid`) with `repeat(auto-fit, minmax(200px, 1fr))` — 4-5 columns on desktop, 2 columns on mobile
- **Each card:** `<div class="cover-card">` with `object-fit: contain` on the image, dark background, gold border on hover
- **Series headers:** `<h3 class="gallery-series-title">` in gold, centered, above each series group
- **Image sizing:** `height: 280px`, `object-fit: contain`, dark `var(--bg-deep)` background, `padding: 0.5rem`
- **Labels:** Series name + book number below each cover

Series order: Age of Lightships (4), No Blue Sky (5), Lunar Foundation (4), Cindy Lou (3), Business (3), Memoir (1) = 20 total covers.

#### CSS
```css
.gallery-series-title {
  font-family: var(--font-display);
  font-size: 1.8rem;
  color: var(--accent-gold);
  margin: 3rem 0 1.5rem;
  text-align: center;
}
.cover-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
}
.cover-card {
  border-radius: var(--radius-sm); overflow: hidden;
  border: 1px solid rgba(255,255,255,0.06);
  background: var(--bg-card);
  transition: var(--transition);
}
.cover-card:hover {
  transform: translateY(-4px);
  border-color: rgba(212,165,84,0.2);
  box-shadow: var(--shadow-gold);
}
.cover-card img {
  width: 100%; height: 280px;
  object-fit: contain; display: block;
  background: var(--bg-deep); padding: 0.5rem;
}
.cover-label {
  padding: 0.8rem;
  font-family: var(--font-sans); font-size: 0.8rem;
  color: var(--text-secondary); text-align: center;
  font-weight: 600;
}
```

## Critical Pitfalls

### Image & CSS
- **No-crop is a hard requirement:** When the user says "do not crop", use `object-fit: contain` with `background` and `padding` on the container. Never use `object-fit: cover` for these images.
- **Author photo must not be circular:** Use `border-radius: var(--radius)` (rounded rectangle) not `border-radius: 50%` (circle) when the user provides a portrait photo and says no-crop.
- **Scene images are small (300-500px):** These are smaller than the cover images they replace. The CSS must use dark backgrounds and padding to make the empty space around them look intentional.
- **Image file extension matters:** The HTML references specific extensions (`.jpg` vs `.png`). Match exactly on the server.

### Deployment
- **Case sensitivity:** Linux servers are case-sensitive. `author-photo.jpg` ≠ `Author_Photo.jpg`.
- **Old file residue:** Old images with different naming conventions (`ai-agents-cover.png`, `series_infographic.png`, `NBS_*.png`) remain after new uploads. Clean them up.
- **Router PHP variable escaping:** Writing PHP via SSH heredocs strips `$` signs. Write file locally, SFTP it, never use remote heredocs.

### Forms & Data
- **subscribe.php returns JSON** — client-side JS parses the `downloads` array and renders download cards. The PHP endpoint is POST-only (405 on GET).
- **subscribers.json file permissions** — Must be writable by the web server user (`dh_mwpxuu`). Create with `touch` and `chmod 644`.
- **No duplicate resubscribes** — API detects existing email and returns existing downloads immediately without creating a duplicate entry.
- **Comments field needs UTF-8 support:** Use `JSON_UNESCAPED_UNICODE` in PHP json_encode to preserve Unicode in international comments.

### Infographics Section (separated from magnets)
- The infographics gallery is now its OWN section (`#infographics`) separate from the gated downloads — free to browse, no signup required.
- If the user talks about free downloads, frame it as "free books" not "free infographics and covers."

> **References:**
> - `references/dreamhost-panel-navigation.md` — step-by-step DreamHost panel login
> - `references/subscribe-api.md` — subscribe API endpoint specs, JSON DB format, download response schema
