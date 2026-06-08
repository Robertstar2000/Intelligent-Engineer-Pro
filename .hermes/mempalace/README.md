# MemPalace Long-Term Memory Enhancement Layer

A comprehensive long-term memory system for Hermes Agent with FAISS embedding integration, designed to improve cross-session recall and memory organization.

## Features

- **Capture System**: Append-only event logging for all user interactions
- **Tagging System**: Automatic context and palace tagging for semantic organization
- **Scoring System**: Multi-factor memory importance scoring (recency, type, length, tags, context)
- **Consolidation System**: Automatic promotion of important memories to semantic/episodic/procedural stores
- **Retrieval System**: Layered retrieval (working → high-confidence → episodic → raw) with FAISS vector search
- **Reinforcement System**: Usage-based memory strengthening
- **Pruning System**: Intelligent memory pruning with archiving
- **Explainability System**: Decision logging for transparency and debugging
- **FAISS Embedding Integration**: Semantic search capabilities with vector similarity
- **Maintenance Automation**: Automated consolidation, pruning, and reporting via cron jobs

## Installation

The MemPalace system is automatically installed when you run the initialization script. It creates the following directory structure:

```
~/.hermes/mempalace/
├── raw/           # Append-only event storage
├── semantic/      # Consolidated factual memories
├── episodic/      # Consolidated experiential memories
├── procedural/    # Consolidated skill/memory memories
├── preferences/   # User preferences and settings
├── indexes/       # FAISS vector index and ID mapping
├── palace/        # Memory palace location data
└── scripts/       # Maintenance and cron scripts
```

## Usage

### Basic Usage

```python
from mempalace import init_mempalace, capture_memory, retrieve_memory

# Initialize the system
init_mempalace()

# Capture a memory
memory_id = capture_memory({
    'type': 'user_interaction',
    'content': 'User asked about book progress on MIFECO dashboard',
    'context': 'MIFECO dashboard, book writing, chapter 5'
})

# Retrieve memories
memories = retrieve_memory("book progress")
for memory in memories:
    print(f"{memory['type']}: {memory['content']}")
```

### Component Usage

Each MemPalace component can be used independently:

```python
from mempalace.capture import capture_memory_event
from mempalace.tag import extract_context_tags, extract_palace_tags
from mempalace.score import calculate_memory_score
from mempalace.consolidate import consolidate_memory
from mempalace.retrieve import retrieve_memories
from mempalace.reinforce import reinforce_memory
from mempalace.prune import prune_memories
from mempalace.explain import log_explanation
from mempalace.embed import add_embedding, search_embeddings
```

## Configuration

### Scoring Weights

Adjust scoring weights in `score.py` to prioritize different types of memories:

```python
weights = {
    'recency': 0.25,      # How recent the memory is
    'type_weight': 0.25,  # Type of memory (user_interaction, learning, etc.)
    'length': 0.15,       # Length of content
    'tags': 0.15,         # Number and relevance of tags
    'context_richness': 0.20  # Presence of contextual information
}
```

### Consolidation Threshold

Adjust the consolidation threshold in `consolidate.py` (default: 0.6):

```python
def should_consolidate_memory(memory_data, threshold=0.6):
```

### Tagging Taxonomy

Extend the context tag taxonomy and palace tag mapping in `tag.py`:

```python
CONTEXT_TAG_TAXONOMY = {
    'your_category': ['keyword1', 'keyword2', 'keyword3']
}

PALACE_TAG_MAPPING = {
    'your_category': 'your_palace_location'
}
```

## Maintenance

MemPalace includes automated maintenance scripts that can be run via cron:

### Daily Maintenance (Consolidation)

Run consolidation daily to promote important memories:

```bash
# Add to crontab (daily at 2 AM)
0 2 * * * cd ~/.hermes/mempalace && python3 scripts/cron_maintenance.py
```

### Weekly Maintenance (Pruning)

Run pruning weekly to remove old, low-importance memories:

```bash
# Add to crontab (weekly on Sundays at 3 AM)
0 3 * * 0 cd ~/.hermes/mempalace && python3 scripts/cron_maintenance.py
```

### Manual Maintenance

You can also run maintenance manually:

```bash
# Full maintenance (consolidation + light pruning)
./scripts/maintenance.sh

# Or run the Python script directly
python3 scripts/cron_maintenance.py
```

## API Reference

### Core Functions

#### `init_mempalace(storage_path=None)`
Initialize the MemPalace system.

#### `capture_memory(memory_data)`
Capture a new memory event.
- `memory_data`: Dict with keys 'type', 'content', optional 'context', 'timestamp'
- Returns: memory_id (string)

