#!/usr/bin/env python3
"""enrichment-engine.py — Lead Enrichment Engine for Pipeline Data"""

import json, re, sys, time
from collections import Counter
from datetime import datetime, timezone, timedelta
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
DATA_DIR = SCRIPT_DIR
STALE_DAYS = 7
SIGNALS_REPORT_FILE = DATA_DIR / "signals-report.json"
SEARCH_DELAY = 1.5

SIGNAL_PATTERNS = {
    "key_player_changed": {
        "keywords": [
            r"\b(?:new\s+)?(?:CEO|CTO|CFO|COO|VP|Chief\s+(?:Executive|Technology|Financial|Operating|Marketing|Product))\s+(?:appointed|hired|joins?|leaves?|departs?|resigns?|steps?\s+down|named|promoted)\b",
            r"\b(?:appointed|hired|named|promoted)\s+(?:as\s+)?(?:new\s+)?(?:CEO|CTO|CFO|COO|VP|Chief\s+(?:Executive|Technology|Financial|Operating|Marketing|Product))\b",
            r"\b(?:leadership|executive|C-suite|management)\s+(?:change|shake.?up|reorg|restructure|transition)\b",
        ],
        "weight": 3,
    },
    "cyber_breach": {
        "keywords": [
            r"\b(?:data\s+)?breach\b",
            r"\b(?:cyber|security|ransomware|hack|malware|phishing)\s+(?:attack|incident|breach|violation|intrusion)\b",
            r"\b(?:data\s+)?leak\b",
            r"\b(?:[Ii]nformation\s+)?[Ss]ecurity\s+incident\b",
            r"\b(?:PII|personally\s+identifiable\s+information)\s+(?:exposed|compromised|stolen)\b",
        ],
        "weight": 4,
    },
    "funding_round": {
        "keywords": [
            r"\b(?:raised|secured|closed|announced)\s+(?:a\s+)?\$[\d,.kmb]+\s+(?:in\s+)?(?:funding|financing|capital|investment|round|Series\s+[A-Z])\b",
            r"\b(?:funding|investment)\s+(?:round|raise)\s+of\s+\$[\d,.kmb]+\b",
            r"\b(?:Series\s+[A-Z]|Seed|Pre.?Seed|IPO|venture\s+capital)\s+(?:round|funding|raise)\b",
            r"\b(?:investor|VC|venture\s+firm)\s+(?:backs|invests|leads|participates)\b",
        ],
        "weight": 3,
    },
    "growth_downsizing": {
        "keywords": [
            r"\b(?:hiring\s+(?:spree|boom|surge|push|initiative|hundreds|thousands))\b",
            r"\b(?:expanding|expansion|growth|new\s+offices?)\s+(?:team|workforce|hiring|staff)\b",
            r"\b(?:plans?\s+to\s+)?(?:hire|add|recruit)\s+[\d,]+\s+(?:new\s+)?(?:employees?|staff|workers|people|roles?)\b",
            r"\b(?:lay(?:ing)?\s*off|laid\s+off|furlough|reduction\s+in\s+force|RIF|downsiz(?:ing|e))\b",
            r"\b(?:cut|slash|eliminate|reduce)\s+(?:jobs?|positions?|workforce|staff|headcount)\b",
            r"\b(?:restructur(?:ing|e)|reorg|right.?siz(?:ing|e))\s+(?:plan|announce|affect|cut)\b",
        ],
        "weight": 3,
    },
    "product_launch": {
        "keywords": [
            r"\b(?:launch(?:es|ed|ing)?|unveil(?:s|ed|ing)?|introduc(?:es|ed|ing)?|releas(?:es|ed|ing)?|debut(?:s|ed|ing)?)\s+(?:new\s+)?(?:product|platform|service|solution|app|feature|tool|version)\b",
            r"\b(?:new\s+)?(?:product|platform|service|solution|app|feature|tool|version)\s+(?:launch|unveil|release|debut|announce)\b",
            r"\b(?:beta|GA|general\s+availability|private\s+preview|public\s+launch)\s+(?:of|for|launch)\b",
        ],
        "weight": 2,
    },
}


