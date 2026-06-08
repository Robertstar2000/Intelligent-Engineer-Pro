# MIFECO Product Line Inventory — May 12, 2026

> Snapshot of all MIFECO product lines, their current state, known issues, and blockers.
> Last updated: 2026-05-12 (CEO Agent daily orchestrator — Tuesday Books/Content day)

---

## 1. SaaS — Cloud Run Apps

### Project Hypatia Pro
- **URL:** `https://project-hypatia-pro-1064319572465.us-west1.run.app`
- **Status:** ✅ Operational (0 JS errors, loads clean)
- **Version:** V3.01
- **Known issues:** Missing all 6 security headers — fix added May 7, never deployed

### PM Accelerator (HMAP Accelerator)
- **URL:** `https://project-management-accelerator-845075991286.us-west1.run.app`
- **Status:** ✅ Operational (0 JS errors)
- **Version:** V2.5.0 (UX improvements coded May 11, not yet deployed)
- **Known issues:** Missing security headers, Express x-powered-by leak

### VibraEngineer
- **URL:** `https://vibraengineer-845075991286.us-west1.run.app`
- **Status:** ✅ Operational (0 JS errors)
- **Version:** V4.03
- **Known issues:** Missing security headers, CORS wildcard, CDN Tailwind (not production build)

### MIFECO.com
- **URL:** `https://mifeco.com`
- **Status:** ✅ Operational — full marketing site on DreamHost (WordPress)
- **Security headers:** ✅ All 6 present

---

## 2. Books Pipeline — 20 Books Total

### No Blue Sky Series (5 books) — Complete Manuscripts

| # | Title | Words | Formats Available | Missing |
|---|-------|-------|-------------------|---------|
| 1 | **Built from Dust** | ~33K | manuscript.md, PDF, HTML, **NEW: KDP package (May 12)** | Needs KDP submission |
| 2 | **The Oxygen Gamble** | ~92K | PDF, EPUB | KDP package |
| 3 | **Rivers Under Mars** | ~36K | PDF, EPUB | KDP package |
| 4 | **The Red Charter** | ~23K | PDF, EPUB | KDP package |
| 5 | **The First Martian Nation** | ~23K | PDF, EPUB | KDP package |

### Moon Base Series (3 books)
| Title | Formats | KDP Package? |
|-------|---------|-------------|
| The Moon Beginning | PDF, EPUB, HTML | ❌ |
| Mooncoming | PDF, EPUB, HTML | ❌ |
| Waters End | PDF, EPUB, HTML | ❌ |

### Other Books (12 remaining)
- **The Unwritten Future (Tomorrow_Remembered, Tomorrow_is_Still_Open):** ✅ Complete with KDP packages (2 books)
- **MIFECO AI Playbook (AI_That_Works_for_Small_Business):** ✅ Complete with KDP package
- **First Generation (legacy):** Review-only PDF in main dir, full manuscript in archive
- **Second Generation, Third Generation:** PDF+EPUB, no KDP package (various splits)

### Status: ⚠️ 15% KDP-ready (3 of 20 have complete KDP packages)
- Book 1 KDP package created May 12 — moving to 20% complete
- 17 books still need KDP publishing packages

---

## 3. Consulting Pipeline

### Location: `/home/bob/book-business/consulting/`
- **Status:** ⚠️ Documentation-only stage
- Has: Pipeline documentation, survey templates (no DATA directory)
- No: Active engagements, leads, follow-up records, survey responses
- **#1 Blocker:** No email sending service configured

---

## 4. System Health

### Agents Status
| Agent | Status | Notes |
|-------|--------|-------|
| `brand-advocate` | 🔴 OFFLINE (ghosting) | Since Apr 30 — no further assignments |
| `engineer` | ⚠️ Weak ghosting | Since May 1 — tasks executed by CEO |
| `security` | ⚠️ Weak ghosting | Since May 4 — tasks executed by CEO |
| `publisher` | ✅ Active | KDP package created today |
| `sales` | ⚠️ Inactive | No tasks assigned recently |
| `writer` | ⚠️ Inactive | No workspace-writer directory found |

### Infrastructure
- 9 cron jobs all active and running
- 210 skills available
- All script permissions ✅
- delivery-queue: empty (expected — cron jobs use direct Telegram delivery)
- SOUL.md: not found (needs initialization)

---

## 5. Market Intelligence (May 12, 2026)

- **MS Project Online retirement:** Sep 30, 2026 (~4.5 months) — migration window tightening
- **Agentic AI PM** is the dominant trend — no single winner yet
- **New entrants:** Kodokyo, Jovis, Onplana, Velox, Lilli, Praxis
- **Book publishing:** AI-assisted content flooding ("slush tsunami"), discovery crisis, audiobook boom