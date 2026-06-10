#!/usr/bin/env python3
"""Seed all MIFECO pipeline leads into the Hermes kanban DB with stage column."""
import sqlite3
from datetime import datetime

DB_PATH = '/home/bob/.hermes/kanban.db'

# All leads with explicit pipeline and stage assignments
all_tasks = [
    # === Books Creation Pipeline === (pipeline = "books-creation")
    {"id": "BC-MKT1", "title": "No Blue Sky Vol 6 — Review Market", "body": "Review market for sci-fi series. Analyze best-selling genres.", "assignee": "writer", "status": "ready", "priority": 3, "pipeline": "books-creation", "stage": 1},
    {"id": "BC-MKT2", "title": "Lunar Foundation Vol 4 — Review Market", "body": "Review market for moon base survival genre.", "assignee": "writer", "status": "ready", "priority": 2, "pipeline": "books-creation", "stage": 1},
    {"id": "BC-BIB1", "title": "No Blue Sky Vol 6 — Build Book Bible", "body": "Extract styles, plots, character descriptions. No character names.", "assignee": "writer", "status": "ready", "priority": 3, "pipeline": "books-creation", "stage": 2},
    {"id": "BC-BIB2", "title": "Lunar Foundation Vol 4 — Build Book Bible", "body": "Extract styles, plots from existing 3 volumes.", "assignee": "writer", "status": "ready", "priority": 2, "pipeline": "books-creation", "stage": 2},
    {"id": "BC-FRM1", "title": "Tomorrow Remembered — Build Framework", "body": "Create characters, chapters, chapter beats.", "assignee": "writer", "status": "ready", "priority": 2, "pipeline": "books-creation", "stage": 3},
    {"id": "BC-WRT1", "title": "No Blue Sky Vol 6 — Write Manuscript", "body": "Write full chapter contents.", "assignee": "writer", "status": "ready", "priority": 3, "pipeline": "books-creation", "stage": 4},
    {"id": "BC-WRT2", "title": "Lunar Foundation Vol 4 — Write Manuscript", "body": "Write full chapter contents.", "assignee": "writer", "status": "ready", "priority": 2, "pipeline": "books-creation", "stage": 4},
    {"id": "BC-ENR1", "title": "AI That Works — Enrich", "body": "Add front matter, TOC, back matter, B&W images.", "assignee": "writer", "status": "ready", "priority": 2, "pipeline": "books-creation", "stage": 5},
    {"id": "BC-EDT1", "title": "No Blue Sky Vol 6 — Edit", "body": "Review grammar, spelling, formatting, images.", "assignee": "writer", "status": "ready", "priority": 3, "pipeline": "books-creation", "stage": 6},
    {"id": "BC-KDP1", "title": "No Blue Sky Vol 6 — Prep for KDP", "body": "Create front cover, description, author bio, keywords.", "assignee": "writer", "status": "ready", "priority": 3, "pipeline": "books-creation", "stage": 7},
    {"id": "BC-FIN1", "title": "Tomorrow Remembered — Finish", "body": "Save to KDP_Packages/, update dashboards, hermes memory, mifeco.com/books", "assignee": "writer", "status": "ready", "priority": 2, "pipeline": "books-creation", "stage": 8},

    # === Books Marketing Pipeline === (pipeline = "books-marketing")
    {"id": "BM-CON1", "title": "No Blue Sky Series — Marketing Content", "body": "Create blurbs, social posts, email templates. Email: bigtruck444@agentmail.to", "assignee": "marketing", "status": "ready", "priority": 3, "pipeline": "books-marketing", "stage": 1},
    {"id": "BM-INF1", "title": "No Blue Sky Series — Infographic", "body": "Design visual assets and infographics.", "assignee": "marketing", "status": "ready", "priority": 2, "pipeline": "books-marketing", "stage": 2},
    {"id": "BM-DIS1", "title": "B-001 Dr. Sarah Chen — Discovery", "body": "Education lead, interested in Built from Dust for curriculum.", "assignee": "marketing", "status": "ready", "priority": 2, "pipeline": "books-marketing", "stage": 3},
    {"id": "BM-PRO1", "title": "Tomorrow Remembered — Promote", "body": "Launch promotional campaigns. Ready for promotion.", "assignee": "marketing", "status": "ready", "priority": 2, "pipeline": "books-marketing", "stage": 4},
    {"id": "BM-B001", "title": "B-001 Dr. Chen — Outreach", "body": "Direct outreach to educator. Promote curriculum adoption.", "assignee": "marketing", "status": "ready", "priority": 2, "pipeline": "books-marketing", "stage": 5},
    {"id": "BM-B002", "title": "B-002 Rev. Torres — Nurture Sequence", "body": "4-email nurture sequence over 14 days. Faith-based youth ministry.", "assignee": "marketing", "status": "ready", "priority": 2, "pipeline": "books-marketing", "stage": 6},
    {"id": "BM-B003", "title": "B-003 Marcus Webb — Outreach", "body": "Domain verification needed (thebookcellar.com FOR SALE). Indie bookstore.", "assignee": "marketing", "status": "blocked", "priority": 3, "pipeline": "books-marketing", "stage": 5},

    # === SaaS Pipeline === (pipeline = "saas")
    {"id": "S-001", "title": "Sarah Chen — TechFlow Labs", "body": "Product: Project Hypatia Pro ($99/mo). ICP: 92. Contacted.", "assignee": "sales", "status": "ready", "priority": 3, "pipeline": "saas", "stage": 2},
    {"id": "S-002", "title": "James Rodriguez — CloudStack", "body": "Product: PM Accelerator ($69/mo). ICP: 88. Needs outreach.", "assignee": "sales", "status": "ready", "priority": 2, "pipeline": "saas", "stage": 1},
    {"id": "S-003", "title": "Priya Sharma — DataSync", "body": "Product: VibraEngineer ($29/mo). ICP: 95. Highest priority.", "assignee": "sales", "status": "ready", "priority": 3, "pipeline": "saas", "stage": 1},
    {"id": "S-004", "title": "Michael Park — NexGen Automation", "body": "Product: Project Hypatia Pro ($99/mo). ICP: 85.", "assignee": "sales", "status": "ready", "priority": 2, "pipeline": "saas", "stage": 1},
    {"id": "S-005", "title": "Elena Vasquez — SwiftScale", "body": "Product: PM Accelerator ($69/mo). ICP: 90.", "assignee": "sales", "status": "ready", "priority": 2, "pipeline": "saas", "stage": 1},

    # === Human Consulting Pipeline === (pipeline = "human-consulting")
    {"id": "C-001", "title": "Phillip Berry — Northwind Health", "body": "Healthcare PBM, Indianapolis. Contacted 2026-05-14. Email: crowdedbutton536@agentmail.to", "assignee": "consultant", "status": "ready", "priority": 2, "pipeline": "human-consulting", "stage": 2},
    {"id": "C-003", "title": "Gregory Shepherd — Meridian Financial", "body": "Collections agency, Asheville NC. Confirmed real. No email.", "assignee": "consultant", "status": "ready", "priority": 2, "pipeline": "human-consulting", "stage": 1},
    {"id": "C-006", "title": "Dr. Luis Dorado — Harbor College", "body": "LA Harbor College. ~8,100 students. Email: ARHELP@LAHC.EDU.", "assignee": "consultant", "status": "ready", "priority": 2, "pipeline": "human-consulting", "stage": 1},
    {"id": "C-007", "title": "Kris Simpson — City of Crestwood", "body": "Municipal government. Confirmed real.", "assignee": "consultant", "status": "ready", "priority": 2, "pipeline": "human-consulting", "stage": 1},
    {"id": "C-009", "title": "Prairie State Manufacturing", "body": "Small manufacturer, Mattoon IL. Website needed.", "assignee": "consultant", "status": "ready", "priority": 2, "pipeline": "human-consulting", "stage": 1},
    {"id": "C-010", "title": "Kathy Andrews — Blue Ridge Environmental", "body": "BREDL, 501(c)(3). NC-based. Contact via web form.", "assignee": "consultant", "status": "ready", "priority": 2, "pipeline": "human-consulting", "stage": 1},

    # === Virtual Consulting Pipeline === (pipeline = "virtual-consulting")
    {"id": "VC-BK1", "title": "Virtual Consulting — Complete KDP Cleanup", "body": "Fix remaining book projects for KDP upload.", "assignee": "writer", "status": "ready", "priority": 2, "pipeline": "virtual-consulting", "stage": 6},
    {"id": "VC-DEL1", "title": "Virtual Consulting — Deliverables Queue", "body": "Generate 2 deliverable reports for pending clients.", "assignee": "analyst", "status": "ready", "priority": 2, "pipeline": "virtual-consulting", "stage": 6},
]

db = sqlite3.connect(DB_PATH)
cursor = db.cursor()

# Clear all existing
cursor.execute("DELETE FROM tasks")

now = int(datetime.now().timestamp())

for t in all_tasks:
    cursor.execute("""
        INSERT INTO tasks (id, title, body, assignee, status, priority, created_by, created_at, tenant, stage)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (t["id"], t["title"], t["body"], t["assignee"], t["status"], t["priority"], "pipeline-seeder", now, t["pipeline"], t["stage"]))

db.commit()

cursor.execute("SELECT COUNT(*) FROM tasks")
count = cursor.fetchone()[0]
print(f"Seeded {count} tasks")

cursor.execute("SELECT tenant, COUNT(*) FROM tasks GROUP BY tenant ORDER BY tenant")
for row in cursor.fetchall():
    print(f"  {row[0]}: {row[1]}")

db.close()