def score_verification(lead: dict) -> int:
    score = 0
    enriched = lead.get("enriched", {}) or {}
    notes = lead.get("notes", "") or ""
    if enriched.get("website") or "website" in notes.lower():
        score += 3
    if enriched.get("location") or re.search(r"\b(?:city|state|country|address|location)", notes, re.I):
        score += 2
    if enriched.get("leadership") or re.search(r"\b(?:CEO|CTO|CFO|founder|president)", notes, re.I):
        score += 2
    if enriched.get("recent_news") or re.search(r"\b(?:news|announce|report)", notes, re.I):
        score += 2
    if enriched.get("signals") and len(enriched.get("signals", [])) > 0:
        score += 1
    return min(score, 10)


def score_contact(lead: dict) -> int:
    score = 0
    contact = lead.get("contact", {}) or {}
    enriched = lead.get("enriched", {}) or {}
    email = contact.get("email") or enriched.get("email") or ""
    phone = contact.get("phone") or enriched.get("phone") or ""
    if email:
        score += 5
    if phone:
        score += 3
    linkedin = enriched.get("linkedin") or contact.get("linkedin") or ""
    if linkedin:
        score += 2
    return min(score, 10)


def score_fit(lead: dict) -> int:
    score = 5
    enriched = lead.get("enriched", {}) or {}
    signals = enriched.get("signals", []) or []
    for s in signals:
        st = s.get("signal_type", "")
        if st in ("funding_round", "product_launch"):
            score += 2
        elif st == "growth_downsizing":
            if any(w in s.get("evidence", "").lower() for w in ("hire", "expand", "grow", "new office")):
                score += 2
            else:
                score -= 1
        elif st == "key_player_changed":
            if any(w in s.get("evidence", "").lower() for w in ("join", "appoint", "promote", "named")):
                score += 1
            else:
                score -= 1
        elif st == "cyber_breach":
            score -= 2
    if enriched.get("website"):
        score += 1
    if enriched.get("leadership"):
        score += 1
    if enriched.get("location"):
        score += 1
    return max(0, min(score, 10))


def compute_scores(lead: dict) -> dict:
    v = score_verification(lead)
    c = score_contact(lead)
    f = score_fit(lead)
    return {"verification_score": v, "contact_availability": c, "fit_score": f, "total_score": v + c + f}


def search_company(name: str) -> dict:
    res = {"website": "", "location": "", "leadership": "", "recent_news": [], "search_summary": ""}
    if not name:
        return res
    try:
        from duckduckgo_search import DDGS
    except ImportError:
        print("[WARN] duckduckgo_search not installed. pip install duckduckgo_search")
        return res
    all_texts, ddgs = [], DDGS()
    for q in [f"{name} company overview", f"{name} news", f"{name} CEO leadership team"]:
        try:
            results = list(ddgs.text(q, max_results=5))
            bodies = [r.get("body", "") for r in results if r.get("body")]
            all_texts.extend(bodies)
            if "news" in q:
                res["recent_news"] = bodies[:3]
            time.sleep(SEARCH_DELAY)
        except Exception as e:
            print(f"  [WARN] Search '{q}' failed: {e}")
    combined = " ".join(all_texts)

    # Extract website
    urls = re.findall(r"https?://(?:www\.)?([a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+)(?:[/\s\"'<>,;)\]|$)", combined)
    skip = {"google.com","bing.com","duckduckgo.com","yahoo.com","youtube.com","linkedin.com","facebook.com","twitter.com","x.com","crunchbase.com","bloomberg.com"}
    real = [u for u in urls if u not in skip]
    if real:
        mc = Counter(real).most_common(1)[0][0]
        if mc.count(".") >= 1:
            res["website"] = f"https://{mc}"

    # Extract location
    for pat in [r"\b(?:based in|headquartered in|located in|offices? in)\s+([A-Z][a-zA-Z]+(?:,\s*[A-Z]{2})?(?:,\s*[A-Za-z]+)?)",
                r"\b([A-Z][a-zA-Z]+(?:,\s*[A-Z]{2}))\s+(?:area|metro|region)"]:
        m = re.search(pat, combined)
        if m: res["location"] = m.group(1).strip(); break

    # Extract leadership
    leaders = []
    for pat in [r"(?:CEO|CTO|CFO|COO|President|Founder|Chief\s+\w+)\s*[:\-–]\s*([A-Z][a-zA-Z]+\s+[A-Z][a-zA-Z]+)",
                r"([A-Z][a-zA-Z]+\s+[A-Z][a-zA-Z]+)\s*,\s*(?:CEO|CTO|CFO|COO|President|Founder|Chief\s+\w+)"]:
        for m in re.finditer(pat, combined):
            leaders.append(m.group(0))
    if leaders:
        res["leadership"] = "; ".join(leaders[:3])
    res["search_summary"] = combined[:500]
    try: ddgs.close()
    except: pass
    return res


