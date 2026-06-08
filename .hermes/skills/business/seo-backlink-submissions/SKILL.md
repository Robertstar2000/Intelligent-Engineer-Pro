---
name: seo-backlink-submissions
title: SEO Backlink Directory Submissions
description: Systematically submit a business website to free SEO backlink directories across consulting, AI/SaaS, and general business categories.
category: business
triggers: ["backlinks", "seo backlinks", "directory submissions", "link building", "submit to directories", "backlink discovery", "opportunity discovery", "write for us", "unlinked mentions", "competitor gaps"]
---

## 🔍 MemPalace Query (MANDATORY FIRST STEP)
Before proceeding, query MemPalace for existing context:
```python
import sys, os; sys.path.insert(0, os.path.expanduser('~/.hermes/mempalace'))
import embed; embed.init_embedding(os.path.expanduser('~/.hermes/mempalace'))
results = embed.search_embeddings("SEO backlink submissions directory business website", k=5)
```
This retrieves previous decisions, domain-specific context, and lessons learned from the vector memory store.

# SEO Backlink Directory Submissions

Systematic workflow for submitting a business to free, dofollow backlink directories.

## Prerequisites
- Target website URL
- Company name, description, founding date
- Product/service names and descriptions
- Founder/contact name and email
- Logo/icon (square, 512x512+)

## Research Phase

1. **Check current backlinks** — identify gaps
2. **Categorize directories** by relevance:
   - Industry-specific (consulting, AI, SaaS)
   - General business directories
   - Review platforms (G2, Capterra)
3. **Check accessibility** — many have Cloudflare; flag these for manual submission:
   ```bash
   for url in "https://clutch.co/get-listed" "https://crunchbase.com"; do
     curl -s -o /dev/null -w "%{http_code}" --max-time 10 "$url"
   done
   ```

## Automated Backlink Opportunity Discovery

