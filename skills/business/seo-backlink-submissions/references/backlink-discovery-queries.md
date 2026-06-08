# Backlink Discovery: Query Quality Notes

> Findings from automated runs of `~/.hermes/pipeline-engine/data/backlink-acquisition.py`
> Last updated: 2026-05-24

## ✅ Fixed (2026-05-24)

All issues below have been patched in `backlink-acquisition.py`:

- **Write-for-us dictionary junk**: Added 22-domain blocklist (dictionary.com, thesaurus.com, merriam-webster, etc.) + `-dictionary -definition -meaning -thesaurus` negative keywords in every query
- **Raptors → birds**: Replaced ambiguous short forms with full product names (e.g., "PM Accelerator" instead of PM, "VibraEngineer" instead of VibraEngineer); added `-bird -raptor` to Mars queries
- **PM → AM/PM time**: All queries use full phrases like `"project management software"` — no standalone PM
- **DuckDuckGo timeouts**: Added `_search_with_retry()` with exponential backoff (2s, 4s) and automatic query shortening for verbose queries
- **Duplicate entries**: `deduplicate()` helper now filters both cross-run duplicates AND same-run duplicates; blocklist applied during dedup
- **Competitor gaps**: Shortened queries from 3+ quoted phrases to 1 quoted + unquoted terms

Remaining known noise domains (in blocklist): sermoncentral.com, timeanddate.com, avibirds.com, news.google.com, facebook.com, and 18 others.
> Status: **ALL KNOWN FAILURE MODES FIXED IN SCRIPT** — see "Fixes Applied" below.

## Script Overview

- **Location:** `~/.hermes/pipeline-engine/data/backlink-acquisition.py`
- **Output:** `~/.hermes/pipeline-engine/data/backlink-opportunities.json`
- **Search backend:** DuckDuckGo (via `duckduckgo_search`/`ddgs` package)
- **Search types:** `write_for_us`, `unlinked_mention`, `competitor_gap`
- **Status tracking per opportunity:** `new`, `actioned`, `dismissed`

## Fixes Applied (2026-05-24)

All 5 failure modes from the earlier "Known Failure Modes" section are now addressed **in the script itself**:

| Failure Mode | Fix Implemented |
|---|---|
| Dictionary/thesaurus junk | 22-domain `BLOCKED_DOMAINS` list + `-dictionary -definition -meaning -thesaurus` negatives on every query |
| Ambiguous "PM" → AM/PM time | No standalone "PM" searches; all queries use `"project management"` or full product names like `"PM Accelerator"` |
| Ambiguous "raptors" → birds | Mars/sci-fi queries use `-bird -raptor` negatives and specific `"Mars exploration"` / `"Mars colony"` phrases |
| Duplicate results across phases | `deduplicate()` helper filters both existing URLs and blocklist before appending |
| DuckDuckGo timeouts on verbose queries | `_search_with_retry()` with exponential backoff; auto-shortens queries with 3+ quoted phrases |
| Generic/irrelevant domains | `BLOCKED_DOMAINS` filters sermoncentral.com, news.google.com, facebook.com, timeanddate.com, etc. |

## Historical Failure Modes (Archived — Fixed)

### 1. "Write For Us" → Dictionary Definitions

The search for literal phrases like `"write for us"` and `"guest post"` combined with industry terms returns **dictionary.com, thesaurus.com, Cambridge, Merriam-Webster** definitions of "write", "guest", "contribute", and "submit".

**Why:** The search engine finds pages containing all query words, and dictionary pages rank high because they are authoritative text-heavy sites. The terms "write", "guest", "contribute", "submit" are common English words with dictionary entries.

**Observed garbage domains:**
- merriam-webster.com
- dictionary.cambridge.org
- dictionary.com
- collinsdictionary.com
- thesaurus.com
- thefreedictionary.com
- oxfordlearnersdictionaries.com
- vocabulary.com
- onlinenotepad.org (text editor)
- write.as (blogging platform)
- justwrite.page (writing app)
- deepl.com/en/write (AI writing companion)