def detect_signals(text: str) -> list:
    signals = []
    if not text:
        return signals
    tl = text.lower()
    for st, cfg in SIGNAL_PATTERNS.items():
        for pat in cfg["keywords"]:
            m = re.search(pat, tl, re.I)
            if m:
                ev = m.group(0)[:200]
                if not any(s["signal_type"] == st for s in signals):
                    signals.append({"signal_type": st, "evidence": ev, "detected_at": datetime.now(timezone.utc).isoformat(), "weight": cfg["weight"]})
                break
    return signals


def find_pipeline_files(flt=None):
    pat = f"pipeline-{flt}.json" if flt else "pipeline-*.json"
    return sorted(DATA_DIR.glob(pat))


def needs_enrichment(lead: dict) -> bool:
    c = lead.get("contact", {}) or {}
    if not c.get("email") and not c.get("phone"):
        return True
    ea = lead.get("enriched_at")
    if ea:
        try:
            if datetime.now(timezone.utc) - datetime.fromisoformat(ea) < timedelta(days=STALE_DAYS):
                return False
        except: pass
    return True


def enrich_lead(lead: dict, cname: str = None) -> dict:
    cname = cname or lead.get("company", lead.get("name", ""))
    print(f"  Enriching: {cname}...")
    r = search_company(cname)
    ct = r["search_summary"] + " " + " ".join(r["recent_news"])
    signals = detect_signals(ct)
    enriched = lead.get("enriched", {}) or {}
    enriched["website"] = r.get("website") or enriched.get("website", "")
    enriched["location"] = r.get("location") or enriched.get("location", "")
    enriched["leadership"] = r.get("leadership") or enriched.get("leadership", "")
    enriched["recent_news"] = r.get("recent_news") or enriched.get("recent_news", [])
    enriched["signals"] = signals
    enriched["last_researched"] = datetime.now(timezone.utc).isoformat()
    lead["enriched"] = enriched
    lead["enriched_at"] = datetime.now(timezone.utc).isoformat()
    scores = compute_scores(lead)
    lead["scores"] = scores
    nows = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    notes = lead.get("notes", "") or ""
    notes += f"\n[Enrichment {nows}]\n  Website: {r.get('website','N/A')}\n  Location: {r.get('location','N/A')}\n  Leadership: {r.get('leadership','N/A')}\n  Signals: {len(signals)}\n  Scores: V={scores['verification_score']} C={scores['contact_availability']} F={scores['fit_score']} Total={scores['total_score']}/30"
    lead["notes"] = notes.strip()
    print(f"    -> Signals: {[s['signal_type'] for s in signals]}")
    print(f"    -> Scores: V={scores['verification_score']} C={scores['contact_availability']} F={scores['fit_score']} Total={scores['total_score']}/30")
    return lead


