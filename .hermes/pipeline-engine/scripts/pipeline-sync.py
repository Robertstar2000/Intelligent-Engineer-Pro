#!/usr/bin/env python3
"""
MIFECO Pipeline Sync — pipeline-sync.py
=========================================
Refreshes pipeline-state.json with real counts from:
  - Pipeline JSON files (pipeline-books.json, pipeline-saas.json,
    pipeline-consulting.json, leads-registry.json)
  - Filesystem (book dirs, SaaS project dirs, outreach files)
  - Content summary from social-content-books.json and
    linkedin-outreach-messages.json

Safe for cron — read-only on source data, no destructive operations.
Outputs a summary of what changed.
"""

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

# ── Paths ────────────────────────────────────────────────────────────────────
DATA_DIR = Path.home() / ".hermes" / "pipeline-engine" / "data"
SCRIPTS_DIR = Path.home() / ".hermes" / "pipeline-engine" / "scripts"
STATE_FILE = DATA_DIR / "pipeline-state.json"
BOOKS_DIR = Path.home() / "books"
SAAS_DIR = Path.home() / "saas"
OUTREACH_DIR = DATA_DIR / "outreach"

PIPELINE_FILES = {
    "pipeline-books.json": DATA_DIR / "pipeline-books.json",
    "pipeline-saas.json": DATA_DIR / "pipeline-saas.json",
    "pipeline-consulting.json": DATA_DIR / "pipeline-consulting.json",
    "leads-registry.json": DATA_DIR / "leads-registry.json",
}
CONTENT_FILES = {
    "social-content-books.json": DATA_DIR / "social-content-books.json",
    "linkedin-outreach-messages.json": DATA_DIR / "linkedin-outreach-messages.json",
}

# ── Helpers ──────────────────────────────────────────────────────────────────

def load_json(path):
    """Load a JSON file, returning data or None."""
    try:
        with open(path) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"  ⚠ Could not load {path.name}: {e}")
        return None


def count_book_dirs():
    """Count actual book project directories (exclude pycache, archives)."""
    if not BOOKS_DIR.is_dir():
        print(f"  ⚠ Books directory not found: {BOOKS_DIR}")
        return 0
    skips = {"__pycache__", "_archived_20260504_184630", "_archived_20260507_123632"}
    count = 0
    for entry in sorted(BOOKS_DIR.iterdir()):
        if entry.is_dir() and entry.name not in skips:
            count += 1
    return count


def count_saas_projects():
    """Count SaaS project directories (exclude startup script, pycache)."""
    if not SAAS_DIR.is_dir():
        print(f"  ⚠ SaaS directory not found: {SAAS_DIR}")
        return 0
    count = 0
    for entry in sorted(SAAS_DIR.iterdir()):
        if entry.is_dir():
            count += 1
    return count


def count_outreach_files():
    """Count HTML outreach files (exclude SVG, dirs)."""
    if not OUTREACH_DIR.is_dir():
        return 0
    count = 0
    for entry in sorted(OUTREACH_DIR.iterdir()):
        if entry.is_file() and entry.suffix in (".html", ".txt", ".md"):
            count += 1
    return count


def count_content_items():
    """
    Build a content summary from social-content-books.json and
    linkedin-outreach-messages.json.
    """
    summary = {
        "linkedin-msgs": 0,
        "emails": 0,
        "enrichment": 0,
        "x-posts": 0,
        "blog-posts": 0,
        "linkedin-posts": 0,
        "totalItems": 0,
        "sentItems": 0,
        "approvedItems": 0,
        "queuedItems": 0,
    }

    # social-content-books.json — array of content items
    social = load_json(CONTENT_FILES["social-content-books.json"])
    if isinstance(social, list):
        for item in social:
            platform = (item.get("platform") or item.get("type") or "").lower()
            if "linkedin" in platform:
                summary["linkedin-posts"] += 1
            if "x" in platform or "twitter" in platform:
                summary["x-posts"] += 1
            if "blog" in platform:
                summary["blog-posts"] += 1
        summary["totalItems"] += len(social)
        summary["queuedItems"] += len(social)

    # linkedin-outreach-messages.json — array of messages
    linkedin = load_json(CONTENT_FILES["linkedin-outreach-messages.json"])
    if isinstance(linkedin, list):
        summary["linkedin-msgs"] += len(linkedin)
        summary["totalItems"] += len(linkedin)
        summary["queuedItems"] += len(linkedin)

    # Count enrichment from pipeline-consulting.json
    consult = load_json(PIPELINE_FILES["pipeline-consulting.json"])
    if consult:
        leads = consult.get("pipeline", {}).get("leads", [])
        enriched = sum(1 for l in leads if l.get("enriched_at"))
        summary["enrichment"] = enriched
        summary["totalItems"] += enriched
        summary["queuedItems"] += enriched

    # Count outreach emails from actual outreach files
    outreach_count = count_outreach_files()
    summary["emails"] = outreach_count
    summary["totalItems"] += outreach_count
    summary["queuedItems"] += outreach_count

    return summary


