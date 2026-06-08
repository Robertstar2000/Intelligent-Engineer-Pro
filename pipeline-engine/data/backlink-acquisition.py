#!/usr/bin/env python3
"""
MIFECO Backlink Opportunity Finder
===================================
Weekly cron job that discovers backlink opportunities for mifeco.com.
Searches for write-for-us pages, broken links, unlinked mentions, and competitor gaps.

Usage:
  python3 backlink-acquisition.py                  # Run full scan
  python3 backlink-acquisition.py --report         # Show pending opportunities
  python3 backlink-acquisition.py --opportunity N  # Mark opportunity N as actioned

Output:
  - data/backlink-opportunities.json — All found opportunities with status
"""

import json, os, re, time, sys
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(BASE, "backlink-opportunities.json")

# Domain blocklist: dictionary sites, junk, platforms — always skip
BLOCKED_DOMAINS = [
    "dictionary.com", "thesaurus.com", "merriam-webster.com",
    "dictionary.cambridge.org", "collinsdictionary.com",
    "oxfordlearnersdictionaries.com", "vocabulary.com",
    "thefreedictionary.com", "onlinenotepad.org",
    "write.as", "justwrite.page", "deepl.com",
    "sermoncentral.com", "timeanddate.com",
    "cuemath.com", "rd.com", "24timezones.com",
    "avibirds.com", "safarisafricana.com",
    "journals.biologists.com", "birdzilla.com",
    "news.google.com", "facebook.com",
]

def is_blocked(url):
    """Return True if URL is on the blocklist."""
    url_lower = url.lower()
    for domain in BLOCKED_DOMAINS:
        if domain in url_lower:
            return True
    return False

def deduplicate(opps, existing_urls):
    """Remove duplicates and blocked domains from opportunity list."""
    seen = set(existing_urls)
    clean = []
    for o in opps:
        url = o.get("source", "")
        if url not in seen and not is_blocked(url):
            seen.add(url)
            clean.append(o)
    return clean

def load_opportunities():
    if os.path.exists(OUTPUT_PATH):
        with open(OUTPUT_PATH) as f:
            return json.load(f)
    return {"last_updated": None, "opportunities": []}

