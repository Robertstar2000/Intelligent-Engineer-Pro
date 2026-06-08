# MemPalace Provider for Hermes

This is a pluggable memory provider for Hermes that implements the MemPalace long-term memory enhancement layer.

## Features

- Capture: Hooks into Hermes memory tool to store raw events in MemPalace raw layer
- Scoring: Scores captured items using weighted features
- Consolidation: Promotes high-value items to consolidated stores (semantic, episodic, procedural, preferences)
- Retrieval: Provides layered retrieval (working, high-confidence semantic/procedural, episodic, deep raw evidence)
- Reinforcement: Tracks successful retrievals and applications
- Pruning: Removes low-value memories based on reinforcement score and age
- Explainability: Maintains metadata for all memories (origin, confidence, context, contradictions, reinforcement history, decay curve)
- Auto-tagging: Automatically assigns context tags and derives palace tags

## Installation

1. Copy this directory to `~/.hermes/mempalace/provider`
2. Add the following to your `~/.hermes/config.yaml`:
   ```yaml
   memory:
     provider: mempalace
   ```
3. Restart Hermes

## Storage Structure

The provider uses the following structure under `~/.hermes/mempalace/`:
- `raw/` - append-only event log (JSON lines)
- `semantic/` - consolidated facts (JSON)
- `episodic/` - consolidated events (JSON)
- `procedural/` - consolidated workflows (JSON)
- `preferences/` - durable preferences (JSON)
- `indexes/` - vector stores (FAISS/HNSW) and graph databases
- `palace/` - spatial organization mappings

## Implementation Details

See the skill documentation for the full MemPalace integration specifications.

## Usage

The provider integrates with Hermes through the MemoryManager interface:
- `initialize()`: Sets up storage and loads indexes
- `system_prompt_block()`: Returns static information about MemPalace
- `prefetch(query)`: Retrieves relevant memories for the upcoming turn
- `sync_turn(user_content, assistant_content)`: Persists a completed turn and triggers capture/scoring
- `get_tool_schemas()`: Exposes MemPalace-specific tools for manual interaction
- `handle_tool_call()`: Handles MemPalace tool calls

## Configuration

The provider can be configured via environment variables or config files in `~/.hermes/mempalace/conf/`:
- `MEMPALACE_ENABLED`: Set to "false" to disable (default: true)
- `MEMPALACE_SCORING_THRESHOLD`: Minimum score for consolidation (default: 0.7)
- `MEMPALACE_REINFORCEMENT_DECAY`: Daily decay factor for reinforcement (default: 0.95)
- `MEMPALACE_PRUNE_AGE_DAYS`: Age after which low-scoring memories are pruned (default: 365)