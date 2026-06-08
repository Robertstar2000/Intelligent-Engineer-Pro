---
name: "book-marketing-launch"
title: "Book Marketing Launch — Low/No-Cost Campaign"
description: "Deploy a low/no-cost book marketing launch for any finished book. Covers strategy per book type (business/how-to vs memoir/history), Substack series creation, book-club kit generation, Facebook group outreach, 30-day launch calendar, and a complete book-launch-system folder."
category: "publishing"
triggers: ["market this book", "promote the book", "no cost marketing", "low cost advertising", "book launch campaign", "marketing strategy"]
---

## 🔍 MemPalace Query (MANDATORY FIRST STEP)
Before proceeding, query MemPalace for existing context:
```python
import sys, os; sys.path.insert(0, os.path.expanduser('~/.hermes/mempalace'))
import embed; embed.init_embedding(os.path.expanduser('~/.hermes/mempalace'))
results = embed.search_embeddings("book marketing launch campaign Substack book-club Facebook outreach", k=5)
```
This retrieves previous decisions, domain-specific context, and lessons learned from the vector memory store.

# Book Marketing Launch Campaign

Low/no-cost book marketing strategy and deployment system for self-published Kindle books.

## Per-Book Marketing Strategy

### For Business/How-To Books (e.g., "AI That Works for Small Business")

**Core Strategy:** LinkedIn authority content + free Kindle promotion + small-business community outreach.

**Don't advertise the book first.** Teach one useful lesson per day:
- Share one small-business problem
- Present one AI workflow that solves it  
- Give one example prompt
- Show one useful result
- Softly point readers to the Kindle book

**Best Channels (ranked):**
1. **A** — LinkedIn posts and comments
2. **A-** — Local business Facebook groups
3. **A-** — Email to existing contacts
4. **B+** — KDP Select free promotion
5. **B** — Podcasts and local business associations
6. **B-** — Amazon ads at $3-$5/day

**Best Message Hook:** *"Here are 25 ways a small business can save 5 hours a week with AI."*

**Target Audience:** Small business owners, entrepreneurs, solopreneurs, operations managers.

### For Memoir/History/Psychology Books (e.g., "Tomorrow Is Still Open")

**Core Strategy:** Story excerpts + book-club positioning + Substack/LinkedIn/Facebook community distribution.

**Main Hook:** *"One life. Seventy years of history. Seventy years of possible future. What changed? What did not? What do humans keep repeating?"*

**Best Campaign:** Run a "14 Stories Across 140 Years" campaign (14-day).

**Best Channels (ranked):**
1. **A** — Substack (best for serialized memoir)
2. **A** — Book clubs (discussion-rich content)
3. **A-** — Facebook groups (nostalgia, history, futurism)
4. **B+** — LinkedIn (thought-leadership angles)
5. **B** — Goodreads
6. **B-** — Amazon free/discount promotion

**Best Positioning:** *"A personal journey through memory, history, psychology, and the future."*

**Best Lead Magnet:** *"70 Years Back / 70 Years Forward: Book Club Questions"* — free download.

## Deployment System

Create a `book-launch-system/` folder with this structure:

```
book-launch-system/
├── book-info.md           ← title, subtitle, author, Amazon link, description, author bio, 3 excerpts
├── audience-map.md        ← who buys this book, where they hang out, what they care about
├── content-pillars.md     ← 5-7 content themes for posts
├── substack/              ← serialized excerpt series
├── book-clubs/            ← discussion guide, flyer, outreach
├── facebook-groups/       ← group-specific post drafts
└── tracking/              ← launch metrics
```

### Substack Deployment

Create a 7-part series (title varies per book):

For memoir books: **"70 Years Back / 70 Years Forward"**

Suggested issues:
1. The Question That Started the Book
2. What Memory Keeps and History Forgets
3. The Psychology of Fear Across Generations
4. Technology Changes. Human Nature Repeats.
5. What the Last 70 Years Taught Me
6. What the Next 70 Years Might Ask of Us
7. A Letter to Readers in the Future

Each issue should be 800-1500 words — excerpt from the book with original framing.