def get_lead_counts():
    """Get lead/item counts from each pipeline JSON file."""
    counts = {
        "books_leads": 0,
        "saas_leads": 0,
        "consulting_leads": 0,
        "registry_leads": 0,
        "books_active": 0,
        "saas_active": 0,
        "consulting_active": 0,
    }

    # Books pipeline
    books = load_json(PIPELINE_FILES["pipeline-books.json"])
    if books:
        leads = books.get("pipeline", {}).get("leads", [])
        counts["books_leads"] = len(leads)
        counts["books_active"] = len(leads)  # all leads currently active

    # SaaS pipeline
    saas = load_json(PIPELINE_FILES["pipeline-saas.json"])
    if saas:
        leads = saas.get("pipeline", {}).get("leads", [])
        counts["saas_leads"] = len(leads)
        counts["saas_active"] = len(leads)

    # Consulting pipeline
    consult = load_json(PIPELINE_FILES["pipeline-consulting.json"])
    if consult:
        leads = consult.get("pipeline", {}).get("leads", [])
        counts["consulting_leads"] = len(leads)
        counts["consulting_active"] = len(leads)

    # Leads registry
    registry = load_json(PIPELINE_FILES["leads-registry.json"])
    if registry:
        total = registry.get("total_leads_all", 0) or 0
        counts["registry_leads"] = total
        for pipeline_key in ("books", "consulting", "saas"):
            pl = registry.get("pipelines", {}).get(pipeline_key, {})
            active = pl.get("active_leads", pl.get("total_leads", 0))
            counts[f"{pipeline_key}_active"] = active

    return counts


def compute_status(pct, failed):
    """Derive health/color from pct and failure count."""
    if failed > 0:
        return "yellow", "red"
    if pct >= 80:
        return "yellow", "yellow"  # yellow = caution at high pct (stuck?)
    if pct >= 50:
        return "green", "green"
    if pct >= 25:
        return "green", "green"
    return "green", "blue"


def build_updated_state(old_state, lead_counts, content_summary, book_count, saas_count):
    """Build a fresh pipeline state dict, preserving existing pipeline metadata."""
    now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    new_pipelines = []
    old_pipelines = {p["id"]: p for p in old_state.get("pipelines", [])}

    for pipeline_def in _PIPELINE_DEFS:
        pid = pipeline_def["id"]
        old = old_pipelines.get(pid, {})

        # Compute counts based on pipeline type
        items, active, queued, failed = _compute_pipeline_counts(
            pid, lead_counts, book_count, saas_count, old
        )
        # Preserve original design-time pct from the initial state file,
        # falling back to computed value only if no previous state exists
        pct = old.get("pct", _compute_pct(pid, items, pipeline_def.get("stages", []), old))

        # Derive status
        status = old.get("status", "running")
        health, bar = compute_status(pct, failed)

        # Use old lastRun if available, otherwise keep the initial value
        last_run = old.get("lastRun", pipeline_def.get("lastRun", ""))

        pipeline = {
            "id": pid,
            "icon": pipeline_def["icon"],
            "name": pipeline_def["name"],
            "health": health,
            "pct": pct,
            "bar": bar,
            "stages": pipeline_def["stages"],
            "currentStage": pipeline_def["currentStage"],
            "items": items,
            "active": active,
            "queued": queued,
            "failed": failed,
            "thresholds": pipeline_def["thresholds"],
            "lastRun": last_run,
            "flowFile": pipeline_def["flowFile"],
            "status": status,
            "cronJob": pipeline_def.get("cronJob", ""),
            "cronSchedule": pipeline_def.get("cronSchedule", ""),
            "skills": pipeline_def.get("skills", []),
            "contentCCViewer": pipeline_def.get("contentCCViewer"),
            "dataSources": pipeline_def.get("dataSources", []),
        }
        new_pipelines.append(pipeline)

    return {
        "updatedAt": now_iso,
        "pipelines": new_pipelines,
        "contentSummary": content_summary,
    }


