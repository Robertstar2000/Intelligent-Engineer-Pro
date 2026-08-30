---
name: openclaw-hermes
description: book publishing preparation and compliance workflow for authors publishing wide through amazon kdp, kobo writing life, barnes and noble press, google play books, and promotion sites such as book barbarian. use when the user asks for publishing checklists, retailer readiness, isbn decisions, compliance review, ai disclosure review, metadata cleanup, launch sequencing, promo readiness, or official publishing links.
---

## Memory context (Hindsight)

Long-term memory context is now provided automatically by Hindsight (bank
`mifeco-default`) on every turn — the retired MemPalace manual query step no
longer applies. Do NOT attempt to import `~/.hermes/mempalace` (it was removed
2026-08-19).This retrieves previous decisions, domain-specific context, and lessons learned from the vector memory store.

# OpenClaw Hermes

## Overview

Use this skill to help authors prepare a book for publication across major self-publishing retailers and promotion channels. Treat the workflow as a compliance-first launch review: verify rights, files, metadata, AI disclosure, ISBN decisions, retailer rules, live links, and promotion readiness.

This skill is not legal advice. When legal risk is material, state the risk plainly and recommend professional legal review.

## Core Workflow

1. Identify the target path:
   - Kindle only: use Amazon KDP checks.
   - Wide eBook: use KDP without KDP Select plus Kobo, Barnes and Noble, and Google Play checks.
   - Print: add print ISBN, trim, cover, barcode, and PDF checks.
   - Promotion: add Book Barbarian readiness checks.

2. Build a master metadata record:
   - title, subtitle, series, author, contributors, publisher, description, categories, keywords, language, publication date, territories, prices, ISBNs, AI-use record, retailer links.

3. Run the universal compliance gates before retailer-specific checks:
   - rights and ownership
   - manuscript quality
   - cover quality
   - metadata consistency
   - ISBN plan
   - AI content disclosure
   - adult/sensitive content classification
   - pricing and territorial rights

4. Run retailer-specific checks using the references:
   - Amazon KDP: see references/kdp.md
   - Kobo Writing Life: see references/kobo.md
   - Barnes and Noble Press: see references/barnes-noble.md
   - Google Play Books: see references/google-play.md
   - Book Barbarian: see references/book-barbarian.md
   - Official links: see references/official-links.md

5. Output a decision:
   - Pass: ready to publish or submit.
   - Fix: clear blocker exists.
   - Risk: not blocked, but needs judgment or legal/policy review.

## Universal Compliance Gates

Always check these before recommending publication.

### Rights

Confirm the user owns or controls rights for text, cover, images, maps, illustrations, fonts, quotes, translations, and any ghostwritten or coauthored material. Flag unlicensed song lyrics, long copyrighted quotes, fanfiction, scraped content, public-domain repackaging, trademark misuse, private personal information, and defamatory claims.

### Manuscript Quality

Check for missing chapters, duplicate chapters, broken links, broken table of contents, placeholder text, unreadable formatting, unsupported characters, strange spacing, accidental blank pages, wrong file uploads, and leftover AI draft artifacts.

### Cover Quality

Check that the cover matches the book, is readable at thumbnail size, signals the genre, and does not include fake award badges, false bestseller claims, unlicensed logos, unlicensed art, or misleading imagery.

### Metadata

Title, subtitle, author, and series details must match the cover and manuscript title page. Do not allow keyword stuffing, competitor names, temporary price claims, fake awards, misleading categories, or Amazon-specific language on non-Amazon retailers.

### ISBN

Use one ISBN per format: eBook, paperback, hardcover, audiobook. Retailer-provided free ISBNs normally stay tied to that retailer. For serious wide publishing, recommend publisher-owned ISBNs from the official ISBN agency for the user's country.

### AI Disclosure

For Amazon KDP, disclose final reader-facing AI-generated text, images, or translations. AI-assisted brainstorming, outlining, editing, proofreading, and refinement do not require KDP disclosure when final content is human-created. For all retailers, keep an AI-use record and reject low-quality automated content.

## Output Templates

### Readiness Scorecard

Use this format for launch reviews:

- Rights audit: Pass / Fix / Risk
- AI disclosure: Pass / Fix / Risk
- Manuscript quality: Pass / Fix / Risk
- Cover quality: Pass / Fix / Risk
- Metadata: Pass / Fix / Risk
- ISBN plan: Pass / Fix / Risk
- Retailer setup: Pass / Fix / Risk
- Pricing and territories: Pass / Fix / Risk
- Promotion readiness: Pass / Fix / Risk

Decision: [publish / do not publish yet / publish but delay promotion]

### Link Pack

When asked for links, provide official publisher portals, help centers, ISBN help pages, and ISBN agency links. Prefer official sources. Add a note that policies change and the user should check current rules before launch.

## Important Rules

