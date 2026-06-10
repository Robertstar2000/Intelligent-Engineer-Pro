## 5 Product Pipelines (rebuilt 2026-06-09)
1. Books Creation (8 stages): Review Market → Bible → Framework → Write → Enrich → Edit → KDP Prep → Finish
2. Books Marketing (8 stages): Content → Infographic → Discovery → Promote → Outreach → Nurture → Analyze → Optimize
3. SaaS (8 stages): Identified → Contacted → Qualified → Process → Demo/Trial → Transaction → Followup → Upsell. Product HMAP Project Accelerator replaced PM Accelerator.
4. Human Consulting (8 stages): Lead → Contact → Qualified → Intent → Strategy Session → Proposal → Negotiation → Closed Won
5. Virtual Consulting (8 stages): Lead → Contacted → Survey → Research → Generate Reports → Quality Review → Delivery → Complete. **CORRECTED: reports are SINGLE PDFs NOT KDP packages.** Each PDF: integrated cover + cover letter + TOC + 30+ page report from survey+LLM+web search. SKILL.md v4.0.0.

**User site content preferences (2026-06-09):**
- Specific book titles listed, not generic series references
- "Ai" caps used in: Ai Assessment, Ai generated strategic roadmap, Ai Solutions
- Money-back guarantee emphasized on Virtual Consulting card
- Human Expert Consulting is separate card with "Request a Quote" (no price)
- Don't change CSS/formatting when replacing text
- Blog link in main navigation
- Source code at /mnt/usb_4tb/project-dirs/mifeco_web/mifeco-website/
§
DreamHost backup saved to /mnt/usb_4tb/Mifeco_Web_Backup/ (~332 MB, 17,287 files). Backup script at scripts/backup_dreamhost.py uses pexpect to pass SSH password from .env to rsync.
§
Project-management-accelerator repo remote updated to production version: project-management-accelerator--production-version on GitHub. Local repo reset to production HEAD (full React/TS app with AWS Lambda, server, auth, Stripe).
§
Pipeline management skill created: mifeco-pipeline-management (devops class). Covers JSON data files, SVG flow diagrams, kanban DB seeding, dashboard rendering, DreamHost sync with cleanup. Key pattern: rsync is additive, must run cleanup_dreamhost.py after removing files locally. Kanban DB at ~/.hermes/kanban.db with tenant=pipeline, stage=1-8 columns.
§
22 MIFECO book titles: No Blue Sky (5), Lunar Foundation (4), Tomorrow Remembered, AI That Works for Small Business, Age of Lightships (4), Cindy Lou (3), Owner's Manual for AI Agents, Crisis Ready Company = 20. Need to identify the remaining 2 titles.