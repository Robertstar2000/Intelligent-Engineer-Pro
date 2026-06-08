---
name: website-audit-and-product-launch
description: >-
  Audit a live business website and design a comprehensive restructuring plan
  that adds dedicated product pages for new SaaS offerings — including tech
  stack analysis, information architecture redesign, full landing page
  copywriting for each product, and technical migration requirements.
version: 1.1.0
author: Hermes Agent
license: MIT
tags:
  - website
  - audit
  - content-strategy
  - information-architecture
  - product-launch
  - saas
  - copywriting
  - landing-page
  - seo
triggers:
  - "User shares a website URL and asks to redesign it to support new products"
  - "Business transitioning from services-only to services + SaaS products"
  - "Need to audit an existing site and plan a product page structure"
  - "Add dedicated landing pages for existing SaaS tools that aren't on the website yet"
  - "Website restructuring with new navigation, subpages, and content strategy"
  - "Move an existing site from static SPA to WordPress with product pages and payment integration"
  - "User asks for landing page copy, product page content, or site structure planning"
  - "Generate WordPress page templates or PHP files for product pages"
  - "Rebuild a consulting/services website to emphasize SaaS products and AI augmentation"
  - "Reframe business positioning from human consulting to AI-augmented consulting"
  - "Create a fixed-price consulting offering ($199, $500, etc.) integrated into a SaaS pricing page"
  - "Build embedded SVG infographics for a marketing site — ecosystem diagrams, methodology flows, workflow visualizations"
  - "Create a dark-mode design system from scratch inline in a PHP/HTML file"
  - "Repurpose existing site assets (client logos, award photos) into a rebuilt site"
---

## 🔍 MemPalace Query (MANDATORY FIRST STEP)
Before proceeding, query MemPalace for existing context:
```python
import sys, os; sys.path.insert(0, os.path.expanduser('~/.hermes/mempalace'))
import embed; embed.init_embedding(os.path.expanduser('~/.hermes/mempalace'))
results = embed.search_embeddings("website audit product launch SaaS restructuring", k=5)
```
This retrieves previous decisions, domain-specific context, and lessons learned from the vector memory store.

# Website Audit & Product Launch Redesign

## Problem

A business has an existing live website but has built new SaaS products that aren't reflected on it. The site may be a single-page app with no subpages, poor SEO, and placeholder content where real products should live. The business needs a systematic approach to:

1. Audit the current site (tech stack, content, structure, SEO)
2. Investigate the actual product apps to understand their features
3. Design a new multi-page site structure
4. Write complete landing page content for each product
5. Document technical migration requirements

## Solution

A 3-part deliverable: (1) new site structure diagram, (2) full product landing page copy for each product, (3) technical requirements document — PLUS optionally (4) deployable WordPress PHP template files with Stripe payment integration.

## Steps

### Step 1: Audit the Live Website

Use browser tools to investigate the current site:

```bash
# Navigate and snapshot the homepage
browser_navigate(url)  # the live URL
browser_vision(question="Describe the full page layout and visual design system")
browser_snapshot(full=false)

# Check for subpages (try common paths)
browser_navigate(url + "/about")    # 200 or 404?
browser_navigate(url + "/products") # 200 or 404?
```

Check infrastructure:
```bash
# Hosting provider + tech stack HTTP headers
curl -sI https://www.example.com | grep -i "^server\\|^x-powered-by\\|^cf-ray"

# DNS resolution
host www.example.com  # or dig +short

# SPA routing detection
browser_console(expression="Array.from(document.querySelectorAll('a')).map(a=>a.href).join('\\\\n')")

# SEO foundation
curl -sI https://www.example.com/robots.txt
curl -sI https://www.example.com/sitemap.xml

# Tech stack (Vite/React? WordPress? etc.)
browser_console(expression="document.querySelectorAll('link[rel=stylesheet]').length")
browser_console(expression="document.querySelector('script[src]')?.src")
```

