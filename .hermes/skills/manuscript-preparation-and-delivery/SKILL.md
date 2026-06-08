---
name: manuscript-preparation-and-delivery
description: Workflow for preparing completed manuscripts for review and delivery, including file consolidation, front matter creation, and messaging platform delivery
category: creative
---


## 🔍 MemPalace Query (MANDATORY FIRST STEP)
Before proceeding, query MemPalace for existing context:
```python
import sys, os; sys.path.insert(0, os.path.expanduser('~/.hermes/mempalace'))
import embed; embed.init_embedding(os.path.expanduser('~/.hermes/mempalace'))
results = embed.search_embeddings("MIFECO business process", k=5)
```
This retrieves previous decisions, domain-specific context, and lessons learned from the vector memory store.

# Manuscript Preparation and Delivery