# React SPA Bundle Modification — Session Pattern

## What Was Done

Added "Virtual Consulting" (`/consult`) and "Books" (`/links`) links throughout the main mifeco.com React SPA by modifying the minified JS bundle in-place. Also updated all consulting-related text to clearly separate **human consulting** (free 30-min expert sessions) from **virtual consulting** ($199 business assessment).

## Human vs Virtual Consulting — CRITICAL DISTINCTION

The main mifeco.com site has TWO types of consulting that must never be confused:

| Type | What | Price | Links To |
|------|------|-------|----------|
| **Human Consulting** | Free 30-min expert session, industry-specific strategic consulting | Free (form) or $500+/session | Consultation form popup (`de(!0)`), "Schedule Free Consultation" buttons |
| **Virtual Consulting** | $199 business assessment — 30-50 question survey, two PDF reports | $199 one-time | `/consult` (new tab) |

**Rules:**
- Human consulting buttons: "Schedule Free Consultation", "Consult with an Expert", "Schedule Industry Consultation" → open the consultation form popup
- Virtual consulting buttons: "Business Assessment — $199", "Start Your Assessment — $199", "Start Assessment — $199" → open `/consult` in new tab
- NEVER make a $199 button open the consultation form popup — this was a bug that was fixed
- The consultation form popup title is "Consult with an Expert" / "Book your free 30-minute strategy session" — clearly human
- Virtual consulting card titles should be clickable links to `/consult`

## Exact Changes Made (This Session)

### Main Site JS Bundle

1. **Desktop nav**: "Virtual Consulting" link → `/consult` (new tab), "Books" → `/books` (new tab)
2. **Mobile nav**: Same as desktop
3. **Hero section**: "Business Assessment — $199" CTA button → opens `/consult`
4. **Hero subtitle**: "get a $199 business assessment" → linked to `/consult`
5. **Products & Services section**:
   - "Virtual Consulting" card title → linked to `/consult`
   - Description: "Business Assessment for Any Issue — a comprehensive 30-50 question survey..."
   - Bullet: "Business Assessment Report (20+ pages)"
   - Bullet: "Strategic Action Plan (20+ pages)"
   - Bullet: "Delivered in 4 hours"
   - Button: "Start Your Assessment — $199" → opens `/consult`
6. **$199 Business Assessment card**: Title linked to `/consult`, description updated, bullets: comprehensive assessment, 30-50 question survey, two PDF reports, 4-hour delivery
7. **"Book for $199" button**: Changed from `onClick:()=>de(!0)` (consultation popup) to `onClick:()=>window.open("/consult","_blank")`
8. **Footer**: "Virtual Consulting" → `/consult`, "Books & Bookstore" → `/books`
9. **All "AI Readiness" references removed** from main site
10. **"AI Confusion" pain point** → "Technology Confusion" (in consulting page, not main site)

### Consulting Landing Page (index.php)

1. Title: "MIFECO Virtual Consulting — Business Assessment for Any Issue"
2. Hero badge: "Comprehensive Business Assessment — Any Issue"
3. Hero headline: "Find Out Exactly Where Your Business Stands — On Any Issue"
4. Hero subtitle: "business assessment" (not "AI readiness assessment")
5. Pain point: "Technology Confusion" (not "AI Confusion")
6. Pain point text: "adopt new technology" (not "use AI")
7. Process step: "Expert Analysis" (not "AI Analysis")
8. CTA: "get clarity on any challenge" (not "build a real AI strategy")

## Python Pattern Used

```python
with open('/tmp/mifeco_bundle.js', 'r') as f:
    bundle = f.read()

# Always verify the exact string exists before replacing
old = 'exact string from bundle'
count = bundle.count(old)
if count == 0:
    print(f"WARNING: String not found: {old[:80]}")
else:
    bundle = bundle.replace(old, new_string, 1)  # Replace one at a time
    print(f"Replaced ({count} occurrences)")

with open('/tmp/mifeco_bundle_modified.js', 'w') as f:
    f.write(bundle)
```

**IMPORTANT**: Replace one string at a time (use `replace(old, new, 1)`), not all at once. Some strings may appear multiple times and you only want to replace a specific instance.

## Key Strings Found in Bundle

| Purpose | String (exact) |
|---------|--------|
| Desktop Books nav | `l.jsx("a",{href:"#bookstore",className:"text-gray-600 hover:text-blue-600 transition-colors",children:"Books"})` |
| Mobile Books nav | Same but `className:"block text-gray-600...` |
| Hero CTA | `children:"Consult with an Expert"` |
| Products grid | `className:"grid md:grid-cols-3 gap-8 max-w-6xl mx-auto"` |
| Footer services end | `children:"Team Development"}})})` |
| Consultation popup trigger | `onClick:()=>de(!0)` — this opens the human consulting form |
| Virtual consulting link | `onClick:()=>window.open("/consult","_blank")` — this opens the $199 assessment |

## Deployment

Upload via SFTP to `/home/dh_mwpxuu/mifeco.com/assets/index-HASH.js` — the filename hash must match what `index.html` references.

Use paramiko for password-based SFTP (sshpass NOT available, pexpect works but paramiko is cleaner):

```python
import paramiko
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("ssh.mifeco.com", username="dh_mwpxuu", password="...", timeout=15)
sftp = client.open_sftp()
sftp.put("/tmp/mifeco_bundle_modified.js", "/home/dh_mwpxuu/mifeco.com/assets/index-Dd5ye8Ze.js")
sftp.close()
client.close()
```

## Verification

```bash
# Count occurrences
grep -o '/consult' /home/dh_mwpxuu/mifeco.com/assets/index-HASH.js | wc -l
grep -o '/books' /home/dh_mwpxuu/mifeco.com/assets/index-HASH.js | wc -l
grep -o 'AI Readiness' /home/dh_mwpxuu/mifeco.com/assets/index-HASH.js | wc -l  # should be 0

# Verify MD5 after upload
md5sum /home/dh_mwpxuu/mifeco.com/assets/index-HASH.js
```

## Important Notes

- Bundle hash changes on React rebuild — changes are lost if site is redeployed from source
- Always download the current bundle before modifying
- Use `execute_code` (Python) for string manipulation, not sed — more reliable for large files
- Verify exact string exists with `.count()` before replacing
- After upload, verify by downloading the live bundle again and grepping for changes
- The "AI-Powered SaaS Solutions" and "AI-Powered Engineering" references in the software section are CORRECT — they describe the SaaS products, not the consulting service. Do NOT change those.
- "AI-Powered" in the context of SaaS products (Hypatia Pro, PM Accelerator, VibraEngineer) is accurate and should be preserved