### Step 1b: Deep Tech Stack Detection

Before planning any modifications, determine the exact frontend technology. This dictates what CAN be edited and how. Use these specific DOM signals:

**React SPA (Vite/Next.js/Gatsby — compiled, no source on server):**
```js
// Check for React SPA signals
browser_console(`{
  hasRootDiv: !!document.getElementById('root'),
  isModuleScript: !!document.querySelector('script[type="module"][src*="/assets/"]'),
  hasTailwind: document.body.className.includes(' ') && !!document.querySelector('[class*="min-h-screen"], [class*="container"]'),
  hasShadcn: !!document.querySelector('[data-slot], [class*="shadcn"]'),
  hasLucideIcons: !!document.querySelector('[class*="lucide"]'),
  hasReactHelmet: !!document.querySelector('[data-rh]'),
  hasViteAssets: !!document.querySelector('script[src*="/assets/index-"], link[href*="/assets/index-"]'),
  bodyFirstChild: document.body.firstElementChild?.tagName || 'none',
  bodyHTML: document.body.innerHTML.substring(0, 200).replace(/</g,'&lt;')
}`)
```
**Signals:** `<div id="root">`, Tailwind utility classes (`min-h-screen`, `bg-white`, `space-y-4`), shadcn/ui (`data-slot="button"`), Lucide icons (`class="lucide lucide-*"`), Vite build (`<script type="module" crossorigin src="/assets/index-*.js">`), react-helmet-async (`data-rh="true"` on meta tags).
**Implication:** Cannot edit landing page content. Source lives on a dev machine. Must rebuild from source or use a different approach (rewrite in WordPress, add via server-side injection).

**WordPress Full Site Editing (block theme):**
```js
// Check for WordPress FSE signals
browser_console(`{
  hasAdminBar: !!document.getElementById('wpadminbar'),
  hasBlockClasses: !!document.querySelector('[class*="wp-block-"]'),
  hasBlockComments: document.body.innerHTML.includes('<!-- wp:'),
  hasExtendifyStyles: !!document.querySelector('[class*="is-style-ext-"]'),
  hasWpContentDir: location.pathname.includes('wp-content'),
  hasWpJson: !!document.querySelector('link[rel="https://api.w.org/"]'),
  bodyHTML: document.body.innerHTML.substring(0, 200).replace(/</g,'&lt;')
}`)
```
**Signals:** `wp-block-*` class names, `<!-- wp:group -->`/`<!-- /wp:group -->` HTML comments in source, `is-style-ext-*` classes (Extendable/Extendify theme), admin toolbar when logged in, `wp-content/themes/` in URLs, REST API link (`rel="https://api.w.org/"`).
**Implication:** Can edit via Site Editor (block editor), page editor, or REST API. Content defined in template files under `wp-content/themes/`.

**WordPress Classic (non-FSE):**
**Signals:** `wp-content/themes/` in URLs, admin bar, no block comments in source, classic PHP template hierarchy.
**Implication:** Edit via theme template files or page editor.

**Plain PHP / Static HTML:**
**Signals:** No `<div id="root">`, no `wp-*` classes, no block comments, `.php` or `.html` in URLs. Server-rendered content visible in raw HTML.
**Implication:** Can edit files directly on server.

**Editing implications summary:**

| Stack | Can edit landing page? | How |
|-------|----------------------|-----|
| React SPA (no source) | ❌ — needs source code | Rebuild from dev env + redeploy |
| WordPress FSE | ✅ — Site Editor | Block editor, REST API, or template files |
| WordPress Classic | ✅ — template files | PHP theme editor or FTP |
| Static HTML/PHP | ✅ — direct file edit | FTP or file manager |

Document the detected stack in memory for future sessions:
```
memory(action="add", target="memory", content="[Site] uses [stack] on [host]. Landing page content [can/cannot] be edited directly.")
```