def update_signals_report(all_leads):
    report = {"generated_at": datetime.now(timezone.utc).isoformat(), "total_leads_scored": 0, "total_signals_detected": 0, "signal_breakdown": {}, "top_signals": [], "leads_with_signals": []}
    for lead in all_leads:
        enriched = lead.get("enriched", {}) or {}
        signals = enriched.get("signals", []) or []
        scores = lead.get("scores", {})
        if not signals and not scores:
            continue
        report["total_leads_scored"] += 1
        ln = lead.get("company", lead.get("name", "Unknown"))
        if signals:
            report["total_signals_detected"] += len(signals)
            report["leads_with_signals"].append({"company": ln, "signals": signals, "scores": scores})
            for s in signals:
                st = s["signal_type"]
                if st not in report["signal_breakdown"]:
                    report["signal_breakdown"][st] = {"count": 0, "weight": s["weight"]}
                report["signal_breakdown"][st]["count"] += 1
    bd = report["signal_breakdown"]
    report["top_signals"] = sorted([{"type": k, "count": v["count"], "weight": v["weight"], "score": v["count"] * v["weight"]} for k, v in bd.items()], key=lambda x: x["score"], reverse=True)
    try:
        with open(SIGNALS_REPORT_FILE, "w") as f:
            json.dump(report, f, indent=2)
        print(f"\n  Signals report saved to: {SIGNALS_REPORT_FILE}")
    except IOError as e:
        print(f"  [ERROR] Could not write signals report: {e}")


def print_report():
    files = find_pipeline_files()
    if not files:
        print("No pipeline-*.json files found.")
        return
    total = stale = complete = 0
    for fp in files:
        try:
            with open(fp) as f:
                data = json.load(f)
        except: continue
        leads = data if isinstance(data, list) else (data.get("leads", data.get("entries", [data])) if isinstance(data, dict) else [])
        if isinstance(leads, dict): leads = [leads]
        ps = sum(1 for l in leads if needs_enrichment(l))
        pc = len(leads) - ps
        total += len(leads); stale += ps; complete += pc
        print(f"  {fp.name}: {len(leads)} leads ({ps} stale, {pc} current)")
    print(f"\n  Total: {total} leads across {len(files)} pipeline(s)")
    print(f"  Need enrichment: {stale}")
    print(f"  Up-to-date: {complete}")


def main():
    args = sys.argv[1:]
    ro = "--report" in args
    pf = None
    if "--pipeline" in args:
        i = args.index("--pipeline")
        if i + 1 < len(args) and not args[i + 1].startswith("--"):
            pf = args[i + 1]
    if ro:
        print("\n=== Pipeline Enrichment Status Report ===\n"); print_report(); return
    files = find_pipeline_files(pf)
    if not files:
        p = f"pipeline-{pf}.json" if pf else "pipeline-*.json"
        print(f"No files matching '{p}' found in {DATA_DIR}"); sys.exit(1)
    print(f"\n=== Enrichment Engine ===")
    print(f"Data directory: {DATA_DIR}")
    print(f"Pipeline filter: {pf or 'all'}")
    print(f"Files found: {[f.name for f in files]}\n")
    all_leads = []
    for fp in files:
        print(f"Processing: {fp.name}")
        try:
            with open(fp) as f:
                data = json.load(f)
        except: continue
        is_list, is_dict = isinstance(data, list), isinstance(data, dict)
        leads = data if is_list else (data.get("leads", data.get("entries", [])) if is_dict else [])
        if isinstance(leads, dict): leads = [leads]
        updated = False
        for i, l in enumerate(leads):
            if needs_enrichment(l):
                leads[i] = enrich_lead(l, l.get("company", l.get("name", f"Lead {i}")))
                updated = True
            else:
                print(f"  Skipping (current): {l.get('company', l.get('name', f'Lead {i}'))}")
        if updated:
            out = leads if is_list else (data if is_dict else leads)
            if is_dict and "leads" in data: data["leads"] = leads; out = data
            elif is_dict and "entries" in data: data["entries"] = leads; out = data
            with open(fp, "w") as f: json.dump(out, f, indent=2)
            print(f"  -> Updated {fp.name}")
        all_leads.extend(leads if isinstance(leads, list) else [leads])
    if all_leads: update_signals_report(all_leads)
    print("\nDone.")

if __name__ == "__main__":
    main()
