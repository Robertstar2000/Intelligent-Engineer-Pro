---
name: multi-app-brand-alignment-audit
description: Systematically audit multiple deployed SaaS/web applications for brand consistency — colors, typography, parent-company branding, CTAs, favicons, HTML metadata, and production readiness. Use when a company has multiple live apps that should look like a cohesive product family.
tags: [saas, branding, audit, landing-page, consistency, production-readiness]
---

## 🔍 MemPalace Query (MANDATORY FIRST STEP)
Before proceeding, query MemPalace for existing context:
```python
import sys, os; sys.path.insert(0, os.path.expanduser('~/.hermes/mempalace'))
import embed; embed.init_embedding(os.path.expanduser('~/.hermes/mempalace'))
results = embed.search_embeddings("brand alignment audit SaaS web application consistency", k=5)
```
This retrieves previous decisions, domain-specific context, and lessons learned from the vector memory store.

# Multi-App Brand Alignment Audit

## When to Use

- The user asks "do the landing pages look consistent?" or "are the apps aligned?"
- A company has multiple deployed SaaS products and needs to ensure brand coherence
- Before launching a new product alongside existing ones — verify brand alignment
- After rebranding the company, audit all products for updated brand guidelines
- User says "assess the SaaS business line" or "check the apps for branding"
- Adding a new app to an existing product family — audit it against the others

## Workflow

### Step 1: Discover the Apps

Get the list of live app URLs. Sources:
- Agent memory (`Memory: "Existing live apps on Cloud Run:..."`)
- User directly provides URLs
- Local repo directories: `ls /home/bob/saas/` or similar
- Previous session search for deployment URLs

```bash
# Check local repos for package.json app names
ls /path/to/saas/dir/
cat */package.json | grep -E '"name"|"version"|"description"'
```

### Step 2: Visit Each Live App and Capture Branding Profile

For each app, use `browser_navigate` + `browser_vision` to capture:

| Element | What to Check |
|---------|---------------|
| **HTML `<title>`** | Format pattern — is it consistent across apps? |
| **Hero heading** | Does it mention the company name (e.g., MIFECO)? Position? |
| **Tagline/subtitle** | Under the main heading — tone and length |
| **Primary colors** | Track: background hex, accent/gradient colors, button colors |
| **Fonts** | Body font, heading font (check DevTools/console) |
| **CSS framework** | Bootstrap, Tailwind, custom? |
| **CTAs** | Button labels — "SIGN IN" vs "Log Out" vs "Start Project" |
| **Favicon** | Is there one? Is it a logo or an emoji? |
| **Logos/imagery** | Any brand logo files on the page? |
| **Version/status** | Footer text, version numbers, status badges |
| **Company refs** | Copyright text, trademark mentions, footer links |
| **Auth state** | Is the app pre-authenticated or showing a sign-in/sign-up form? |

```bash
# Capture for each app URL:
browser_navigate(url="https://app1.example.com")
browser_vision(question="Describe the full page layout: hero, colors, CTAs, branding, fonts, favicon, version text, footer")
browser_console(expression="document.title")
browser_snapshot(full=false)
```

### Step 3: Build a Comparison Matrix

Create a table comparing every app across all brand elements:

| Aspect | App A | App B | App C |
|--------|-------|-------|-------|
| **HTML title** | "Hypatia Pro \| MIFECO" | "Accelerator \| MIFECO OS" | "VibraEngineer" |
| **Hero heading** | "MIFECO" | "Project Management Accelerator" | "MIFECO" |
| **Primary color** | `#00f2fe` cyan | `#6366f1` indigo | `#4ECDC4` teal |
| **Background** | `#050507` | `#0f172a` | `#121212` |
| **MIFECO branding** | ✅ Hero + Footer | ✅ Footer + Tagline | ❌ None |
| **Favicon** | ❌ None | ❌ None | 🤖 Emoji |
| **CTA label** | "SIGN IN/SIGN UP" | "New Project" (authed) | "SIGN IN/SIGN UP" |
| **CSS framework** | Bootstrap 5 | Tailwind v4 | Tailwind CDN |
| **Version** | V3.01 | V2.5.0-STABLE | V4.03 |