#### `retrieve_memory(query, layers=None)`
Retrieve memories using layered search.
- `query`: Search string
- `layers`: List of layers to search (default: all)
- Returns: List of memory dictionaries

#### `reinforce_memory(memory_id, reinforcement_amount=0.1)`
Reinforce a memory based on usage.
- `memory_id`: ID of memory to reinforce
- `reinforcement_amount`: Amount to increase score (0-1)
- Returns: Boolean success

#### `prune_memory(memory_id, archive=True)`
Prune a memory from the system.
- `memory_id`: ID of memory to prune
- `archive`: Whether to archive before deletion
- Returns: Boolean success

#### `log_explanation(explanation_data)`
Log an explanation for debugging/transparency.
- `explanation_data`: Dict with memory_id, action, and relevant details
- Returns: Boolean success

### Embedding Functions

#### `add_embedding(memory_id, raw_text)`
Add a memory embedding to FAISS index.
- `memory_id`: Unique memory identifier
- `raw_text`: Text to embed
- Returns: Boolean success

#### `search_embeddings(query_text, k=5)`
Search for similar memories using vector similarity.
- `query_text`: Text to search for
- `k`: Number of results to return
- Returns: List of (memory_id, score) tuples

## Architecture Details

### Storage Layers

1. **Raw Storage**: Append-only event log, one JSON file per memory
2. **Semantic Store**: Consolidated factual knowledge and insights
3. **Episodic Store**: Consolidated experiences and events
4. **Procedural Store**: Consolidated skills, habits, and procedures
5. **Preferences Store**: User preferences and settings
6. **Indexes**: FAISS vector index for semantic search
7. **Palace**: Memory palace location mappings

### Memory Lifecycle

1. **Capture**: Event stored in raw/ with initial scoring and tagging
2. **Tagging**: Context and palace tags extracted automatically
3. **Scoring**: Memory importance calculated using multiple factors
4. **Consolidation**: High-scoring memories promoted to appropriate long-term store
5. **Retrieval**: Layered search using both vector similarity and tag matching
6. **Reinforcement**: Used memories get score boosts
7. **Pruning**: Old, low-score, unused memories archived and removed
8. **Explainability**: All operations logged for transparency

### Retrieval Layers

1. **Working Current Session**: Most recent memories (handled by Hermes)
2. **High Confidence**: Semantic memories with scores > 0.8
3. **Episodic**: Consolidated experiential memories
4. **Raw**: Recent unconsolidated events

## Troubleshooting

### Common Issues

#### FAISS Index Errors
- **"Failed to load FAISS index"**: Check file permissions and disk space
- **"Dimension mismatch"**: Ensure embedding model matches index dimension
- **"add_with_ids not available"**: Some FAISS builds don't support this - fallback implemented

#### Embedding Issues
- **Sentence-transformers bug**: All embedding calls now wrap input in lists: `model.encode([text])`
- **Empty search results**: Verify memories are being added to the index correctly

#### Memory Not Found
- Check that memory ID exists in the appropriate store directory
- Verify JSON files are valid and not corrupted

#### Performance Issues
- Large numbers of memories can slow retrieval - consider increasing consolidation threshold
- FAISS index rebuild may be needed after bulk operations

### Debugging

Enable debug logging by setting environment variables:
```bash
export MEMPALACE_DEBUG=true
```

Check explanation logs:
```bash
cat ~/.hermes/mempalace/explanations.jsonl
```

## Integration with Hermes

MemPalace integrates with Hermes through:

1. **Automatic Capture**: Hook into Hermes memory tool to also store in MemPalace/raw/
2. **Enhanced Retrieval**: Augment Hermes memory retrieval with MemPalace layered search
3. **Usage Tracking**: Reinforce memories that are successfully retrieved and used
4. **Preference Sync**: Keep user preferences synchronized between systems

## Extending MemPalace

### Adding New Memory Types

1. Add the type to `score.py` type_weights dictionary
2. Add context keywords to `tag.py` CONTEXT_TAG_TAXONOMY
3. Add palace mapping to `tag.py` PALACE_TAG_MAPPING if needed

### Custom Scoring Factors

Modify `score.py` calculate_memory_score() function to add new factors.

### Alternative Vector Stores

Replace the embed.py implementation with:
- Annoy
- HNSWLIB
- Pinecone (cloud)
- Weaviate
- Or custom similarity search

## License

MIT License - see LICENSE file for details.

## Acknowledgements

Based on the MemPalace architecture concepts for long-term memory enhancement in AI systems.