- Use current web search for retailer rules, pricing, promotion rules, ISBN policies, or policy details when freshness matters.
- Do not claim legal certainty.
- Do not advise KDP Select if the user wants Kobo, Barnes and Noble, Google Play, Apple, or other eBook retailers live at the same time.
- Always distinguish publishing platforms from promotion platforms. Book Barbarian is a promotion site, not a publisher.

## No-AI Login Process (KDP / Kindle Publishing)

**Amazon KDP does NOT allow automated or AI-driven logins.** The AI cannot enter a username/password, complete CAPTCHAs, do 2FA, or access the KDP dashboard programmatically. Instead, a shared-browser handoff process is required:

### Step 1: AI Prepares Everything Offline

Before Bob touches a browser, the AI:
1. Generates the final manuscript (HTML + EPUB + PDF)
2. Generates the cover art with proper typography
3. Creates the KDP AI Disclosure record
4. Builds the marketing copy (short + long descriptions, categories, keywords)
5. Produces the final publishing package ZIP

**Critical pre-flight check:** Verify the KDP_PACKAGE directory is complete BEFORE opening the browser. A partial package (marketing files only, missing Kindle/Print/zip) will waste Bob's time at the login stage. See `references/kdp-publishing-techniques.md` → "Partial KDP Package Anti-Pattern" for the detection checklist.

### Step 2: Bob Opens & Logs Into the Browser

The AI opens a browser session to KDP, but login is blocked for AI:
1. AI navigates to `https://kdp.amazon.com`
2. AI calls `browser_vision(question="Show the login screen to Bob")`
3. AI tells Bob: *"Bob, please log into KDP. I've opened the KDP login page — enter your credentials manually."*
4. Bob types KDP username/password and completes 2FA in the shared browser
5. After Bob confirms, AI checks `browser_snapshot` for the KDP bookshelf dashboard

### Step 3: AI Guides Data Entry

Once logged in, the AI sees the dashboard and guides entry:

1. **Create New Title** — AI navigates and clicks the "+ Create" button
2. **Metadata Entry** — AI reads each field, then:
   - Types data directly into text fields via `browser_type`
   - Tells Bob what to select for dropdowns/radio buttons
   - Fields: Title, Subtitle, Series, Author, Description, Categories, Keywords, ISBN
3. **File Upload** — AI identifies upload buttons; Bob selects the file manually (file dialogs can't be automated)
4. **Cover Upload** — Same — Bob uploads the cover file
5. **Pricing & Royalty** — AI reads options and guides selection
6. **AI Disclosure** — AI identifies the disclosure checkbox and tells Bob to check it
7. **Submit** — AI confirms all fields, Bob clicks "Publish Your Kindle eBook"

### Browser Workflow Pseudocode

```
1. browser_navigate("https://kdp.amazon.com")
2. browser_vision("Confirm login screen is showing")
3. → Tell Bob: "Log in manually. I'll wait."
4. browser_navigate("https://kdp.amazon.com/en_US/bookshelf")
5. browser_snapshot → confirm we're on bookshelf
6. browser_click("@create_button") → "+ Create"
7. browser_type("@title_field", book.title)
8. browser_type("@author_field", book.author)
9. browser_type("@description_field", book.description)
10. → Tell Bob: "Upload the manuscript file at: /path/to/manuscript.epub"
11. → Tell Bob: "Upload the cover file at: /path/to/cover.png"
12. browser_click("@pricing_section") → configure royalty
13. browser_click("@ai_disclosure") → check AI box
14. → Tell Bob: "Click 'Publish Your Kindle eBook' to submit"
15. browser_snapshot → capture ASIN and confirmation
```

### KDP Publishing Checklist (No-AI Login Version)

| Step | Who | Action |
|------|-----|--------|
| 1 | **AI** | Prepare manuscript, cover, metadata, compliance docs |
| 2 | **AI** | Open browser to KDP login page |
| 3 | **Bob** | Log in manually (credentials + 2FA) |
| 4 | **AI** | Navigate to "Create New Title" |
| 5 | **AI** | Fill metadata fields (title, author, description, categories, keywords) |
| 6 | **Bob** | Upload manuscript EPUB/PDF file |
| 7 | **Bob** | Upload cover image |
| 8 | **AI** | Guide pricing & royalty selection |
| 9 | **AI** | Mark AI disclosure checkbox |
| 10 | **Bob** | Click "Publish Your Kindle eBook" button |
| 11 | **AI** | Capture ASIN and product page URL |
| 12 | **AI** | Deliver confirmation to Bob |

### Other Retailers With Same Restriction

This "no-AI login" process applies to ALL publishing platforms:
- **Kobo Writing Life** — `writinglife.kobo.com`
- **Barnes & Noble Press** — `press.barnesandnoble.com`
- **Google Play Books** — `play.google.com/books/publish`
- **Apple Books** — `authors.apple.com`
- **IngramSpark** — `ingramspark.com`
- **Draft2Digital** — `draft2digital.com`

For all: AI prepares → Bob logs in → AI guides entry via shared browser.
