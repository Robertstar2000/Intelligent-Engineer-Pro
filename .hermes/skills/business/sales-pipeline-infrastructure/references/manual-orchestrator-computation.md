# Manual Orchestrator Computation (Fallback)

**Created:** 2026-06-22  
**Source:** Pipeline Orchestrator run when `daily-pipeline-analysis.py` was unavailable  
**Purpose:** Reference for inline Python computation of days-in-stage and pipeline metrics

## When to Use

When `scripts/daily-pipeline-analysis.py` is missing, broken, or produces incorrect results, run the orchestrator manually using inline Python via `terminal()`. This pattern is read-only (no file writes) and gives you real-time computed values.

## Days-in-Stage Computation Pattern

```python
from datetime import datetime, timezone

# Always anchor to a fixed datetime for reproducibility
now = datetime(2026, 6, 22, 8, 0, 0, tzinfo=timezone.utc)

def calc_days(entered_str):
    """Handle both ISO timestamps and date-only formats."""
    if not entered_str:
        return '?'
    try:
        dt = datetime.fromisoformat(entered_str.replace('Z', '+00:00'))
    except:
        try:
            dt = datetime.strptime(entered_str, '%Y-%m-%d').replace(tzinfo=timezone.utc)
        except:
            return '?'
    delta = now - dt
    return delta.days
```

## Key Date Format Mapping

| Pipeline | Format | Example | Parser |
|----------|--------|---------|--------|
| Books | ISO 8601 | `2026-05-14T16:38:10Z` | `datetime.fromisoformat(s.replace('Z', '+00:00'))` |
| SaaS | ISO 8601 | `2026-06-17T12:01:11.367582+00:00` | `datetime.fromisoformat(s)` |
| Consulting | Date-only | `2026-05-07` | `datetime.strptime(s, '%Y-%m-%d').replace(tzinfo=timezone.utc)` |

## Field Name Mapping Per Pipeline

| Pipeline | Name Field | Org Field | Email Field | Stage Field | Value Field |
|----------|-----------|-----------|-------------|-------------|-------------|
| Books | `contact.name` | `contact.organization` | `contact.email` | `current_stage` | `value` |
| SaaS | `name` | `company` | `email` | `stage` | (none standard) |
| Consulting | `contact_name` | `company_name` | `contact_email` | `stage` | `value_estimate` |

## Blocker Threshold Logic

```python
# Books: Stage 3 (Discovery) >7 days = blocker, Stage 5 (Negotiation) >7 days = blocker
if stage == 3 and days > 7: blocker = True
if stage == 5 and days > 7: blocker = True

# Consulting: Any stage >7 days = blocker
if days > 7: blocker = True

# SaaS: Stage 1 >=7 days = auto-advance candidate (not a blocker per se, flag for action)
if stage == 1 and days >= 7: auto_advance = True
```

## Nurture Discrepancy Check Pattern

Collect ALL product titles from ALL sections of each pipeline JSON, then verify each appears in the corresponding nurture sequence:

```python
# Books: must check ALL product sections
pipeline_titles = []
products = pipeline_json['pipeline']['products']
for section in ['titles', 'moon_books.titles', 'age_of_lightships.titles', 
               'cindy_lou.titles', 'standalone', 'business_books.titles']:
    # Navigate nested structure and collect all title fields
    ...

# Then compare against nurture sequence email bodies
```

## Registry Integrity Check

```python
# Compare registry total_leads_all vs sum of actual leads in pipeline JSONs
actual_count = sum(len(json.load(open(f'data/pipeline-{p}.json'))['pipeline']['leads']) 
                  for p in ['books', 'saas', 'consulting'])
registry_total = registry['total_leads_all']
assert registry_total == actual_count, f"Mismatch: {registry_total} vs {actual_count}"
```

## Report Output

After computation, write the report using `write_file()` to `data/daily-pipeline-report.md`. Follow the template at `references/report-format-2026-06-20.md` for structure.
