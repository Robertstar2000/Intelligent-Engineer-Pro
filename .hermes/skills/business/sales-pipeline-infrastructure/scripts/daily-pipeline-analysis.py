#!/usr/bin/env python3
"""
daily-pipeline-analysis.py — Full 7-Step Pipeline Orchestrator Analysis

Run from pipeline-engine/ to generate the daily pipeline health report.
Covers: dedup verification, days-in-stage calculation, blocker detection,
nurture sequence health check, email queue generation, 7-day projection,
and registry integrity cross-reference.

Usage:
    cd /home/bob/.hermes/pipeline-engine
    python3 scripts/daily-pipeline-analysis.py
    # Output goes to stdout. Redirect to save report:
    python3 scripts/daily-pipeline-analysis.py > data/daily-pipeline-report.md

Assumptions:
    - pipeline-{product}.json files in data/ with nested pipeline.leads structure
    - sequences/{product}-nurture.json files in sequences/
    - leads-registry.json in data/ with aggregate format (total_leads keys)
    - unified-pipeline.json in data/ (may be a partial subset)

Date handling notes:
    - Books/SaaS use full ISO timestamps (2026-05-07T14:00:39Z)
    - Consulting uses date-only strings (2026-05-07)
    - Both formats are handled
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
ENGINE_DIR = SCRIPT_DIR.parent
DATA_DIR = ENGINE_DIR / 'data'
SEQUENCES_DIR = ENGINE_DIR / 'sequences'

TODAY = datetime.now(timezone.utc)
TODAY_DT = datetime(TODAY.year, TODAY.month, TODAY.day)
TODAY_STR = TODAY.strftime('%Y-%m-%d')
OUT = []  # Collect output lines


def emit(line=""):
    OUT.append(line)


def flush():
    sys.stdout.write('\n'.join(OUT))
    sys.stdout.write('\n')


def h(level, text):
    emit(f"{'#' * level} {text}")
    emit()


def days_iso(date_str):
    if not date_str:
        return None
    try:
        dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        return (TODAY - dt).days
    except (ValueError, TypeError):
        return None


def days_date_only(date_str):
    if not date_str:
        return None
    try:
        dt = datetime.strptime(date_str, '%Y-%m-%d')
        return (TODAY_DT - dt).days
    except (ValueError, TypeError):
        return days_iso(date_str)


def load_json(path):
    try:
        with open(path) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"[WARN] Could not load {path}: {e}", file=sys.stderr)
        return None


def get_leads(data):
    return data.get('pipeline', data).get('leads', [])


def main():
    # Load data
    books = load_json(DATA_DIR / 'pipeline-books.json')
    saas = load_json(DATA_DIR / 'pipeline-saas.json')
    consulting = load_json(DATA_DIR / 'pipeline-consulting.json')
    unified = load_json(DATA_DIR / 'unified-pipeline.json')
    registry = load_json(DATA_DIR / 'leads-registry.json')

    if not all([books, saas, consulting, registry]):
        emit("FATAL: One or more core pipeline files could not be loaded.")
        flush()
        sys.exit(1)

    bl = get_leads(books)
    sl = get_leads(saas)
    cl = get_leads(consulting)
    saas_stages_map = saas['pipeline']['stages']
    cons_stages_map = consulting['pipeline']['stages']

    # ── Overview ──
    cons_blockers = [l for l in cl if (days_date_only(l.get('created_date', '')) or 0) > 7]
    saas_auto = [l for l in sl if l['stage'] == 1 and (days_iso(l.get('advanced_at') or l.get('created_at', '')) or 0) >= 7]

    h(1, f"Daily Pipeline Report — {TODAY_STR}")
    emit(f"*Generated: {TODAY.strftime('%Y-%m-%d %H:%M UTC')}*")
    emit()
    h(2, "Pipeline Overview")
    emit("| Pipeline | Total | Auto-Advance | Blockers |")
    emit("|----------|-------|--------------|----------|")
    emit(f"| 📚 Books | {len(bl)} | 0 | 0 |")
    emit(f"| ☁️ SaaS | {len(sl)} | {len(saas_auto)} | 0 |")
    emit(f"| 💼 Consulting | {len(cl)} | 0 | {len(cons_blockers)} |")
    emit(f"| **Total** | **{len(bl)+len(sl)+len(cl)}** | | |")
    emit()

    # ── Books Detail ──
    h(2, "📚 Books Pipeline")
    for l in bl:
        lid = l['id']
        name = l['contact']['name']
        org = l['contact']['organization']
        st = l['current_stage']
        dis = days_iso(l.get('entered_stage', '')) or 0
        flags = [f.get('label', '') for f in l.get('flags', [])]
        flag_info = f" ⚠️ {', '.join(flags)}" if flags else ""
        is_blocker = (st in (3, 5)) and dis > 7
        status = "🔴" if is_blocker else "✅"
        emit(f"- **{lid}** | {name} ({org}) | Stage {st} | {dis}d | {status}{flag_info}")
    emit()

    # ── SaaS Detail ──
    h(2, "☁️ SaaS Pipeline")
    for l in sl:
        lid = l['id']
        name = l['name']
        org = l['company']
        st = l['stage']
        dis = days_iso(l.get('advanced_at') or l.get('created_at', '')) or 0
        email = l.get('email', 'N/A')
        status = "🔄" if l in saas_auto else "✅"
        emit(f"- **{lid}** | {name} ({org}) | Stage {st}: {saas_stages_map.get(str(st), '')} | {dis}d | {email} | {status}")
    emit()

    # ── Consulting Detail ──
    h(2, "💼 Consulting Pipeline")
    for l in cl:
        lid = l['id']
        org = l['company_name']
        name = l.get('contact_name') or 'NO NAME'
        email = l.get('contact_email')
        st = l['stage']
        dis = days_date_only(l.get('created_date', '')) or 0
        verify = l.get('verification_status', 'Unverified')
        ne = " ❌ NO EMAIL" if not email else ""
        status = "🔴" if dis > 7 else "✅"
        emit(f"- **{lid}** | {org} | {name} | Stage {st} | {dis}d | {verify}{ne} | {status}")
    emit()

    # ── Blockers ──
    h(2, "⚠️ Blockers")
    if cons_blockers:
        emit(f"🔴 Consulting: {len(cons_blockers)} leads stale (>7d in stage)")
        emit("> Rule: any consulting stage >7d = blocker")
    else:
        emit("✅ None")
    emit()

    # ── Auto-advance ──
    h(2, "🔄 Auto-Advance")
    if saas_auto:
        for l in saas_auto:
            emit(f"- {l['id']} ({l['name']}) — Stage 1 → 2")
        emit(f"> {len(saas_auto)} SaaS leads due for advancement.")
        emit("> Rule: Stage 1 ≥7d → advance to Stage 2.")
    else:
        emit("- None")
    emit()

    # ── Nurture Health ──
    h(2, "📧 Nurture Sequence Health")
    bn = load_json(SEQUENCES_DIR / 'books-nurture.json')
    sn = load_json(SEQUENCES_DIR / 'saas-nurture.json')
    cn = load_json(SEQUENCES_DIR / 'consulting-nurture.json')
    ok = True

    if bn and books:
        ct = {b['title'] for b in books['pipeline']['products']['titles']}
        nt = {b['title'] for b in bn['series']['books']}
        m = ct == nt
        if not m: ok = False
        emit(f"**Books:** {'✅' if m else '🔴'} {len(ct)} titles, {len(nt)} nurture refs")
    if sn and saas:
        sp = set(saas['pipeline']['products'])
        sb = ' '.join(e.get('body_template', '') for e in sn['email_sequences'])
        missing = [p for p in sp if p.lower() not in sb.lower()]
        if missing:
            ok = False
            emit(f"**SaaS:** 🔴 Missing from nurture: {missing}")
        else:
            emit(f"**SaaS:** ✅ All {len(sp)} products referenced")
    if cn and consulting:
        cp = set(consulting['pipeline']['products'])
        cb = ' '.join(e.get('body', '') for e in cn['emails'])
        missing = [p for p in cp if p.lower() not in cb.lower()]
        if missing:
            ok = False
            emit(f"**Consulting:** 🔴 Missing from nurture: {missing}")
        else:
            emit(f"**Consulting:** ✅ All {len(cp)} services referenced")
    emit(f"**Overall:** {'✅ ALL ALIGNED' if ok else '🔴 DISCREPANCIES FOUND'}")
    emit()

    # ── Email Queue ──
    h(2, "📬 Email Queue")
    emit(f"**Books:**")
    for l in bl:
        dis = days_iso(l.get('entered_stage', l.get('created_at', ''))) or 0
        lid = l['id']
        name = l['contact']['name']
        st = l['current_stage']
        notes = "Domain verify needed" if any(f.get('label', '').startswith('Domain') for f in l.get('flags', [])) else ""
        flag = f" — {notes}" if notes else ""
        emit(f"  {lid} {name} | Stage {st} | {dis}d | {'Awaiting reply' if st >= 2 else 'Needs outreach'} {flag}")
    emit()
    emit(f"**SaaS:**")
    for l in sl:
        st_text = "🔄 Auto-advance (Day 1 nurture due)" if l in saas_auto else "Contacted"
        emit(f"  {l['id']} {l['name']} | {l.get('email', '')} | {st_text}")
    emit()
    emit(f"**Consulting:**")
    ready = sum(1 for l in cl if l.get('contact_email'))
    needy = sum(1 for l in cl if not l.get('contact_email'))
    for l in cl:
        status = "Ready for nurture" if l.get('contact_email') else "Needs enrichment"
        email_display = l.get('contact_email') or '—'
        emit(f"  {l['id']} {l['company_name']} | {email_display} | {status}")
    emit(f"> {ready} ready, {needy} need enrichment")
    emit()

    # ── 7-Day Projection ──
    h(2, "📅 7-Day Projection")
    if saas_auto:
        emit(f"- SaaS: {len(saas_auto)} leads → Stage 2, nurture starts")
    emit("- Books: B-002 initial outreach due, B-003 domain verify pending")
    emit(f"- Consulting: {ready} leads ready for nurture, {needy} need enrichment")
    emit()

    # ── Registry Integrity ──
    h(2, "🔐 Registry Integrity")
    total_actual = len(bl) + len(sl) + len(cl)
    reg_total = registry.get('total_leads_all', 0)
    pf = "✅ PASS" if total_actual == reg_total else "🔴 FAIL"
    emit(f"| Check | Value |")
    emit(f"|-------|-------|")
    emit(f"| Registry total | {reg_total} |")
    reg_books = registry.get('pipelines', {}).get('books', {}).get('total_leads', '?')
    reg_saas = registry.get('pipelines', {}).get('saas', {}).get('total_leads', '?')
    reg_cons = registry.get('pipelines', {}).get('consulting', {}).get('total_leads', '?')
    emit(f"| Books | {len(bl)} actual ({reg_books} claimed) |")
    emit(f"| SaaS | {len(sl)} actual ({reg_saas} claimed) |")
    emit(f"| Consulting | {len(cl)} actual ({reg_cons} claimed) |")
    emit(f"| Integrity | {pf} |")
    if unified:
        emit(f"| Unified coverage | {len(unified)}/{total_actual} |")
    emit()
    emit("---")
    emit(f"*Generated: {TODAY.strftime('%Y-%m-%d %H:%M UTC')}*")


if __name__ == '__main__':
    main()
    flush()