### Book-Club Deployment

Create these files:
- `discussion-guide.md` — 10-15 questions, grouped by theme
- `one-page-book-club-flyer.md` — formatted summary for distribution
- `outreach-list.csv` — Book club names, contact info, genre focus
- `outreach-email-templates.md` — Cold email + follow-up templates
- `follow-up-log.csv` — Track who was contacted and responses

The **discussion guide** should be offered as a free lead magnet on Substack and social media.

### Facebook Groups Deployment

- Create group-specific drafts (one per target group type)
- Manually post only after reading group rules
- Use value-first discussion questions, not direct links
- Include versions WITH and WITHOUT links
- Groups to target:
  - Small business owners (for business books)
  - History enthusiasts (for memoir)
  - Psychology/memory (for memoir)
  - Nostalgia/70s/80s (for memoir with generational content)
  - Futurism/sci-fi (for memoir covering future speculation)

## Marketing Infographic Generation

For each book/series, generate portrait marketing infographics with QR codes and sales copy.
See `references/marketing-infographic-generation.md` for the complete v2 spec including:
- Exact layout structure (two-column, horizontal framework icons)
- Color schemes per series, typography minimums
- Pure PIL approach (not WeasyPrint, not Gemini Image)
- Content keep-short guidelines for 1350px height
- All pitfalls learned from 9 iterations

Use `scripts/generate_series_infographics.py` as the reference generator script.

Quick pattern: run the generator script → validate with Gemini → iterate on gaps.

## 30-Day Launch Calendar

### Week 1 — Setup & Drafting
- [ ] Set up Substack profile/publication
- [ ] Draft all 7 Substack issues
- [ ] Create book-club kit (discussion guide, flyer, email templates)
- [ ] Build outreach list (20+ book clubs)
- [ ] Draft 10 Facebook group posts
- [ ] **Create marketing infographics** (4 formats per series — see Marketing Infographic Generation section)
- [ ] Create book-launch-system/ folder with all files

### Week 2 — Launch First Wave
- [ ] Publish Substack Issue 1
- [ ] Manually post 2 Facebook discussion posts
- [ ] Contact 5 libraries/book clubs via email
- [ ] Ask 5 early readers for honest reviews
- [ ] Post first LinkedIn educational content (business book) or story excerpt (memoir)

### Week 3 — Expand
- [ ] Publish Substack Issue 2
- [ ] Manually post 2 more Facebook discussion posts
- [ ] Contact 5 more groups/clubs
- [ ] Share the discussion guide publicly (free download)
- [ ] Post second LinkedIn/Facebook round

### Week 4 — Sustain & Measure
- [ ] Publish Substack Issue 3
- [ ] Post a launch reflection on all channels
- [ ] Follow up with all contacted book clubs
- [ ] Review metrics — repeat what worked
- [ ] Plan for Issues 4-7 based on engagement

## Safety Rules (Must Follow)

- **Never auto-post into Facebook Groups** — must be manual, human-approved
- **Never auto-message followers at scale** — use Message Ads or opt-in CRM/email instead
- **Never scrape people, groups, member lists, or private posts**
- **Never publish anything without user approval**
- **Hermes should automate: drafting, scheduling files, reminders, tracking, approved platform actions**
- **Hermes should NOT auto-post or spam communities**

## Agent Work Order Template

When user asks to deploy a book launch:

> "Create the full book-launch-system folder. Use the book concept below:
> - Book title: [title]
> - Amazon link: [link]
> - Description: [description]
> - Author bio: [bio]
> - 3 favorite excerpts: [excerpts]
> 
> Create all files in book-launch-system/. Show me:
> 1. The 30-day calendar
> 2. First Substack issue draft
> 3. First 3 Facebook group posts
> 
> Wait for my approval before publishing or scheduling anything."

## Related Skills & Pipeline

**Related Skills:**
- `book-deliverable-kdp` — Build KDP packages (precedes marketing)
- `book-identity-rebranding` — Rename books before marketing

**Pipeline Integration:** References this skill as the marketing layer in the publishing workflow.