Beyond manual directory submissions, use search-based automated discovery to find three types of backlink opportunities: **write-for-us** (guest post programs), **unlinked mentions** (brand/product mentions without a link), and **competitor gaps** (competitors' backlinks you can chase).

### Pipeline Engine Script

MIFECO has an automated discovery script at `~/.hermes/pipeline-engine/data/backlink-acquisition.py`. It uses DuckDuckGo search to find opportunities and writes results to `~/.hermes/pipeline-engine/data/backlink-opportunities.json`.

**Run it:**
```bash
cd /home/bob && python3 ~/.hermes/pipeline-engine/data/backlink-acquisition.py
```

The script outputs a terminal summary and saves all results (with `new`/`actioned`/`dismissed` statuses) to the JSON file for tracking.

### Avoiding Query Noise (Fixed in Script)

The script (`~/.hermes/pipeline-engine/data/backlink-acquisition.py`) now handles all known failure modes autonomously:

- **Domain blocklist** — 22 known junk domains (dictionary sites, sermon platforms, time pages, bird sites) are automatically filtered out
- **Negative keywords** — every query includes `-dictionary -definition -meaning -thesaurus` (and `-bird -raptor` where relevant)
- **Ambiguous abbreviations** — search uses full product names (`"Project Hypatia Pro"`, `"PM Accelerator"`) instead of bare `"PM"` or `"raptor"`
- **Deduplication** — duplicate URLs across search phases are filtered before saving
- **Retry with fallback** — verbose queries that timeout are automatically retried with shorter versions

**Historical reference:** See `skill_view(name='seo-backlink-submissions', file_path='references/backlink-discovery-queries.md')` for the full catalog of past failure modes and fixes.

### Post-Discovery Actions

When the script returns genuine opportunities:
1. Mark them `actioned` in the JSON file (`"status": "actioned"`) once pursued
2. For **write-for-us**: craft a guest post pitch per the site's guidelines
3. For **unlinked mentions**: reach out to the site owner requesting a link
4. For **competitor gaps**: add those sites to the manual submission list above

### Reference File

See `skill_view(name='seo-backlink-submissions', file_path='references/backlink-discovery-queries.md')` for query-specific notes and troubleshooting from automated discovery runs.

## Accessibility Check

Before attempting browser submissions, test which directories are accessible (not behind Cloudflare):

```bash
for url in \
  "https://startup-list.org/submit" \
  "https://www.futurepedia.io/submit-tool" \
  "https://www.saashub.com/submit" \
  "https://feedmystartup.com/submit/" \
  "https://launchboosts.com/submit" \
  "https://theresanaiforthat.com/submit-tool/" \
  "https://toolify.ai/submit" \
  "https://www.alternativeto.net/submit/" \
  "https://clutch.co/get-listed" \
  "https://crunchbase.com"; do
  status=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 "$url" 2>/dev/null)
  echo "$status $url"
done
```

- **200** = accessible via browser automation
- **301/302** = redirects (follow to final URL)
- **403** = Cloudflare — flag for manual submission from a home/residential IP

## Session Management (Multi-Directory Work)

Submitting to multiple directories is a high-iteration task. The browser session can reset to `about:blank` between tool-call batches, losing all form state. To minimize rework:

1. **Do the highest-value/quickest directories first** — in case you hit iteration limits
2. **Save credentials immediately** after each account creation to `~/hermes/secrets/{directory}-password.txt`
3. **Write a session reference file** at the end (`references/{project}-session-{date}.md`) so future sessions pick up without rediscovery
4. **When resuming** a prior session: load the reference file first, then re-authenticate on each directory's login page before navigating to the submission form
5. **Flag CAPTCHA-gated steps** early (SaaSHub hCaptcha, etc.) — these require user action; don't waste iterations trying to bypass them

## Submission Techniques

### Technique A: Direct Browser Form
Works for most accessible directories (SaaSHub, LaunchBoosts). Navigate, fill fields, submit.

### Technique C: LaunchBoosts Sign-Up Flow

LaunchBoosts requires an account before submitting a tool. The sign-up form is a React state toggle on the same page (not a separate URL):

1. Navigate to `https://launchboosts.com/auth/signin`
2. **Toggle to Sign-Up mode** — click **"Sign Up"** button. The heading changes from *"Sign in to your account"* → *"Create your account"*. The accessibility tree may not update; verify via browser_console:
   ```javascript
   document.querySelector('h2').textContent
   // Should say "Create your account" — if still "Sign in", use JS click:
   Array.from(document.querySelectorAll('button')).find(b => b.textContent.includes('Sign Up'))?.click()
   ```
3. Fill: **Full Name**, **Email Address**, **Password** (min 6 chars; complex pw with letters, digits, symbols accepted)
4. Click **Sign Up** → account created, redirects back to sign-in form
5. **Email verification required** — check inbox for verification link before you can submit a tool
6. After verifying, sign in at `/auth/signin` and navigate to `/submit` to fill the tool listing

**Pitfalls:**
- **First-signup password trap**: the initial signup can create the account entity but fail to persist the password. You'll see "User already exists" on retry but "Invalid email or password" on sign-in. **Workaround:** use an email alias (e.g. `user+launchboosts@domain.com`) to start fresh
- The sign-in/sign-up toggle is React state-only (no URL change). Use `browser_console` to click if the accessibility tree doesn't toggle
- **No "Forgot password"** link visible on the sign-in form — if locked out, recreate with aliased email
- **Email verification gate**: can't submit a tool until verification link is clicked. Plan accordingly — the submission step requires the user to check their inbox
- Google OAuth and GitHub OAuth options available as alternatives
- **Submit page renders sign-in modal**: navigating to `/submit` without auth shows a full-screen modal overlay with no visible close button
- **Session volatility**: after a signup redirect, the sign-in form fields may pre-fill but the session isn't actually authenticated. Always verify by checking for your name in the navigation bar or the URL path before proceeding with form submissions

### Technique D: Google Form Curl Submission (Reliable Alternative to Browser)

Some directories (e.g. Feed My Startup) embed Google Forms. Rather than filling via browser automation, submit directly via curl for greater reliability:

1. **Find the form ID** — inspect the embedded Google Form iframe `src` attribute:
   ```
   https://docs.google.com/forms/d/e/{FORM_ID}/viewform?...
   ```

2. **Open the form** in the browser and inspect hidden inputs to discover `entry.*` field IDs:
   ```javascript
   // Run in browser console on the Google Form page
   var entries = {};
   document.querySelectorAll('input:not([type="hidden"]), textarea, select').forEach(el => {
     entries[el.name || 'no-name'] = el.placeholder || el.type || el.tagName;
   });
   console.table(entries);
   ```

3. **Find the form action URL** (the `formResponse` endpoint):
   ```javascript
   document.querySelector('form').action
   // Returns: https://docs.google.com/forms/d/e/{FORM_ID}/formResponse
   ```

4. **Submit via curl** with the discovered `entry.*` IDs as form data:
   ```bash
   curl -s -L -o /dev/null -w "HTTP %{http_code}\n" --max-time 15 \
     -d "entry.1234567890=Company Name" \
     -d "entry.9876543210=https://example.com" \
     -d "entry.5555555555=Founder Name" \
     -d "entry.1111111111=Detailed description..." \
     "https://docs.google.com/forms/d/e/{FORM_ID}/formResponse"
   ```

   - **HTTP 200** = successful submission (Google returns 200 even on success, not a redirect)
   - No confirmation page — you can verify by checking the `Your response has been recorded` text, or simply trust the 200

5. **Building the field map efficiently**: use a helper to collect all form input names at once:
   ```javascript
   Array.from(document.querySelectorAll('[name^="entry."]')).map(e => e.name)
   ```

**Pitfall:** Google Forms may show a spinner overlay after programmatic `input.value` changes in the browser — this is why submitting directly via curl to `formResponse` is more reliable than trying to click the native Submit button inside the browser.

### Technique E: SaaSHub Registration

SaaSHub (saashub.com/submit) offers a free tool submission that lists you across 107+ directories. Registration needed:

1. Navigate to `https://www.saashub.com/submit` → click **Register**
2. Fill: **Email**, **Username** (letters, digits, dashes only), **Password** (letters + digits + special symbols required), **Confirmation**
3. **hCaptcha blocks automation** — a human must click the "I am human" checkbox
4. Uncheck "Send me the SaaSHub Weekly report" unless desired
5. Click **Register**, then sign in and submit the product

**Pitfall:** hCaptcha cannot be bypassed via browser automation. The user must complete this step manually. Prepare all form data beforehand so the user only needs to click the hCaptcha and submit.

### Technique F: Startup List Submission

Startup List (startup-list.org) offers free dofollow backlinks with a multi-step submission form. No CAPTCHA on registration.

**Registration:**
1. Go to `https://startup-list.org/register`
2. Fill: **Your name**, **Email**, **Password** — that's it (no CAPTCHA)
3. Click **Create Account** → immediately redirected to sign-in
4. Sign in → you're on the homepage, logged in

**Submission (multi-step):**
1. Go to `https://startup-list.org/submit`
2. **Step 1 — Basics**: Product Name, Website URL, Short Description (max 200 chars), Long Description, Logo URL (optional or upload)
3. **Step 2 — Details**: Categories, tags, pricing, social links (if applicable)
4. **Step 3 — Review**: Preview your listing and submit
5. After submission, you get a permanent public page at `https://startup-list.org/products/{your-product}`

**Pitfalls:**
- The Continue button may not advance if validation fails silently — check each field for errors. Try clicking via `browser_console` JS if the accessibility element click doesn't advance.
- Logo is optional; skip if you don't have a URL handy
- Short description has a 200-char limit — keep it punchy
- No email verification required — account works immediately after registration
- **Category combobox**: the Step 2 category selector is a React combobox that may not open via standard browser_click. If clicking the "Search or select a category..." button doesn't open a dropdown, try keyboard dispatch (`Element: dispatchEvent(new KeyboardEvent(...))`) or fall back to selecting a different field and coming back. If all else fails, flag this for manual completion.
- **Session volatility**: the browser can reset to `about:blank` between tool-call batches, losing all form progress. When resuming from a prior session, always start by re-authenticating at the login page before navigating to the submission form.

## Credential Management

When submitting to multiple directories, each generates separate credentials. Keep track:

```
Save credentials to ~/hermes/secrets/{directory}-password.txt for each:
{directory}: {email} / {username} / {password}
```

The format varies per directory — some use email-only, others use username+email. Standardize on email for the user's benefit.

### Credentials Template

Use `skill_view(name='seo-backlink-submissions', file_path='references/credentials-template.md')` to load a fill-in-the-blank template. Make a copy for each project session.

### Session Reference Files

At the end of a multi-directory submission session, write a filled session reference to `references/{project}-session-{date}.md` with:
- Completed submissions (what, method, content submitted)
- Pending items needing user action (credentials, what's left to do, exact URLs)
- Blocked items (why, what to do)
- All credentials used

This lets future sessions (or the user themselves) pick up exactly where you left off without rediscovery.

## Free Directories by Tier

### Tier 1 — Highest Value (DR 40+)
- **Startup List** (startup-list.org) — Create account → submit
- **Feed My Startup** (feedmystartup.com) — Google Form, requires detailed submission (150+ word description, founders, competitors, business model, launch date)
- **SaaSHub** (saashub.com) — Submit tool lists 107 other directories
- **LaunchBoosts** (launchboosts.com) — Requires account + email verification before submitting tool. Sign-in/sign-up toggles via React state on `/auth/signin` (not separate URLs). See pitfalls below.
- **AlternativeTo** (alternativeto.net) — Cloudflare blocked

### Tier 2 — Business Directories
- **Google Business Profile** — business.google.com (essential for local SEO)
- **Yelp Business** — yelp.com/business
- **Crunchbase** — crunchbase.com (Cloudflare blocked)
- **Hotfrog** — hotfrog.com
- **Manta** — manta.com
- **Cylex** — cylex.us.com

### Tier 3 — SaaS/AI Directories
- **G2** — g2.com (submit products, get reviews; needs 10+ reviews to rank)
- **Capterra** — capterra.com (Gartner-owned)
- **SaaSWorthy** — saasworthy.com
- **Betalist** — betalist.com (free with waitlist)
- **There's An AI For That (TAAFT)** — theresanaiforthat.com (DR 77, Cloudflare blocked)
- **Toolify.ai** — toolify.ai (Cloudflare blocked)

### Not Free / Paid Only
- **Futurepedia** — $247+ (Basic Listing sold out, Verified $497)
- **Clutch.co** — $499/year for Verified profile (free Basic listing has no dofollow backlink)

## Feed My Startup — Submission Template

When submitting to Feed My Startup (feedmystartup.com/submit-your-startup/), prepare:

| Field | Content |
|-------|---------|
| **Startup Name** | Company name |
| **Startup URL** | Full website URL with https:// |
| **Launching Date** | Year-month-day when the company was founded |
| **Founders** | Founder name(s) |
| **Short Description** | 150-200 words covering what the company does, key products/services, unique differentiators |
| **Description** | 250-300 words — deeper dive into services, products, clients, awards, partnerships |
| **Benefits** | Bullet-style list of key value propositions |
| **System Requirements** | What users need to use the product/service |
| **Scope of Improvement** | Future plans, roadmap items, expansion areas |
| **Business Model** | How the company makes money (consulting, SaaS, products, etc.) |
| **Competitors** | Main competitors in each vertical |
| **Name** | Submitter's name |
| **Email** | Contact email |

## Pitfalls
- Many directories use Cloudflare (Clutch, Crunchbase, TAAFT, Toolify, AlternativeTo) — these need submission from a home/residential IP; browser automation will be blocked
- Some require payment for premium placement — stick to free basic listings
- Account creation is often needed — use the company email
- Directory approval can take 1-14 days
- Some AI directories (Futurepedia) are now paid-only ($247+)
- Feed My Startup requires a detailed submission — prepare all fields before starting
- Google Forms may not accept programmatic `input.value` changes — the form tracks state through events. Use curl POST to the `formResponse` URL as a reliable fallback
- Some directories (Clutch) have free Basic listings but the backlink is nofollow or only visible on paid tiers — check before spending time
- **LaunchBoosts first-signup trap**: the initial signup can create the account entity but fail to persist the password. You'll see "User already exists" on retry but "Invalid email or password" on sign-in. **Workaround**: use an email alias (`user+launchboosts@domain.com`) to start a clean account
- **LaunchBoosts email verification gate**: even after successful signup, you cannot submit a tool until you click the verification link sent to the registered email. Plan for this — delay the submission step until the user confirms verification
- **LaunchBoosts submit page**: navigates to `/submit` but renders a sign-in modal overlay if not authenticated. The modal has no visible close button — you must sign in first
