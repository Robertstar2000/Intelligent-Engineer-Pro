# Generic Paragraph Detection & Replacement

When AI-assisted book prose is expanded to hit word-count targets, the expansion often
produces generic/placeholder paragraphs. These undermine reader engagement and must be
replaced with specific, dramatic, character-driven content before delivery.

## Detection Patterns

Search for these opening phrases (case-insensitive substring match):

### Narrative Fillers
- "The work continued through the long hours"
- "In the silence of the habitat, broken only by"
- "The data painted a complex picture"
- "The implications were staggering"
- "The team gathered around the monitor"
- "The situation demanded action"
- "Time was running out"
- "The investigation was proceeding slowly"
- "The data continued to flow in"
- "The days blurred together"

### Generic Dialogue Tags
- `"We're making progress," someone reported slowly`
- `"This doesn't make sense," someone muttered`
- `"We need to consider all possibilities,"`
- `"We're not going to survive this if we keep arguing,"`
- `"We've faced worse," someone said`

### Generic Scene Transitions
- "What are you thinking about?" someone asked softly
- "About home. About the people we left behind."
- "The equipment hummed softly in the background"
- "The computer terminal flickered as another batch of data"

## Replacement Strategy

Each replacement must:

1. **Name specific characters** — not "someone," "the team," "the lead scientist"
2. **Show emotion through action** — trembling hands, not "he was scared"
3. **Advance plot** — reveal new information, raise stakes, force a decision
4. **Use sensory specificity** — numbers (12% oxygen), sounds (respirator hiss), physical details
5. **Include dialogue with subtext** — what characters don't say matters as much as what they do

### Example: Generic → Dramatic

**Generic:**
> "The work continued through the long hours, each member of the team pushing themselves beyond the limits of exhaustion. They knew the window of opportunity was narrow — every moment of delay could mean the difference between success and failure."

**Replacement:**
> "Sarah's hands were raw from gripping the same valve for three hours. She couldn't feel her fingers anymore. But every time she thought about stopping, she pictured David's face — the way he'd looked at her before the extraction team left, trusting her to bring help. She hadn't brought help. She'd brought herself, and that would have to be enough."

## Bulk Replacement Code

```python
import re

replacements = [
    ('The work continued through the long hours, each member...',
     'Sarah\'s hands were raw from gripping the same valve...'),
    ('In the silence of the habitat, broken only by...',
     'The respirator hissed in Sarah\'s ears...'),
    # ... add all generic→dramatic pairs
]

def quality_pass(path):
    with open(path) as f:
        html = f.read()
    
    changes = 0
    for generic, replacement in replacements:
        count = html.count(generic)
        if count > 0:
            html = html.replace(generic, replacement, count)
            changes += count
    
    if changes > 0:
        with open(path, "w") as f:
            f.write(html)
    
    return changes
```

Use `reversed(ordered_replacements_by_length)` to prevent longer phrases from matching
inside shorter ones if you work with substring patterns rather than exact matches.