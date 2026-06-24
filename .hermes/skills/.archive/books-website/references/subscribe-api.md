# Subscribe API — books-website Reference

## Endpoint: POST /books/api/subscribe.php

Handles newsletter signup, gated download unlock, and subscriber storage.

### Request (multipart/form-data)

| Field | Type | Key | Required | Validation |
|-------|------|-----|:--------:|------------|
| First Name | text | `first_name` | ✅ | 100 chars max, alphanumeric + spaces + apostrophes |
| Email | email | `email` | ✅ | Validated via `filter_var(FILTER_VALIDATE_EMAIL)` |
| Interests | checkbox[] | `interests[]` | ❌ | Whitelist: Business, SciFi, Fun Beach Reads, Serious Thought Provoking |
| Comments | textarea | `comments` | ❌ | 2000 chars max, Unicode-safe |
| Source | text | `source` | ❌ | URL-safe chars only, default "books-page" |

### Success Response (HTTP 200)

```json
{
  "success": true,
  "is_new": true,
  "subscriber": {
    "first_name": "Bob",
    "email": "bob@example.com"
  },
  "message": "Welcome, Bob! Your free book downloads are ready.",
  "downloads": [
    {"title": "Cindy Lou and the Case of the Missing Retainer", "url": "/books/magnets/cindy-lou-missing-retainer.pdf", "series": "Cindy Lou Legal Capers"},
    {"title": "No Blue Sky: Before the Dust", "url": "/books/magnets/no-blue-sky-before-the-dust.pdf", "series": "No Blue Sky"},
    {"title": "The Lunar Foundation: First Light", "url": "/books/magnets/lunar-foundation-first-light.pdf", "series": "The Lunar Foundation"},
    {"title": "The Age of Lightships: Last Transmission", "url": "/books/magnets/lightships-last-transmission.pdf", "series": "Age of Lightships"},
    {"title": "AI for Small Business", "url": "/books/magnets/ai-for-small-business.pdf", "series": "Business Books"}
  ]
}
```

### Duplicate Email Response (HTTP 200, is_new: false)

Same shape with `is_new: false`. No duplicate entry created in the database. Returns downloads immediately.

### Error Responses

**Missing first name (400):**
```json
{"success": false, "message": "Please enter your first name."}
```

**Invalid email (400):**
```json
{"success": false, "message": "Please enter a valid email address."}
```

**Wrong method (405):**
```json
{"success": false, "message": "Method not allowed"}
```

**Server write failure (500):**
```json
{"success": false, "message": "Server error. Please try again later."}
```

## Database Format: subscribers.json

Location on DreamHost: `/home/dh_mwpxuu/mifeco.com/books/api/subscribers.json`
Local backup: `/mnt/usb_4tb/books/books-section/api/subscribers.json`

### Schema

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

### File Management
- Created automatically on first signup
- Permissions: 644 (world-readable, owner-writable)
- No manual edit needed — append-only via API
- Duplicate email detection skips re-entry

## Client-Side Handler (js/main.js)

The subscribe form (`#subscribeForm`) uses vanilla XHR:

```javascript
var subscribeForm = document.getElementById('subscribeForm');
subscribeForm.addEventListener('submit', function(e) {
  e.preventDefault();

  // Validate first name + email client-side
  // Build FormData from form
  // AJAX POST to /books/api/subscribe.php
  // On success: hide form, show #downloadSection with rendered cards
  // On error: show error message in #formMessage with .form-error class
});
```

### Download Card Rendering

Each download in the response array renders as an `<a class="download-card">`:
```html
<a href="/books/magnets/cindy-lou-missing-retainer.pdf" class="download-card" target="_blank">
  <div class="download-card-title">Cindy Lou and the Case of the Missing Retainer</div>
  <div class="download-card-series">Cindy Lou Legal Capers</div>
  <div class="download-card-btn">📥 Download Free PDF</div>
</a>
```

### CSS Classes for Download Section

| Class | Purpose |
|-------|---------|
| `.download-grid` | 2-column grid (1-col on mobile) for download cards |
| `.download-card` | Gold-bordered card with hover lift effect |
| `.download-card-title` | Book title (bold, white) |
| `.download-card-series` | Series name (gold, uppercase) |
| `.download-card-btn` | CTA button within card |
| `.success-icon` | 🎉 emoji, 4rem |
| `.form-message` | General message container |
| `.form-error` | Red-bordered error variant |

## CSS Form Styles

### Subscribe Form
```css
.subscribe-form { max-width: 500px; margin: 0 auto; text-align: left; }
.form-field { margin-bottom: 1.2rem; }
.form-field label { display: block; font-size: 0.85rem; font-weight: 600; color: var(--text-primary); margin-bottom: 0.4rem; }
.form-field input[type="text"],
.form-field input[type="email"],
.form-field textarea {
  width: 100%; padding: 0.85rem 1rem;
  border: 1px solid rgba(255,255,255,0.15); border-radius: var(--radius-sm);
  background: rgba(6,6,15,0.6); color: var(--text-primary);
  font-size: 1rem; font-family: var(--font-sans);
}
.form-field input:focus, .form-field textarea:focus {
  border-color: var(--accent-gold); box-shadow: 0 0 0 3px rgba(212,165,84,0.15);
}
```

### Checkbox Grid
```css
.checkbox-group {
  display: grid; grid-template-columns: 1fr 1fr; gap: 0.6rem;
}
.checkbox-label {
  display: flex; align-items: center; gap: 0.6rem;
  font-family: var(--font-sans); font-size: 0.9rem;
  color: var(--text-secondary); cursor: pointer;
  padding: 0.5rem 0.8rem;
  border: 1px solid rgba(255,255,255,0.08); border-radius: var(--radius-sm);
  background: rgba(255,255,255,0.02);
}
.checkbox-label:hover { border-color: rgba(212,165,84,0.3); background: rgba(212,165,84,0.05); }
.checkbox-label input[type="checkbox"] { accent-color: var(--accent-gold); width: 18px; height: 18px; }
```

At mobile (<768px): `checkbox-group` changes to single column.

## Deployment Verification

After deploying subscribe API changes, test with:

```bash
# Test validation
curl -X POST https://www.mifeco.com/books/api/subscribe.php -d "email="
# Should return 400 with error message

# Test success  
curl -X POST https://www.mifeco.com/books/api/subscribe.php \
  -d "first_name=Test&email=test@example.com&interests[]=SciFi&interests[]=Business&comments=Great+books!"
# Should return 200 with 5 download links

# Test duplicate
curl -X POST https://www.mifeco.com/books/api/subscribe.php \
  -d "first_name=Test&email=test@example.com"
# Should return 200 with is_new:false and same 5 download links

# Clean up test entries via SSH
ssh dh_mwpxuu@IAD1-SHARED-B8-42.DREAMHOST.COM
python3 -c "
import json
with open('/home/dh_mwpxuu/mifeco.com/books/api/subscribers.json') as f:
    db = json.load(f)
clean = [e for e in db if e.get('email') != 'test@example.com']
with open('/home/dh_mwpxuu/mifeco.com/books/api/subscribers.json', 'w') as f:
    json.dump(clean, f, indent=2)
print(f'Cleaned: {len(db)} → {len(clean)} subscribers')
"
