# Fabricated Claim Reframing for Non-Fiction Books

When a business/advice book manuscript presents fiction as real personal history — "I spent $43k on Salesforce," "Our company MIFECO built 30 agents," "My employee Jen did X" — those claims need reframing as anonymized case studies before publication.

## When to Use

- Manuscript uses first-person "I did X at my company" or "We at [Company] spent Y" with fabricated specifics
- Characters (Jen, Carlos, Dan) are invented but presented as real colleagues
- Specific dollar amounts, timeframes, or events are presented as real when they aren't
- Author bio claims specific achievements that didn't happen

## Scan Targets

Run a grep-based scan for these categories:

```bash
# 1. Specific dollar claims
grep -n '\$[0-9]' manuscript.md | grep -i 'cost\|spent\|dollars\|month\|lost\|invested\|generated\|paid'

# 2. Company/personal names presented as real
grep -n 'MIFECO\b\|my company\|our company\|our system\|our agent\|my agent\|my first\|our first' manuscript.md

# 3. Named individuals (likely fabricated)
grep -n 'Jen\|Carlos\|Dan\|Mark' manuscript.md

# 4. Author bio overclaims
grep -A5 'About the Author' manuscript.md
```

## Rewrite Patterns

| Original Pattern | Replacement |
|---|---|
| "At MIFECO, we spent $43k..." | "Consider one company that spent $43k..." |
| "I built our lead agent..." | "A lead agent was built..." |
| "Jen handled 15 leads/day..." | "A rep handled 15 leads/day..." |
| "Our system costs $380/month" | "A typical system might run ~$380/month" |
| "Carlos spent 3 hours/day on escalations" | "The senior rep spent 3 hours/day on escalations" |
| "I lost a $73k deal..." | "Here's a scenario: a $73k deal was lost..." |
| "My brother-in-law Mark..." | "A LinkedIn contact Mark..." |
| "Built 30 production agents at MIFECO" | "Writes about AI agents based on research" |

## Pitfall: Downstream Reference Chains

When you change a fabricated character's relationship label (e.g., "brother-in-law" → "LinkedIn contact"), the same character may appear later in the chapter with a different relational reference (e.g., "Mark's brother-in-law" → a downstream unrelated usage). Always grep for ALL occurrences of the character's name after the primary replacement — not just the first match.

Example from a real session:
1. Changed "My brother-in-law Mark" → "A LinkedIn contact Mark" ✓
2. 10 paragraphs later, found "The third was Mark's brother-in-law" — an unrelated usage of the same family relationship that needed changing to "Mark's friend"

Fix: after the primary replacement, search for the character name and any family/relational terms near it.

## Strategy: Bulk Rewrite with Python

Write a single Python script that does all replacements in one pass:

```python
from pathlib import Path
text = Path("manuscript.md").read_text()
changes = 0

# 1. Reframe money claims
replacements = [
    ("At MIFECO, we spent forty-three thousand dollars on Salesforce",
     "Consider a company that spent forty-three thousand dollars on Salesforce"),
    ("Our first attempt at an agent system at MIFECO",
     "The first attempt at an agent system at one company"),
    # ... add every unique fabricated phrase
]

for old, new in replacements:
    if old in text:
        text = text.replace(old, new)
        changes += 1

# 2. Reframe named individuals as anonymized roles
for name, role in [("Jen", "the sales rep"), ("Carlos", "the senior support person")]:
    matches = re.findall(rf'\\b{name}\\b', text)
    for m in matches:
        # Manual replacement per occurrence needed
        pass

# 3. Fix author bio
bio_start = text.find("## About the Author")
if bio_start > 0:
    bio_end = text.find("---", bio_start)
    # Replace bio with corrected version

Path("manuscript.md").write_text(text)
print(f"Made {changes} replacement passes")
```

## Verification

After all replacements, verify:

```bash
# Check for remaining "At MIFECO" / "At our company" claims
grep -n "At MIFECO\|at MIFECO\|MIFECO spent\|our company\|my company" manuscript.md | head -20

# Check for remaining first-person fabricated money claims
grep -n '\$[0-9]' manuscript.md | grep -i 'cost\|spent\|lost\|invested\|generated' | head -20

# Verify chapter structure preserved
grep -c "^## Chapter" manuscript.md

# Verify total word count
wc -w manuscript.md
```

The goal is not to remove all first-person voice — the author can still say "I think" or "I recommend" as the narrator. The goal is to stop presenting specific fabricated events, people, or dollar amounts as if they were real personal history.