### Step 2: Investigate Live Product Apps

For each product, visit the live app URL and capture a structured feature profile:

```bash
browser_navigate(url=product_url)
```

Capture these fields for each product:
- **Product name** (from `<title>` tag and hero heading)
- **Tagline / subtitle** (under the main heading)
- **Status badge** (e.g., "v2.5.0-STABLE — System Online")
- **Feature modules** — each numbered step with its icon, title, and verbatim description paragraph
- **Login/Signup CTAs** — button labels and placement
- **Pricing hints** (any mention of tiers, waitlists, free/Pro)
- **Copyright/version** in footer

Organize as a feature matrix:

```
Product A:
  Module 1: [Name] — [30-word description]
  Module 2: [Name] — [30-word description]
  Module 3: [Name] — [30-word description]
  ...
```

Also check local repo copies if available:
```bash
ls /path/to/saas/dir/
cat package.json  # app name, version, description
```

### Step 3: Design the New Site Structure

Create a side-by-side comparison of current vs. proposed structure:

```
Current (single page):                   Proposed (multi-page):
example.com/                             example.com/
├── Hero (consulting only)               ├── Hero (consulting + products)
├── Services (6 cards)                   ├── /products        ← NEW hub
├── Industries (4)                       │   ├── /product-a   ← NEW
├── Software Tools (placeholder)         │   ├── /product-b   ← NEW
├── Pricing (consulting only)            │   └── /product-c   ← NEW
├── Contact / Footer                     ├── /services
                                         ├── /industries
                                         ├── /pricing (SaaS + consulting)
                                         ├── /about
                                         ├── /contact
                                         └── /blog (future)
```

For each existing section, decide: **Keep** | **Rewrite** | **Replace** | **Move to subpage**

### Step 4: Write Product Landing Page Content

For each product, write complete page content including:

| Element | Description |
|---------|-------------|
| **Hero** | Headline, subhead, tagline, CTAs, status badge |
| **Problem/Solution** | 1-2 sentence framing (if the product solves a clear pain) |
| **Features** | Numbered or tabbed walkthrough — each with icon, title, 2-3 sentence description, benefit metric |
| **Use Cases** | 3-5 industry/role-based scenarios with audience targeting |
| **Pricing Section** | Tiers: Free → Pro/Professional → Enterprise — with feature lists and CTAs |
| **FAQ** | 2-3 common questions with answers (export, security, collaboration) |
| **Final CTA** | Bottom-of-page conversion section |

### Step 4.5: Reframe Business Positioning

When the business is transitioning from **services-only** to **services + SaaS products**, add a positioning reframing step:

1. **Identify which services to de-emphasize vs. AI-augment** — Go through each existing service offering and decide: does it stay as-is, get reframed as AI-powered, or get removed entirely?
2. **Create a comparison table** — Show "Traditional Consulting" vs. "AI-Augmented Consulting" side-by-side. Highlight: cost, speed, methodology, scalability.
3. **Add a fixed-price consulting tier** — A one-time virtual session (e.g., $199) that acts as both a standalone product and an upsell bridge to SaaS subscriptions. Include: AI-powered analysis, personalized roadmap, SaaS recommendation, follow-up.
4. **Write the new hero/narrative** — The homepage needs to communicate both services AND products. A dual-value proposition like "AI Consulting & Intelligent SaaS Platforms" signals the new positioning.

```html
<!-- Comparison table pattern -->
<div class="consulting-compare">
  <div class="old">
    <h4>❌ Traditional Consulting</h4>
    <ul>
      <li>Manual analysis — weeks to complete</li>
      <li>Static recommendations</li>
      <li>High hourly overhead</li>
      <li>One-size-fits-all frameworks</li>
    </ul>
  </div>
  <div class="new">
    <h4>✅ AI-Augmented Consulting</h4>
    <ul>
      <li>AI-assisted analysis — insights in hours</li>
      <li>Dynamic recommendations</li>
      <li>Fixed-price virtual engagements</li>
      <li>Tailored to your data & context</li>
    </ul>
  </div>
</div>
```

