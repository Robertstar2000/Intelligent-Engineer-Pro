# Detecting and Replacing Fabricated First-Person Claims in Non-Fiction Manuscripts

When an author writes a non-fiction/practitioner book but has not actually done what the manuscript claims ("I spent $43k on Salesforce," "My company built 30 agents," "We lost a $73k deal"), these claims need to be reframed as **anonymized case studies** or **illustrative examples** rather than first-person testimony.

## Detection Patterns

Search for these patterns in the manuscript:

| Pattern | Example | Replacement |
|---------|---------|-------------|
| `MIFECO spent $X` / `Our company spent $X` | "MIFECO spent forty-three thousand dollars on Salesforce" | "Consider a company that spent $43k..." |
| `I lost a $X deal` / `We lost` | "I lost a seventy-three thousand dollar deal" | "Here's a scenario that plays out often..." |
| `I built an agent` / `my agent` | "I built a lead agent at MIFECO" | "A lead agent was built..." |
| Specific named employees | "Jen, our SDR" / "Carlos the support lead" | "The sales rep" / "The senior support person" |
| First-person with specific dates/times | "2 AM on a Wednesday in February 2024" | "Imagine it's late at night and you're staring at a spreadsheet..." |
| `Our $X per month` / `costs $X` | "Our agents cost $380 a month to run" | "A typical system might run about $380/month" |
| Personal bio claims | "Built 30 production agents at MIFECO" | "Writes about AI agents based on research" |

## Rewriting Approach

**Goal:** Preserve the narrative flow and technical advice while removing false claims of personal experience.

**Framing options:**
- **Anonymized case study:** "A logistics company we'll call SwiftShip..." — keeps a concrete story with a fictional company name
- **Illustrative example:** "Consider a time audit done at a technology consultancy..." — generalizes to "one company"
- **Hypothetical:** "Picture this: you're asleep when a deal closes at 2:47 AM..." — puts the reader in the scenario
- **General observation:** "In my experience..." / "I've seen this pattern..." — keeps first person but truthfully vague

## Pitfalls

- **Don't just delete claims** — the narrative relies on concrete examples. Replace each one with an equivalent fictional or anonymized version.
- **Check downstream references** — if "Jen the SDR" is mentioned across multiple chapters, all instances must be updated consistently.
- **Author bio needs rewriting too** — it's often the most exaggerated section ("built 30 agents" → "writes about AI agents").
- **Disclaimer needs updating** — change from "the numbers are real" to "the numbers are illustrative" / "scenarios are based on observed patterns."
- **Run a grep for remaining fabrications after each pass** — search for `MIFECO`, `$[0-9]`, `my agent`, `I built`, `I lost`, `I spent` to catch stragglers.
