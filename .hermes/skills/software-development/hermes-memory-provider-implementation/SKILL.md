---
name: hermes-memory-provider-implementation
category: software-development
description: Approach for implementing a pluggable memory provider for Hermes to add long-term memory capabilities
---


## 🔍 MemPalace Query (MANDATORY FIRST STEP)
Before proceeding, query MemPalace for existing context:
```python
import sys, os; sys.path.insert(0, os.path.expanduser('~/.hermes/mempalace'))
import embed; embed.init_embedding(os.path.expanduser('~/.hermes/mempalace'))
results = embed.search_embeddings("MIFECO business process", k=5)
```
This retrieves previous decisions, domain-specific context, and lessons learned from the vector memory store.

# Hermes Memory Provider Implementation Approach

## Goal
Implement a pluggable memory provider for Hermes that adds long-term memory capabilities.

## When to use
When you need to add external memory capabilities to Hermes while preserving the built-in memory as source of truth.

## Steps

### 1. Understand the Hermes Memory Provider Interface
- Review `agent.memory_provider.MemoryProvider` abstract base class
- Note required methods: `is_available`, `initialize`, `system_prompt_block`, `prefetch`, `queue_prefetch`, `sync_turn`, `get_tool_schemas`, `handle_tool_call`
- Note optional hooks: `on_turn_start`, `on_session_end`, `on_pre_compress`, `on_memory_write`, `on_delegation`, `shutdown`

### 2. Set Up the Directory Structure
```
~/.hermes/mempalace/
├── raw/                 # append-only event log
├── semantic/            # consolidated facts
├── episodic/            # consolidated events
├── procedural/          # consolidated workflows
├── preferences/         # durable preferences
├── indexes/             # vector stores and graphs
└── palace/              # spatial organization mappings
```

### 3. Implement the Provider Plugin
Create `~/.hermes/hermes-agent/plugins/memory/mempalace/mempalace_provider.py` with:
- Proper inheritance from `MemoryProvider`
- Correct implementation of the `name` property (not `provider_name`)
- Storage path initialization using `get_hermes_home()`
- Basic capture mechanism that stores raw events
- Placeholder implementations for scoring, consolidation, etc.
- Tool schemas for manual interaction (stats, consolidate, prune)

### 4. Configure Hermes to Use the Provider
Configuration guidance: To use this provider, set the memory provider in Hermes configuration. Refer to Hermes documentation for configuring external memory providers.

### 5. Test the Implementation
- Verify the provider can be imported
- Check `is_available()` returns True
- Initialize with a test session
- Test basic capture functionality
- Verify prefetch returns appropriate context
- Check system prompt block
- Verify tool schemas are returned correctly

### 6. Key Implementation Details
- Use `ENTRY_DELIMITER = "\n§\n"` for memory entries if mirroring built-in memory format
- Store raw events as JSON lines in `raw/events.jsonl`
- Implement proper file locking for concurrent access
- Use atomic writes (temp file + rename) for durability
- Scan content for injection/exfiltration patterns before storing
- Implement layered retrieval approach in `prefetch`
- Provide explainability metadata with all memories
- Implement auto-tagging for context and palace tags

## DOX Integration

When implementing in a project that uses the [DOX (Self-documenting AGENTS.md)](https://github.com/agent0ai/dox) framework:

- **Read Before Editing:** Walk the DOX tree from root to the target path. Read every AGENTS.md along the route before making any changes.
- **Update After Editing:** If the implementation affects purpose, scope, ownership, structure, workflows, or operating rules, update the closest owning AGENTS.md and refresh the Child DOX Index.
- **Reference:** [agent0ai/dox](https://github.com/agent0ai/dox) — copy `AGENTS.md` from the repo root into your project to initialize.

## Pitfalls to Avoid
- Forgetting to implement the `name` property correctly (must return string)
- Not properly initializing storage directories
- Missing required methods from the MemoryProvider interface
- Not handling errors gracefully in provider methods
- Forgetting to call `_reload_target()` under file lock before modifying entries
- Not implementing proper file locking for concurrent access
- Making `sync_turn` blocking when it should be non-blocking
- Not respecting the session agent_context (skip writes for non-primary contexts)

## Verification
After implementation:
1. Provider loads without errors
2. `is_available()` returns True when storage is accessible
3. Raw events are stored and retrievable
4. Prefetch returns contextual information
5. System prompt block is returned
6. Tool schemas are properly defined
7. Optional hooks don't cause errors when called