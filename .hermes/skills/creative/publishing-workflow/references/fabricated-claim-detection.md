# Fabricated First-Person Claim Detection and Rewrite

## When to Use
- A non-fiction/guide/business-book manuscript presents fabricated claims as the author's real experience ("I did X," "my company spent Y," "we built Z")
- The user says "these need to be redone as fictional case studies," "don't say things that aren't true," or similar
- The manuscript contains specific dollar amounts, named people, exact dates, or concrete events that are not real

## Detection Patterns

Scan for these categories of fabricated first-person claims:

### 1. Specific Dollar Amounts
- "My company spent $43,000 on [product]"
- "It cost us $1,200 in margin when..."  
- "That saved us $39,000 per year"
- "We lost a $73,000 deal"
- "My agents cost $380 a month to run"
- Any specific number presented as fact about the author's business

### 2. Named People (who don't exist)
- "Our sales rep, Jen, handles 15 leads per day"
- "Carlos, our senior support person, spent 3 hours on escalations"
- "My friend Dan runs a construction company"
- Any named individual presented as a real employee/associate who is actually fabricated

### 3. Specific Dates and Events
- "2 AM on a Wednesday in February 2024"
- "The email went out at 10:34 AM"
- "I decided to automate this on a Friday afternoon"
- "That incident cost me a day of apologizing"
- Specific timestamps that imply a real event

### 4. "We built / we did / we created" Claims
- "At MIFECO, we built a lead agent"
- "We rebuilt the system with three specialized agents"
- "I spent two weeks on the orchestrator"
- "We analyzed six months of HubSpot data"
- Any claim about work done specifically at the author's company

### 5. Quantitative System Claims
- "Our pipeline agents have an uptime of 99.3%"
- "The approval rate started at 60%"
- "About 8% of inbound leads need repair"
- "The hybrid approach handles 70% of cases"
- Specific metrics presented as real from the author's system

### 6. Author Bio Claims
- "He built his first agent pipeline in 2024 and has since deployed over 30 production agents"
- "His non-fiction is grounded in what he's actually built"
- Any bio claim that fabricates the author's actual experience

## Rewrite Strategy

For each fabricated claim, choose the appropriate rewrite approach:

### Option A: Anonymized Case Study
Replace "I/we did X at MIFECO" with "Consider a company that did X":

| Before | After |
|--------|-------|
| "At MIFECO, we spent $43k on Salesforce" | "Consider a company that spent $43,000 on Salesforce" |
| "Our lead agent handles..." | "A lead agent handles..." |
| "I built this system in 2024" | "One team built this system in 2024" |

### Option B: Second-Person Framing
Replace "I did X" with "You might do X" or "Picture this":

| Before | After |
|--------|-------|
| "The lead came in at 3:14 PM. My agent caught it." | "Picture this: A lead comes in. Your agent catches it." |
| "I took a real vacation last year. Ten days in Maine." | "Consider taking a vacation. Ten days with no cell service." |
| "I check the dashboard every morning." | "You check the dashboard every morning." |

### Option C: Impersonal/General Framing
Replace specific claims with general observations:

| Before | After |
|--------|-------|
| "I now track four categories of metrics" | "Track four categories of metrics" |
| "I have identified three specific failure modes" | "There are three specific failure modes" |
| "My first version used the premium model" | "A first version might use the premium model" |

### Option D: Cautionary Tale Framing
For stories that include mistakes or failures:

| Before | After |
|--------|-------|
| "I deployed an agent that sent a hundred wrong emails" | "Here's a cautionary tale. An agent was deployed..." |
| "The email went out at 10:34 AM. It was wrong." | "The email went out. It was addressed to the company's biggest customer. It was also completely wrong." |

### Option E: Example Prompts (Acceptable as-is)
Claims inside example prompt templates (showing what an agent's system prompt might say) are fine to leave as MIFECO references since they are explicitly presented as template examples, not real claims.

### Preserve: Genuinely General Advice
Philosophical reflections, general observations about business or human nature, and actionable frameworks that don't depend on fabricated personal experience should be preserved as-is.

## Batch Rewrite Approach

For large manuscripts (40+ chapters), write a Python script rather than editing by hand:

1. **Scan the full manuscript** for all instances of the patterns above
2. **Write targeted replacements** — prefer exact-match `text.replace(old, new)` over regex for safety
3. **Organize replacements by pattern category** — group dollar-amount rewrites together, name rewrites together, etc.
4. **Run the script** and verify with grep that no residual fabricated claims remain
5. **Check for remaining first-person MIFECO claims** after the first pass

Example script structure:
```python
from pathlib import Path

text = Path("manuscript.md").read_text()
changes = 0

# Group 1: MIFECO-specific money claims
for old, new in [
    ("At MIFECO, we spent forty-three thousand dollars",
     "Consider a company that spent forty-three thousand dollars"),
    # ...
]:
    if old in text:
        text = text.replace(old, new)
        changes += 1

# Group 2: Named people
for old, new in [
    ("I sat with our sales development rep, Jen",
     "The best way to start is to sit with your sales development rep"),
    # ...
]:
    if old in text:
        text = text.replace(old, new)
        changes += 1

# ... etc for each pattern category

Path("manuscript.md").write_text(text)
print(f"Made {changes} replacements")
```

## Verification

After the rewrite pass, verify:
1. **No remaining fabricated MIFECO claims**: `grep -n "MIFECO" manuscript.md | grep -iv "copyright\|published by\|publishing\|disclaimer"`
2. **No remaining "$" dollar claims presented as real**: Check that cost examples are framed as illustrative ("might cost," "consider") not factual ("cost me," "we spent")
3. **No remaining "I lost / I spent / I built" fabricated claims**: Check that remaining first-person statements are either general reflections or clearly marked as illustrative
4. **Chapter count and word count are preserved** — rewriting shouldn't change chapter boundaries or significantly alter word count
5. **Author bio is honest** — remove claims about "built X agents" / "deployed Y systems" if not true

## Pitfalls
- **Don't strip genuinely useful content**: Technical advice, frameworks, and step-by-step instructions should survive the rewrite intact — only the framing of who did what needs to change.
- **Example prompts are special**: A system prompt like "You are a lead qualification assistant for MIFECO" inside an example is fine — it's explicitly a template, not a claim about reality.
- **First-person narrative voice vs. false claims**: The author can still say "I think" or "I recommend" — that's opinion, not fabrication. The problem is claiming specific events happened when they didn't.
- **Run multiple passes**: After the script's bulk find-and-replace, remaining embedded references (like "Our thirty-plus agents cost roughly $380 per month" in the middle of a paragraph) need targeted patches.
- **Rebuild after rewriting**: Change the manuscript markdown, then regenerate HTML, EPUB, and PDF from the corrected source — don't patch the output formats separately.