def save_opportunities(data):
    data["last_updated"] = datetime.now().isoformat()
    with open(OUTPUT_PATH, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Saved {len(data['opportunities'])} opportunities")

def search_write_for_us():
    """Find websites accepting guest posts in MIFECO niches.
    
    Uses specific, contextual queries instead of bare literal phrases.
    Avoids dictionary/thesaurus junk via -negative keywords.
    """
    opportunities = []
    from duckduckgo_search import DDGS
    ddgs = DDGS()
    
    queries = [
        # Guest post programs — specific + negative keywords
        '"write for us" "artificial intelligence" -dictionary -definition -meaning -thesaurus',
        '"write for us" "project management software" -dictionary -definition -meaning -thesaurus',
        '"write for us" "small business" AI -dictionary -definition -meaning',
        '"guest post" "AI tools" -dictionary -definition -meaning -thesaurus',
        '"guest post" "project management" SaaS -dictionary -definition',
        # Contribute/submit article queries
        '"submit a guest post" "technology" -dictionary -definition',
        '"contribute an article" "business consulting" -dictionary -definition',
        '"become a contributor" "startup" "AI" -dictionary -definition',
        # Specific high-value sites via site: operator
        '"write for us" "artificial intelligence" site:techcrunch.com OR site:venturebeat.com OR site:thenextweb.com',
        '"guest post" "project management" site:forbes.com OR site:entrepreneur.com OR site:inc.com',
        '"submit article" "SaaS" site:techcrunch.com OR site:producthunt.com',
        # Mars/sci-fi niche
        '"write for us" "space technology" -dictionary -definition',
        '"guest post" "Mars exploration" -dictionary -definition -bird -raptor',
        '"write for us" "science fiction" "Mars colony" -dictionary',
    ]
    
    for q in queries:
        try:
            results = list(_search_with_retry(ddgs, q, max_results=5))
            for r in results:
                url = r.get('href', '')
                title = r.get('title', '')
                if url and 'mifeco' not in url.lower():
                    opportunities.append({
                        "type": "write_for_us",
                        "source": url,
                        "title": title,
                        "snippet": r.get('body', '')[:200],
                        "status": "new",
                        "found_at": datetime.now().isoformat()
                    })
            time.sleep(1.5)
        except Exception as e:
            print(f"  Search failed for '{q}': {e}")
    
    return opportunities

def _search_with_retry(ddgs, query, max_results=5, max_retries=2):
    """Search with retry logic. On timeout with verbose query, try shorter version."""
    attempt = 0
    while attempt <= max_retries:
        try:
            results = ddgs.text(query, max_results=max_results)
            return list(results)
        except Exception as e:
            attempt += 1
            if attempt > max_retries:
                raise
            # If query is very long (multiple quoted phrases), retry with shorter version
            quote_count = query.count('"')
            if quote_count > 4:
                # Strip to first quoted phrase + key context
                import re
                m = re.search(r'"[^"]+"', query)
                if m:
                    short_q = m.group(0) + " " + " ".join(query.split()[-3:])
                    print(f"    Retrying shorter query: {short_q}")
                    return list(ddgs.text(short_q, max_results=max_results))
            time.sleep(2 ** attempt)

def search_unlinked_mentions():
    """Find mentions of MIFECO or products without links.
    
    Uses full product names (not ambiguous short forms like 'PM' or 'raptors').
    """
    opportunities = []
    from duckduckgo_search import DDGS
    ddgs = DDGS()
    
    queries = [
        # Full product names — no ambiguous abbreviations
        '"Project Hypatia Pro" review',
        '"Project Hypatia Pro" alternative',
        '"PM Accelerator" "project management"',  # PM here is part of the product name, not standalone
        '"VibraEngineer" simulation',
        '"VibraEngineer" "engineering software"',
        '"No Blue Sky" "Bob J Mills" book',
        '"MIFECO" consulting',
        '"Bob J Mills" "No Blue Sky"',
    ]
    
    for q in queries:
        try:
            results = list(_search_with_retry(ddgs, q, max_results=5))
            for r in results:
                url = r.get('href', '')
                title = r.get('title', '')
                body = r.get('body', '')
                if url and 'mifeco.com' not in url.lower() and 'mifeco' not in url.lower():
                    opportunities.append({
                        "type": "unlinked_mention",
                        "source": url,
                        "title": title,
                        "snippet": body[:300],
                        "status": "new",
                        "found_at": datetime.now().isoformat()
                    })
            time.sleep(1.5)
        except Exception as e:
            print(f"  Search failed for '{q}': {e}")
    
    return opportunities

def search_competitor_gaps():
    """Find sites linking to competitors but not MIFECO.
    
    Uses shorter, simpler queries to avoid DuckDuckGo timeouts.
    """
    opportunities = []
    from duckduckgo_search import DDGS
    ddgs = DDGS()
    
    # Shorter queries — avoid 3+ quoted phrases that caused timeout
    competitors = [
        '"ClickUp" project management review',
        '"Asana" project management alternative',
        '"Monday.com" engineering tools',
        '"Jira" project management tool',
        '"Notion" project management vs',
        'best project management software review',
        '"Trello" alternative project management',
    ]
    
    for q in competitors:
        try:
            results = list(_search_with_retry(ddgs, q, max_results=3))
            for r in results:
                url = r.get('href', '')
                if url and 'mifeco' not in url.lower():
                    opportunities.append({
                        "type": "competitor_gap",
                        "source": url,
                        "title": r.get('title', ''),
                        "snippet": r.get('body', '')[:200],
                        "competitor_query": q,
                        "status": "new",
                        "found_at": datetime.now().isoformat()
                    })
            time.sleep(1.5)
        except Exception as e:
            print(f"  Search failed for '{q}': {e}")
    
    return opportunities

def generate_report(data):
    """Print a summary report of all opportunities."""
    opps = data.get("opportunities", [])
    new = [o for o in opps if o.get("status") == "new"]
    actioned = [o for o in opps if o.get("status") == "actioned"]
    dismissed = [o for o in opps if o.get("status") == "dismissed"]
    
    print(f"\n{'='*60}")
    print(f"BACKLINK OPPORTUNITIES REPORT")
    print(f"{'='*60}")
    print(f"Total: {len(opps)} | New: {len(new)} | Actioned: {len(actioned)} | Dismissed: {len(dismissed)}\n")
    
    for t in ["write_for_us", "unlinked_mention", "competitor_gap"]:
        type_opps = [o for o in new if o["type"] == t]
        if not type_opps:
            continue
        label = t.replace("_", " ").title()
        print(f"  📝 {label} ({len(type_opps)}):")
        for o in type_opps[:5]:
            print(f"     • {o.get('title', 'No title')}")
            print(f"       {o['source']}")
        print()

    if not new:
        print("  ✅ No new opportunities found.\n")

def mark_actioned(data, index):
    """Mark an opportunity as actioned."""
    opps = data.get("opportunities", [])
    if 0 <= index < len(opps):
        opps[index]["status"] = "actioned"
        opps[index]["actioned_at"] = datetime.now().isoformat()
        print(f"Marked opportunity #{index} as actioned")
    return data

def main():
    data = load_opportunities()
    
    if "--report" in sys.argv:
        generate_report(data)
        return
    
    if "--opportunity" in sys.argv:
        idx = int(sys.argv[sys.argv.index("--opportunity") + 1])
        data = mark_actioned(data, idx)
        save_opportunities(data)
        return
    
    print("🔍 Searching for write-for-us opportunities...")
    new_opps = search_write_for_us()
    
    print("🔍 Searching for unlinked mentions...")
    new_opps += search_unlinked_mentions()
    
    print("🔍 Searching for competitor gaps...")
    new_opps += search_competitor_gaps()
    
    # Deduplicate by URL and remove blocked domains
    existing_urls = {o["source"] for o in data["opportunities"]}
    truly_new = deduplicate(new_opps, existing_urls)
    
    data["opportunities"].extend(truly_new)
    save_opportunities(data)
    
    print(f"\nFound {len(truly_new)} new opportunities (from {len(new_opps)} raw)")
    generate_report(data)

if __name__ == "__main__":
    main()