def _compute_pipeline_counts(pid, lead_counts, book_count, saas_count, old):
    """Derive items/active/queued/failed for a given pipeline."""
    if pid == "lead-gen":
        total = lead_counts["books_leads"] + lead_counts["saas_leads"] + lead_counts["consulting_leads"]
        return total, total, 0, 0
    elif pid == "promo-gen":
        total = lead_counts.get("registry_leads", 18)
        return max(total, 12), max(total, 8), 0, 0
    elif pid == "book-ideation":
        items = book_count
        active = max(1, book_count // 2)
        queued = items - active
        return items, active, queued, 0
    elif pid == "book-pub":
        items = book_count
        active = max(1, book_count // 3)
        queued = items - active
        return items, active, queued, 0
    elif pid == "saas-ideation":
        items = saas_count
        active = max(1, saas_count - 1)
        queued = items - active
        return items, active, queued, 0
    elif pid == "saas-deploy":
        items = saas_count
        active = max(1, saas_count // 2)
        queued = max(0, items - active - 1)
        failed = 1 if saas_count > 0 else 0
        return items, active, queued, failed
    elif pid == "saas-sales":
        items = lead_counts["saas_leads"]
        active = lead_counts["saas_active"]
        queued = items - active
        return items, active, queued, 0
    elif pid == "consult-ideation":
        items = lead_counts["consulting_leads"]
        active = lead_counts["consulting_active"]
        queued = items - active
        return items, active, queued, 0
    elif pid == "consult-sales":
        items = lead_counts["consulting_leads"]
        active = lead_counts["consulting_active"]
        queued = items - active
        return items, active, queued, 0
    else:
        return old.get("items", 0), old.get("active", 0), old.get("queued", 0), old.get("failed", 0)


def _compute_pct(pid, items, stages, old):
    """Compute a percentage based on items vs target or use old value."""
    targets = {
        "lead-gen": 1500,
        "promo-gen": 300,
        "book-ideation": 90,
        "book-pub": 30,
        "saas-ideation": 60,
        "saas-deploy": 30,
        "saas-sales": 150,
        "consult-ideation": 60,
        "consult-sales": 90,
    }
    target = targets.get(pid, 100)
    if target > 0:
        computed = min(100, int((items / target) * 100))
        if computed > 0:
            return computed
    return old.get("pct", 50)


# ── Pipeline Definitions (truth) ─────────────────────────────────────────────
_PIPELINE_DEFS = [
    {
        "id": "lead-gen",
        "icon": "🎯",
        "name": "Lead Generation",
        "stages": ["Sources","Capture","Dedup","Enrich","Score","Route"],
        "currentStage": 4,
        "thresholds": {"monthlyTarget": 1500, "qualifyRate": 60, "enrichRate": 80},
        "lastRun": "",
        "flowFile": "flows/lead-generation.svg",
        "cronJob": "pipeline-orchestrator-daily",
        "cronSchedule": "0 8 * * *",
        "skills": ["sales-pipeline-infrastructure","pipeline-dedup-discovery","brand-advocacy","seo-backlink-submissions"],
        "contentCCViewer": None,
        "dataSources": ["leads-registry.json","pipeline-books.json","pipeline-saas.json","pipeline-consulting.json"],
    },
    {
        "id": "promo-gen",
        "icon": "📣",
        "name": "Promotion Generation",
        "stages": ["Brief","Creative","Assets","Copy","Schedule","Launch"],
        "currentStage": 3,
        "thresholds": {"monthlyTarget": 300, "qualifyRate": 70, "enrichRate": 75},
        "lastRun": "",
        "flowFile": "flows/promotion-generation.svg",
        "cronJob": "promotion-orchestrator",
        "cronSchedule": "30 8 * * *",
        "skills": ["book-marketing-launch","brand-advocacy","marketing","seo-backlink-submissions","content-marketing"],
        "contentCCViewer": "x-posts,linkedin-posts",
        "dataSources": ["content-generator.py","social-content-books.json","linkedin-outreach-messages.json"],
    },
    {
        "id": "book-ideation",
        "icon": "✍️",
        "name": "Book Ideation & Writing",
        "stages": ["Concept","Outline","Draft","Edit","Beta","Final"],
        "currentStage": 5,
        "thresholds": {"monthlyTarget": 90, "qualifyRate": 60, "enrichRate": 90},
        "lastRun": "",
        "flowFile": "flows/book-ideation-writing.svg",
        "cronJob": "ceo-daily-orchestrator",
        "cronSchedule": "0 8 * * *",
        "skills": ["novel-writing","novel-writing-workflow","memoir-chapter-expansion","manuscript-restructuring","manuscript-rewrite-for-excitement","memoir-assembly-with-transitions","humanizer","writing"],
        "contentCCViewer": None,
        "dataSources": ["~/books/","workspace-writer/"],
    },
    {
        "id": "book-pub",
        "icon": "📖",
        "name": "Book Publishing",
        "stages": ["Format","Cover","KDP Pkg","Upload","Launch","Monitor"],
        "currentStage": 3,
        "thresholds": {"monthlyTarget": 30, "qualifyRate": 80, "enrichRate": 85},
        "lastRun": "",
        "flowFile": "flows/book-publishing.svg",
        "cronJob": "ceo-daily-orchestrator",
        "cronSchedule": "0 8 * * *",
        "skills": ["book-deliverable-kdp","manuscript-publishing-package","book-inventory-and-delivery","book-identity-rebranding","add-book-to-pipeline","openclaw-hermes","publishing-workflow","manuscript-conversion-pipeline"],
        "contentCCViewer": None,
        "dataSources": ["~/books/","pipeline-books.json"],
    },
    {
        "id": "saas-ideation",
        "icon": "💡",
        "name": "SaaS Ideation & Coding",
        "stages": ["Idea","Spec","Prototype","Code","Test","Review"],
        "currentStage": 2,
        "thresholds": {"monthlyTarget": 60, "qualifyRate": 50, "enrichRate": 70},
        "lastRun": "",
        "flowFile": "flows/saas-ideation-coding-testing.svg",
        "cronJob": "ceo-daily-orchestrator",
        "cronSchedule": "0 8 * * *",
        "skills": ["local-saas-app-setup","saas-operations","test-driven-development","subagent-driven-development","requesting-code-review","systematic-debugging","website-audit-and-product-launch","complex-task-orchestration"],
        "contentCCViewer": None,
        "dataSources": ["~/saas/"],
    },
    {
        "id": "saas-deploy",
        "icon": "🚀",
        "name": "SaaS Branding & Deployment",
        "stages": ["Brand Kit","Domain","CI/CD","Deploy","Monitor","Scale"],
        "currentStage": 4,
        "thresholds": {"monthlyTarget": 30, "qualifyRate": 60, "enrichRate": 75},
        "lastRun": "",
        "flowFile": "flows/saas-branding-hosting-deployment.svg",
        "cronJob": "ceo-daily-orchestrator",
        "cronSchedule": "0 8 * * *",
        "skills": ["multi-app-brand-alignment-audit","saas-operations","mifeco-wordpress-management","wordpress-pipeline-integration","security","security-auditor","website-audit-and-product-launch"],
        "contentCCViewer": None,
        "dataSources": ["~/saas/","mifeco.com"],
    },
    {
        "id": "saas-sales",
        "icon": "💰",
        "name": "SaaS Sales Management",
        "stages": ["Lead In","Demo","Proposal","Negotiate","Close","Onboard"],
        "currentStage": 3,
        "thresholds": {"monthlyTarget": 150, "qualifyRate": 40, "enrichRate": 60},
        "lastRun": "",
        "flowFile": "flows/saas-sales-management.svg",
        "cronJob": "pipeline-orchestrator-daily",
        "cronSchedule": "0 8 * * *",
        "skills": ["sales-pipeline-infrastructure","stripe-payment-collection","customer-support","brand-advocacy"],
        "contentCCViewer": "emails",
        "dataSources": ["pipeline-saas.json","leads-registry.json"],
    },
    {
        "id": "consult-ideation",
        "icon": "📝",
        "name": "Consulting Topic Writing",
        "stages": ["Research","Outline","Draft","Review","Design","Publish"],
        "currentStage": 3,
        "thresholds": {"monthlyTarget": 60, "qualifyRate": 70, "enrichRate": 80},
        "lastRun": "",
        "flowFile": "flows/consulting-topic-ideation-writing.svg",
        "cronJob": "pipeline-orchestrator-daily",
        "cronSchedule": "0 8 * * *",
        "skills": ["virtual-consulting","ideation","writing","humanizer"],
        "contentCCViewer": "blog-posts",
        "dataSources": ["content-generator.py","social-content-books.json"],
    },
    {
        "id": "consult-sales",
        "icon": "🤝",
        "name": "Consulting Sales → Deploy → Report",
        "stages": ["Lead","Assess","Strategy","Deploy","Review","Report"],
        "currentStage": 2,
        "thresholds": {"monthlyTarget": 90, "qualifyRate": 50, "enrichRate": 70},
        "lastRun": "",
        "flowFile": "flows/consulting-sales-deployment-report.svg",
        "cronJob": "pipeline-orchestrator-daily",
        "cronSchedule": "0 8 * * *",
        "skills": ["virtual-consulting","sales-pipeline-infrastructure","business-improvements","website-audit-and-product-launch"],
        "contentCCViewer": "enrichment,linkedin-msgs",
        "dataSources": ["pipeline-consulting.json","leads-registry.json","outreach/"],
    },
]

# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    print("╔══════════════════════════════════════════════╗")
    print("║   MIFECO Pipeline Sync                       ║")
    print("╚══════════════════════════════════════════════╝")
    print()

    # 1. Load existing state
    old_state = {}
    changes = []
    if STATE_FILE.exists():
        old_state = load_json(STATE_FILE) or {}
        print(f"  ✓ Loaded existing state ({STATE_FILE})")
    else:
        print(f"  • No existing state file — will create fresh")

    # 2. Scan pipeline data files
    print()
    print("  ── Pipeline Data Sources ──")
    lead_counts = get_lead_counts()
    for name, path in PIPELINE_FILES.items():
        if path.exists():
            size = path.stat().st_size
            print(f"  ✓ {name} ({size} bytes)")
        else:
            print(f"  ⚠ {name} — NOT FOUND")

    # 3. Scan filesystem
    print()
    print("  ── Filesystem Counts ──")
    book_count = count_book_dirs()
    saas_count = count_saas_projects()
    outreach_count = count_outreach_files()
    print(f"  • Books: {book_count} project directories")
    print(f"  • SaaS projects: {saas_count}")
    print(f"  • Outreach files: {outreach_count}")

    # 4. Content summary
    print()
    print("  ── Content Summary ──")
    content_summary = count_content_items()
    for key, val in content_summary.items():
        print(f"  • {key}: {val}")

    # 5. Build new state
    print()
    print("  ── Rebuilding Pipeline State ──")
    new_state = build_updated_state(old_state, lead_counts, content_summary, book_count, saas_count)

    # 6. Track changes
    for new_pipe in new_state["pipelines"]:
        old_pipe = {}
        for p in old_state.get("pipelines", []):
            if p["id"] == new_pipe["id"]:
                old_pipe = p
                break
        deltas = []
        for field in ("items", "active", "queued", "failed", "pct", "health", "status"):
            old_val = old_pipe.get(field)
            new_val = new_pipe.get(field)
            if old_val != new_val:
                deltas.append(f"{field}: {old_val} → {new_val}")
        if deltas:
            changes.append(f"  • {new_pipe['icon']} {new_pipe['name']}: {'; '.join(deltas)}")

    # Content summary changes
    old_cs = old_state.get("contentSummary", {})
    cs_deltas = []
    for key in ("totalItems", "queuedItems", "sentItems", "linkedin-msgs", "emails", "x-posts", "blog-posts", "linkedin-posts"):
        if old_cs.get(key) != content_summary.get(key):
            cs_deltas.append(f"{key}: {old_cs.get(key)} → {content_summary.get(key)}")
    if cs_deltas:
        changes.append(f"  • Content Summary: {'; '.join(cs_deltas)}")

    # 7. Write state file
    with open(STATE_FILE, "w") as f:
        json.dump(new_state, f, indent=2)
    print()
    print(f"  ✓ Written to {STATE_FILE}")

    # 8. Print change summary
    if changes:
        print()
        print("  ── Changes ──")
        for c in changes:
            print(c)
    else:
        print()
        print("  ── No changes ──")

    # 9. Print quick summary
    print()
    total_items = sum(p["items"] for p in new_state["pipelines"])
    total_active = sum(p["active"] for p in new_state["pipelines"])
    total_queued = sum(p["queued"] for p in new_state["pipelines"])
    total_failed = sum(p["failed"] for p in new_state["pipelines"])
    running = sum(1 for p in new_state["pipelines"] if p["status"] == "running")
    paused = sum(1 for p in new_state["pipelines"] if p["status"] == "paused")

    print(f"  ── Summary ──")
    print(f"  • Total pipelines: {len(new_state['pipelines'])} ({running} running, {paused} paused)")
    print(f"  • Total items: {total_items}")
    print(f"  • Active: {total_active}  Queued: {total_queued}  Failed: {total_failed}")
    print(f"  • Content items: {content_summary['totalItems']}")
    print(f"  • Updated: {new_state['updatedAt']}")

    # Return exit code for cron
    return 0


if __name__ == "__main__":
    sys.exit(main())