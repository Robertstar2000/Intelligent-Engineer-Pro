# Fabricated First-Person Claim Detection & Correction

When a non-fiction/business book presents itself as a memoir of the author's real experience
but contains fabricated claims about what "I" or "my company" did/spent/achieved, those
claims must be reframed as anonymized case studies, illustrative examples, or general
observations before publishing.

## When to Use

- The manuscript uses first-person ("I built", "I spent", "my company", "we automated")
  to describe events, costs, people, or systems that the author did NOT actually build/spend/operate
- The book presents specific dollar amounts, deal sizes, headcount, timelines as personal
  experience rather than illustrative examples
- Named real-company employees (agents, directors) are described doing work that never happened
- The author bio makes unsupported claims about what the author built or operates

## Detection Patterns

Search for these classes of fabricated claims (case-insensitive):

### Specific dollar claims
```python
patterns = [
    r"\$\d[\d,]*\s*(thousand|million|k|K)\s*(dollar|deal|contract|sale|cost|spent|investment)",
    r"(cost|spent|paid|invested|lost|wasted)\s+\$[\d,]+",
    r"\$[\d,]+\s*(a|per)\s*(month|year|week|day)",
]
```

### "I and my company" verb claims
```
I spent <time/money>
I lost <amount>
I built <system>
our <team/agent/system> <verb> <specific-number>
my first <agent/attempt>
```

### Named real people in fictional scenarios
```
Jen (our sales rep)
Carlos (our support lead)
Dan (my friend who runs <business>)
```

### Specific personal timeline events
```
2 AM on a Wednesday in February 2024
Ten days in Maine with no cell service
published a blog post that got traction → 47 leads
```

## Correction Strategy

Three tiers of correction, applied in order:

### Tier 1: Anonymize specific actors and amounts

**Before:**
> MIFECO spent forty-three thousand dollars on Salesforce.

**After:**
> Consider what happened at a mid-sized B2B company. They spent forty-three thousand dollars on Salesforce.

### Tier 2: Reframe as illustrative/typical rather than real

**Before:**
> Our agents cost $380 a month to run.

**After:**
> A typical agent system might run about $380 a month.

### Tier 3: Replace specific narrative with anonymous cautionary tale

**Before:**
> The email went out at 10:34 AM. Subject line: "Your Invoice — Payment Overdue." ... The customer called me at 10:37 AM. "What the hell is this?"

**After:**
> Here's a cautionary tale. The email went out at 10:34 AM. Subject line: "Your Invoice — Payment Overdue." ... The customer called at 10:37 AM. "What the hell is this?"

## Bulk Rewrite Pattern

Use a Python script with targeted `text.replace()` calls per claim.
Example structure for the rewrite script:

```python
# Tier 1: Anonymize company name + specific amounts
for old, new in [
    ("MIFECO spent forty-three thousand dollars",
     "Consider a company that spent forty-three thousand dollars"),
    ("I built a lead agent at MIFECO",
     "A lead agent was built to solve this"),
]:
    text = text.replace(old, new)

# Tier 2: Frame figures as illustrative
for old, new in [
    ("Our agents cost $380 a month",
     "A typical system might run about $380 a month"),
    ("I had an agent running for three weeks before I realized",
     "Here's a story that illustrates the monitoring problem. An agent was running for three weeks before anyone realized"),
]:
    text = text.replace(old, new)

# Tier 3: Named characters → anonymous roles
for old, new in [
    ("Jen, our sales development rep",
     "the sales development rep"),
    ("Carlos, the senior support person",
     "the senior support person"),
]:
    text = text.replace(old, new)
```

## Verification

After all replacements:
1. **Scan for remaining MIFECO mentions** (grep -n "MIFECO" manuscript.md) — should only appear in copyright, disclaimer, or prompt examples
2. **Check dollar amounts** are framed as illustrative ("might cost", "typically runs")
3. **Verify author bio** doesn't make unsupported claims
4. **Spot-check 5 chapters** for first-person claims that slipped through

## When NOT to Correct

- General first-person observations about the learning process:
  _"I learned that agents fail in predictable ways"_ → This is valid authorial voice
- Technical advice in first person:
  _"I use a three-stage testing method"_ → Fine as opinion/advice framing  
- Obvious hypothetical examples:
  _"Imagine you're asleep when a deal closes at 2:47 AM"_ → This is a thought experiment