### Step 4.6: Create Embedded SVG Infographics

Instead of external image files, create inline SVG infographics directly in the HTML/PHP. This avoids dependency on image hosting and keeps everything in one deployable file.

Types of infographics to create:

1. **Ecosystem diagram** — Show how consulting feeds into SaaS products, which generate data that feeds back into consulting intelligence (a flywheel diagram).
2. **Methodology flow** — Product-specific frameworks (e.g., 6-phase lifecycle, 5-step workflow) as horizontal flowcharts with labeled steps.
3. **Protocol/stack visualization** — For engineering or technical products, show the protocol stack or methodology components as connected nodes (e.g., hexagons for a V-I-B-E acronym layout).
4. **Hero orbital graphic** — An SVG with orbiting nodes around a center point, great for showing multiple products around a core AI platform.

```html
<!-- Pattern for inline SVG infographic -->
<svg viewBox="0 0 820 340" fill="none" xmlns="http://www.w3.org/2000/svg" font-family="Inter">
  <defs>
    <linearGradient id="g1" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#6366f1"/>
      <stop offset="100%" stop-color="#8b5cf6"/>
    </linearGradient>
  </defs>
  <!-- Background -->
  <rect x="0" y="0" width="820" height="340" rx="16" fill="#1e293b"/>
  <!-- Nodes + connections... -->
</svg>
```

Key SVG techniques for marketing infographics:
- Use `<linearGradient>` for modern, polished fills and strokes
- Set `font-family="Inter"` (or whatever heading font) on the `<svg>` tag
- Use `fill="rgba(99,102,241,0.08)"` for subtle card backgrounds
- Add dashed connecting lines with `stroke-dasharray="4,3"` and low opacity (0.3)
- Use `<rect rx="8">` for rounded card elements inside the SVG
- Add a `<style>` block or inline styles on SVG text elements for bold/weight control
- Marker endpoints (`<marker id="arrow"...>`) for directional flows

### Step 4.7: Build a Complete Design System Inline

When rebuilding as a single PHP file (no external CSS framework), build a complete dark-mode design system with CSS custom properties:

```css
:root {
  /* Brand palette */
  --indigo-600: #6366f1;
  --teal-500: #14b8a6;
  --amber-500: #f59e0b;
  
  /* Backgrounds */
  --slate-900: #0f172a;
  --slate-800: #1e293b;
  --slate-700: #334155;
  
  /* Gradients — one per product line */
  --gradient-accent: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
  --gradient-teal: linear-gradient(135deg, #0d9488 0%, #06b6d4 100%);
  --gradient-warm: linear-gradient(135deg, #f59e0b 0%, #ef4444 100%);
  
  /* Effects */
  --shadow-glow: 0 0 40px rgba(99,102,241,0.15);
}
```

Design patterns to include:
- **Sticky blur nav** — `background: rgba(15,23,42,0.85); backdrop-filter: blur(20px);`
- **Product card hover glows** — colored box-shadow per product on hover, matching its gradient
- **Section separators** — use `::before` and `::after` pseudo-elements with radial gradients for glow effects
- **Tabbed content** — clickable methodology tabs with active states (vanilla JS)
- **Pricing card elevation** — featured card gets `transform: scale(1.05)` with a badge pill

### Step 5: Document Technical Requirements

Include:

- **Apache SPA routing (.htaccess)** — rewrite rules for subpage support
- **SEO foundation** — robots.txt, sitemap.xml, per-page OG tags + JSON-LD `SoftwareApplication` schema
- **Navigation changes** — current nav items vs. proposed Products dropdown
- **Content migration plan** — what to keep, rewrite, move to each subpage
- **Priority matrix** — P0 (blocker), P1 (critical), P2 (nice-to-have), P3 (future)