**Proposed fixes for the script:**
- Add `-dictionary -definition -meaning -thesaurus -vocabulary -thesaurus.com -collinsdictionary -cambridge -oxfordlearners -merriam-webster` negative keywords
- Restrict to sites that accept guest posts via domain allowlist (e.g., `site:techcrunch.com`, `site:smashingmagazine.com`)
- Use `"write for us" technology` instead of bare `"write for us"`
- Use `"guest post"` + industry + `"accepting"` to filter for active programs

### 2. "Unlinked Mentions" → Bird Articles (Raptors)

Searching for `"raptors"` linked with mentions of MIFECO's products or competitor names returns **bird of prey articles** because "raptor" is the common term for eagles, hawks, falcons, etc.

**Observed garbage domains:**
- avibirds.com
- safarisafricana.com
- journals.biologists.com
- en.wikipedia.org/wiki/Bird_of_prey
- birdzilla.com

**Proposed fixes:**
- Search `"Raptor" software` or `"Raptor" project management` instead of bare `raptors`
- Add `-bird -birdzilla -avibirds -predator -eagle -hawk -falcon -owl` negatives
- Use company/product full names instead of ambiguous short forms

### 3. "Unlinked Mentions" → AM/PM Time (PM)

Searching for `PM` (intended as Project Management) returns **AM/PM time display pages** because "PM" is the standard abbreviation for "post meridiem."

**Observed garbage domains:**
- timeanddate.com/time/am-and-pm.html
- rd.com/article/what-does-am-and-pm-stand-for
- cuemath.com/measurement/am-pm
- oxfordlearnersdictionaries.com/definition/english/p-m
- 24timezones.com/am-pm

**Proposed fixes:**
- Always use `"project management"` (quoted) instead of just `PM`
- Or use `PM software` with `-am -time -clock -meridiem -midnight -noon` negatives
- Or search for specific PM tools: `"Project Hypatia Pro"`, `"ClickUp" "project management"`

### 4. Generic/Unrelated Matches

The script also pulled in:
- **sermoncentral.com** (5 results) — religious sermon resources
- **news.google.com/swg/ui/v1/serviceiframe** — Google News iframe
- **facebook.com/video/embed** — Facebook video embed page
- **github.com/annontopicmodel/unsupervised_topic_modeling** — unrelated ML repo
- **baseball-reference.com/players/f/fellebo01.shtml** — Bob Feller baseball stats
- **inquirer.com** (via redirect/rebate link) — Philadelphia Inquirer archives

These are either irrelevant domains that happen to mention the brand name ("Bob"), generic Google UI frames, or error pages. The script lacks any relevance filtering.

### 5. DuckDuckGo Timeouts

One query timed out during the run:
```
'"ClickUp" "project management" "review"'
```

This suggests the script should either:
- Reduce query complexity (fewer quoted phrases)
- Add retry logic with longer timeouts
- Fall back to a shorter query on timeout
- Cache results between runs

## Data Quality Checklist

Before treating JSON output as actionable:

- [ ] Scan for dictionary/thesaurus/vocabulary domains — dismiss them
- [ ] Scan for bird articles if "raptor" was a search term — dismiss them
- [ ] Scan for AM/PM time sites if "PM" was a search term — dismiss them
- [ ] Scan for religious/sermon domains — dismiss them
- [ ] Scan for generic platforms (notepad, writing apps) — dismiss them
- [ ] Verify URLs are reachable and content is actually about the target industry
- [ ] Remove exact duplicates (same source URL appearing multiple times)

## Running the Script

```bash
cd /home/bob && python3 ~/.hermes/pipeline-engine/data/backlink-acquisition.py
```

The script prints a terminal summary and saves to JSON. Expected runtime: ~60-120 seconds.

## Recommended Query Improvements

Rather than fixing the in-line queries in the script, consider defining queries externally (e.g., a config file or env vars) so they can be tuned without editing the script. The three search phases need different query strategies:

| Phase | Current Approach | Recommended Approach |
|-------|-----------------|---------------------|
| write_for_us | `"write for us" + keyword` | `"guest post" + industry + site:.com -dictionary -definition` |
| unlinked_mention | `keyword + "mentioned" OR "referenced"` | `"exact brand name" + "mentioned" -bird -time -clock` |
| competitor_gap | `competitor + backlink + "related"` | Use dedicated backlink analysis tools (Ahrefs, Moz, Majestic) via their APIs |