### Step 4: Identify Alignment Issues

Flag each inconsistency as:
- 🔴 **Critical** — Different company name presentation, missing logo, or completely different design language
- 🟡 **Minor** — Different version numbering, slightly different button labels
- ✅ **Aligned** — Same font family, same company reference format, consistent CTA pattern

### Step 5: Assess Production Readiness

Beyond branding, check deployment readiness for each app:

```bash
# Check for Dockerfile
ls /path/to/saas/app/Dockerfile 2>/dev/null || echo "Missing: Dockerfile"
ls /path/to/saas/app/cloudbuild.yaml 2>/dev/null || echo "Missing: cloudbuild.yaml"
ls -d /path/to/saas/app/dist/ 2>/dev/null || echo "Not built (no dist/)"
cat /path/to/saas/app/package.json | grep -E '"build"|"start"|"dev"'
```

Check these for each app:
- ✅ Express server with static file serving (production-ready architecture)
- ❌ Missing Dockerfile for containerization
- ❌ Missing cloudbuild.yaml for Cloud Run deploy
- ❌ Not built (no `dist/` directory)
- ❌ SQLite path — uses `./database.sqlite` (won't persist on Cloud Run) vs `/tmp/db.sqlite` (ephemeral/correct)
- ❌ Uses `tsx` instead of `node` for production start (adds runtime dependency)
- ❌ Uses Tailwind via CDN instead of build-time

### Step 6: Report Findings

Present a structured report with:
1. **The Brand Matrix** — comparison table (from Step 3)
2. **Alignment Issues** — numbered list of 🔴/🟡 issues found
3. **Production Readiness** — per-app checklist
4. **Recommendations** — prioritized: what to fix first

Example report format:

```
## 📊 Brand Alignment Audit

### Current State
All 3 apps are live on Cloud Run — functional but visually disconnected.

### 🔴 Critical Issues
1. Three different primary colors — users won't know they're from the same company
2. VibraEngineer has zero MIFECO brand mentions
3. No favicons or logos across any app

### 🟡 Minor Issues
1. Version numbering inconsistent (V3.01 vs V2.5.0 vs V4.03)
2. HTML title formats don't match
3. PM Accelerator shows authenticated view while others show login

### ✅ What's Good
- All use same fonts (Inter + Space Grotesk)
- All use dark themes
- All deployed and functional on Cloud Run

### Production Readiness
| App | Dockerfile | Build Config | Built | SQLite Path |
|-----|-----------|-------------|-------|-------------|
| Hypatia Pro | ❌ | ❌ | ❌ | ✅ /tmp/ |
| PM Accelerator | ❌ | ❌ | ❌ | ❌ ./database.sqlite |
| VibraEngineer | ❌ | ❌ | ❌ | ❌ ./database.sqlite |

### Recommendations
1. Create a shared brand design system (colors, favicon, logo)
2. Add MIFECO branding to all apps with consistent placement
3. Standardize HTML title format: "[App Name] | MIFECO"
4. Create Dockerfiles and cloudbuild.yaml for each app
5. Fix SQLite paths for Cloud Run compatibility
```

## Pitfalls

- **Live apps may differ from local source** — always check live URLs with browser tools, don't rely solely on local code inspection. The deployed version may have different branding than the repo.
- **Auth state changes the landing page** — if you're logged in, you see a dashboard, not a landing page. Use a fresh/incognito session or note the auth state.
- **Version numbers in footers may be stale** — check the app's actual features, not just the footer text.
- **Favicons may load dynamically** — check the page source `<link rel="icon">` rather than relying on the browser's tab icon.
- **Don't confuse "deployed" with "production-ready"** — all apps may be running on Cloud Run but still missing Dockerfiles, build configs, or persistent storage.
- **The local repos may be ahead or behind** the live deployment. Check both if available.
