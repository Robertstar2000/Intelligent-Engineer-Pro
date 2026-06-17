import json, datetime

path = '/home/bob/.hermes/.openclaw/workspace/memory/agent-communications.jsonl'
now = datetime.datetime.utcnow()
today_str = now.strftime('%Y-%m-%dT%H:%M:%SZ')
today_date = now.strftime('%Y%m%d')

with open(path) as f:
    lines = [l.strip() for l in f if l.strip()]

# Parse all entries
entries = []
for i, line in enumerate(lines):
    try:
        entries.append(json.loads(line))
    except json.JSONDecodeError:
        print(f"WARNING: Invalid JSON at line {i+1}")

# STEP 4: Mark stale pending entries (>7 days) as failed
stale_count = 0
for entry in entries:
    if entry.get('status') == 'pending':
        ts_str = entry.get('timestamp', '')
        try:
            ts = datetime.datetime.fromisoformat(ts_str.replace('Z', '+00:00'))
            age_days = (now - ts.replace(tzinfo=None)).days
            if age_days > 7:
                entry['status'] = 'failed'
                entry['payload'] = entry.get('payload', {})
                entry['payload']['reason'] = 'Expired — no agent claimed this task within 7 days'
                entry['payload']['expired_at'] = today_str
                stale_count += 1
                print(f"EXPIRED: {entry.get('task_id')} (age={age_days}d)")
        except:
            pass

print(f"\nMarked {stale_count} stale entries as failed")

# STEP 2: Write new tasks for Tuesday (Books Pipeline & Writing focus)
# Since all 20 books are KDP-complete, focus on content marketing + consulting activation
new_tasks = [
    {
        "timestamp": today_str,
        "task_id": f"ceo-consultant-{today_date}-001",
        "from": "ceo",
        "to": "consultant",
        "type": "request",
        "priority": "high",
        "task": "TUESDAY: Consulting pipeline activation — Update pipeline tracker from 10 to 15 leads + create follow-up drafts for 5 new leads",
        "payload": {
            "instructions": "1. Update ~/book-business/consulting/DATA/conversions/pipeline-tracker-2026-05.json to include all 15 leads (5 new leads added June 10: Knowunity, Simbie AI, Gizmo, Nexus Clinical, Subject). 2. Create follow-up email drafts for the 5 new leads in ~/book-business/consulting/DATA/followups/. 3. All drafts must be marked 'DO NOT SEND — No email infrastructure configured'. 4. Prioritize Simbie AI (score 8) and Nexus Clinical (score 7) for first follow-up drafts.",
            "deadline": "2026-06-18T08:00:00Z",
            "pipeline": "consult-sales"
        },
        "status": "pending"
    },
    {
        "timestamp": today_str,
        "task_id": f"ceo-brand-advocate-{today_date}-001",
        "from": "ceo",
        "to": "brand-advocate",
        "type": "request",
        "priority": "normal",
        "task": "TUESDAY: Content marketing — Create social media campaign for MIFECO 20-book catalog",
        "payload": {
            "instructions": "1. Create a content calendar for promoting the 20-book catalog across social channels. 2. Focus on series highlights: No Blue Sky (sci-fi), Lunar Foundation (sci-fi), Age of Lightships (sci-fi), Business Series (AI/tech), Cindy Lou Legal Capers (legal thriller). 3. Draft 5 social post templates (Twitter/LinkedIn) that can be reused. 4. Include QR code references from ~/books/_SHARED_QR/. 5. All content should drive to mifeco.com bookstore section.",
            "deadline": "2026-06-20T08:00:00Z",
            "pipeline": "promo-gen"
        },
        "status": "pending"
    },
    {
        "timestamp": today_str,
        "task_id": f"ceo-researcher-{today_date}-001",
        "from": "ceo",
        "to": "researcher",
        "type": "request",
        "priority": "normal",
        "task": "TUESDAY: Market research — KDP retailer optimization for 20-book catalog",
        "payload": {
            "instructions": "1. Research current KDP best practices for pricing sci-fi series (No Blue Sky, Lunar Foundation, Age of Lightships). 2. Research keyword optimization for AI/tech nonfiction (Business Series) and legal thriller (Cindy Lou). 3. Identify top 3 discoverability opportunities across the catalog. 4. Deliver findings as structured report at ~/book-business/research/kdp-optimization-2026-06.md",
            "deadline": "2026-06-19T08:00:00Z",
            "pipeline": "book-pub"
        },
        "status": "pending"
    },
    {
        "timestamp": today_str,
        "task_id": f"ceo-system-{today_date}-001",
        "from": "ceo",
        "to": "system",
        "type": "status",
        "priority": "normal",
        "task": "TUESDAY CEO Briefing — Business state assessment complete",
        "payload": {
            "saas_status": "All 4 apps operational",
            "books_status": "20/20 KDP-ready, pipeline complete",
            "consulting_status": "15 leads, 0 contacted, no email infra",
            "agent_status": "All OFFLINE except writer (active, no work needed)",
            "stale_tasks_cleaned": stale_count,
            "new_tasks_assigned": 4
        },
        "status": "completed"
    }
]

# Append new tasks
entries.extend(new_tasks)

# Write back
with open(path, 'w') as f:
    for entry in entries:
        f.write(json.dumps(entry) + '\n')

print(f"Written {len(new_tasks)} new tasks")
print(f"Total entries: {len(entries)}")

# Validate
valid = 0
for i, entry in enumerate(entries):
    if isinstance(entry, dict) and 'task_id' in entry:
        valid += 1
    else:
        print(f"WARNING: Entry {i+1} invalid")

print(f"Validation: {valid}/{len(entries)} entries valid")