### Step 6: Determine Platform & Generate Deliverables

Before generating deliverables, determine the target platform:

```bash
# Ask the user: "Will this go on WordPress or stay as a static SPA?"
# If WordPress: generate PHP templates + plugin
# If static SPA: stay with the redesign document only
```

**Option A — Static SPA (document only):**
Write the full document to a project file:
```bash
write_file(
  path="/path/to/SITE_REDESIGN.md",
  content="# [Site Name] Redesign Plan\n\n...full document..."
)
```

**Option B — WordPress (.php): Generate deployable template files.**

Create the following deliverable set:

1. **WordPress .htaccess** — with security headers, caching, compression, WordPress permalink rewrites, and blocking sensitive files
2. **WordPress Plugin file** (`mifeco-core.php`) — registers page templates, provides Stripe helper functions and shortcodes
3. **Shared CSS** — responsive styles for product cards, pricing grids, use cases, FAQ
4. **Individual page templates** — one `.php` file per product, each with full landing page content
5. **Deployment guide** (`_SETUP.md`) — step-by-step installation instructions

Each template file should include:
- Page Template Name header comment (for WordPress template dropdown)
- Inline styles scoped to the template's brand color
- Stripe payment buttons on every pricing CTA
- "Launch App" links to live Cloud Run apps
- Responsive grid layouts

### Step 7: Integrate Payment Links

For each product pricing section, embed payment buttons that call a host-platform helper:

```php
// WordPress — use a helper function and shortcodes:
function mifeco_stripe_button($price_id, $label, $class) {
    $links = [
        'hypatia-free'      => 'https://buy.stripe.com/...',
        'hypatia-pro'       => 'https://buy.stripe.com/...',
        'accelerator-free'  => 'https://buy.stripe.com/...',
        'vibra-pro'         => 'https://buy.stripe.com/...',
        'enterprise'        => 'https://buy.stripe.com/...',
        'suite'             => 'https://buy.stripe.com/...',
    ];
    return sprintf('<a href="%s" class="%s">%s</a>', $links[$price_id], $class, $label);
}

// Usage in template: <?= mifeco_stripe_button('hypatia-pro', 'Subscribe $39/mo', 'btn-primary') ?>
```

Also register a shortcode for embedding anywhere in content:
```
[mifeco_pricing product="hypatia" tier="pro"]
```

Stripe Payment Links are preferred over raw Checkout Sessions because they require zero server-side code and can be managed from the Stripe dashboard.

## Pitfalls

- **Don't assume the site has subpages** — many business sites are single-page SPAs. Verify by trying URLs before designing a multi-page structure.
- **Check for 404s on robots.txt and sitemap.xml** — missing SEO files mean zero foundation. This is a P0 fix.
- **Don't trust the "Software" or "Tools" section** — it may contain placeholder/generic products that need replacement with real ones.
- **Verify each product's actual features** by visiting the live app, not by guessing from names. Product names can be misleading.
- **Note the hosting provider** — if the user has a preferred host (e.g., Hostinger) but the current site is on another provider (e.g., DreamHost), document this as a potential migration item.
- **Don't skip the local file system check** — there may be local repos with more detail than the live apps show.
- **SPA routing on Apache** requires mod_rewrite and an .htaccess with `RewriteCond %{REQUEST_FILENAME} !-f`. Without this, every subpage returns 404.
- **Ask about payment provider early** — Stripe Payment Links require no server-side code and can be embedded as simple `<a>` tags. Plan the pricing constants/URLs into the templates from the start.
- **The user may prefer a different CMS than current** — the live site may be a React SPA but the user wants WordPress. Don't assume the current platform is the target platform. Ask before generating deliverables.
- **Save the user's preferred stack to memory** — hosting provider, CMS preference, domain registrar, payment provider. This prevents re-clarifying next time.
