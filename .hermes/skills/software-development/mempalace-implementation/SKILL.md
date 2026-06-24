---
name: mempalace-implementation
description: Implements MemPalace long-term memory enhancement layer for Hermes Agent
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [memory, mempalace, long-term-memory, implementation]
    related_skills: [mempalace-integration]
---


## 🔍 MemPalace Query (MANDATORY FIRST STEP)
Before proceeding, query MemPalace for existing context:
```python
import sys, os; sys.path.insert(0, os.path.expanduser('~/.hermes/mempalace'))
import embed; embed.init_embedding(os.path.expanduser('~/.hermes/mempalace'))
results = embed.search_embeddings("MIFECO business process", k=5)
```
This retrieves previous decisions, domain-specific context, and lessons learned from the vector memory store.

# MemPalace Implementation for Hermes Agent

Implements the MemPalace long-term memory enhancement layer for Hermes Agent following the guidelines from the mempalace-integration skill.

## When to Use

Use this skill when you want to add a long-term memory enhancement layer to Hermes Agent for improved cross-session recall, following the MemPalace architecture guidelines.

## Implementation Approach

This skill documents the approach taken to implement MemPalace integration based on practical experience, including lessons learned from debugging and iteration.

### 1. Storage Structure Setup

Create the required directory structure:
```bash
mkdir -p ~/.hermes/mempalace/{raw,semantic,episodic,procedural,preferences,indexes,palace}
mkdir -p ~/.hermes/mempalace/scripts
```

### 2. Component Implementation Order

Implement components in this order for easiest debugging:
1. Capture system (append-only event logging)
2. Tagging system (context and palace tags)
3. Scoring system
4. Consolidation system
5. Retrieval system
6. Reinforcement system
7. Pruning system
8. Explainability system

### 3. Key Lessons Learned

#### Data Type Handling
- Always validate JSON loaded from files is the expected type (dict vs list)
- In retrieval and pruning functions, add type checks:
  ```python
  data = json.loads(line.strip())
  if not isinstance(data, dict):
      # Handle or skip non-dict data
      continue
  ```
- Summary JSON files (`semantic/mifeco_summary.json`, `procedural/workflow_summary.json`) are now dict-wrapped structures with `metadata` and `entries` keys rather than bare lists — check type before iterating

#### FAISS Index Rebuild
- `embed.py`'s `rebuild_index()` was a stub that only cleared the index. Fixed to actually scan `mempalace/semantic/`, `procedural/`, `palace/`, `preferences/` for `mem_*.json` files, extract content+summary text, embed each, and persist both the fresh index and id_map.json.
- Before rebuilding, clear stale entries from id_map.json — memory IDs pointing to archived or deleted files waste vector slots. Run the rebuild:
  ```bash
  cd ~/.hermes/mempalace && python3 -c "
  import sys, os; sys.path.insert(0, os.path.expanduser('~/.hermes/mempalace'))
  import embed; embed.init_embedding(os.path.expanduser('~/.hermes/mempalace'))
  embed.rebuild_index()
  "
  ```
- After rebuild, verify stats: `embed.get_index_stats()` should show matching `total_vectors` and `id_map_entries` counts.

#### Scoring Algorithm Tuning
- The weighted scoring system works well but weights may need tuning based on domain
- Start with equal weights and adjust based on what types of memories you want to prioritize
- Recency decay with 24-hour half-life works well for most use cases

#### Consolidation Logic
- Promote only memories that clear a threshold (start with 0.5-0.6)
- When consolidating, detect contradictions with existing memories rather than overwriting
- Generate meaningful summary text that adds value over raw text

#### Retrieval Layering
- Implement layered retrieval exactly as specified: working → semantic/procedural → episodic → raw
- Use different scoring approaches for each layer
- Always return explainability metadata with results

#### Tagging System
- Context tagging should happen at capture time for efficiency
- Palace tags can be derived from context tags using predefined mapping
- Fallback mappings are important when no direct palace mapping exists

#### Error Handling
- Wrap file operations in try/except blocks
- Provide meaningful error messages that include file paths
- Continue processing other items when one fails

#### Practical Implementation Notes
- **Environment considerations**: In some environments, writing directly to dotfiles via terminal redirection may trigger security blocks. Use the write_file tool or equivalent safe file writing methods instead.
- **Modular development**: Implement and test each component (capture, score, consolidate, etc.) individually before integrating. This makes debugging much easier.
- **Operational automation**: Create maintenance scripts (like maintenance.sh) for periodic scoring, consolidation, and pruning to run via cron jobs.
- **Documentation**: Include a comprehensive README with usage instructions for all commands and scripts.
- **Integration points**: Provide clear examples of how to hook into Hermes' existing memory system (see hermes_hook.py).
- **Verification**: Test each layer of retrieval independently to ensure the layered approach works correctly.

### 4. Integration with Hermes

The integration points are:
- **Capture**: Hook into Hermes memory tool to also write to mempalace/raw/
- **Retrieval**: Enhance Hermes memory retrieval with MemPalace layers
- **Reinforcement**: Track successful retrievals and applications from Hermes usage

### 5. Verification Checklist

After implementation, verify:
1. New memories appear in both Hermes and MemPalace stores
2. Scoring properly promotes important items to consolidated stores
3. Retrieval shows layered responses with appropriate detail levels
4. Reinforcement increases with successful use
5. Pruning removes low-value items while preserving important history
6. Explainability metadata is maintained for all memories

### 6. Maintenance

- Run consolidation periodically (daily via cron job)
- Run pruning less frequently (weekly)
- Monitor archive growth to ensure important memories aren't being pruned incorrectly
- Adjust scoring weights based on observed performance

## DOX Integration

When implementing in a project that uses the [DOX (Self-documenting AGENTS.md)](https://github.com/agent0ai/dox) framework:

- **Read Before Editing:** Walk the DOX tree from root to the target path. Read every AGENTS.md along the route before making any changes.
- **Update After Editing:** If the implementation affects purpose, scope, ownership, structure, workflows, or operating rules, update the closest owning AGENTS.md and refresh the Child DOX Index.
- **Reference:** [agent0ai/dox](https://github.com/agent0ai/dox) — copy `AGENTS.md` from the repo root into your project to initialize.

## Pitfalls to Avoid

1. **Over-consolidation**: Don't promote low-score memories - they create noise
2. **Type confusion**: Always check that loaded JSON is expected type (dict/list)
3. **Circular dependencies**: Don't let MemPalace components depend on each other in ways that create init issues
4. **Performance issues**: Don't load entire event files into memory for large datasets
5. **Over-tagging**: Be selective with context tags to maintain signal-to-noise ratio

## Example Workflow

See `demo_integration.py` for a complete end-to-end example showing:
- Capturing a user interaction
- Tagging the event
- Scoring for consolidation
- Retrieving relevant memories
- Reinforcing through successful use
- Pruning low-value memories

## Customization Points

1. **Scoring weights**: Adjust in score.py based on what memory types you value most
2. **Consolidation threshold**: Tune in consolidate.py based on your volume of memories
3. **Tagging taxonomy**: Extend CONTEXT_TAG_TAXONOMY and PALACE_TAG_MAPPING in tag.py
4. **Pruning criteria**: Modify should_prune_memory() in prune.py based on your retention policies