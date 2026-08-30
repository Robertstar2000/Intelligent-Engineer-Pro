---
name: compressed-manuscript-preparation-and-delivery
description: ""
goal: "Produce a formatted manuscript and deliver via Telegram. For KDP publishing, use no-AI login browser handoff."
---

## Memory context (Hindsight)

Long-term memory context is now provided automatically by Hindsight (bank
`mifeco-default`) on every turn — the retired MemPalace manual query step no
longer applies. Do NOT attempt to import `~/.hermes/mempalace` (it was removed
2026-08-19).This retrieves previous decisions, domain-specific context, and lessons learned from the vector memory store.

{
  "name": "manuscript-preparation-and-delivery",
  "goal": "Produce a formatted manuscript and deliver via Telegram. For KDP publishing: AI prepares files, Bob logs into kdp.amazon.com manually (no-AI login), AI guides data entry via shared browser.",
  "steps": [
    {"action": "consolidate", "input": "chapters/", "output": "combined.html"},
    {"action": "apply_style", "input": "combined.html", "params": {"font": "Times New Roman", "margin": "2.5cm", "size": "A4"}},
    {"action": "generate_front_matter", "output": ["cover", "title", "copyright", "dedication", "toc"]},
    {"action": "insert_transitions", "input": "memoir", "params": {"length": "15-20"}},
    {"action": "add_back_cover"},
    {"action": "validate", "required": ["cover", "title", "copyright", "dedication", "toc", "chapters", "back"]},
    {"action": "output", "format": "html", "name": "final_manuscript.html"},
    {"action": "deliver", "platform": "telegram", "format": "media", "path": "MEDIA:/final_manuscript.html"},
    {
      "action": "kdp_publish",
      "note": "No-AI login required. AI opens browser to kdp.amazon.com → Bob logs in manually → AI fills metadata via browser_type → Bob uploads files → Bob clicks Publish → AI captures ASIN."
    }
  ]
}
