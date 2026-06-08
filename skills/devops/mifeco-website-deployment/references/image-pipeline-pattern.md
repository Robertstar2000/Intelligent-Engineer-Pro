# Website Image Pipeline — Lessons Learned

## Session: 2026-06-05 — Full Image Rebuild for mifeco.com/books

### Task
Replace all infographics and cover art on the books website with images from the magnets directory and generated_images directories. Deploy everything clean.

### Key Steps

#### 1. Image Discovery
Before touching anything, map ALL sources:
```bash
find /mnt/usb_4tb/books -name "cover*" \( -name "*.png" -o -name "*.jpg" \) -type f
find /mnt/usb_4tb/books -maxdepth 4 -name "Infographic.png" -type f
grep -o 'src="/books/images/[^"]*"' index.html | sort -u
```

#### 2. Image Naming Convention
- Magnet art: `magnet-{series-slug}.png`
- Cover art: `cover-{book-slug}.png`  
- Scene/feature: `scene-{series-slug}.png`
- Author: `author-photo.jpg`
- NO spaces — hyphens only

#### 3. CSS Rules (Bob's Preferences)
- **NO cropping**: always `object-fit: contain`, never `cover`
- **NO circular author photo**: rectangle only, no `border-radius`
- Dark background: `background: var(--bg-deep)`
- Padding: `0.5rem`–`1rem` inside containers

#### 4. Deployment Pattern
1. Copy images to `images/` with clean names
2. Update HTML references
3. Upload ALL references + HTML/CSS/JS via paramiko SFTP
4. **Remove stale files from server** — always
5. **Remove stale files locally** — always
6. Verify every reference returns HTTP 200

#### 5. Known Image Locations
| Source | What |
|--------|------|
| `books-section/magnets/[Series]/` | Magnet cover art |
| `[Series]/Book_*/generated_images/cover_final.png` | Best cover per book |
| `[Series]/Book_*/Cover.jpg` or `Cover.png` | Alt cover location |
| `/home/bob/Pictures/` | Scene art and author photo |

### What NOT to Do
- No `object-fit: cover` — Bob wants no cropping
- No `border-radius` on author photo
- Don't skip stale file cleanup (server AND local)
- Don't assume first `cover*.png` found is the right one