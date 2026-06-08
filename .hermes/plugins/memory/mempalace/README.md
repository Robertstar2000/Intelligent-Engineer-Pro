# MemPalace Memory Provider for Hermes

This provider implements the MemPalace long-term memory enhancement layer as a pluggable memory provider for Hermes.

## Overview

MemPalace adds a long-term memory layer that works alongside Hermes' built-in memory system:
- Built-in memory: Working memory (current session state)
- MemPalace: Long-term memory for cross-session recall

The provider hooks into Hermes' memory tool calls to capture events, then processes them through the MemPalace pipeline:
1. Capture - Store raw events with metadata
2. Score - Evaluate importance using weighted features
3. Consolidate - Promote high-value items to durable stores
4. Retrieve - Provide layered recall for enhanced context
5. Reinforce - Strengthen memories through use
6. Prune - Remove low-value memories
7. Explainability - Maintain provenance and confidence metadata
8. Auto-tagging - Assign context and palace tags for organization

## Installation

1. Ensure the MemPalace directory structure exists:
   ```bash
   mkdir -p ~/.hermes/mempalace/{raw,semantic,episodic,procedural,preferences,indexes,palace}
   ```

2. Place this provider in `~/.hermes/plugins/memory/mempalace/`

3. Configure Hermes to use the provider in `~/.hermes/config.yaml`:
   ```yaml
   memory:
     provider: mempalace
   ```

4. Restart Hermes

## Configuration

Optional configuration in `~/.hermes/mempalace/provider/config.yaml`:
```yaml
# Scoring thresholds
consolidation_threshold: 0.7
reinforcement_decay: 0.95
prune_age_days: 365

# Storage paths (relative to ~/.hermes/mempalace/)
storage:
  raw: raw/
  semantic: semantic/
  episodic: episodic/
  procedural: procedural/
  preferences: preferences/
  indexes: indexes/
  palace: palace/

# Embedding model for vector search
embedding:
  model: sentence-transformers/all-MiniLM-L6-v2
  dimension: 384

# Palace mapping (context tag -> palace location)
palace_mapping:
  aws: infrastructure
  deployment: infrastructure
  staging: infrastructure
  eu-west-2: infrastructure
  python: programming
  api: programming
  database: storage
  latency: performance
```