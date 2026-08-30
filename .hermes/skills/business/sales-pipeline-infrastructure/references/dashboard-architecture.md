# MIFECO Dashboard Architecture

## File Locations
- Pipeline dashboard: `/home/bob/.hermes/pipeline-engine/dashboard/pipeline-dashboard.html`
- Outreach dashboard: `/home/bob/.hermes/pipeline-engine/dashboard/outreach-dashboard.html` ← **primary send interface**
- Content command center: `/home/bob/.hermes/pipeline-engine/dashboard/content-command-center.html` ← **NOT DEPLOYED** (spec-only; use outreach dashboard instead)
- Hermes dashboard: `/home/bob/.hermes/pipeline-engine/dashboard/hermes-dashboard.html`
- Pipeline data: `/home/bob/.hermes/pipeline-engine/data/`
- Pipeline sequences: `/home/bob/.hermes/pipeline-engine/sequences/`
- Pipeline forms: `/home/bob/.hermes/pipeline-engine/forms/`
- Dashboard server: port 5540/5543 (HTTP redirect → HTTPS), serving from `dashboard/` directory
- Pipeline data API: `dashboard/https-server.py` imports `scripts/pipeline_data_api.py` for POST endpoints
- Mock inbox: `data/mock-inbox.json` — captures test mode emails

## Serving
```bash
cd /home/bob/.hermes/pipeline-engine/dashboard && python3 -m http.server 5540 --bind 0.0.0.0
```
**Root access:** To serve at `http://192.168.1.77:5540/` instead of needing the `/pipeline-dashboard.html` path, copy the file to index.html in the same directory and restart the server:
```bash
cp pipeline-dashboard.html index.html
# Kill old server, start new one
```

## 5 Panels of Pipeline Dashboard

### Books Catalog
10 books across 3 series + standalones. Status: written or packaged.
Data array in JS: `const booksCatalog = [...]`
Status badges: ideation=gray, written=blue, edited=cyan, packaged=green, published=gold
Sources: scan `/home/bob/books/` for manuscript.md, PDF, and FINAL_PACKAGE directories.

### SaaS Apps
- Project Hypatia Pro — GitHub: `https://github.com/Robertstar2000/https-github.com-Robertstar2000-HypatiaPro.git` — Cloud Run: `https://project-hypatia-pro-1064319572465.us-west1.run.app`
- PM Accelerator — GitHub: `https://github.com/Robertstar2000/Project-management-accelerator.git` — Cloud Run: `https://project-management-accelerator-845075991286.us-west1.run.app`
- VibraEngineer — GitHub: `https://github.com/Robertstar2000/Intelligent-Engineer.git` — Cloud Run: `https://vibraengineer-845075991286.us-west1.run.app`
- mifeco.com Website — GitHub: `https://github.com/Robertstar2000/mifeco_web.git` — DreamHost (no production URL exposed)
Local code paths: `/home/bob/Desktop/hermesfiles/saas/Project_Hypatia_Pro/`, `/home/bob/Desktop/hermesfiles/saas/Project_Management_Accelerator/`, `/home/bob/Desktop/hermesfiles/saas/VibraEngineer/`, `/home/bob/Desktop/hermesfiles/mifeco_web/`

### Consulting Pipeline  
8 leads (human consulting), 3 tiers ($199/$1,499/$3,999). AgentMail inbox: crowdedbutton536@agentmail.to  
Pipeline flow: Lead → Contact → Qualified → Intent → Strategy Session → Proposal Sent → Negotiation → Closed Won  
Nurture: 5 emails over 10 days

### Virtual Consulting Pipeline
No leads yet, 3 tiers ($199/$1,499/$3,999). Email: backdoor@mifeco.com  
Pipeline flow: Lead → Contacted → Qualifier → Buy → Process → Deliverables → Edit → Complete Delivery

### Lead & Promotion
Cross-pipeline stats. Links to Content Command Center and Outreach SVG dashboard.

### Pipeline Health (5th panel)
Per-pipeline operational status cards showing:
- Status dot (green/yellow/red)
- Last Run timestamp (from orchestrator or daily report)
- Latest Project description
- Lead counts (total, active, stale)
- Contextual tags
Data is a static JS array: `const pipelineHealth = [...]`

## Content Command Center Sidebar Stats
The 4 sidebar stat labels (Total Items, Approved, Sent, Queued) are clickable. Clicking opens a modal listing all items in that state across all 6 viewer arrays (including EMAIL_TEMPLATES — the enrichment queue). Clicking an item in the modal jumps to its viewer tab with search pre-filled.

**Critical: EMAIL_TEMPLATES must be included in both:**
- `showStatusList()` — under `const allViewers`, add `{key:'enrichment', label:'Email Tmpl', arr:EMAIL_TEMPLATES}`
- `updateSidebarStats()` — add `EMAIL_TEMPLATES` to the array iterated (currently `[LINKEDIN_MSGS, EMAILS, EMAIL_TEMPLATES, X_POSTS, BLOG_POSTS, LINKEDIN_POSTS]`)
